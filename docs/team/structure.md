# Team Structure & Roles

This page provides detailed information about each team role in the DRIP project. For an interactive version with fillable contact fields, visit the **[Interactive Team Structure Page](../team-page/index.html)**.

## Mechanical/Systems Lead

### Primary Responsibilities
- System architecture and integration planning
- Mechanical design and CAD modeling (SolidWorks/Fusion 360)
- Assembly planning and fixture design
- Test campaign management and coordination
- Tolerance analysis and stack-ups
- Interface control documentation (ICDs)

### Subsystems Owned
- **Frame Subsystem**: 11 components (9 custom designed)
- **Chamber Assembly**: Pressure vessel design for 300°C operation
- **System Integration**: Coordination of all subsystem interfaces
- **Test Management System**: 100 test procedures defined

### Key Deliverables
- Complete frame structural FEA and optimization
- Chamber pressure vessel design (atmospheric pressure, 300°C)
- Detailed assembly procedures and work instructions
- Test fixtures for all subsystems
- Integration documentation and 10 ICDs
- System verification reports

### Stanford Resources Available
- Product Realization Lab (PRL) - CNC, waterjet, 3D printing
- Mechanical Testing Lab - Instron, vibration testing
- XCT Lab - X-ray computed tomography for internal inspection
- SNSF - Surface analysis and metrology

### Required Skills
- Strong CAD skills (SolidWorks preferred)
- FEA experience (ANSYS or similar)
- Understanding of GD&T and tolerance analysis
- Project management capabilities
- Technical documentation experience

---

## Thermal/Materials Engineer

### Primary Responsibilities
- Thermal system design and modeling
- Material processing parameter optimization
- Crucible and melting system design
- Heat transfer and cooling system analysis
- Material compatibility assessment
- Phase change and solidification calculations

### Subsystems Owned
- **Heated Bed Subsystem**: 6 components (4 custom)
- **Crucible Subsystem**: 25 components (14 custom)
- **Thermal Isolation Systems**: Ceramic barriers and insulation
- **Material Feed Mechanisms**: Powder/wire delivery
- **Induction Heating System**: 3kW coil design

### Key Deliverables
- Complete thermal FEA models (COMSOL/ANSYS)
- Crucible design for 700-1580°C operation
- Induction heating coil optimization
- Cooling system sizing (15kW capacity)
- Material compatibility matrix
- Thermal test procedures and validation

### Stanford Resources Available
- Geballe Laboratory - High-temperature testing to 1600°C
- GLAM - Advanced materials analysis
- MSE Thermal Lab - DSC, TGA, thermal conductivity
- Soft Materials Facility - Rheology and phase analysis
- High-temperature furnaces and pyrometry

### Required Skills
- Thermal modeling (COMSOL/ANSYS Fluent)
- High-temperature materials knowledge
- Induction heating principles
- Heat transfer and fluid dynamics
- Materials science background

---

## Power/Electronics Engineer

### Primary Responsibilities
- Power distribution architecture design (3kW dual PSU system)
- Electrical safety system implementation
- PCB design and layout (4 custom boards required)
- EMI/EMC compliance planning and testing
- Heater control circuit design
- Emergency stop system implementation

### Subsystems Owned
- **Power Distribution**: 48V primary, 24V/12V/5V secondary rails
- **Safety Interlock Systems**: E-stop and fault detection
- **Control Electronics Boards**: STM32, FPGA interface boards
- **Thermal Control Circuits**: PID controllers for heaters
- **Wiring Harness Design**: High-current distribution

### Key Deliverables
- Complete electrical schematics (Altium/KiCAD)
- PCB layouts: Control, Acoustic, Thermal, Interface boards
- Wiring harness documentation and assembly
- Emergency stop system with <100ms response
- EMC pre-compliance testing results
- Electrical safety test procedures

