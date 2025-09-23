# Induction Heater Safety and Commissioning Procedures

## ⚠️ SAFETY WARNINGS - READ BEFORE PROCEEDING

### HIGH VOLTAGE - 240V AC
- This system uses lethal voltages
- Always lock out power before servicing
- Use insulated tools and PPE
- Never bypass safety interlocks

### HIGH TEMPERATURE - Up to 1580°C  
- Crucible and coil reach extreme temperatures
- Molten metal can cause severe burns
- Always wear face shield and heat-resistant gloves
- Keep fire extinguisher nearby (Class D for metals)

### STRONG MAGNETIC FIELDS
- Magnetic field extends >30cm from coil
- Keep pacemakers at least 1m away
- Remove all metal jewelry before operation
- Secure loose metal objects

### WATER + ELECTRICITY HAZARD
- Check for leaks before every startup
- Never operate without cooling flow
- Immediately shut down if leak detected
- Keep electrical connections elevated

---

## Pre-Installation Safety Checklist

### Required Safety Equipment
- [ ] Face shield (ANSI Z87.1)
- [ ] Heat-resistant gloves (rated 500°C)
- [ ] Insulated tools (1000V rated)
- [ ] Class D fire extinguisher
- [ ] First aid kit with burn gel
- [ ] Emergency shower/eyewash station nearby

### Electrical Requirements
- [ ] 240V 30A circuit installed by licensed electrician
- [ ] GFCI breaker installed and tested
- [ ] Proper grounding (<0.1Ω to earth)
- [ ] Lockout/tagout devices available
- [ ] Emergency stop accessible within 1m

### Environmental Requirements
- [ ] Minimum 1m clearance around unit
- [ ] Adequate ventilation (>200 CFM)
- [ ] No flammable materials within 2m
- [ ] Concrete or metal floor (no wood)
- [ ] Temperature 10-35°C, <80% humidity

---

## Commissioning Test Sequence

### Stage 1: Electrical Safety Tests (Power OFF)

#### 1.1 Continuity Tests
```
Equipment: Digital multimeter
Settings: Resistance (Ω)

Test Points                Expected Result
-----------                ---------------
L1 to L2                   >1MΩ (open)
L1 to Ground               >1MΩ (insulated)
L2 to Ground               >1MΩ (insulated)
Ground to Chassis          <0.1Ω (bonded)
E-stop NC contacts         <1Ω (closed)
Door interlock NC          <1Ω (closed)
```

#### 1.2 Insulation Resistance Test
```
Equipment: Megger (insulation tester)
Test Voltage: 500V DC

Test                       Expected Result
----                       ---------------
All circuits to ground     >1MΩ minimum
Between power circuits     >1MΩ minimum
Record all readings in log
```

#### 1.3 Ground Fault Test
```
Test GFCI function:
1. Press TEST button → Breaker should trip
2. Reset breaker
3. Press RESET button → Power restored
4. Inject 5mA to ground → Trip in <30ms
```

### Stage 2: Control System Tests (24V Only)

#### 2.1 STM32 Interface Test
```
Power: 24V control only (mains OFF)

Verify:
□ STM32 boots correctly
□ All status LEDs functional
□ UART communication established
□ Emergency stop input reads correctly
□ Flow sensor input detected
□ Temperature ADC channels reading
```

#### 2.2 Interlock Logic Test
```
Test each safety interlock:

1. Press E-stop → Enable output goes LOW
2. Open door → Enable output goes LOW
3. Disconnect flow sensor → Fault after 2s
4. Simulate over-temp → Shutdown triggered
5. Verify all faults logged correctly
```

### Stage 3: Cooling System Tests (No Power)

#### 3.1 Pressure Test
```
1. Cap work coil outlet
2. Apply 3 bar (45 PSI) air pressure
3. Monitor pressure gauge for 15 minutes
4. Pressure drop <0.1 bar = PASS
5. Check all connections with soap solution
```

#### 3.2 Flow Test
```
1. Fill system with water
2. Run pump at full speed
3. Measure flow rate: Must be >2.0 L/min
4. Check for air bubbles
5. Verify no leaks at full flow
```

#### 3.3 Thermal Test
```
1. Install all temperature sensors
2. Verify ambient readings (20-25°C)
3. Heat water to 40°C with external source
4. Confirm all sensors track correctly
5. Test high-temperature alarm at 35°C
```

### Stage 4: Low Power Tests (10% Power)

