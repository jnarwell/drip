# ICD-003: Sensor-Control Interface

## Document Control
- **ICD Number**: ICD-003
- **Revision**: 1.0
- **Date**: 2025-09-14
- **Status**: Draft
- **Criticality**: MEDIUM

## 1. Interface Overview
- **Purpose**: Define interface between Crucible Subsystem and Power/Control Subsystem
- **Interface Types**: data, electrical
- **Side A Components**: Optris PI 1M Thermal Camera
- **Side B Components**: Industrial PC

## 2. Interface Requirements

| Parameter | Nominal | Min | Max | Units | Verification |
|-----------|---------|-----|-----|-------|--------------|
| Data Rate | 32 | 30 | 1000 | Hz | Network analyzer |
| Latency | 5 | 0 | 10 | ms | Oscilloscope measurement |
| Supply Voltage | 24 | 20 | 28 | VDC | Multimeter measurement |

## 3. Physical Interface

### 3.1 Mechanical Details
Not specified

### 3.2 Thermal Details
Not specified

### 3.3 Electrical Details
- **Interface**: Gigabit Ethernet
- **Connector**: RJ45
- **Cable Type**: Cat6A shielded
- **Max Distance**: 100m

## 4. Component Specifications

### Side A Components
**Optris PI 1M Thermal Camera**
- ⚠️ Component not found in registry


### Side B Components
**Industrial PC**
- Power Consumption: 65W
- Operating Temp: 0-50°C
- Weight: 2.0kg
- Cost: $0
- Supplier: None


## 5. Verification & Validation

### 5.1 Test Equipment
- Network analyzer
- Ethernet tester
- Multimeter

### 5.2 Test Procedure
1. **Pre-Test Setup**
   - Verify all components installed correctly
   - Check electrical connections and continuity
   - Calibrate test equipment
   - Document baseline conditions

2. **Baseline Measurements**
   - Measure Data Rate using Network analyzer
     * Expected: 32 Hz (±485.0)
   - Measure Latency using Oscilloscope measurement
     * Expected: 5 ms (±5.0)
   - Measure Supply Voltage using Multimeter measurement
     * Expected: 24 VDC (±4.0)

3. **Functional Verification**
   - Power on system incrementally
   - Monitor all interface parameters
   - Verify normal operation for 30 minutes
   - Check for error conditions or alarms

4. **Stress Testing**
   - Gradually increase to maximum rated conditions
   - Monitor for parameter drift or instability
   - Verify parameters remain within specification
   - Document any degradation or warnings

5. **Acceptance Testing**
   - Run full 4-hour endurance test
   - Verify all requirements continuously met
   - Document final measurements
   - Generate acceptance report

### 5.3 Acceptance Criteria
- All parameters within specified min/max ranges
- No thermal damage to components
- Stable operation for 4+ hours
- Interface meets all functional requirements

## 6. Interface Compatibility Analysis
### Compatibility Status: ❌ INCOMPATIBLE

**Critical Issues:**
- ❌ Insufficient power supply: 65W demand vs 0W supply



## 7. Risk Assessment
| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Electrical fault causing component damage | Low | High | Circuit protection, isolation, ground fault detection |
| Data corruption or communication loss | Medium | Medium | Error checking, redundant paths, watchdog timers |


## 8. Design Considerations

### 8.1 Safety Requirements
- All electrical interfaces must meet IEC 61010-1 safety standards
- Thermal interfaces require overheat protection
- Mechanical interfaces must have fail-safe mounting

### 8.2 Environmental Conditions
- Operating Temperature: 15-35°C ambient
- Relative Humidity: 20-80% non-condensing
- Vibration: <0.5g RMS

### 8.3 Maintenance Access
- All connectors accessible within 30 seconds
- Test points marked and accessible
- Service documentation required for each interface

## 9. Change History
| Date | Revision | Description | Author |
|------|----------|-------------|--------|
| 2025-09-14 | 1.0 | Initial release | System Engineer |

---
*This ICD was auto-generated from component specifications on 2025-09-14 14:18:04*
