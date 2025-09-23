# N2 Interface Chart

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
