"""
Dynamic Power Budget Calculator
Calculates power budget from actual component specifications
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
from models.component_registry import ComponentRegistry, ComponentCategory

@dataclass
class PowerNode:
    """Represents a power distribution node"""
    name: str
    input_power: float = 0.0  # Power supplied TO this node
    output_power: float = 0.0  # Power supplied BY this node
    consumed_power: float = 0.0  # Power consumed AT this node
    efficiency: float = 1.0  # Conversion efficiency
    
    @property
    def net_power(self) -> float:
        """Net power flow (positive = consuming, negative = supplying)"""
        return self.consumed_power + (self.output_power / self.efficiency) - self.input_power
    
    @property
    def losses(self) -> float:
        """Power lost in conversion"""
        return self.output_power * (1.0 - self.efficiency) / self.efficiency if self.efficiency > 0 else 0

class PowerBudgetCalculator:
    """Calculate system power budget from component specifications"""
    
    def __init__(self):
        self.registry = ComponentRegistry()
        self.power_nodes: Dict[str, PowerNode] = {}
        self.initialize_nodes()
    
    def initialize_nodes(self):
        """Create power nodes for each subsystem"""
        for category in ComponentCategory:
            self.power_nodes[category.value] = PowerNode(name=category.value)
    
    def calculate_parametric_budget(self) -> Dict:
        """Calculate power budget from actual component values"""
        budget = {
            "power_sources": {},
            "power_consumers": {},
            "subsystem_totals": {},
            "system_totals": {
                "total_supply_capacity": 0.0,
                "total_consumption": 0.0,
                "total_losses": 0.0,
                "net_power_required": 0.0,
                "power_margin": 0.0
            },
            "warnings": [],
            "errors": []
        }
        
        # Scan all components for power characteristics
        for component in self.registry.components:
            if component.tech_specs:
                # Check if it's a power source
                if component.tech_specs.power_supply:
                    power_out = component.tech_specs.power_supply * component.quantity
                    efficiency = component.tech_specs.efficiency or 100.0
                    
                    budget["power_sources"][component.name] = {
                        "output_power": power_out,
                        "efficiency": efficiency / 100.0,
                        "losses": power_out * (1 - efficiency/100),
                        "quantity": component.quantity,
                        "unit_power": component.tech_specs.power_supply
                    }
                    
                    budget["system_totals"]["total_supply_capacity"] += power_out
                    
                    # Add to node
                    node = self.power_nodes[component.category.value]
                    node.output_power += power_out
                    node.efficiency = efficiency / 100.0
                
                # Check if it's a power consumer
                if component.tech_specs.power_consumption:
                    power_in = component.tech_specs.power_consumption * component.quantity
                    
                    budget["power_consumers"][component.name] = {
                        "power_consumption": power_in,
                        "quantity": component.quantity,
                        "unit_power": component.tech_specs.power_consumption,
                        "subsystem": component.category.value
                    }
                    
                    budget["system_totals"]["total_consumption"] += power_in
                    
                    # Add to node
                    node = self.power_nodes[component.category.value]
                    node.consumed_power += power_in
        
        # Calculate subsystem totals
        for category, node in self.power_nodes.items():
            budget["subsystem_totals"][category] = {
                "consumption": node.consumed_power,
                "supply": node.output_power,
                "net": node.net_power,
                "losses": node.losses
            }
            budget["system_totals"]["total_losses"] += node.losses
        
        # Calculate system-level metrics
        budget["system_totals"]["net_power_required"] = (
            budget["system_totals"]["total_consumption"] - 
            budget["system_totals"]["total_supply_capacity"]
        )
        
        budget["system_totals"]["power_margin"] = (
            budget["system_totals"]["total_supply_capacity"] - 
            budget["system_totals"]["total_consumption"]
        )
        
        # Generate warnings and errors
        if budget["system_totals"]["net_power_required"] > 0:
            budget["errors"].append(
                f"INSUFFICIENT POWER: System requires {budget['system_totals']['net_power_required']:.1f}W "
                f"more than available supply capacity"
            )
        
        if budget["system_totals"]["power_margin"] < 1000 and budget["system_totals"]["power_margin"] >= 0:
            budget["warnings"].append(
                f"LOW POWER MARGIN: Only {budget['system_totals']['power_margin']:.1f}W margin remaining"
            )
        
        # Check individual PSU capacity against actual rated capacity
        for source_name, source_data in budget["power_sources"].items():
            rated_capacity = source_data["output_power"]
            if budget["system_totals"]["total_consumption"] > rated_capacity:
                budget["warnings"].append(
                    f"PSU OVERLOAD: {source_name} rated for {rated_capacity:.0f}W but system requires "
                    f"{budget['system_totals']['total_consumption']:.1f}W"
                )
        
        return budget
    
    def generate_power_report(self) -> str:
        """Generate markdown power budget report"""
        budget = self.calculate_parametric_budget()
        
        lines = ["# Power Budget Analysis (Parametric)", ""]
        lines.append(f"*Generated from component specifications*")
        lines.append("")
        
        # Errors first
        if budget["errors"]:
            lines.append("## ⚠️ CRITICAL ERRORS")
            for error in budget["errors"]:
                lines.append(f"- **{error}**")
            lines.append("")
        
        # Warnings
        if budget["warnings"]:
            lines.append("## ⚠️ Warnings")
            for warning in budget["warnings"]:
                lines.append(f"- {warning}")
            lines.append("")
        
        # System totals
        lines.append("## System Power Summary")
        lines.append("| Metric | Value |")
        lines.append("|--------|-------|")
        lines.append(f"| Total Supply Capacity | {budget['system_totals']['total_supply_capacity']:.1f}W |")
        lines.append(f"| Total Consumption | {budget['system_totals']['total_consumption']:.1f}W |")
        lines.append(f"| Conversion Losses | {budget['system_totals']['total_losses']:.1f}W |")
        lines.append(f"| **Net Power Required** | **{budget['system_totals']['net_power_required']:.1f}W** |")
        lines.append(f"| **Power Margin** | **{budget['system_totals']['power_margin']:.1f}W** |")
        lines.append("")
        
        # Power sources
        lines.append("## Power Sources")
        lines.append("| Component | Quantity | Unit Power | Total Output | Efficiency | Losses |")
        lines.append("|-----------|----------|------------|--------------|------------|--------|")
        for name, data in budget["power_sources"].items():
            lines.append(
                f"| {name} | {data['quantity']} | {data['unit_power']:.1f}W | "
                f"{data['output_power']:.1f}W | {data['efficiency']*100:.1f}% | {data['losses']:.1f}W |"
            )
        lines.append("")
        
        # Major consumers
        lines.append("## Major Power Consumers (>100W)")
        lines.append("| Component | Subsystem | Quantity | Unit Power | Total |")
        lines.append("|-----------|-----------|----------|------------|-------|")
        for name, data in sorted(budget["power_consumers"].items(), 
                                key=lambda x: x[1]["power_consumption"], 
                                reverse=True):
            if data["power_consumption"] >= 100:
                lines.append(
                    f"| {name} | {data['subsystem']} | {data['quantity']} | "
                    f"{data['unit_power']:.1f}W | {data['power_consumption']:.1f}W |"
                )
        lines.append("")
        
        # Subsystem breakdown
        lines.append("## Subsystem Power Distribution")
        lines.append("| Subsystem | Consumption | Supply | Net | Status |")
        lines.append("|-----------|-------------|--------|-----|--------|")
        for subsystem, data in budget["subsystem_totals"].items():
            status = "✅" if data["net"] <= 0 else "⚠️ Deficit"
            lines.append(
                f"| {subsystem} | {data['consumption']:.1f}W | "
                f"{data['supply']:.1f}W | {data['net']:.1f}W | {status} |"
            )
        
        return "\n".join(lines)
    
    def validate_power_architecture(self) -> List[str]:
        """Validate the power distribution architecture"""
        issues = []
        budget = self.calculate_parametric_budget()
        
        # Check if we have sufficient primary power
        if budget["system_totals"]["net_power_required"] > 0:
            issues.append(
                f"Primary PSU undersized by {budget['system_totals']['net_power_required']:.1f}W"
            )
        
        # Check for missing power specs
        for component in self.registry.components:
            if component.category == ComponentCategory.POWER_CONTROL:
                if not component.tech_specs or (
                    not component.tech_specs.power_consumption and 
                    not component.tech_specs.power_supply
                ):
                    issues.append(f"Missing power specification for {component.name}")
        
        # Check heating power specifically
        heating_power = sum(
            c.tech_specs.power_consumption * c.quantity
            for c in self.registry.components
            if c.tech_specs and c.tech_specs.power_consumption and 
            ("heat" in c.name.lower() or "crucible" in c.name.lower())
        )
        
        if heating_power > budget["system_totals"]["total_supply_capacity"]:
            issues.append(
                f"Heating systems alone ({heating_power:.1f}W) exceed PSU capacity"
            )
        
        return issues

# Usage
if __name__ == "__main__":
    calculator = PowerBudgetCalculator()
    
    # Generate report
    print(calculator.generate_power_report())
    
    # Validate architecture
    issues = calculator.validate_power_architecture()
    if issues:
        print("\nArchitecture Issues Found:")
        for issue in issues:
            print(f"  - {issue}")