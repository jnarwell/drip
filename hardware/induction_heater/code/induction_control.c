/**
 * @file induction_control.c
 * @brief Safety-critical induction heater control for DRIP system
 * @author DRIP Team
 * @date 2024
 * 
 * SAFETY CRITICAL - DO NOT MODIFY INTERLOCKS
 * This controls 3kW of induction heating power
 */

#include "stm32f4xx_hal.h"
#include "induction_heater.h"
#include "safety_interlocks.h"
#include "pid_controller.h"
#include <string.h>
#include <math.h>

/* Pin Definitions */
#define HEATER_ENABLE_PIN    GPIO_PIN_0  // PA0 - Enable signal to OEM module
#define HEATER_PWM_PIN       GPIO_PIN_1  // PA1 - TIM2_CH2 for power control
#define FLOW_SENSOR_PIN      GPIO_PIN_2  // PA2 - EXTI interrupt
#define TEMP_SENSOR_ADC      ADC_CHANNEL_3  // PA3 - Coil temp
#define EMERGENCY_STOP_PIN   GPIO_PIN_4  // PA4 - NC contact
#define WATER_TEMP_ADC       ADC_CHANNEL_5  // PA5 - Water temp
#define DOOR_INTERLOCK_PIN   GPIO_PIN_6  // PA6 - Enclosure door

/* Safety Limits - DO NOT INCREASE */
#define MIN_FLOW_RATE        1.5   // L/min - below this = immediate shutdown
#define MAX_COIL_TEMP        60    // °C - coil temperature limit
#define MAX_WATER_TEMP       35    // °C - cooling water limit
#define MAX_CRUCIBLE_TEMP    1600  // °C - absolute maximum
#define TEMP_RATE_LIMIT      100   // °C/min - prevent thermal shock
#define COOLDOWN_TIME        300   // seconds - minimum cooldown after shutdown

/* PID Parameters */
#define PID_KP              0.5f
#define PID_KI              0.1f
#define PID_KD              0.05f
#define PID_MAX_OUTPUT      100.0f
#define PID_MIN_OUTPUT      0.0f
#define PID_SAMPLE_TIME     100    // ms

/* Fault Codes */
typedef enum {
    FAULT_NONE = 0,
    FAULT_ESTOP,
    FAULT_NO_FLOW,
    FAULT_OVERTEMP_COIL,
    FAULT_OVERTEMP_WATER,
    FAULT_OVERTEMP_CRUCIBLE,
    FAULT_DOOR_OPEN,
    FAULT_POWER_LOSS,
    FAULT_COMM_ERROR,
    FAULT_SENSOR_ERROR
} FaultCode;

/* System State */
typedef struct {
    float power_setpoint;       // 0-100%
    float actual_power;         // Watts from power meter
    float frequency;            // Hz from module
    float coil_temperature;     // °C
    float water_temperature;    // °C
    float crucible_temperature; // °C from thermal camera
    float flow_rate;            // L/min
    uint8_t enabled;
    uint8_t temp_control_mode;  // 0=manual, 1=auto PID
    uint8_t material_type;      // 0=aluminum, 1=steel
    FaultCode fault_code;
    uint32_t runtime_seconds;
    uint32_t cooldown_timer;
} InductionState;

/* Global Variables */
static InductionState heater = {0};
static PIDController temp_pid;
static uint32_t flow_pulse_count = 0;
static uint32_t last_flow_calc_time = 0;
static char fault_log[100];

/* External interfaces */
extern ADC_HandleTypeDef hadc1;
extern TIM_HandleTypeDef htim2;
extern UART_HandleTypeDef huart2;  // Power meter UART

/* Function Prototypes */
static uint8_t check_safety_interlocks(void);
static void emergency_shutdown(void);
static float read_temperature(uint32_t adc_channel);
static void log_fault(FaultCode code);
static void update_power_output(float percent);

/**
 * @brief Initialize induction heater control system
 * @return 0 on success, -1 on failure
 */
