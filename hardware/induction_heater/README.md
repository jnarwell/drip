# DRIP Induction Heater Subsystem

## Overview

This directory contains the complete implementation for the 3kW induction heating system used in the DRIP acoustic steering manufacturing system. The design uses a hybrid approach: commercial OEM power module + custom safety integration.

**⚠️ SAFETY CRITICAL SYSTEM - 3kW @ 240V AC**

## System Specifications

### Power Module
- **Model**: HCGF HCX-3000W-50K (or equivalent)
- **Power**: 3000W continuous, 3500W peak
- **Frequency**: 30-80kHz auto-tracking
- **Input**: 220V single-phase
- **Cooling**: Water-cooled (2 L/min minimum)
- **Cost**: $420 (via Alibaba)

### Integration Features
- Hardware safety interlocks (E-stop, door, flow, temperature)
- STM32 digital control interface
- Real-time power monitoring
- PID temperature control
- Closed-loop water cooling
- EMI filtering
- GFCI protection

### Performance
- **Materials**: Aluminum (700°C), Steel (1580°C)
- **Efficiency**: >85%
- **Melt Time**: <5 minutes for 100g aluminum
- **Temperature Control**: ±10°C with PID
- **Safety Response**: <10ms E-stop

## Directory Structure

```
induction_heater/
├── README.md                  # This file
├── bom/
│   └── induction_heater_bom.py    # Bill of materials ($963 total)
├── code/
│   ├── induction_control.c        # STM32 safety-critical control
│   └── induction_heater.h         # Header file
├── docs/
│   ├── coil_design.md            # Work coil winding instructions
│   ├── cooling_system.py         # Cooling calculations & design
│   └── troubleshooting.md        # Diagnostic procedures
├── safety/
│   ├── commissioning_procedures.md   # Step-by-step testing
│   └── emergency_procedures.md       # Emergency response
└── pcb/
    └── interface/               # KiCad files (future)
```

## Quick Start Guide

### 1. Procurement
```bash
# Generate shopping list
python3 bom/induction_heater_bom.py

# Key suppliers:
# - OEM Module: Alibaba (search "HCGF 3000W induction")
# - Contactor: Grainger #3210847
# - EMI Filter: Mouser #448-FN2090-16-06
# - Enclosure: DigiKey #377-1894-ND
```

### 2. Safety Requirements
- 240V 30A circuit with GFCI breaker
- Licensed electrician for mains connection
- Emergency stop within 1m reach
- Face shield and heat gloves
- Class D fire extinguisher

### 3. Assembly Overview
1. Mount module in ventilated enclosure
2. Install cooling system and leak test
3. Wind work coil per specifications
4. Wire safety interlocks in series
5. Connect STM32 control interface
6. Commission per test procedures

### 4. Software Setup
```c
// In your main STM32 project:
#include "induction_heater.h"

// Initialize in main()
induction_heater_init();

// In 100Hz timer interrupt
induction_heater_update();

// To set power
set_heater_power(50.0);  // 50% = 1500W
```

## Critical Safety Information

### Electrical Hazards
- **240V can kill** - Always lock out power
- Never bypass safety interlocks  
- Use insulated tools
- Verify ground <0.1Ω

### Thermal Hazards
- Crucible reaches **1580°C**
- Always wear face shield
- Keep clear of coil during operation
- Cool 30 minutes before service

### Magnetic Field Hazards
- Pacemaker exclusion zone: **1 meter**
- Remove metal jewelry
- Secure loose metal objects
- Do not place tools near coil

### Water + Electricity
- Check for leaks before **every** startup
- Never run without cooling flow
- Mount electronics above water level
- Use GFCI protection

## Integration with DRIP System

### Power Architecture
- Induction heater connects directly to 240V mains
- Controlled via SSR from main control
- Bypasses main PSU (AC load)
- Shares E-stop circuit with system

### Control Interface
```
STM32 → Optocoupler → OEM Module Enable
STM32 ← UART ← Power Meter
STM32 ← ADC ← Temperature Sensors  
STM32 ← GPIO ← Flow Sensor
STM32 → PWM → Power Control (0-100%)
```

### Thermal Camera Integration
The Optris Xi 400 thermal cameras monitor crucible temperature for closed-loop control. Mount camera with clear view of crucible interior.

## Operating Parameters

| Material | Temp (°C) | Power (%) | Ramp Rate | Frequency |
|----------|-----------|-----------|-----------|-----------|
| Aluminum | 700 | 60 | 50°C/min | ~45kHz |
| Steel | 1580 | 95 | 30°C/min | ~55kHz |
| Standby | 400 | 20 | - | Variable |

## Maintenance Schedule

- **Daily**: Check flow & temperature
- **Weekly**: Inspect for arcing, clean coil
- **Monthly**: Test all safety interlocks
- **Quarterly**: Replace coolant, deep clean
- **Annually**: Professional inspection

## Troubleshooting Quick Reference

| Problem | Likely Cause | First Check |
|---------|--------------|-------------|
| No power | E-stop/interlock | Safety chain continuity |
| Low power | Poor coupling | Coil-crucible gap |
| Overheating | Low flow | Pump & radiator |
| EMI/noise | Bad ground | Ground resistance |
| Won't melt | Frequency off | Coil inductance |

## Cost Summary

- OEM Power Module: $420
- Safety Integration: $543  
- **Total System**: $963

Compared to $1200 pure COTS solution, this saves $237 while providing better integration.

## Support Resources

### Documentation
- [OEM Module Manual](docs/module_manual.pdf) - Request from supplier
- [Safety Standards](safety/standards.md) - IEC 61010-1 compliance
- [Training Videos](https://youtube.com/playlist?...) - Coming soon

### Community
- DRIP Discord: #induction-heater channel
- Issues: GitHub issues for bugs/questions
- Wiki: Additional tips and modifications

## Version History

- v1.0 (2024-01): Initial implementation
- v1.1 (2024-02): Added PID temperature control
- v1.2 (2024-03): Enhanced safety interlocks

---

**Remember**: This is a SAFETY CRITICAL system. When in doubt, shut it down and ask for help. Your safety is worth more than any deadline or part.