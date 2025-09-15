# Power Budget Analysis (Parametric)

*Generated from component specifications*

## ⚠️ CRITICAL ERRORS
- **INSUFFICIENT POWER: System requires 4595.5W more than available supply capacity**

## ⚠️ Warnings
- PSU OVERLOAD: 10kW PSU rated for 10kW but system requires 14595.5W

## System Power Summary
| Metric | Value |
|--------|-------|
| Total Supply Capacity | 10000.0W |
| Total Consumption | 14595.5W |
| Conversion Losses | 2967.0W |
| **Net Power Required** | **4595.5W** |
| **Power Margin** | **-4595.5W** |

## Power Sources
| Component | Quantity | Unit Power | Total Output | Efficiency | Losses |
|-----------|----------|------------|--------------|------------|--------|
| 10kW PSU | 1 | 10000.0W | 10000.0W | 91.0% | 900.0W |

## Major Power Consumers (>100W)
| Component | Subsystem | Quantity | Unit Power | Total |
|-----------|-----------|----------|------------|-------|
| Heating Rods | Heated Bed Subsystem | 4 | 1000.0W | 4000.0W |
| Heated Bed Assembly | Heated Bed Subsystem | 1 | 4000.0W | 4000.0W |
| Induction Heater | Crucible Subsystem | 1 | 3000.0W | 3000.0W |
| Micro Heaters | Crucible Subsystem | 25 | 40.0W | 1000.0W |
| Material Delivery System | Crucible Subsystem | 1 | 1000.0W | 1000.0W |
| 10kW PSU | Power/Control Subsystem | 1 | 900.0W | 900.0W |
| 6-Channel Amp Modules | Power/Control Subsystem | 4 | 100.0W | 400.0W |
| 40kHz Transducers | Acoustic Cylinder Subsystem | 18 | 10.0W | 180.0W |

## Subsystem Power Distribution
| Subsystem | Consumption | Supply | Net | Status |
|-----------|-------------|--------|-----|--------|
| Frame Subsystem | 0.0W | 0.0W | 0.0W | ✅ |
| Heated Bed Subsystem | 24000.0W | 0.0W | 24000.0W | ⚠️ Deficit |
| Acoustic Cylinder Subsystem | 555.0W | 0.0W | 555.0W | ⚠️ Deficit |
| Crucible Subsystem | 15204.0W | 0.0W | 15204.0W | ⚠️ Deficit |
| Power/Control Subsystem | 4027.5W | 30000.0W | 36994.5W | ⚠️ Deficit |