int induction_heater_init(void) {
    /* Initialize PID controller */
    pid_init(&temp_pid, PID_KP, PID_KI, PID_KD, PID_SAMPLE_TIME);
    pid_set_limits(&temp_pid, PID_MIN_OUTPUT, PID_MAX_OUTPUT);
    
    /* Configure GPIO */
    GPIO_InitTypeDef GPIO_InitStruct = {0};
    
    /* Enable output (push-pull, initially low) */
    GPIO_InitStruct.Pin = HEATER_ENABLE_PIN;
    GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
    GPIO_InitStruct.Pull = GPIO_PULLDOWN;
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
    HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);
    HAL_GPIO_WritePin(GPIOA, HEATER_ENABLE_PIN, GPIO_PIN_RESET);
    
    /* Safety inputs (pull-up for NC contacts) */
    GPIO_InitStruct.Pin = EMERGENCY_STOP_PIN | DOOR_INTERLOCK_PIN;
    GPIO_InitStruct.Mode = GPIO_MODE_INPUT;
    GPIO_InitStruct.Pull = GPIO_PULLUP;
    HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);
    
    /* Flow sensor interrupt */
    GPIO_InitStruct.Pin = FLOW_SENSOR_PIN;
    GPIO_InitStruct.Mode = GPIO_MODE_IT_RISING;
    GPIO_InitStruct.Pull = GPIO_PULLUP;
    HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);
    
    /* Enable flow sensor interrupt */
    HAL_NVIC_SetPriority(EXTI2_IRQn, 0, 0);
    HAL_NVIC_EnableIRQ(EXTI2_IRQn);
    
    /* Start PWM timer */
    HAL_TIM_PWM_Start(&htim2, TIM_CHANNEL_2);
    __HAL_TIM_SET_COMPARE(&htim2, TIM_CHANNEL_2, 0);  // Start at 0%
    
    /* Initial safety check */
    if (!check_safety_interlocks()) {
        return -1;  // Cannot start with safety fault
    }
    
    return 0;
}

/**
 * @brief Safety interlock check - MUST pass before any operation
 * @return 1 if safe to operate, 0 if fault detected
 * 
 * CRITICAL: This function must NEVER be bypassed
 */
static uint8_t check_safety_interlocks(void) {
    uint8_t safe = 1;
    
    /* Check emergency stop (NC contact - low = pressed) */
    if (HAL_GPIO_ReadPin(GPIOA, EMERGENCY_STOP_PIN) == GPIO_PIN_RESET) {
        heater.fault_code = FAULT_ESTOP;
        safe = 0;
    }
    
    /* Check enclosure door (NC contact) */
    if (HAL_GPIO_ReadPin(GPIOA, DOOR_INTERLOCK_PIN) == GPIO_PIN_RESET) {
        heater.fault_code = FAULT_DOOR_OPEN;
        safe = 0;
    }
    
    /* Check water flow rate */
    if (heater.flow_rate < MIN_FLOW_RATE) {
        heater.fault_code = FAULT_NO_FLOW;
        safe = 0;
    }
    
    /* Check coil temperature */
    if (heater.coil_temperature > MAX_COIL_TEMP) {
        heater.fault_code = FAULT_OVERTEMP_COIL;
        safe = 0;
    }
    
    /* Check water temperature */
    if (heater.water_temperature > MAX_WATER_TEMP) {
        heater.fault_code = FAULT_OVERTEMP_WATER;
        safe = 0;
    }
    
    /* Check crucible temperature */
    if (heater.crucible_temperature > MAX_CRUCIBLE_TEMP) {
        heater.fault_code = FAULT_OVERTEMP_CRUCIBLE;
        safe = 0;
    }
    
    return safe;
}

/**
 * @brief Emergency shutdown procedure
 * 
 * CRITICAL: This must execute within 10ms
 */
