#!/usr/bin/env python3
"""
Generate wiring diagram for induction heater system
Creates both ASCII art and connection list
"""

def generate_power_wiring_diagram():
    """Main power wiring schematic"""
    
    diagram = """
INDUCTION HEATER POWER WIRING DIAGRAM
=====================================

240V MAINS INPUT                           CONTROL POWER (48V DC from PSU)
    L1 ───┬─[30A]─┬─[EMI]─┬─────────┬─────────→ [OEM MODULE L1]
          │       │       │         │
    L2 ───┼─[30A]─┼─[EMI]─┼─────────┼─────────→ [OEM MODULE L2]
          │       │       │         │
    GND ──┴───────┴─[EMI]─┴─────────┴─────────→ [OEM MODULE GND]
                          │
                    [CONTACTOR K1]
                          │
                    ┌─────┴─────┐
                    │   COIL    │
                    │   230V    │
                    └─────┬─────┘
                          │
    ┌──────[E-STOP]───────┴───────[DOOR]────────[STM32 RELAY]────┐
    │                                                              │
    N ─────────────────────────────────────────────────────────────┘

Legend:
[30A] = 30A Circuit Breaker (2-pole)
[EMI] = Schaffner FN2090-16-06 Filter  
[E-STOP] = NC Emergency Stop Button
[DOOR] = NC Door Interlock Switch
[STM32 RELAY] = Control Enable Output

Wire Specifications:
- Mains: 10 AWG THHN (L1, L2, GND)
- Control: 14 AWG THHN
- Ground: 10 AWG Green
"""
    return diagram

def generate_control_wiring_diagram():
    """Control system interconnections"""
    
    diagram = """
CONTROL SYSTEM WIRING
=====================

STM32 CONTROL BOARD                    INDUCTION MODULE
┌─────────────────┐                    ┌──────────────┐
│                 │                    │              │
│ PA0 (Enable) ───┼──[OPTO]──[5V/24V]─┼─→ Enable IN  │
│                 │                    │              │
│ PA1 (PWM) ──────┼──[OPTO]──[RC]─────┼─→ Power Ctrl │
│                 │                    │              │
│ PA2 (Flow) ←────┼────────────────────┼── Flow Pulse │
│                 │                    │              │
│ PA3 (ADC1) ←────┼──[THERMO K]───────┼── Coil Temp  │
│                 │                    │              │
│ PA4 (E-Stop) ←──┼────────────────────┼── E-Stop NC  │
│                 │                    │              │
│ PA5 (ADC2) ←────┼──[THERMO K]───────┼── Water Temp │
│                 │                    │              │
│ PA6 (Door) ←────┼────────────────────┼── Door NC    │
│                 │                    │              │
│ UART2 RX ←──────┼────────────────────┼── Power Meter│
│                 │                    │              │
│ GND ────────────┼────────────────────┼── GND        │
└─────────────────┘                    └──────────────┘

[OPTO] = PC817 Optocoupler
[RC] = 1kΩ/0.1μF filter
[THERMO K] = Type K Thermocouple Amplifier

Signal Specifications:
- Digital: 3.3V/5V logic levels
- PWM: 1kHz, 0-100% duty
- Flow: 5V pulses, 4.5/L
- Temp: 0-3.3V = 0-100°C
"""
    return diagram

def generate_cooling_connections():
    """Cooling system plumbing connections"""
    
    diagram = """
COOLING SYSTEM CONNECTIONS
==========================

[RESERVOIR 5L]
      │
      ├──6mm──→ [PUMP Hygger HG-909]
      │              │
      │              ├──6mm──→ [FLOW SENSOR YF-S201]
      │              │                │
      │              │                ├──6mm──→ [WORK COIL IN]
      │              │                │              │
      │              │                │              ├──8 turns──┐
      │              │                │              │           │
      │              │                │              └───────────┘
      │              │                │                    │
      │              │                ├──6mm──→ [MODULE COOLING IN]
      │              │                │              │
      │              │                │         [INTERNAL BLOCK]
      │              │                │              │
      │              │                ├──6mm──← [MODULE COOLING OUT]
      │              │                │
      │              │                ├──6mm──→ [RADIATOR IN]
      │              │                │              │
      │              │                │         [120mm + FAN]
      │              │                │              │
      └──────────6mm─────────────────────────← [RADIATOR OUT]

Materials:
- Tubing: 6mm ID silicone, high-temp
- Fittings: Push-connect 6mm
- Clamps: Worm gear at connections
- Coolant: Distilled water + 10% glycol
"""
    return diagram

