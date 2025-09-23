/**
 * @file fpga_thermal_interface.h
 * @brief FPGA interface for thermal droplet tracking data
 * @details Receives real-time droplet position and temperature from FLIR A35
 * 
 * Protocol: UDP packets at 60Hz containing droplet state information
 * Used for acoustic field steering control
 */

#ifndef FPGA_THERMAL_INTERFACE_H
#define FPGA_THERMAL_INTERFACE_H

#include <stdint.h>
#include <string.h>

/* Configuration */
#define THERMAL_UDP_PORT        5000
#define THERMAL_PACKET_SIZE     28    // 7 floats × 4 bytes
#define MAX_TRACKED_DROPLETS    10
#define POSITION_TIMEOUT_MS     100   // Lost if no update for 100ms

/* Droplet state data structure - matches Python struct.pack format */
typedef struct __attribute__((packed)) {
    uint32_t track_id;        // Unique droplet identifier
    float x_mm;               // X position in mm from center
    float y_mm;               // Y position in mm from center  
    float z_mm;               // Z position (from acoustic model)
    float temperature_c;      // Temperature in Celsius
    float velocity_x;         // X velocity in mm/s
    float velocity_y;         // Y velocity in mm/s
} DropletData;

/* Tracking state for each droplet */
typedef struct {
    DropletData data;
    uint32_t last_update_ms;  // Timestamp of last update
    uint8_t active;           // 1 if currently tracked
    uint8_t stable;           // 1 if position stable for control
} DropletTracker;

/* Global tracking state */
static DropletTracker droplet_trackers[MAX_TRACKED_DROPLETS];
static uint8_t num_active_droplets = 0;

/**
 * @brief Initialize thermal tracking interface
 */
void thermal_interface_init(void) {
    memset(droplet_trackers, 0, sizeof(droplet_trackers));
    num_active_droplets = 0;
}

/**
 * @brief Process received thermal tracking data packet
 * @param packet Raw UDP packet data
 * @param timestamp_ms Current system time in milliseconds
 */
void process_thermal_packet(uint8_t* packet, uint32_t timestamp_ms) {
    DropletData* droplet = (DropletData*)packet;
    
    // Validate packet
    if (droplet->track_id >= MAX_TRACKED_DROPLETS) {
        return;  // Invalid ID
    }
    
    // Sanity check position (chamber is ±50mm)
    if (droplet->x_mm < -50 || droplet->x_mm > 50 ||
        droplet->y_mm < -50 || droplet->y_mm > 50) {
        return;  // Out of bounds
    }
    
    // Sanity check temperature
    if (droplet->temperature_c < 0 || droplet->temperature_c > 2000) {
        return;  // Unrealistic temperature
    }
    
    // Update tracker
    DropletTracker* tracker = &droplet_trackers[droplet->track_id];
    memcpy(&tracker->data, droplet, sizeof(DropletData));
    tracker->last_update_ms = timestamp_ms;
    
    // Mark as active if new
    if (!tracker->active) {
        tracker->active = 1;
        num_active_droplets++;
    }
    
    // Check if position is stable (low velocity)
    float speed = sqrtf(droplet->velocity_x * droplet->velocity_x + 
                       droplet->velocity_y * droplet->velocity_y);
    tracker->stable = (speed < 5.0);  // <5mm/s considered stable
}

/**
 * @brief Update tracking timeouts and remove stale tracks
 * @param current_time_ms Current system time in milliseconds
 */
void update_tracking_timeouts(uint32_t current_time_ms) {
    for (int i = 0; i < MAX_TRACKED_DROPLETS; i++) {
        DropletTracker* tracker = &droplet_trackers[i];
        
        if (tracker->active) {
            // Check for timeout
            if (current_time_ms - tracker->last_update_ms > POSITION_TIMEOUT_MS) {
                tracker->active = 0;
                tracker->stable = 0;
                num_active_droplets--;
            }
        }
    }
}

/**
 * @brief Get droplet position for acoustic control
 * @param track_id Droplet identifier
 * @param x_mm Output X position
 * @param y_mm Output Y position
 * @return 1 if droplet active and stable, 0 otherwise
 */
uint8_t get_droplet_position(uint32_t track_id, float* x_mm, float* y_mm) {
    if (track_id >= MAX_TRACKED_DROPLETS) {
        return 0;
    }
    
    DropletTracker* tracker = &droplet_trackers[track_id];
    
    if (tracker->active && tracker->stable) {
        *x_mm = tracker->data.x_mm;
        *y_mm = tracker->data.y_mm;
        return 1;
    }
    
    return 0;
}

/**
 * @brief Get full droplet state for advanced control
 * @param track_id Droplet identifier
 * @param data Output droplet data structure
 * @return 1 if droplet active, 0 otherwise
 */
uint8_t get_droplet_state(uint32_t track_id, DropletData* data) {
    if (track_id >= MAX_TRACKED_DROPLETS) {
        return 0;
    }
    
    DropletTracker* tracker = &droplet_trackers[track_id];
    
    if (tracker->active) {
        memcpy(data, &tracker->data, sizeof(DropletData));
        return 1;
    }
    
    return 0;
}

/**
 * @brief Calculate acoustic steering requirements based on droplet state
 * @param droplet Current droplet data
 * @param target_x Desired X position
 * @param target_y Desired Y position
 * @param force_x Output X steering force
 * @param force_y Output Y steering force
 */
void calculate_steering_force(const DropletData* droplet, 
                            float target_x, float target_y,
                            float* force_x, float* force_y) {
    // Position error
    float error_x = target_x - droplet->x_mm;
    float error_y = target_y - droplet->y_mm;
    
    // Simple PD control
    const float Kp = 0.1f;  // Proportional gain
    const float Kd = 0.05f; // Derivative gain
    
    *force_x = Kp * error_x - Kd * droplet->velocity_x;
    *force_y = Kp * error_y - Kd * droplet->velocity_y;
    
    // Temperature compensation (hotter = less dense = needs more force)
    float temp_factor = 1.0f + (droplet->temperature_c - 700.0f) / 1000.0f;
    *force_x *= temp_factor;
    *force_y *= temp_factor;
    
    // Clamp maximum force
    const float max_force = 1.0f;
    if (*force_x > max_force) *force_x = max_force;
    if (*force_x < -max_force) *force_x = -max_force;
    if (*force_y > max_force) *force_y = max_force;
    if (*force_y < -max_force) *force_y = -max_force;
}

/**
 * @brief Get statistics for debugging
 */
void get_tracking_stats(uint8_t* active_count, uint8_t* stable_count) {
    uint8_t stable = 0;
    
    for (int i = 0; i < MAX_TRACKED_DROPLETS; i++) {
        if (droplet_trackers[i].active && droplet_trackers[i].stable) {
            stable++;
        }
    }
    
    *active_count = num_active_droplets;
    *stable_count = stable;
}

#endif /* FPGA_THERMAL_INTERFACE_H */