static void emergency_shutdown(void) {
    /* Immediately disable power - hardware level */
    HAL_GPIO_WritePin(GPIOA, HEATER_ENABLE_PIN, GPIO_PIN_RESET);
    
    /* Set PWM to 0% */
    __HAL_TIM_SET_COMPARE(&htim2, TIM_CHANNEL_2, 0);
    
    /* Update state */
    heater.enabled = 0;
    heater.power_setpoint = 0;
    
    /* Start cooldown timer */
    heater.cooldown_timer = COOLDOWN_TIME;
    
    /* Log the fault */
    log_fault(heater.fault_code);
    
    /* Keep cooling pump running (handled by separate circuit) */
}

/**
 * @brief Set induction heater power level
 * @param power_percent Power level 0-100%
 */
void set_heater_power(float power_percent) {
    /* Clamp input */
    if (power_percent < 0) power_percent = 0;
    if (power_percent > 100) power_percent = 100;
    
    heater.power_setpoint = power_percent;
    
    /* Only apply if safety checks pass */
    if (check_safety_interlocks()) {
        update_power_output(power_percent);
        heater.enabled = 1;
    } else {
        emergency_shutdown();
    }
}

/**
 * @brief Update PWM output to module
 * @param percent Power percentage 0-100
 */
static void update_power_output(float percent) {
    /* PWM period is 1000, so duty = percent * 10 */
    uint32_t duty = (uint32_t)(percent * 10.0f);
    
    /* Apply to timer */
    __HAL_TIM_SET_COMPARE(&htim2, TIM_CHANNEL_2, duty);
    
    /* Enable output if not already */
    if (!heater.enabled) {
        HAL_GPIO_WritePin(GPIOA, HEATER_ENABLE_PIN, GPIO_PIN_SET);
    }
}

/**
 * @brief Main control loop - call from 100Hz timer interrupt
 */
void induction_heater_update(void) {
    static uint32_t last_update = 0;
    uint32_t now = HAL_GetTick();
    
    /* Calculate flow rate from pulses */
    if (now - last_flow_calc_time >= 1000) {
        heater.flow_rate = (float)flow_pulse_count * 60.0f / 4.5f / 1000.0f;
        flow_pulse_count = 0;
        last_flow_calc_time = now;
    }
    
    /* Read all sensors */
    heater.coil_temperature = read_temperature(TEMP_SENSOR_ADC);
    heater.water_temperature = read_temperature(WATER_TEMP_ADC);
    heater.actual_power = read_power_meter();
    
    /* Update runtime */
    if (heater.enabled && (now - last_update >= 1000)) {
        heater.runtime_seconds++;
        last_update = now;
    }
    
    /* Handle cooldown timer */
    if (heater.cooldown_timer > 0) {
        if (now - last_update >= 1000) {
            heater.cooldown_timer--;
            if (heater.cooldown_timer == 0) {
                heater.fault_code = FAULT_NONE;  // Clear fault after cooldown
            }
        }
        return;  // Don't process anything during cooldown
    }
    
    /* Continuous safety check */
    if (heater.enabled && !check_safety_interlocks()) {
        emergency_shutdown();
        return;
    }
    
    /* Temperature control mode */
    if (heater.enabled && heater.temp_control_mode) {
        float target_temp = 0;
        
        /* Set target based on material */
        switch (heater.material_type) {
            case 0:  // Aluminum
                target_temp = 700.0f;
                break;
            case 1:  // Steel
                target_temp = 1580.0f;
                break;
        }
        
        /* Run PID control */
        float error = target_temp - heater.crucible_temperature;
        float output = pid_calculate(&temp_pid, error);
        
        /* Apply rate limiting */
        static float last_temp = 0;
        float temp_rate = (heater.crucible_temperature - last_temp) * 60.0f;  // °C/min
        if (fabs(temp_rate) > TEMP_RATE_LIMIT) {
            output *= 0.5f;  // Reduce power if heating too fast
        }
        last_temp = heater.crucible_temperature;
        
        /* Apply new power setting */
        set_heater_power(output);
    }
}

/**
 * @brief Read temperature from ADC channel
 * @param adc_channel ADC channel to read
 * @return Temperature in °C
 */
