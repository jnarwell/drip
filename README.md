# Acoustic Manufacturing System - SysML v2 Model

## Overview

This repository contains the complete Bill of Materials (BOM) and component registry for an acoustic steering-based manufacturing system. The system uses ultrasonic transducers to create acoustic fields that steer falling molten metal droplets for precise deposition control.

## Project Structure

```
acoustic-sysml-v2/
├── models/              # SysML models and component registry
│   ├── component_registry.py    # Main component database
│   ├── requirements.sysml       # System requirements
│   └── acoustic_system.sysml    # System architecture
├── notebooks/           # Jupyter notebooks for analysis
│   └── bom_analysis.ipynb      # Interactive BOM analysis
├── reports/             # Generated reports and exports
├── tests/              # Validation and verification
├── tools/              # Utility scripts
└── docs/               # Documentation
```

## Key Features

- **Complete Level 1 BOM**: ~$14,000 system with 60+ components
- **Expansion Path**: Detailed upgrade paths from L1 to L4 ($14k → $117k)
- **Component Registry**: Python-based tracking with expansion markers
- **Cost Analysis**: COTS vs Custom breakdown, subsystem analysis
- **SysML v2 Models**: Requirements and system architecture

## System Subsystems

1. **Frame Subsystem**: Structural support and chamber
2. **Heated Bed Subsystem**: Temperature-controlled build platform
3. **Acoustic Cylinder Subsystem**: 40kHz ultrasonic transducer arrays
4. **Crucible Subsystem**: Material melting and delivery (25 outlets)
5. **Power/Control Subsystem**: FPGA-based control with 1.5kW PSU (RSP-1500-48)

## Quick Start

### View BOM Analysis
```bash
# Launch Jupyter notebook
jupyter lab notebooks/bom_analysis.ipynb
```

### Generate Reports
```bash
python reports/generate_bom_report.py
```

### Component Registry Usage
```python
from models.component_registry import ComponentRegistry

registry = ComponentRegistry()
registry.print_summary()
```

## Expansion Levels

- **Level 1**: Basic aluminum/polymer capability ($13,988)
- **Level 2**: Steel capability, larger volume ($25,748)
- **Level 3**: Dual-material, thermal cameras ($48,889)
- **Level 4**: Production system, 400mm platform ($116,935)

## Technologies

- **Control**: FPGA (Cyclone IV) + STM32F4
- **Acoustics**: 18-72 transducers @ 40kHz
- **Materials**: Aluminum, steel, polymers
- **Temperature**: Up to 1580°C (Level 2+)
- **Build Volume**: 125cm³ → 8,000cm³

## Requirements

- Python 3.8+
- Jupyter Lab (for notebooks)
- Java 21 (for SysML kernel)

## Installation

1. Clone the repository
2. Install Python dependencies:
   ```bash
   pip install pandas matplotlib numpy openpyxl
   ```
3. Launch Jupyter:
   ```bash
   ./launch_jupyter.sh
   ```

## License

This project is for educational and research purposes.

## Contact

For questions about the acoustic manufacturing system design, please open an issue.