### Stanford Resources Available
- EE Shop - PCB fabrication and assembly
- RF/EMC Test Facility - Pre-compliance testing
- Power Electronics Lab - High-power testing
- Allen Building - Oscilloscopes, power analyzers
- Component inventory and SMT assembly

### Required Skills
- PCB design (Altium Designer preferred)
- Power electronics (SMPS, motor drives)
- Microcontroller programming (STM32)
- EMI/EMC knowledge
- Electrical safety standards (IEC 61010)

---

## Acoustics/Control Engineer

### Primary Responsibilities
- Acoustic field modeling and optimization
- Control algorithm development
- FPGA programming (Cyclone IV)
- Real-time software architecture
- Thermal camera integration (FLIR A35, 60Hz)
- Multi-droplet coordination algorithms

### Subsystems Owned
- **Acoustic Cylinder Subsystem**: 9 components (7 custom)
- **Control System Architecture**: PC-STM32-FPGA hierarchy
- **Software/Firmware Stack**: Real-time control implementation
- **Sensor Integration**: Thermal cameras, position feedback
- **Transducer Arrays**: 18-72 units at 40kHz

### Key Deliverables
- Acoustic field models (COMSOL Acoustics)
- FPGA control algorithms (<3ms control loop)
- STM32 firmware for device coordination
- Python/C++ PC control software with GUI
- Droplet tracking system with 60Hz update rate
- Real-time steering algorithms for multi-droplet control

### Stanford Resources Available
- Stanford Acoustics Lab - Anechoic chamber, hydrophones
- SAIL - GPU clusters for ML/simulation
- Ultrasound Research Lab - Transducer characterization
- High-speed cameras - Photron systems
- EE368 Lab - Computer vision resources

### Required Skills
- Acoustic modeling (COMSOL preferred)
- FPGA development (Verilog/VHDL)
- Embedded C/C++ programming
- Real-time systems experience
- Computer vision basics
- Control theory knowledge

---

## Computer Science/Mathematics Engineer

### Primary Responsibilities
- ALL code development and maintenance
- COMSOL/MATLAB simulation scripts
- Computer vision and tracking algorithms
- GUI development (PyQt/Tkinter)
- Data analysis pipelines (Pandas)
- Mathematical models and optimization
- Test automation and CI/CD

### Subsystems Owned
- **All Software Repositories**: Complete code ownership
- **Simulation Frameworks**: COMSOL/MATLAB integration
- **Data Processing Pipelines**: Test data analysis
- **Control Software Interfaces**: PC/FPGA communication
- **Documentation Generation**: Automated docs systems
- **Testing Frameworks**: Unit/integration test suites

### Key Deliverables
- Control software (Python/C++)
- FPGA interface libraries
- Real-time tracking system (60Hz)
- Physics simulation models
- Data analysis notebooks
- Automated test suites
- Technical documentation generation

### Stanford Resources Available
- SAIL - GPU clusters for ML/simulations
- Sherlock HPC cluster
- GitHub Enterprise
- MATLAB/COMSOL licenses
- CS department computing resources
- Software development tools

### Required Skills
- Python/C++ proficiency
- Numerical methods and optimization
- Computer vision (OpenCV)
- Scientific computing (NumPy, SciPy)
- Version control (Git)
- Technical documentation

---

## Cross-Functional Responsibilities

All team members share responsibility for:

1. **Safety Compliance**: Following all lab safety protocols
2. **Documentation**: Maintaining clear technical documentation
3. **Integration**: Coordinating interfaces with other subsystems
4. **Testing**: Supporting system-level testing campaigns
5. **Communication**: Regular updates and team coordination

## Onboarding Process

New team members should:

1. Complete required safety training
2. Review system architecture documentation
3. Meet with subsystem leads
4. Access shared resources and repositories
5. Attend weekly team meetings

## Contact Information

For current team member contact information and to join the team, visit the **[Interactive Team Structure Page](../team-page/index.html)**.

Project questions: Contact the project lead through the team page.