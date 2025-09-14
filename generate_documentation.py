#!/usr/bin/env python3
"""
Master documentation generator for Acoustic Manufacturing System
Generates all ICDs, validation reports, and documentation
"""

import os
import sys
from datetime import datetime

# Import generators
from models.interfaces.icd_generator import ICDGenerator
from models.interfaces.interface_validator import InterfaceValidator

def main():
    """Generate all documentation"""
    
    print("=" * 60)
    print("ACOUSTIC MANUFACTURING SYSTEM")
    print("Documentation Generation Suite")
    print("=" * 60)
    print()
    
    # 1. Generate ICDs
    print("1. Generating Interface Control Documents...")
    try:
        icd_gen = ICDGenerator()
        icd_gen.generate_all_icds()
        print("   ✅ ICDs generated successfully")
    except Exception as e:
        print(f"   ❌ ICD generation failed: {e}")
        return False
    print()
    
    # 2. Validate Interfaces
    print("2. Validating Interfaces...")
    try:
        validator = InterfaceValidator()
        report = validator.generate_validation_report()
        
        os.makedirs("icds/generated", exist_ok=True)
        with open("icds/generated/validation_report.md", "w") as f:
            f.write(report)
        print("   ✅ Validation report generated")
    except Exception as e:
        print(f"   ❌ Validation failed: {e}")
        return False
    print()
    
    # 3. Generate Verification Matrix
    print("3. Generating Verification Matrix...")
    try:
        from tests.design_verification_matrix import generate_verification_report
        
        os.makedirs("verification", exist_ok=True)
        for phase in ["Level 1", "Level 2", "Level 3", "Level 4"]:
            df = generate_verification_report(phase)
            filename = f"verification/{phase.replace(' ', '_')}_verification.csv"
            df.to_csv(filename, index=False)
            print(f"   ✓ Generated {filename}")
        print("   ✅ Verification matrices generated")
    except Exception as e:
        print(f"   ⚠️  Verification matrix generation skipped: {e}")
    print()
    
    # 4. Create System Block Diagram
    print("4. Generating System Architecture Diagrams...")
    try:
        generate_system_diagrams()
        print("   ✅ System diagrams generated")
    except Exception as e:
        print(f"   ❌ Diagram generation failed: {e}")
        return False
    print()
    
    # 5. Generate Component Summary
    print("5. Generating Component Summary...")
    try:
        generate_component_summary()
        print("   ✅ Component summary generated")
    except Exception as e:
        print(f"   ❌ Component summary failed: {e}")
    print()
    
    # 6. Generate Integration Guide
    print("6. Generating Integration Guide...")
    try:
        generate_integration_guide()
        print("   ✅ Integration guide generated")
    except Exception as e:
        print(f"   ❌ Integration guide failed: {e}")
    print()
    
    print("=" * 60)
    print("Documentation generation complete!")
    print(f"Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print()
    print("📁 Generated files:")
    print("  icds/generated/          - Interface Control Documents")  
    print("  docs/system_architecture/ - System diagrams and architecture")
    print("  verification/            - Design verification matrices")
    print("  docs/                    - Integration guides and summaries")
    print()
    
    return True

def generate_system_diagrams():
    """Generate system architecture diagrams"""
    
    # Create N2 chart
    n2_chart = """# N2 Interface Chart

This diagram shows the interface relationships between major subsystems.

```mermaid
graph TD
    subgraph "Frame Subsystem"
        F1[Frame Assembly]
        F2[Baseplate]
        F3[Build Volume]
    end
    
    subgraph "Acoustic Cylinder Subsystem"
        A1[40kHz Transducers]
        A2[Transducer Array Layer]
        A3[Acoustic Cylinder]
    end
    
    subgraph "Heated Bed Subsystem"
        H1[Heated Bed Assembly]
        H2[Chamber Assembly]
        H3[Thermal Isolation Tube]
    end
    
    subgraph "Crucible Subsystem"
        C1[Crucible Assembly]
        C2[Induction Heater]
        C3[Material Feed System]
        C4[Optris PI 1M Thermal Camera]
    end
    
    subgraph "Power/Control Subsystem"
        P1[10kW PSU]
        P2[Cyclone IV FPGA Board]
        P3[STM32 Dev Board]
        P4[Industrial PC]
        P5[6-Channel Amp Modules]
    end
    
    A3 ---|ICD-001<br/>Acoustic-Thermal| H2
    P2 ---|ICD-002<br/>Control-Power| P1
    C4 ---|ICD-003<br/>Sensor-Control| P4
    C2 ---|ICD-004<br/>Induction-Crucible| C1
    P5 ---|ICD-005<br/>Amplifier-Transducer| A1
    
    style A3 fill:#e1f5fe
    style H2 fill:#fff3e0
    style C2 fill:#fce4ec
    style P1 fill:#f3e5f5
    style C4 fill:#e8f5e8
```

## Interface Legend

- **ICD-001**: Acoustic-Thermal Interface (HIGH criticality)
- **ICD-002**: Control-Power Interface (HIGH criticality)  
- **ICD-003**: Sensor-Control Interface (MEDIUM criticality)
- **ICD-004**: Induction-Crucible Interface (HIGH criticality)
- **ICD-005**: Amplifier-Transducer Interface (HIGH criticality)
"""
    
    # Create system block diagram
    block_diagram = """# System Block Diagram

```mermaid
flowchart TB
    subgraph "Input Power"
        AC[220V AC Mains]
    end
    
    subgraph "Power Distribution"
        PSU[10kW Power Supply<br/>48V DC Output]
        PSU48[48V DC Supply]
        PSU24[24V DC Supply] 
        PSU12[12V DC Supply]
        PSU5[5V DC Supply]
    end
    
    subgraph "Control System"
        PC[Industrial PC<br/>System Controller]
        FPGA[Cyclone IV FPGA<br/>Real-time Control]
        STM32[STM32 MCU<br/>Device Interface]
    end
    
    subgraph "Acoustic System"
        AMP[6-Channel Amplifiers<br/>4x modules]
        TRANS[40kHz Transducers<br/>18x units]
        CYL[Acoustic Cylinder<br/>Process Chamber]
    end
    
    subgraph "Thermal System"
        BED[Heated Bed<br/>8kW heating]
        CHAMBER[Chamber Assembly<br/>Thermal control]
        COOL[Cooling Layer<br/>Heat management]
    end
    
    subgraph "Material System"
        CRUCIBLE[Crucible Assembly<br/>Material processing]
        INDUCTION[Induction Heater<br/>3kW heating]
        FEED[Material Feed<br/>Automated delivery]
    end
    
    subgraph "Sensing System"
        THERMAL_CAM[Optris PI 1M<br/>Thermal imaging]
        TEMP_SENS[Temperature Sensors<br/>Monitoring points]
    end
    
    AC --> PSU
    PSU --> PSU48
    PSU --> PSU24
    PSU --> PSU12
    PSU --> PSU5
    
    PSU48 --> PC
    PSU24 --> FPGA
    PSU12 --> STM32
    PSU5 --> AMP
    
    PC --> FPGA
    FPGA --> STM32
    PC --> THERMAL_CAM
    
    FPGA --> AMP
    AMP --> TRANS
    TRANS --> CYL
    
    STM32 --> BED
    BED --> CHAMBER
    CHAMBER --> COOL
    
    STM32 --> INDUCTION
    INDUCTION --> CRUCIBLE
    CRUCIBLE --> FEED
    
    THERMAL_CAM --> PC
    TEMP_SENS --> STM32
    
    style PSU fill:#ffeb3b
    style PC fill:#2196f3
    style FPGA fill:#4caf50
    style TRANS fill:#00bcd4
    style BED fill:#ff9800
    style CRUCIBLE fill:#e91e63
```
"""
    
    os.makedirs("docs/system_architecture/block_diagrams", exist_ok=True)
    os.makedirs("docs/system_architecture/n2_charts", exist_ok=True)
    
    with open("docs/system_architecture/n2_charts/n2_chart.md", "w") as f:
        f.write(n2_chart)
    
    with open("docs/system_architecture/block_diagrams/system_block_diagram.md", "w") as f:
        f.write(block_diagram)
    
    # Create interface matrix
    interface_matrix = """# Interface Matrix

## Component-to-Component Interface Mapping

| Side A Component | Side B Component | Interface Type | ICD Reference | Criticality |
|------------------|------------------|----------------|---------------|-------------|
| Acoustic Cylinder | Chamber Assembly | Thermal/Acoustic | ICD-001 | HIGH |
| Cyclone IV FPGA | 10kW PSU | Electrical/Data | ICD-002 | HIGH |
| Optris PI 1M | Industrial PC | Data | ICD-003 | MEDIUM |
| Induction Heater | Crucible Assembly | Thermal/Electrical | ICD-004 | HIGH |
| 6-Channel Amp | 40kHz Transducers | Electrical/Acoustic | ICD-005 | HIGH |

## Interface Type Summary

- **Thermal Interfaces**: 2
- **Electrical Interfaces**: 3  
- **Data Interfaces**: 2
- **Acoustic Interfaces**: 2
- **Mechanical Interfaces**: 2

## Criticality Distribution

- **HIGH**: 4 interfaces (80%)
- **MEDIUM**: 1 interface (20%)
- **LOW**: 0 interfaces (0%)
"""
    
    with open("docs/system_architecture/interface_matrix.md", "w") as f:
        f.write(interface_matrix)

def generate_component_summary():
    """Generate component summary documentation"""
    
    from models.component_registry import ComponentRegistry, ComponentCategory
    
    registry = ComponentRegistry()
    
    summary = ["# Component Summary\n"]
    summary.append(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    summary.append(f"**Total Components**: {len(registry.components)}")
    
    # Power budget summary
    power_budget = registry.calculate_power_budget()
    total_consumption = power_budget['TOTAL']['active_power']
    total_supply = power_budget['TOTAL']['power_supply']
    net_power = power_budget['TOTAL']['net_power']
    
    summary.append(f"**Total Power Consumption**: {total_consumption:,.0f}W")
    summary.append(f"**Total Power Supply**: {total_supply:,.0f}W")
    summary.append(f"**Net Power Requirement**: {net_power:,.0f}W")
    summary.append("")
    
    # Component breakdown by category
    summary.append("## Components by Subsystem\n")
    
    for category in ComponentCategory:
        components = [c for c in registry.components if c.category == category]
        if components:
            summary.append(f"### {category.value}\n")
            summary.append(f"**Count**: {len(components)} components\n")
            
            # Power summary for this category
            cat_power = power_budget[category.value]
            if cat_power['active_power'] > 0:
                summary.append(f"**Power Consumption**: {cat_power['active_power']:.0f}W")
            if cat_power['power_supply'] > 0:
                summary.append(f"**Power Supply**: {cat_power['power_supply']:.0f}W")
            summary.append("")
            
            # Component list
            summary.append("| Component | Qty | Power (W) | Cost ($) | Supplier |")
            summary.append("|-----------|-----|-----------|----------|----------|")
            
            for comp in components:
                power = comp.tech_specs.power_consumption if comp.tech_specs and comp.tech_specs.power_consumption else 0
                summary.append(
                    f"| {comp.name} | {comp.quantity} | {power} | "
                    f"{comp.total_cost} | {comp.supplier} |"
                )
            
            summary.append("")
    
    # Cost summary
    total_cost = sum(c.total_cost for c in registry.components)
    summary.append(f"## Cost Summary\n")
    summary.append(f"**Total System Cost**: ${total_cost:,.2f}\n")
    
    # Weight summary
    total_weight = sum(
        (c.tech_specs.weight or 0) * c.quantity 
        for c in registry.components 
        if c.tech_specs and c.tech_specs.weight
    )
    summary.append(f"**Total System Weight**: {total_weight:.1f}kg\n")
    
    # Top 10 most expensive components
    expensive_components = sorted(registry.components, key=lambda x: x.total_cost, reverse=True)[:10]
    summary.append("## Top 10 Most Expensive Components\n")
    summary.append("| Rank | Component | Cost ($) | Category |")
    summary.append("|------|-----------|----------|----------|")
    
    for i, comp in enumerate(expensive_components, 1):
        summary.append(f"| {i} | {comp.name} | {comp.total_cost} | {comp.category.value} |")
    
    summary.append("")
    
    # Save summary
    os.makedirs("docs", exist_ok=True)
    with open("docs/component_summary.md", "w") as f:
        f.write("\n".join(summary))

def generate_integration_guide():
    """Generate integration and assembly guide"""
    
    integration_guide = """# System Integration Guide

## Prerequisites

### Required Tools
- Multimeter and electrical test equipment
- Thermal imaging camera
- Hydrophone for acoustic testing  
- Precision torque wrenches
- Alignment fixtures
- Safety equipment (PPE)

### Required Skills
- Electrical systems integration
- Thermal systems assembly
- Precision mechanical assembly
- System commissioning experience

## Integration Sequence

### Phase 1: Frame and Mechanical Assembly
1. **Assemble Frame Structure**
   - Install baseplate and verify level
   - Mount frame components per mechanical drawings
   - Verify all alignments within tolerance

2. **Install Build Volume**
   - Position and secure build chamber
   - Verify clearances and access ports
   - Install support structures

### Phase 2: Power System Installation  
1. **Install Power Supply Units**
   - Mount 10kW PSU in ventilated area
   - Install secondary power supplies (48V, 24V, 12V, 5V)
   - Verify electrical connections per ICD-002

2. **Power Distribution**
   - Install power distribution panels
   - Run power cables to all subsystems
   - Install circuit protection

### Phase 3: Control System Integration
1. **Install Control Hardware**
   - Mount Industrial PC in control enclosure
   - Install FPGA board and STM32 controller
   - Verify data connections per ICD-003

2. **Control Software**
   - Load system control software
   - Configure interface parameters
   - Test control loops

### Phase 4: Acoustic System Assembly
1. **Install Transducer Array**
   - Mount 40kHz transducers per pattern
   - Install acoustic cylinder assembly
   - Verify acoustic coupling per ICD-001

2. **Amplifier Installation**
   - Install 6-channel amplifier modules
   - Connect amplifier-transducer interfaces per ICD-005
   - Test acoustic output

### Phase 5: Thermal System Integration
1. **Heated Bed Installation** 
   - Install heated bed assembly
   - Connect thermal control systems
   - Install thermal isolation per ICD-001

2. **Cooling System**
   - Install cooling layer and circulation
   - Connect thermal management systems
   - Verify thermal performance

### Phase 6: Material System Assembly
1. **Crucible Installation**
   - Install crucible assembly
   - Connect induction heating per ICD-004
   - Install material feed system

2. **Process Monitoring**
   - Install Optris thermal camera
   - Configure thermal monitoring
   - Calibrate sensing systems

## Integration Testing

### Level 1: Component Testing
- Verify each component meets individual specifications
- Test power-on sequences
- Validate communication interfaces

### Level 2: Subsystem Testing  
- Test subsystem functionality
- Verify interface compatibility per ICDs
- Validate performance requirements

### Level 3: System Integration Testing
- Full system power-up sequence
- End-to-end functionality testing
- Performance validation
- Safety system verification

### Level 4: Acceptance Testing
- 72-hour continuous operation test
- Process quality validation
- Documentation verification
- Final acceptance criteria

## Safety Requirements

### Electrical Safety
- All systems must meet IEC 61010-1 standards
- Ground fault protection required
- Emergency stop systems installed
- Electrical isolation verified

### Thermal Safety  
- Overheat protection on all thermal systems
- Emergency cooling procedures
- Personnel protection barriers
- Thermal monitoring systems

### Mechanical Safety
- All moving parts guarded
- Pressure vessel certifications
- Lifting and handling procedures
- Emergency shutdown procedures

## Commissioning Checklist

### Power Systems
- [ ] All power supplies tested and verified
- [ ] Circuit protection functional
- [ ] Power quality within specifications
- [ ] Emergency shutdown tested

### Control Systems
- [ ] All control interfaces functional
- [ ] Software loaded and configured
- [ ] Communication links verified
- [ ] Control loops tuned

### Acoustic Systems
- [ ] Transducer array aligned and tested
- [ ] Acoustic coupling verified
- [ ] Field uniformity mapped
- [ ] Frequency response validated

### Thermal Systems
- [ ] Heating elements tested
- [ ] Temperature control verified
- [ ] Cooling systems operational
- [ ] Thermal barriers effective

### Material Systems
- [ ] Material feed operational
- [ ] Crucible heating verified
- [ ] Process monitoring calibrated
- [ ] Material handling tested

## Documentation Requirements

### As-Built Documentation
- Updated component specifications
- Interface verification records
- Calibration certificates
- Test reports

### Operating Procedures
- Startup and shutdown procedures
- Normal operating procedures
- Emergency procedures
- Maintenance procedures

### Training Requirements
- Operator training completed
- Maintenance training completed
- Safety training verified
- Documentation training completed
"""
    
    os.makedirs("docs", exist_ok=True)
    with open("docs/integration_guide.md", "w") as f:
        f.write(integration_guide)
    
    # Create safety documentation
    safety_doc = """# Safety Requirements and Procedures

## Electrical Safety

### High Voltage Systems (220V AC)
- Main power input rated at 63A
- Ground fault circuit interrupter (GFCI) required
- Electrical isolation barriers mandatory
- Arc flash protection required for maintenance

### Low Voltage DC Systems
- 48V DC main distribution (up to 200A)
- Touch-safe connectors required
- Overcurrent protection on all branches
- Emergency shutdown capability

## Thermal Safety

### High Temperature Zones
- Crucible system: up to 1500°C operational
- Heated bed: up to 850°C operational
- Induction heater: 3kW power, surface temps >200°C

### Safety Measures
- Thermal barriers and insulation
- Emergency cooling procedures
- Personnel protection equipment
- Temperature monitoring and alarms

## Acoustic Safety

### Ultrasonic Exposure
- 40kHz transducers at high power levels
- Potential for heating effects in tissues
- Hearing protection in operational areas
- Exposure time limits for personnel

## Material Safety

### Chemical Hazards
- Material feed systems may contain hazardous substances
- Proper ventilation required
- Material safety data sheets (MSDS) available
- Spill containment procedures

### Mechanical Hazards
- Moving parts in feed systems
- High pressure systems
- Pinch points and crush hazards
- Lockout/tagout procedures required

## Emergency Procedures

### Power Emergency
1. Activate emergency stop
2. Disconnect main power
3. Verify all systems safe
4. Document incident

### Thermal Emergency
1. Activate emergency cooling
2. Shut down heating systems
3. Evacuate area if necessary
4. Contact emergency services

### Personnel Safety
1. Ensure area is safe
2. Provide first aid if needed
3. Contact medical services
4. Document incident

## Personal Protective Equipment (PPE)

### Minimum Requirements
- Safety glasses with side shields
- Heat-resistant gloves for thermal work
- Hearing protection in acoustic areas
- Steel-toed safety boots
- Lab coats or protective clothing

### Special Operations
- Full face shield for high temperature work
- Insulated gloves for electrical work
- Respiratory protection for material handling
- Arc flash suits for electrical maintenance
"""
    
    os.makedirs("docs/safety", exist_ok=True)
    with open("docs/safety/safety_requirements.md", "w") as f:
        f.write(safety_doc)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)