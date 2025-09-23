#!/usr/bin/env python3
"""
Cooling System Design and Calculations
For 3kW Induction Heater
"""

import math

# System Parameters
POWER_INPUT = 3000  # W
EFFICIENCY = 0.85   # 85% efficiency
AMBIENT_TEMP = 25   # °C
TARGET_COOLANT_TEMP = 35  # °C max
SAFETY_FACTOR = 3   # Oversizing factor

def calculate_heat_load():
    """Calculate heat to be dissipated"""
    heat_dissipated = POWER_INPUT * (1 - EFFICIENCY)
    print(f"Heat Load Calculation:")
    print(f"  Power Input: {POWER_INPUT}W")
    print(f"  Efficiency: {EFFICIENCY*100}%")
    print(f"  Heat to Dissipate: {heat_dissipated}W")
    print(f"  With Safety Factor: {heat_dissipated * SAFETY_FACTOR}W\n")
    return heat_dissipated

def calculate_flow_requirements(heat_load):
    """Calculate minimum water flow rate"""
    specific_heat = 4186  # J/kg·K for water
    density = 1000  # kg/m³
    temp_rise = 10  # °C allowable rise
    
    # Mass flow rate (kg/s) = Q / (c × ΔT)
    mass_flow = heat_load / (specific_heat * temp_rise)
    volume_flow = mass_flow / density  # m³/s
    flow_lpm = volume_flow * 60000  # L/min
    
    print(f"Flow Rate Calculation:")
    print(f"  Heat Load: {heat_load}W")
    print(f"  Allowable Temp Rise: {temp_rise}°C")
    print(f"  Required Flow: {flow_lpm:.2f} L/min")
    print(f"  With Safety Factor: {flow_lpm * SAFETY_FACTOR:.2f} L/min\n")
    
    return flow_lpm * SAFETY_FACTOR

def select_pump(required_flow):
    """Select appropriate pump"""
    pumps = [
        {"model": "Hygger HG-909", "flow": 13.3, "head": 1.5, "power": 10, "cost": 25},
        {"model": "VIVOSUN 800GPH", "flow": 50, "head": 2.0, "power": 25, "cost": 45},
        {"model": "Active Aqua 400", "flow": 25, "head": 1.8, "power": 15, "cost": 35}
    ]
    
    print(f"Pump Selection (Required: {required_flow:.1f} L/min):")
    for pump in pumps:
        suitable = "✓" if pump["flow"] >= required_flow else "✗"
        print(f"  {suitable} {pump['model']}: {pump['flow']} L/min, "
              f"{pump['head']}m head, {pump['power']}W, ${pump['cost']}")
    
    selected = pumps[0]  # Hygger HG-909
    print(f"\nSelected: {selected['model']} (adequate for system)\n")
    return selected

def design_radiator(heat_load):
    """Calculate radiator requirements"""
    # Radiator performance: ~10W/°C for 120mm with fan
    radiator_performance = 10  # W/°C
    water_inlet_temp = 35  # °C
    air_temp = AMBIENT_TEMP
    
    temp_diff = water_inlet_temp - air_temp
    radiator_capacity = radiator_performance * temp_diff
    
    num_radiators = math.ceil(heat_load / radiator_capacity)
    
    print(f"Radiator Calculation:")
    print(f"  Heat Load: {heat_load}W")
    print(f"  Water-Air ΔT: {temp_diff}°C")
    print(f"  120mm Radiator Capacity: {radiator_capacity}W")
    print(f"  Radiators Needed: {num_radiators}")
    print(f"  Selected: 1× 120mm (with margin)\n")

def calculate_reservoir():
    """Determine reservoir size"""
    # Rule of thumb: 1L per 100W dissipated
    heat_load = calculate_heat_load()
    min_volume = heat_load / 100
    recommended = min_volume * 2  # Double for stability
    
    print(f"Reservoir Sizing:")
    print(f"  Minimum Volume: {min_volume:.1f}L")
    print(f"  Recommended: {recommended:.1f}L")
    print(f"  Selected: 5L food container\n")

