"""
Example usage of the Component Registry
Shows how to mark components for expansion and add notes
"""

from component_registry import ComponentRegistry, ComponentCategory

def demonstrate_registry_usage():
    """Show how to use the component registry"""
    
    # Initialize the registry
    registry = ComponentRegistry()
    
    print("Component Registry Usage Example")
    print("=" * 80)
    
    # Example 1: Get components by category
    print("\n1. Getting all Acoustic Cylinder components:")
    acoustic_components = registry.get_components_by_category(ComponentCategory.ACOUSTIC)
    for comp in acoustic_components:
        print(f"   - {comp.name}: ${comp.total_cost}")
    
    # Example 2: Mark components for expansion
    print("\n2. Marking components for expansion:")
    # This is where you would mark specific components based on your analysis
    # Example (commented out - you'll fill these based on your needs):
    
    # registry.mark_for_expansion("Frame", "Needs detailed structural analysis")
    # registry.mark_for_expansion("Acoustic Cylinder", "Requires acoustic simulation")
    # registry.mark_for_expansion("Control Bus PCB", "Complex routing needs review")
    
    # Example 3: Update expansion notes
    print("\n3. Updating expansion notes:")
    # Example (commented out - you'll fill these based on your needs):
    
    # registry.update_expansion_notes("Frame", "Added: Check for resonance frequencies")
    
    # Example 4: Get a specific component
    print("\n4. Getting specific component details:")
    component = registry.get_component_by_name("10kW PSU")
    if component:
        print(f"   Name: {component.name}")
        print(f"   Specification: {component.specification}")
        print(f"   Cost: ${component.total_cost}")
        print(f"   Supplier: {component.supplier}")
    
    # Example 5: Get components requiring expansion
    print("\n5. Components requiring expansion:")
    expansion_list = registry.get_components_requiring_expansion()
    if expansion_list:
        for comp in expansion_list:
            print(f"   - {comp.name}: {comp.expansion_notes}")
    else:
        print("   None marked yet - use mark_for_expansion() to flag components")
    
    # Print full summary
    print("\n" + "=" * 80)
    registry.print_summary()


if __name__ == "__main__":
    demonstrate_registry_usage()