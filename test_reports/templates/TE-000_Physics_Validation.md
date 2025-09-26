---
test_id: TE-000
test_name: Acoustic Steering Physics Validation
test_purpose: Validate lateral steering forces on falling droplets are achievable
verification_type: FEASIBILITY
components_verified:
- name: 40kHz Transducers
  id: 40KHZ_TRANSDUCERS
  part_number: TBD
prerequisite_tests: []
enables_tests: 
- TE-001
estimated_duration: 16.0 hours
required_equipment:
- Single 40kHz transducer
- Function generator
- Audio amplifier (100W)
- High-speed camera (>1000fps)
- Laser vibrometer or pressure sensor
- Test droplets (Tin/Bismuth low-temp)
- Precision positioning stage
- Data acquisition system
status: NOT_STARTED
date_executed: null
test_engineer: null
result: null
---

# Test Report: TE-000 - Acoustic Steering Physics Validation

!!! critical "GATEWAY TEST"
    **This test MUST PASS before ANY other testing proceeds**
    **Validates core physics assumption of acoustic steering**

## 1.0 Test Overview

**Purpose**: Prove that a single 40kHz transducer can generate sufficient lateral force to deflect a falling droplet by 1-2mm during its descent, validating the steering (not levitation) approach.

**Success Criteria**:
- Demonstrate lateral force of 10⁻⁷ to 10⁻⁸ N on 2mm droplet
- Achieve 1-2mm lateral deflection during 150mm fall
- Confirm force scales with acoustic power as predicted
- Validate no attempt at vertical levitation is made

## 2.0 Physics Validation Tests

### 2.1 Acoustic Pressure Field Characterization
- Map pressure distribution at 20-100mm from transducer
- Verify 2-3 kPa pressure amplitude achievable
- Confirm beam width ~λ/2 (4.3mm) at focus
- Document lateral pressure gradients

### 2.2 Force Measurement on Static Target
- Suspend 2mm aluminum sphere on microbalance
- Measure lateral force vs. acoustic power
- Expected: ~10⁻⁷ N at 10W input
- Verify force direction perpendicular to gravity

### 2.3 Droplet Deflection Test
- Release test droplet (tin/bismuth, melting point ~138°C)
- Fall height: 150mm
- Measure lateral displacement with/without acoustic field
- Target: 1-2mm deflection achieved
- High-speed camera tracking at 1000+ fps

### 2.4 Scaling Validation
- Test with 1mm, 2mm, 3mm droplets
- Verify force scales with r³ as predicted
- Document minimum droplet size for effective steering
- Maximum droplet size before control lost

## 3.0 Critical Measurements

| Parameter | Expected Value | Tolerance | Pass Criteria |
|-----------|---------------|-----------|---------------|
| Acoustic frequency | 40 kHz | ±100 Hz | Within range |
| Pressure amplitude | 2-3 kPa | ±20% | >2 kPa achieved |
| Lateral force | 10⁻⁷ N | Order of magnitude | Measurable deflection |
| Droplet deflection | 1-2 mm | ±0.5 mm | >0.5 mm minimum |
| Response time | <10 ms | ±5 ms | Fast enough for control |

## 4.0 Go/No-Go Decision

**PROCEED if ALL are true:**
- [ ] Lateral deflection >0.5mm achieved
- [ ] Force measurements match physics model ±50%
- [ ] No vertical levitation attempted or expected
- [ ] Scaling laws validated

**STOP and REDESIGN if ANY are true:**
- [ ] Lateral deflection <0.5mm
- [ ] Forces 10× weaker than predicted
- [ ] Acoustic coupling fails above 200°C
- [ ] Control response >50ms

## 5.0 Test Information

### 5.1 Test Overview
- **Test ID**: TE-000
- **Test Name**: Acoustic Steering Physics Validation
- **Purpose**: Validate lateral steering forces on falling droplets are achievable
- **Type**: FEASIBILITY
- **Duration**: 16.0 hours (2 days)
- **Date Executed**: _[To be filled]_
- **Test Engineer**: _[To be filled]_

### 5.2 Components Under Test
| Component | ID | Part Number | Serial Number |
|-----------|----|--------------|--------------|
| 40kHz Transducers | 40KHZ_TRANSDUCERS | _[TBD]_ | _[Record S/N]_ |