#### 4.1 Initial Power-On
```
⚠️ DANGER ZONE - Full PPE Required

1. Verify cooling running >5 minutes
2. Close all safety interlocks  
3. Enable 240V mains power
4. Check phase rotation (if 3-phase)
5. Listen for abnormal sounds
6. Check for arcing/sparking
```

#### 4.2 Frequency Sweep
```
Power Setting: 10% (300W)
Duration: 30 seconds per test

1. Insert ferrite test slug in coil
2. Enable power at 10%
3. Verify frequency 30-80kHz
4. Monitor module temperature
5. Confirm slug heats uniformly
6. Check for electromagnetic interference
```

#### 4.3 Control Response
```
1. Set power to 0% → Output disabled
2. Increase to 10% → 300W ±10%
3. Test E-stop → Immediate shutdown
4. Restart and verify normal operation
5. Test PWM control linearity
```

### Stage 5: Progressive Power Tests

#### 5.1 Power Ramp Test
```
Increase power in steps:
- 10% (300W) for 1 minute
- 25% (750W) for 1 minute
- 50% (1500W) for 1 minute
- 75% (2250W) for 1 minute
- 100% (3000W) for 10 seconds

Monitor at each step:
□ Actual power matches setpoint ±10%
□ Frequency remains 30-80kHz
□ Coil temperature <60°C
□ Water outlet <35°C
□ No abnormal sounds/smells
```

#### 5.2 Load Test with Material
```
Material: 100g aluminum slug
Crucible: Installed and centered

1. Preheat system 50% for 5 min
2. Insert aluminum slug
3. Ramp to 100% over 60 seconds
4. Achieve melt in <5 minutes
5. Monitor temperature rise rate
6. Verify PID control stability
```

### Stage 6: Full System Validation

#### 6.1 Thermal Imaging
```
Equipment: FLIR or similar (>320x240)

Scan at 100% power:
□ Coil <80°C (water cooled)
□ Connections <60°C
□ Module heatsink <70°C
□ No hot spots on wiring
□ Uniform coil heating
```

#### 6.2 Efficiency Test
```
Measure at steady state:
- Input: Power meter on AC side
- Output: Calorimetry on water loop
- Calculate: η = P_out/P_in
- Expected: >80% efficiency
```

#### 6.3 Extended Run Test
```
Duration: 1 hour continuous
Power: 80% (2400W)
Material: Steel slugs

Monitor every 10 minutes:
- System temperatures
- Power consumption  
- Cooling performance
- Frequency stability
- No component degradation
```

---

## Commissioning Sign-Off

### Test Results Summary

| Test Stage | Test Name | Result | Technician | Date |
|------------|-----------|---------|------------|------|
| 1.1 | Continuity | _____ | _______ | __/__/__ |
| 1.2 | Insulation | _____ | _______ | __/__/__ |
| 1.3 | GFCI | _____ | _______ | __/__/__ |
| 2.1 | Control System | _____ | _______ | __/__/__ |
| 2.2 | Interlocks | _____ | _______ | __/__/__ |
| 3.1 | Pressure Test | _____ | _______ | __/__/__ |
| 3.2 | Flow Test | _____ | _______ | __/__/__ |
| 4.1 | Initial Power | _____ | _______ | __/__/__ |
| 4.2 | Frequency | _____ | _______ | __/__/__ |
| 5.1 | Power Ramp | _____ | _______ | __/__/__ |
| 5.2 | Material Test | _____ | _______ | __/__/__ |
| 6.1 | Thermal Image | _____ | _______ | __/__/__ |
| 6.2 | Efficiency | _____ | _______ | __/__/__ |
| 6.3 | Extended Run | _____ | _______ | __/__/__ |

### Final Measurements
- Resonant Frequency: _______ kHz
- Max Power Achieved: _______ W
- System Efficiency: _______ %
- Melt Time (Al): _______ minutes
- Coolant Flow Rate: _______ L/min

### Certification

I certify that this induction heating system has been installed, tested, and commissioned according to all safety procedures and performs within specifications.

**Lead Technician**: _________________________ Date: ___________

**Safety Officer**: __________________________ Date: ___________

**System Owner**: ____________________________ Date: ___________

---

## Post-Commissioning

### Training Requirements
All operators must complete:
1. 2-hour safety orientation
2. Hands-on operation with supervision
3. Emergency response procedures
4. Written test (>80% to pass)

### Documentation Package
Provide to owner:
1. This completed commissioning report
2. All test data and thermal images
3. Operating procedures manual
4. Emergency contact list
5. Maintenance schedule
6. Spare parts list

### Warranty Activation
- Register OEM module serial number
- Submit commissioning report
- Note any deviations from spec
- Schedule 30-day follow-up