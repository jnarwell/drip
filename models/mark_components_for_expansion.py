"""
Script to mark components for expansion based on the upgrade path L1->L2->L3->L4
"""

from component_registry import ComponentRegistry

def mark_expansion_components(verbose=True):
    """Mark all components that need expansion with detailed notes"""
    
    registry = ComponentRegistry()
    
    # FRAME SUBSYSTEM
    registry.mark_for_expansion(
        "SS Tube",
        "L2: Upgrade to 180mm ID × 200mm (+$200) | L3: Same as L2 | L4: Upgrade to 400mm ID × 500mm (+$3,000)"
    )
    
    registry.mark_for_expansion(
        "Thermal Isolation Layer",
        "L2: Double thickness for 1580°C (+$400) | L3: Same as L2 | L4: Industrial grade multi-layer (+$2,000)"
    )
    
    registry.mark_for_expansion(
        "Air/Gas Border",
        "L2: Upgrade to graphite/metal for 1580°C (+$300) | L3: Add dual-zone sealing (+$200) | L4: Full production seals with purge (+$500)"
    )
    
    registry.mark_for_expansion(
        "Build Volume",
        "L2: 1,000 cm³ chamber (+$600) | L3: Same as L2 | L4: 8,000 cm³ chamber (+$3,000)"
    )
    
    # HEATED BED SUBSYSTEM
    registry.mark_for_expansion(
        "Heating Rods",
        "L2: 6× 1kW for larger platform (+$50) | L3: Same as L2 | L4: 12× 1kW for 400mm platform (+$300)"
    )
    
    registry.mark_for_expansion(
        "Thermocouples",  # This will match the heated bed thermocouples
        "L2: 4× Type K (+$24) | L3: 6× Type K for dual zones (+$24) | L4: 8× Type K (+$24)"
    )
    
    registry.mark_for_expansion(
        "Conductive Block",
        "L2: Larger block for 180mm (+$200) | L3: Dual-zone capability (+$300) | L4: 400mm multi-zone block (+$1,000)"
    )
    
    # ACOUSTIC CYLINDER SUBSYSTEM
    registry.mark_for_expansion(
        "40kHz Transducers",
        "L2: 36 units (+$36) | L3: Same 36 but higher power drivers | L4: 72 units (+$72)"
    )
    
    registry.mark_for_expansion(
        "Transducer Rings",
        "L2: 6 rings (+$450) | L3: Same 6 rings | L4: 12 rings (+$1,800)"
    )
    
    registry.mark_for_expansion(
        "6-Channel Amp Modules",
        "L2: 8 units (+$60) | L3: Upgrade to higher power TPA3116 (+$180) | L4: 12 units total (+$60)"
    )
    
    registry.mark_for_expansion(
        "Air/Water Jacket",  # Part of cooling system
        "L2: Enhanced flow for 36 transducers (+$800) | L3: Same as L2 | L4: Industrial cooling for 72 units (+$2,000)"
    )
    
    # CRUCIBLE SUBSYSTEM
    registry.mark_for_expansion(
        "Induction Heater",
        "L2: Ambrell 8kW for steel (+$2,150) | L3: Add second 8kW unit (+$3,000) | L4: 4× total units (+$5,600)"
    )
    
    registry.mark_for_expansion(
        "Crucible Assembly",
        "L2: Larger steel-rated crucible (+$600) | L3: Add second crucible (+$2,000) | L4: 4× crucibles total (+$4,000)"
    )
    
    registry.mark_for_expansion(
        "Feed Lines",
        "L2: 100 lines (+$750) | L3: 100 lines × 2 materials (+$1,000) | L4: 400 lines total (+$3,000)"
    )
    
    registry.mark_for_expansion(
        "Micro Heaters",
        "L2: 100× (+$600) | L3: 100× × 2 systems (+$800) | L4: 400× total (+$2,400)"
    )
    
    registry.mark_for_expansion(
        "Outlet Array",
        "L2: 100 outlets (10×10) (+$600) | L3: 100 × 2 separate arrays (+$600) | L4: 400 outlets (20×20) (+$3,000)"
    )
    
    # POWER/CONTROL SUBSYSTEM
    registry.mark_for_expansion(
        "10kW PSU",
        "L2: Upgrade to 25kW (+$2,500) | L3: Same 25kW | L4: 45kW system (+$5,000)"
    )
    
    registry.mark_for_expansion(
        "FPGA Board",
        "L2: Same (software upgrade only) | L3: Add second FPGA for dual control (+$75) | L4: Upgrade to larger FPGAs (+$200)"
    )
    
    registry.mark_for_expansion(
        "8-Channel Relays",
        "L2: 10 units (+$40) | L3: 15 units for dual systems (+$40) | L4: 20 units total (+$40)"
    )
    
    registry.mark_for_expansion(
        "STM32 Dev Board",
        "L2: Add second for expanded I/O (+$25) | L3: Same 2 boards | L4: 4× boards for distributed control (+$50)"
    )
    
    # Additional notes for level-specific additions
    if verbose:
        print("\nMARKING COMPONENTS FOR EXPANSION")
        print("=" * 80)
        
        # Print components marked for expansion
        expansion_components = registry.get_components_requiring_expansion()
        print(f"\nTotal components marked for expansion: {len(expansion_components)}")
        
        for comp in expansion_components:
            print(f"\n{comp.name}:")
            print(f"  Category: {comp.category.value}")
            print(f"  Current spec: {comp.specification}")
            print(f"  Expansion path: {comp.expansion_notes}")
        
        # Print additional level requirements
        print("\n\nADDITIONAL LEVEL REQUIREMENTS:")
        print("=" * 80)
    
    if verbose:
        print("\nLevel 2 Additions:")
        print("  - Argon purge capability (basic) (+$1,000)")
        print("  - High-temp chamber windows (+$300)")
        print("  - Steel-compatible materials throughout")
        
        print("\nLevel 3 Additions:")
        print("  - Complete second material system")
        print("  - Acoustic pulse control software for thermal expansion")
        print("  - Dual independent feed systems")
        print("  - 2× Optris Xi 400 thermal cameras (+$8,000)")
        print("  - No interface materials needed!")
        
        print("\nLevel 4 Additions:")
        print("  - Full argon atmosphere system (+$8,000)")
        print("  - Production control software (+$10,000)")
        print("  - Automated door system (+$3,000)")
        print("  - Industrial filtration (+$5,000)")
        print("  - Upgrade thermal cameras to Optris PI 1M (+$7,000)")
        
        print("\n\nNOTE: The modular design means most L1 components get reused and expanded")
        print("rather than replaced. Only major items like the induction heater and PSU")
        print("need complete replacement when scaling up.")
    
    return registry


if __name__ == "__main__":
    registry = mark_expansion_components(verbose=True)
    
    # Save the updated registry summary
    print("\n\n" + "=" * 80)
    print("UPDATED COMPONENT REGISTRY SUMMARY")
    print("=" * 80)
    registry.print_summary()