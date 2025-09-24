# Test Procedures
!!! danger "PLANNING DOCUMENTATION ONLY"
    **No hardware exists. No simulations completed. These are conceptual targets only.**

!!! warning "Test Status: Planning Only"
    - Hardware: Not available
    - Simulations: Not yet performed  
    - Expected Execution: After prototype assembly
    - Current Status: Defining test procedures and acceptance criteria

## General Test Requirements

### Pre-Test Preparation
1. Will verify all safety systems operational
2. Will check calibration certificates current
3. Will review test procedure with team
4. Will prepare data collection sheets
5. Will verify environmental conditions

### Test Environment
- Temperature: 20±5°C
- Humidity: 30-70% RH
- Vibration: <0.1g RMS
- EMI: Controlled environment
- Power: Stable ±5%

## Detailed Test Procedures

### TP-001: Acoustic Frequency Verification

**Purpose**: Will verify transducer array operates at 40kHz ±100Hz

**Equipment**:
- Oscilloscope with FFT capability
- Current probe
- Hydrophone (optional)

**Procedure**:
1. Power on acoustic system at 50% power
2. Allow 10 minutes warmup
3. Connect current probe to transducer drive
4. Capture waveform (10ms window)
5. Perform FFT analysis
6. Record peak frequency
7. Repeat for all 18 transducers
8. Increase to 100% power
9. Verify frequency stability

**Pass Criteria**:
- Frequency: 40kHz ±100Hz
- All transducers within ±50Hz
- <1% drift over 1 hour

### TP-002: Acoustic Field Uniformity

**Purpose**: Will verify acoustic field uniformity within specifications

**Equipment**:
- Hydrophone array (3×3 minimum)
- 3-axis positioning system
- Data acquisition system

**Procedure**:
1. Fill chamber with standard atmosphere
2. Position hydrophone at center
3. Energize transducers at nominal power
4. Record pressure amplitude
5. Move hydrophone in 10mm grid
6. Map entire build volume
7. Calculate uniformity metrics
8. Generate 3D field plot

**Pass Criteria**:
- Central 80% volume: ±5% uniformity
- No dead zones >5mm diameter
- Symmetric field pattern

### TP-003: Temperature Range Validation

**Purpose**: Verify system achieves required temperature range

**Equipment**:
- Type R thermocouples (3)
- Data logger
- Thermal camera

**Procedure**:
1. Install thermocouples in crucible
2. Start with ambient temperature
3. Ramp heating at 50°C/min
4. Record temperatures every second
5. Hold at 700°C for 10 minutes
6. Continue ramp to 1580°C
7. Hold for 5 minutes
8. Emergency cooling test
9. Verify cooling rate >1000°C/s

**Pass Criteria**:
- Achieves 700°C for aluminum
- Achieves 1580°C for steel
- Stable temperature control ±10°C
- No thermal runaway

### TP-004: Position Accuracy Test

**Purpose**: Verify droplet positioning accuracy

**Equipment**:
- High-speed camera (>1000 fps)
- Calibration grid
- Image analysis software

**Procedure**:
1. Place calibration grid in view
2. Generate test droplet (2mm diameter)
3. Command position changes:
   - X: -10, -5, 0, +5, +10mm
   - Y: -10, -5, 0, +5, +10mm
   - Z: -5, 0, +5mm
4. Record actual positions
5. Calculate positioning error
6. Test dynamic tracking
7. Verify response time

**Pass Criteria**:
- Static accuracy: ±0.3mm
- Dynamic accuracy: ±0.5mm
- Response time: <100ms
- No oscillation/instability

### TP-005: Power Consumption Analysis

**Purpose**: Verify power consumption within budget

**Equipment**:
- 3-phase power analyzer
- Current probes
- Data logger

**Procedure**:
1. Connect analyzer to main power
2. Start with system idle
3. Record baseline power
4. Energize subsystems sequentially:
   - Control system only
   - Add acoustic system
   - Add heating system
   - Add cooling system
5. Run at full power for 1 hour
6. Record power factor
7. Calculate efficiency

**Pass Criteria**:
- Idle power: <500W
- Full power: <5kW net consumption
- Power factor: >0.95
- Efficiency: >90%

## Data Recording

### Test Data Sheet Template
```
Test ID: _______    Date: _______    Operator: _______

Environmental Conditions:
- Temperature: ___°C    Humidity: ___%    Pressure: ___mbar

Equipment Used:
- Model: _______    Cal Due: _______    Serial: _______

Measurements:
Time | Parameter | Value | Units | Notes
_____|___________|_______|_______|_______

Result: PASS / FAIL
Comments: _________________________________________________
```

### Electronic Data
- Store all raw data in `/test_data/[date]/[test_id]/`
- Export processed results as CSV
- Generate plots as PNG/PDF
- Archive within 24 hours

## Safety Procedures

### PPE Requirements
- Safety glasses (always)
- Heat-resistant gloves (thermal tests)
- Hearing protection (acoustic tests)
- Lab coat (material handling)

### Emergency Procedures
1. **Emergency Stop**: Red button at operator station
2. **Fire**: CO2 extinguisher nearby
3. **Injury**: First aid kit, call 911
4. **Spill**: Spill kit under bench

### Hazard Mitigation
- High voltage: Lockout/tagout procedures
- High temperature: Barriers and warnings
- Ultrasonic: Exposure time limits
- Laser (if used): Proper eyewear
