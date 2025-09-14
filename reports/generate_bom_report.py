"""
Generate BOM Analysis Report
"""

import sys
sys.path.append('../models')
from component_registry import ComponentRegistry, ComponentCategory, ComponentType
from mark_components_for_expansion import mark_expansion_components
import re

def generate_bom_report():
    """Generate comprehensive BOM report"""
    
    # Initialize registry with expansion data
    registry = mark_expansion_components(verbose=False)
    
    print("=" * 80)
    print("BOM ANALYSIS REPORT - ACOUSTIC MANUFACTURING SYSTEM")
    print("=" * 80)
    
    # 1. FULL BOM BY SUBSYSTEM
    print("\n1. FULL BOM BY SUBSYSTEM")
    print("-" * 80)
    
    for subsystem in ComponentCategory:
        print(f"\n{subsystem.value}:")
        components = registry.get_components_by_category(subsystem)
        
        # Separate COTS and Custom
        cots_components = [c for c in components if c.type == ComponentType.COTS]
        custom_components = [c for c in components if c.type == ComponentType.CUSTOM]
        
        if cots_components:
            print("\n  COTS Components:")
            for comp in cots_components:
                print(f"    • {comp.name}: ${comp.total_cost:,.2f} ({comp.specification})")
        
        if custom_components:
            print("\n  Custom Components:")
            for comp in custom_components:
                print(f"    • {comp.name}: ${comp.total_cost:,.2f} ({comp.specification})")
        
        # Subsystem totals
        cots_total = sum(c.total_cost for c in cots_components)
        custom_total = sum(c.total_cost for c in custom_components)
        print(f"\n  Subtotals: COTS: ${cots_total:,.2f} | Custom: ${custom_total:,.2f} | Total: ${cots_total + custom_total:,.2f}")
    
    # 2. COST BREAKDOWN BY TYPE
    print("\n\n2. COST BREAKDOWN ANALYSIS")
    print("-" * 80)
    
    totals = registry.get_grand_totals()
    print(f"\nTotal System Cost: ${totals['Total']:,.2f}")
    print(f"  - COTS Components: ${totals['COTS']:,.2f} ({totals['COTS']/totals['Total']*100:.1f}%)")
    print(f"  - Custom Components: ${totals['Custom']:,.2f} ({totals['Custom']/totals['Total']*100:.1f}%)")
    
    # Classification breakdown
    electrical_keywords = ['Heater', 'Thermocouple', 'PSU', 'Transducer', 'Amp', 'Relay', 'FPGA', 'STM32', 'Controller']
    mechanical_keywords = ['Frame', 'Tube', 'Plate', 'Block', 'Ring', 'Housing', 'Cylinder', 'Rails', 'Panel', 'Crucible']
    control_keywords = ['FPGA', 'STM32', 'Controller', 'Bus', 'PCB']
    
    classification = {'Electrical': 0, 'Mechanical': 0, 'Control': 0, 'Other': 0}
    
    for component in registry.components:
        name = component.name
        if any(keyword in name for keyword in control_keywords):
            classification['Control'] += component.total_cost
        elif any(keyword in name for keyword in electrical_keywords):
            classification['Electrical'] += component.total_cost
        elif any(keyword in name for keyword in mechanical_keywords):
            classification['Mechanical'] += component.total_cost
        else:
            classification['Other'] += component.total_cost
    
    print("\nClassification Breakdown:")
    for category, cost in classification.items():
        print(f"  - {category}: ${cost:,.2f} ({cost/totals['Total']*100:.1f}%)")
    
    # Top 10 most expensive
    print("\nTop 10 Most Expensive Components:")
    sorted_components = sorted(registry.components, key=lambda x: x.total_cost, reverse=True)[:10]
    for i, comp in enumerate(sorted_components, 1):
        print(f"  {i}. {comp.name}: ${comp.total_cost:,.2f}")
    
    # 3. EXPANSION ANALYSIS
    print("\n\n3. EXPANSION PATH ANALYSIS")
    print("-" * 80)
    
    expansion_components = registry.get_components_requiring_expansion()
    print(f"\nComponents requiring expansion: {len(expansion_components)}")
    
    # Calculate expansion costs
    total_upgrades = {'L2': 0, 'L3': 0, 'L4': 0}
    
    print("\nExpansion Details:")
    for comp in expansion_components:
        notes = comp.expansion_notes
        
        # Parse costs
        l2_match = re.search(r'L2:.*?\(\+\$([0-9,]+)\)', notes)
        l3_match = re.search(r'L3:.*?\(\+\$([0-9,]+)\)', notes)
        l4_match = re.search(r'L4:.*?\(\+\$([0-9,]+)\)', notes)
        
        l2_cost = int(l2_match.group(1).replace(',', '')) if l2_match else 0
        l3_cost = int(l3_match.group(1).replace(',', '')) if l3_match else 0
        l4_cost = int(l4_match.group(1).replace(',', '')) if l4_match else 0
        
        if 'L3: Same as L2' in notes:
            l3_cost = 0
        
        total_upgrades['L2'] += l2_cost
        total_upgrades['L3'] += l3_cost
        total_upgrades['L4'] += l4_cost
        
        if l2_cost + l3_cost + l4_cost > 0:
            print(f"\n  {comp.name}:")
            print(f"    L1 Base: ${comp.total_cost:,.2f}")
            if l2_cost > 0:
                print(f"    L2 Upgrade: +${l2_cost:,.2f}")
            if l3_cost > 0:
                print(f"    L3 Upgrade: +${l3_cost:,.2f}")
            if l4_cost > 0:
                print(f"    L4 Upgrade: +${l4_cost:,.2f}")
    
    # Additional level costs
    additional_costs = {
        'L2': 1300,  # Argon purge + windows
        'L3': 8000,  # Thermal cameras
        'L4': 31000  # Full atmosphere + software + door + filtration + camera upgrade
    }
    
    print("\n\nAdditional Level Requirements:")
    print("  Level 2: +$1,300 (Argon purge, high-temp windows)")
    print("  Level 3: +$8,000 (Thermal cameras)")
    print("  Level 4: +$31,000 (Atmosphere system, software, automation)")
    
    # Total costs by level
    base_cost = totals['Total']
    cumulative_costs = {
        'L1': base_cost,
        'L2': base_cost + total_upgrades['L2'] + additional_costs['L2'],
        'L3': base_cost + total_upgrades['L2'] + total_upgrades['L3'] + additional_costs['L2'] + additional_costs['L3'],
        'L4': base_cost + total_upgrades['L2'] + total_upgrades['L3'] + total_upgrades['L4'] + 
              additional_costs['L2'] + additional_costs['L3'] + additional_costs['L4']
    }
    
    print("\n\nTOTAL SYSTEM COSTS BY LEVEL:")
    print("-" * 40)
    for level, cost in cumulative_costs.items():
        if level == 'L1':
            print(f"  {level}: ${cost:,.2f}")
        else:
            prev_level = f'L{int(level[1])-1}'
            increase = cost - cumulative_costs[prev_level]
            percent_increase = (cost - cumulative_costs[prev_level]) / cumulative_costs[prev_level] * 100
            print(f"  {level}: ${cost:,.2f} (+${increase:,.2f}, +{percent_increase:.1f}%)")
    
    print("\n\nKEY INSIGHTS:")
    print("-" * 40)
    print(f"  • Total expansion cost (L1→L4): ${cumulative_costs['L4'] - cumulative_costs['L1']:,.2f}")
    print(f"  • L4 system is {cumulative_costs['L4'] / cumulative_costs['L1']:.1f}x the cost of L1")
    print(f"  • Largest component upgrade: Induction Heater (${2150+3000+5600:,.2f} total)")
    print(f"  • Most components are expanded rather than replaced (modular design)")
    
    print("\n" + "=" * 80)
    print("END OF REPORT")
    print("=" * 80)


if __name__ == "__main__":
    generate_bom_report()