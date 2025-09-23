#!/usr/bin/env python3
"""
Induction Heater Integration Bill of Materials
For DRIP Acoustic Levitation Manufacturing System
Total cost: ~$963 ($420 OEM module + $543 integration)
"""

INTEGRATION_BOM = {
    # Primary OEM Module
    "oem_module": {
        "part": "HCGF HCX-3000W-50K",
        "specs": "3kW, 30-80kHz auto-tracking, water cooled",
        "quantity": 1,
        "cost": 420,
        "source": "Alibaba - search 'HCGF 3000W induction heater module'",
        "notes": "Includes power board, control board, current transformer"
    },
    
    # Electrical Safety Components
    "main_contactor": {
        "part": "Schneider LC1D32P7",
        "specs": "32A, 230V coil, 3-pole",
        "quantity": 1,
        "cost": 85,
        "source": "Grainger #3210847"
    },
    
    "emergency_stop": {
        "part": "Allen-Bradley 800T-FX",
        "specs": "Illuminated mushroom, NC contacts",
        "quantity": 1,
        "cost": 65,
        "source": "DigiKey #800T-FXQL24RA1"
    },
    
    "emi_filter": {
        "part": "Schaffner FN2090-16-06",
        "specs": "16A, 250VAC, medical grade",
        "quantity": 1,
        "cost": 45,
        "source": "Mouser #448-FN2090-16-06"
    },
    
    "circuit_breaker": {
        "part": "Square D HOM230",
        "specs": "30A, 2-pole, 240V",
        "quantity": 1,
        "cost": 25,
        "source": "Home Depot #HOM230CP"
    },
    
    # Control Interface
    "interface_pcb": {
        "part": "Custom PCB",
        "specs": "2-layer, FR4, HASL finish",
        "quantity": 1,
        "cost": 30,
        "source": "JLCPCB - see gerbers/"
    },
    
    "optocouplers": {
        "part": "PC817",
        "specs": "5V/24V isolation",
        "quantity": 4,
        "cost": 2,
        "source": "DigiKey #PC817X4NSZ0F"
    },
    
    "power_meter": {
        "part": "PZEM-022",
        "specs": "AC 80-260V, 100A CT",
        "quantity": 1,
        "cost": 18,
        "source": "Amazon #B07J2Q4YWW"
    },
    
    # Cooling System
    "water_pump": {
        "part": "Hygger HG-909",
        "specs": "800L/h, 10W, submersible",
        "quantity": 1,
        "cost": 25,
        "source": "Amazon #B07L54XBDL"
    },
    
    "radiator": {
        "part": "120mm aluminum PC radiator",
        "specs": "With fan, G1/4 fittings",
        "quantity": 1,
        "cost": 35,
        "source": "Amazon #B019OCLHKE"
    },
    
    "flow_sensor": {
        "part": "YF-S201",
        "specs": "1-30L/min, Hall effect",
        "quantity": 1,
        "cost": 8,
        "source": "Amazon #B00VKAT7EE"
    },
    
    # Mechanical
    "enclosure": {
        "part": "BUD Industries NBF-32026",
        "specs": "14\"×10\"×6\", NEMA 12",
        "quantity": 1,
        "cost": 95,
        "source": "DigiKey #377-1894-ND"
    },
    
    "cooling_tubing": {
        "part": "6mm ID silicone",
        "specs": "High-temp, 5 meters",
        "quantity": 1,
        "cost": 20,
        "source": "Amazon #B01MXZB469"
    },
    
    "work_coil": {
        "part": "Custom wound",
        "specs": "6mm copper tube, 8 turns",
        "quantity": 1,
        "cost": 40,
        "source": "Local - see coil_design.md"
    },
    
    # Additional Safety Items
    "gfci_outlet": {
        "part": "Leviton GFNT2-W",
        "specs": "20A GFCI outlet",
        "quantity": 1,
        "cost": 25,
        "source": "Home Depot #GFNT2-W"
    },
    
    "warning_labels": {
        "part": "Safety label kit",
        "specs": "High voltage, hot surface, magnetic field",
        "quantity": 1,
        "cost": 15,
        "source": "Amazon #B07KQXJXWX"
    },
    
    "terminal_blocks": {
        "part": "Phoenix Contact 3273500",
        "specs": "35A feed-through blocks",
        "quantity": 6,
        "cost": 20,
        "source": "DigiKey #277-1667-ND"
    },
    
    "misc_hardware": {
        "part": "Wiring, connectors, fuses",
        "specs": "12 AWG wire, ring terminals, etc",
        "quantity": 1,
        "cost": 50,
        "source": "Local electrical supplier"
    }
}

# Calculate totals
integration_cost = sum(item["cost"] for item in INTEGRATION_BOM.values() if "oem_module" not in item)
module_cost = INTEGRATION_BOM["oem_module"]["cost"]
total_cost = integration_cost + module_cost

print(f"\nInduction Heater BOM Summary:")
print(f"{'='*40}")
print(f"OEM Module Cost: ${module_cost}")
print(f"Integration Cost: ${integration_cost}")
print(f"Total System Cost: ${total_cost}")
print(f"\nCost savings vs pure COTS: ${1200 - total_cost}")

def generate_shopping_list():
    """Generate formatted shopping list"""
    print(f"\n\nShopping List by Supplier:")
    print(f"{'='*40}")
    
    # Group by source
    suppliers = {}
    for name, item in INTEGRATION_BOM.items():
        source = item["source"].split()[0]  # Get supplier name
        if source not in suppliers:
            suppliers[source] = []
        suppliers[source].append({
            "name": name,
            "part": item["part"],
            "cost": item["cost"]
        })
    
    for supplier, items in sorted(suppliers.items()):
        print(f"\n{supplier}:")
        total = 0
        for item in items:
            print(f"  - {item['part']}: ${item['cost']}")
            total += item["cost"]
        print(f"  Subtotal: ${total}")

if __name__ == "__main__":
    generate_shopping_list()