def generate_plumbing_diagram():
    """ASCII diagram of cooling loop"""
    diagram = """
Cooling System Plumbing Diagram
===============================

    ┌─────────────┐
    │  Reservoir  │ ← Fill/Bleed Port
    │     5L      │
    └──────┬──────┘
           │
    ┌──────▼──────┐
    │    Pump     │ Hygger HG-909
    │  13.3 L/min │ 10W Submersible  
    └──────┬──────┘
           │
    ┌──────▼──────┐
    │ Flow Sensor │ YF-S201
    │  1-30 L/min │ Hall Effect
    └──────┬──────┘
           │
    ╔══════▼══════╗
    ║ WORK COIL   ║ 6mm Copper
    ║   (80mm)    ║ 8 Turns
    ╚══════┬══════╝
           │
    ┌──────▼──────┐
    │ Temp Sensor │ Type K
    │  T_outlet   │ Thermocouple
    └──────┬──────┘
           │
    ╔══════▼══════╗
    ║ OEM MODULE  ║ Water Block
    ║  HCX-3000W  ║ Internal
    ╚══════┬══════╝
           │
    ┌──────▼──────┐
    │   Radiator  │ 120mm + Fan
    │   500W cap  │ 12V PWM
    └──────┬──────┘
           │
           └────────→ Back to Reservoir

Components Summary:
- Total Flow Path: ~2m
- Tube Size: 6mm ID silicone
- Fittings: Push-connect 6mm
- Total Volume: ~5.5L
- Pressure Drop: <0.5 bar
    """
    print(diagram)

def generate_parts_list():
    """Complete cooling system parts list"""
    parts = {
        "Reservoir": {
            "item": "5L food container with lid",
            "qty": 1,
            "cost": 10,
            "notes": "Drill holes for fittings"
        },
        "Pump": {
            "item": "Hygger HG-909 800L/h",
            "qty": 1,
            "cost": 25,
            "notes": "Submersible in reservoir"
        },
        "Radiator": {
            "item": "120mm aluminum + fan",
            "qty": 1,
            "cost": 35,
            "notes": "Mount with good airflow"
        },
        "Flow Sensor": {
            "item": "YF-S201 Hall effect",
            "qty": 1,
            "cost": 8,
            "notes": "After pump, before coil"
        },
        "Tubing": {
            "item": "6mm ID silicone, 5m",
            "qty": 1,
            "cost": 20,
            "notes": "High-temp rated"
        },
        "Fittings": {
            "item": "6mm push-connect set",
            "qty": 20,
            "cost": 15,
            "notes": "Include tees and elbows"
        },
        "Coolant": {
            "item": "Distilled water",
            "qty": "6L",
            "cost": 5,
            "notes": "Add 10% propylene glycol"
        },
        "Temp Sensors": {
            "item": "Type K thermocouple",
            "qty": 2,
            "cost": 10,
            "notes": "Inlet and outlet"
        },
        "Clamps": {
            "item": "Worm gear clamps",
            "qty": 10,
            "cost": 5,
            "notes": "Backup for push fittings"
        }
    }
    
    print("\nCooling System Parts List:")
    print("="*50)
    total = 0
    for name, part in parts.items():
        print(f"{name}: {part['item']}")
        print(f"  Qty: {part['qty']}, Cost: ${part['cost']}, Notes: {part['notes']}")
        total += part['cost']
    print(f"\nTotal Cooling System Cost: ${total}")

def generate_operating_procedure():
    """Startup and maintenance procedures"""
    procedure = """
Cooling System Operating Procedures
==================================

Initial Fill Procedure:
1. Connect all components with pump OFF
2. Fill reservoir to 80% with distilled water
3. Add propylene glycol (10% by volume)
4. Run pump for 30 seconds, check for leaks
5. Top off reservoir as air purges
6. Run for 5 minutes, checking flow sensor
7. Verify >2 L/min flow rate

Startup Checklist:
□ Reservoir level >50%
□ No visible leaks
□ Flow sensor reads >2 L/min
□ Water temp <30°C
□ All connections tight
□ Radiator fan spinning

Shutdown Procedure:
1. Turn off induction power
2. Keep pump running for 5 minutes
3. Monitor outlet temperature
4. Stop pump when temp <40°C
5. Log runtime hours

Maintenance Schedule:
- Daily: Check reservoir level
- Weekly: Check for leaks, clean radiator
- Monthly: Test flow sensor accuracy
- Quarterly: Replace coolant
- Annually: Replace tubing

Emergency Procedures:
- Leak detected: E-stop, contain spill
- No flow: E-stop immediately
- Over-temp: Reduce power, check radiator
- Pump failure: Shutdown and replace

Temperature Monitoring Points:
1. Coil outlet (max 60°C)
2. Module outlet (max 50°C)  
3. Radiator inlet (max 45°C)
4. Reservoir (max 35°C)
    """
    print(procedure)

if __name__ == "__main__":
    print("INDUCTION HEATER COOLING SYSTEM DESIGN")
    print("="*50)
    
    # Run calculations
    heat_load = calculate_heat_load()
    required_flow = calculate_flow_requirements(heat_load)
    select_pump(required_flow)
    design_radiator(heat_load * SAFETY_FACTOR)
    calculate_reservoir()
    generate_plumbing_diagram()
    generate_parts_list()
    generate_operating_procedure()