static float read_temperature(uint32_t adc_channel) {
    uint32_t adc_value = 0;
    
    /* Configure ADC channel */
    ADC_ChannelConfTypeDef sConfig = {0};
    sConfig.Channel = adc_channel;
    sConfig.Rank = 1;
    sConfig.SamplingTime = ADC_SAMPLETIME_84CYCLES;
    
    if (HAL_ADC_ConfigChannel(&hadc1, &sConfig) != HAL_OK) {
        heater.fault_code = FAULT_SENSOR_ERROR;
        return 999.0f;  // Return high value to trigger safety
    }
    
    /* Start conversion */
    HAL_ADC_Start(&hadc1);
    if (HAL_ADC_PollForConversion(&hadc1, 10) == HAL_OK) {
        adc_value = HAL_ADC_GetValue(&hadc1);
    }
    HAL_ADC_Stop(&hadc1);
    
    /* Convert to temperature (assuming 10mV/°C sensor) */
    float voltage = (float)adc_value * 3.3f / 4096.0f;
    float temperature = voltage * 100.0f;
    
    return temperature;
}

/**
 * @brief Read power from PZEM-022 meter
 * @return Power in watts
 */
float read_power_meter(void) {
    static uint8_t rx_buffer[25];
    static float last_power = 0;
    
    /* PZEM-022 protocol implementation */
    uint8_t request[] = {0xF8, 0x04, 0x00, 0x00, 0x00, 0x0A, 0x64, 0x64};
    
    /* Send request */
    HAL_UART_Transmit(&huart2, request, sizeof(request), 10);
    
    /* Receive response */
    if (HAL_UART_Receive(&huart2, rx_buffer, 25, 50) == HAL_OK) {
        /* Parse power value (bytes 7-8) */
        uint16_t power_raw = (rx_buffer[7] << 8) | rx_buffer[8];
        last_power = (float)power_raw * 0.1f;
    }
    
    return last_power;
}

/**
 * @brief Log fault to non-volatile memory
 * @param code Fault code to log
 */
static void log_fault(FaultCode code) {
    const char* fault_names[] = {
        "NONE", "ESTOP", "NO_FLOW", "OVERTEMP_COIL", 
        "OVERTEMP_WATER", "OVERTEMP_CRUCIBLE", "DOOR_OPEN",
        "POWER_LOSS", "COMM_ERROR", "SENSOR_ERROR"
    };
    
    /* Format fault message */
    snprintf(fault_log, sizeof(fault_log), 
             "FAULT: %s at %lu seconds, Temp: %.1f°C, Power: %.0fW",
             fault_names[code], heater.runtime_seconds,
             heater.crucible_temperature, heater.actual_power);
    
    /* TODO: Write to EEPROM or flash */
}

/**
 * @brief Flow sensor interrupt handler
 */
void EXTI2_IRQHandler(void) {
    if (__HAL_GPIO_EXTI_GET_IT(GPIO_PIN_2) != RESET) {
        __HAL_GPIO_EXTI_CLEAR_IT(GPIO_PIN_2);
        flow_pulse_count++;
    }
}

/**
 * @brief Get current system status
 * @param status Pointer to status structure to fill
 */
void get_heater_status(InductionStatus* status) {
    status->enabled = heater.enabled;
    status->power_setpoint = heater.power_setpoint;
    status->actual_power = heater.actual_power;
    status->crucible_temp = heater.crucible_temperature;
    status->coil_temp = heater.coil_temperature;
    status->water_temp = heater.water_temperature;
    status->flow_rate = heater.flow_rate;
    status->fault_code = heater.fault_code;
    status->runtime_hours = heater.runtime_seconds / 3600.0f;
}

/**
 * @brief Set temperature control parameters
 * @param mode 0=manual, 1=auto
 * @param material 0=aluminum, 1=steel
 */
void set_temp_control_mode(uint8_t mode, uint8_t material) {
    heater.temp_control_mode = mode;
    heater.material_type = material;
    
    /* Reset PID on mode change */
    if (mode) {
        pid_reset(&temp_pid);
    }
}