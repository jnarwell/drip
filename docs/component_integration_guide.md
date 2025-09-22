# Component Integration Guide
!!! danger "PLANNING DOCUMENTATION ONLY"
    **No hardware exists. No simulations completed. These are conceptual targets only.**

## Overview
This guide covers the component selection, procurement, and integration process for the Acoustic Manufacturing System.

## Component Library Structure

### 1. Component Specifications (`models/component_library.py`)
- **Component Database**: Central repository of all component specifications
- **COTS Options**: Multiple vendor options for each component
- **Trade Study Support**: Scoring and comparison framework
- **BOM Generation**: Automatic bill of materials by level

### 2. Supplier Management (`models/supplier_database.py`)
- **Contact Information**: Vendor contacts and payment terms
- **Lead Time Tracking**: Typical delivery schedules
- **Volume Discounts**: Quantity-based pricing calculations
- **Category Filtering**: Find suppliers by component type

### 3. Verification Matrix (`tests/design_verification_matrix.py`)
- **Test Requirements**: Maps requirements to test methods
- **Acceptance Criteria**: Clear pass/fail criteria
- **Test Equipment**: Required instrumentation
- **Progress Tracking**: Monitor verification status

## Key Components by Subsystem

### Acoustic Array
- **Transducers**: 10kHz ultrasonic, 25W per unit
  - Level 1: 18 units
  - Level 4: 72 units
  - Primary: APC International APC-10K-25W-HT
  - Lead time: 4 weeks

### Control System
- **FPGA**: Phase control for transducer array
  - Intel Cyclone V or Xilinx Artix-7
  - 72+ channels for Level 4
  - Lead time: 2-3 weeks

### Thermal Sensing
- **IR Camera**: See [Thermal Camera Specifications](components/specs.md#thermal-sensing-specifications)
  - Lead time: 6 weeks (critical path)

### Thermal System (Level 2+)
- **Induction Heater**: Ambrell EASYHEAT
  - 8kW power
  - Water cooled
  - Lead time: 8 weeks (critical path)

## Procurement Strategy

### Phase 1: Long Lead Items (Week 1)
1. Optris PI 1M thermal camera
2. Ambrell induction system (for Level 2)
3. Custom transducers (if selected)

### Phase 2: Standard Components (Week 2-3)
1. FPGA development boards
2. STM32 microcontrollers
3. Power supplies and cooling

### Phase 3: Mechanical/Integration (Week 4+)
1. Chamber materials
2. Mounting hardware
3. Cables and connectors

## Cost Optimization

### Volume Discounts
- Transducers: 5% at 50 units, 10% at 100 units
- FPGAs: Better pricing at 100+ units
- Consider bulk orders for Level 4

### Alternative Sourcing
- Piezo Technologies: Lower cost, longer lead
- Used/refurbished thermal cameras
- Academic discounts where applicable

## Risk Mitigation

### High Risk Components
1. **Thermal Camera**: Single source, high cost
   - Mitigation: Order early, consider backup
   
2. **Induction System**: Long lead time
   - Mitigation: Start procurement in Week 1
   
3. **Custom Transducers**: Unproven performance
   - Mitigation: Order samples first

### Supply Chain Backup Plans
- Maintain alternate vendor options
- Keep critical spares for Level 1
- Document all custom modifications

## Integration Checklist

### Mechanical Integration
- [ ] Transducer array mounting verified
- [ ] Thermal isolation implemented
- [ ] Cable routing completed
- [ ] Cooling connections tested

### Electrical Integration
- [ ] Power distribution verified
- [ ] Signal integrity checked
- [ ] Grounding scheme implemented
- [ ] EMI/RFI mitigation tested

### Software Integration
- [ ] FPGA firmware loaded
- [ ] STM32 firmware programmed
- [ ] PC software configured
- [ ] Communication verified

### System Validation
- [ ] Component acceptance tests
- [ ] Subsystem integration tests
- [ ] Full system verification
- [ ] Performance validation

## Using the Tools

### Component Selector GUI
```bash
python tools/component_selector.py
```
- Browse components by category
- Compare COTS options
- Generate BOMs
- Export selections

### Verification Tracking
```bash
python tests/design_verification_matrix.py
```
- View test requirements
- Generate test procedures
- Track completion status

### Analysis Notebooks
```bash
jupyter lab notebooks/component_analysis.ipynb
```
- Cost analysis by level
- Lead time visualization
- Risk assessment
- Supplier analysis

## Next Steps
1. Review component selections with team
2. Request quotes from suppliers
3. Finalize Level 1 BOM
4. Begin procurement process
5. Set up verification tracking