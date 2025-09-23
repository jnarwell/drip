/**
 * @file induction_heater.h
 * @brief Header for induction heater control system
 */

#ifndef INDUCTION_HEATER_H
#define INDUCTION_HEATER_H

#include <stdint.h>

/* Status structure for external monitoring */
typedef struct {
    uint8_t enabled;
    float power_setpoint;
    float actual_power;
    float crucible_temp;
    float coil_temp;
    float water_temp;
    float flow_rate;
    uint8_t fault_code;
    float runtime_hours;
} InductionStatus;

/* Public functions */
int induction_heater_init(void);
void induction_heater_update(void);
void set_heater_power(float power_percent);
void get_heater_status(InductionStatus* status);
void set_temp_control_mode(uint8_t mode, uint8_t material);
void emergency_shutdown(void);

/* Material constants */
#define MATERIAL_ALUMINUM   0
#define MATERIAL_STEEL      1

/* Control modes */
#define CONTROL_MANUAL      0
#define CONTROL_AUTO_PID    1

#endif /* INDUCTION_HEATER_H */