### 5.3 Prerequisites
_No prerequisite tests - This is the first test_

### 5.4 Test Dependencies
This test enables:
- TE-001 through TE-015 (All acoustic tests)
- Full system development

## 6.0 Required Equipment

### 6.1 Primary Equipment
| Equipment | Model/Spec | Calibration Due | Setup Notes |
|-----------|------------|-----------------|-------------|
| 40kHz Transducer | Single unit from batch | N/A | Mount on precision stage |
| Function Generator | 40kHz, 10Vpp min | _[Date]_ | Verify frequency accuracy |
| Audio Amplifier | 100W, 40kHz capable | N/A | Check impedance matching |
| High-Speed Camera | >1000fps, 640x480 min | _[Date]_ | Position for side view |

### 6.2 Measurement Equipment
| Equipment | Purpose | Accuracy Required |
|-----------|---------|-------------------|
| Laser Vibrometer | Pressure field mapping | ±5% |
| Microbalance | Force measurement | 0.01mg resolution |
| Data Acquisition | Record all signals | 100kHz sampling |
| Positioning Stage | Transducer alignment | ±0.1mm |

## 7.0 Test Procedure

### 7.1 Setup
1. Mount single transducer on positioning stage
2. Connect function generator through amplifier
3. Position high-speed camera for side view
4. Set up laser vibrometer for pressure mapping
5. Prepare test droplets (Tin/Bismuth alloy)
6. Configure data acquisition system

### 7.2 Pressure Field Characterization
1. Set transducer to 40kHz, 5W input power
2. Map pressure field in 5mm grid, 20-100mm from face
3. Record pressure amplitude at each point
4. Increase power to 10W, repeat mapping
5. Document beam profile and focal region

### 7.3 Static Force Measurement
1. Suspend 2mm aluminum sphere on microbalance
2. Position sphere 50mm from transducer
3. Apply acoustic field at varying power (1-10W)
4. Record lateral force vs. power
5. Repeat at different distances (30-70mm)

### 7.4 Droplet Deflection Test
1. Heat crucible with test alloy to 150°C
2. Release single droplet from 200mm height
3. Apply acoustic field when droplet at 150mm
4. Track droplet trajectory with high-speed camera
5. Measure lateral displacement at substrate
6. Repeat 10 times for statistics

### 7.5 Scaling Validation
1. Repeat deflection test with 1mm droplets
2. Repeat with 3mm droplets
3. Plot deflection vs. droplet size
4. Verify r³ scaling relationship

## 8.0 Data Analysis

### 8.1 Required Calculations
- Acoustic pressure from vibrometer data
- Lateral force from balance readings
- Droplet trajectory from video analysis
- Deflection statistics (mean, std dev)
- Force scaling verification

### 8.2 Acceptance Criteria
- Lateral deflection >0.5mm (target 1-2mm)
- Force measurements within 50% of theory
- Consistent results across 10 trials
- Proper scaling with droplet size

## 9.0 Results

### 9.1 Pressure Field Results
_[To be completed during test]_
- Maximum pressure achieved: ______ kPa
- Beam width at focus: ______ mm
- Optimal distance: ______ mm

### 9.2 Force Measurement Results
_[To be completed during test]_
- Force at 10W: ______ N
- Force scaling: ______ N/W
- Optimal position: ______ mm

### 9.3 Droplet Deflection Results
_[To be completed during test]_
- Mean deflection: ______ mm
- Standard deviation: ______ mm
- Success rate: ______ %

### 9.4 Go/No-Go Decision
_[To be completed after test]_
- [ ] Physics validated - PROCEED
- [ ] Insufficient performance - REDESIGN REQUIRED

## 10.0 Safety Considerations

### 10.1 Hazards
- High-frequency acoustic energy (hearing protection required)
- Hot metal droplets (150°C)
- Electrical hazards (100W amplifier)

### 10.2 PPE Required
- Safety glasses
- Hearing protection
- Heat-resistant gloves
- Lab coat

### 10.3 Emergency Procedures
- E-stop for all power
- Fire extinguisher nearby
- First aid for burns

## 11.0 Notes and Observations

_[Space for test engineer notes during execution]_

---

**Test Status**: NOT_STARTED  
**Next Steps**: Schedule test after component procurement  
**Estimated Cost**: $2,000-3,000 for basic equipment if not available