def generate_connection_checklist():
    """Printable connection checklist"""
    
    checklist = """
INDUCTION HEATER CONNECTION CHECKLIST
====================================

POWER CONNECTIONS
□ L1 to breaker (10 AWG)
□ L2 to breaker (10 AWG)  
□ Breaker to EMI filter
□ EMI filter to contactor
□ Contactor to module L1/L2
□ Ground to module chassis
□ Ground to enclosure
□ EMI filter ground

CONTROL CONNECTIONS
□ STM32 enable to optocoupler
□ Optocoupler to module enable
□ STM32 PWM to module control
□ Flow sensor to STM32 PA2
□ E-stop NC contacts in series
□ Door NC contacts in series
□ Contactor coil to safety chain

COOLING CONNECTIONS
□ Reservoir to pump inlet
□ Pump outlet to flow sensor
□ Flow sensor to coil inlet
□ Coil outlet to module inlet
□ Module outlet to radiator
□ Radiator to reservoir
□ All clamps tight
□ System filled and bled

SENSOR CONNECTIONS
□ Coil thermocouple to PA3
□ Water thermocouple to PA5
□ Power meter CT around L1
□ Power meter UART to STM32
□ All shields grounded

TEST POINTS
□ 240V at module input
□ 3.3V at STM32 enable out
□ Flow >2 L/min
□ All temps <30°C cold
□ E-stop breaks contactor
□ Door switch breaks contactor

Checked by: _____________ Date: _______
"""
    return checklist

def calculate_wire_sizes():
    """Calculate required wire gauges"""
    
    print("\nWIRE SIZE CALCULATIONS")
    print("=" * 40)
    
    # Main power
    current_3kw = 3000 / 240  # Amps
    print(f"3kW at 240V = {current_3kw:.1f}A")
    print(f"With 125% NEC factor = {current_3kw * 1.25:.1f}A")
    print(f"Required: 10 AWG THHN (30A rated)")
    
    # Control circuits
    print(f"\nControl circuits (<2A):")
    print(f"Required: 18 AWG minimum")
    print(f"Recommended: 16 AWG for durability")
    
    # High frequency
    print(f"\nHigh frequency coil (100A at 50kHz):")
    print(f"Skin depth at 50kHz = 0.3mm")
    print(f"Required: 8 AWG welding cable")
    print(f"Or: Multiple 12 AWG in parallel")

def generate_terminal_assignments():
    """Terminal block layout"""
    
    layout = """
TERMINAL BLOCK ASSIGNMENTS
=========================

TB1 - AC POWER INPUT (35A rated)
1: L1 Input (10 AWG)
2: L2 Input (10 AWG)
3: Ground (10 AWG)
4: L1 to Module (10 AWG)
5: L2 to Module (10 AWG)
6: Chassis Ground (10 AWG)

TB2 - CONTROL SIGNALS (10A rated)
1: +48V from PSU
2: GND
3: E-Stop NC
4: E-Stop NC Return
5: Door NC  
6: Door NC Return
7: Contactor Coil L
8: Contactor Coil N

TB3 - LOW VOLTAGE (5A rated)
1: +5V Logic
2: GND
3: Enable Signal
4: PWM Signal
5: Flow Pulse
6: Thermocouple 1+
7: Thermocouple 1-
8: Thermocouple 2+
9: Thermocouple 2-
10: UART TX
11: UART RX
12: Shield/GND
"""
    return layout

if __name__ == "__main__":
    print("INDUCTION HEATER WIRING DOCUMENTATION")
    print("=" * 50)
    print("\nGenerating documentation...\n")
    
    # Generate all diagrams
    print(generate_power_wiring_diagram())
    print(generate_control_wiring_diagram())
    print(generate_cooling_connections())
    print(generate_terminal_assignments())
    
    # Calculate wire sizes
    calculate_wire_sizes()
    
    # Print checklist
    print(generate_connection_checklist())
    
    print("\n" + "=" * 50)
    print("Print this document and keep with equipment")
    print("Update after any modifications")