# Induction Heater Troubleshooting Guide

## Diagnostic Tools Required
- Digital multimeter (true RMS)
- Oscilloscope (100MHz bandwidth minimum)  
- Clamp-on current meter (AC/DC)
- Infrared thermometer or thermal camera
- Insulation tester (megger)

---

## Problem: No Output Power

### Symptom
- Enable signal present but no heating
- Power meter reads 0W
- No acoustic noise from coil

### Diagnostic Steps

1. **Check Enable Chain**
   ```
   Measure at STM32 output (PA0):
   - Enabled: 3.3V HIGH
   - Disabled: 0V LOW
   
   Trace to optocoupler:
   - Input: 3.3V = LED on
   - Output: Check isolation side
   
   Verify at module:
   - Enable terminal: 5-24V present?
   ```

2. **Check Safety Interlocks**
   ```
   Emergency Stop: NC contacts closed?
   Door Switch: NC contacts closed?
   Flow Sensor: >1.5 L/min?
   Over-temp: All temps normal?
   ```

3. **Check Power Input**
   ```
   At main breaker: 240V present?
   After contactor: 240V when enabled?
   After EMI filter: 240V, low noise?
   At module input: 220-240V AC?
   ```

4. **Check Module Status**
   ```
   Module LEDs:
   - Power: Green?
   - Fault: Red? (check manual)
   - Ready: Green?
   
   Listen for:
   - Relay clicks on enable
   - Cooling fan running
   ```

### Solutions
- Reset E-stop and verify latch
- Check all connector seating
- Verify phase sequence (if 3-phase)
- Power cycle module (30s off)
- Replace enable optocoupler

---

## Problem: Low Power Output

### Symptom  
- Heating occurs but slowly
- Power <50% of setpoint
- Frequency unstable

### Diagnostic Steps

1. **Measure Actual Power**
   ```
   Clamp meter on L1:
   - Expected: ~13A at 3kW
   - Low: Check voltage
   
   Power meter reading:
   - Compare to setpoint
   - Check power factor
   ```

2. **Check Resonance**
   ```
   Oscilloscope on coil:
   - Frequency: 30-80kHz?
   - Waveform: Clean sine?
   - Amplitude: Stable?
   ```

3. **Verify Coil Inductance**
   ```
   Disconnect coil, measure:
   - Inductance: ~15μH
   - Resistance: <0.5Ω
   - No shorts between turns
   ```

4. **Inspect Work Coil**
   ```
   Visual check:
   - Turns spacing even?
   - No arcing marks?
   - Connections tight?
   - Proper coupling to load?
   ```

### Solutions
- Move coil closer to workpiece (5mm gap)
- Clean oxidation from connections
- Verify correct capacitor bank in module
- Check for shorted turns in coil
- Increase input voltage if low

---

## Problem: Overheating

### Symptom
- Coil temperature >60°C
- Module thermal fault
- Automatic power reduction

### Diagnostic Steps

1. **Check Cooling Flow**
   ```
   Flow rate: Must be >2 L/min
   Temperature rise: <10°C
   
   Inlet temp: <25°C ideal
   Outlet temp: <35°C max
   ```

2. **Inspect Cooling System**
   ```
   - Pump running full speed?
   - Radiator fan operating?
   - Radiator fins clean?
   - No kinks in tubing?
   - Reservoir level OK?
   ```

3. **Thermal Image Scan**
   ```
   Check for hot spots:
   - Coil connections
   - Module heatsink
   - Power terminals
   - Work coil turns
   ```

4. **Verify Heat Load**
   ```
   Calculate actual dissipation:
   - Power in × (1 - efficiency)
   - Should be <450W
   - If higher, check tuning
   ```

### Solutions
- Increase cooling flow rate
- Clean radiator with compressed air
- Add second radiator in series
- Reduce duty cycle (80% max)
- Improve ventilation around unit

---

## Problem: Electrical Noise/EMI

### Symptom
- Nearby equipment malfunction
- Radio interference
- Computer crashes

### Diagnostic Steps

1. **Check Grounding**
   ```
   Measure with megger:
   - Chassis to earth: <0.1Ω
   - Star ground point intact?
   - No ground loops?
   ```

2. **Verify EMI Filter**
   ```
   - Properly installed?
   - Earth connected?
   - Sufficient rating?
   ```

3. **Check Shielding**
   ```
   - Control cables shielded?
   - Shield grounded one end?
   - Power/control separated?
   ```

### Solutions
- Add ferrite cores to cables
- Improve equipment grounding
- Increase separation distance
- Add line filter on affected equipment
- Use twisted pair for signals

---

## Problem: Erratic Operation

### Symptom
- Power fluctuates randomly
- Frequency hunting
- Intermittent shutdowns

### Diagnostic Steps

1. **Monitor Power Quality**
   ```
   Oscilloscope on mains:
   - Voltage stability?
   - Harmonic distortion?
   - Voltage dips?
   ```

2. **Check Control Signals**
   ```
   PWM from STM32:
   - Frequency stable?
   - Duty cycle smooth?
   - No noise on signal?
   ```

3. **Inspect Connections**
   ```
   Wiggle test (POWER OFF):
   - All terminals tight?
   - No corroded contacts?
   - No loose crimps?
   ```

### Solutions
- Add input line reactor
- Replace control wiring with shielded
- Tighten all connections (15 Nm)
- Clean contacts with DeoxIT
- Stabilize input voltage

---

## Problem: Won't Reach Temperature

### Symptom
- Power at 100% but temperature low
- Extended melt times
- Poor coupling efficiency

### Diagnostic Steps

1. **Verify Power Delivery**
   ```
   At maximum power:
   - Input current: ~13A?
   - Frequency: optimal?
   - No current limiting?
   ```

2. **Check Coupling**
   ```
   - Coil centered on crucible?
   - Correct coil height?
   - Crucible material suitable?
   - No magnetic shielding?
   ```

3. **Measure Losses**
   ```
   - Excessive radiative loss?
   - Insulation degraded?
   - Air gaps in magnetic path?
   ```

### Solutions
- Optimize coil position (trial and error)
- Add susceptor for poor conductors
- Increase insulation around crucible
- Verify material properties
- Check for heat sink effects

---

## Maintenance Actions

### Daily
- Check cooling flow and temperature
- Verify no error codes
- Listen for unusual sounds
- Visual inspection for arcing

### Weekly
- Check electrical connections tightness
- Clean coil of any debris
- Verify cooling fluid level
- Test emergency stop

### Monthly
- Megger test insulation
- Calibrate power meter
- Clean radiator fins
- Check door interlocks

### Quarterly
- Replace cooling fluid
- Deep clean all components
- Thermal image under load
- Verify all safety systems

### Annually
- Replace cooling tubing
- Recalibrate sensors
- Professional inspection
- Update documentation

---

## Error Code Reference

| Code | Meaning | Action |
|------|---------|--------|
| E01 | Over-temperature module | Check cooling, reduce power |
| E02 | Over-current | Check for shorts, reduce load |
| E03 | Phase loss | Check input power |
| E04 | Frequency fault | Check coil/capacitor |
| E05 | Communication error | Check control connection |
| E06 | Flow fault | Check cooling system |
| E07 | Door open | Close enclosure |
| E08 | E-stop active | Reset emergency stop |

---

## When to Call Support

Contact manufacturer support if:
- Multiple components failed
- Repeated shutdowns after checks
- Unusual sounds from module
- Visible damage to power devices
- Errors not in manual

**Have ready:**
- Model and serial number
- Error codes displayed
- Power/frequency readings
- Description of events
- Commissioning report