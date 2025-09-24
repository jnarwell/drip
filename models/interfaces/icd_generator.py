"""
ICD Generator - Creates formal Interface Control Documents from component specs
"""

import os
from typing import List, Dict, Optional
from datetime import datetime
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from models.component_registry import ComponentRegistry
from models.interfaces.interface_registry import Interface, SYSTEM_INTERFACES, InterfaceType

class ICDGenerator:
    """Generate Interface Control Documents from component registry and interface definitions"""
    
    def __init__(self):
        self.registry = ComponentRegistry()
        self.template = self._load_template()
    
    def _load_template(self) -> str:
        """Load ICD markdown template"""
        return """# {icd_number}: {name}

## Document Control
- **ICD Number**: {icd_number}
- **Revision**: {revision}
- **Date**: {date}
- **Status**: {status}
- **Criticality**: {criticality}

## 1. Interface Overview
- **Purpose**: Define interface between {side_a_subsystem} and {side_b_subsystem}
- **Interface Types**: {interface_types}
- **Side A Components**: {side_a_components}
- **Side B Components**: {side_b_components}

## 2. Interface Requirements

| Parameter | Nominal | Min | Max | Units | Verification |
|-----------|---------|-----|-----|-------|--------------|
{requirements_table}

## 3. Physical Interface

### 3.1 Mechanical Details
{mechanical_details}

### 3.2 Thermal Details
{thermal_details}

### 3.3 Electrical Details
{electrical_details}

## 4. Component Specifications

### Side A Components
{side_a_specs}

### Side B Components
{side_b_specs}

## 5. Verification & Validation

### 5.1 Test Equipment
{test_equipment}

### 5.2 Test Procedure
{test_procedure}

### 5.3 Acceptance Criteria
- All parameters within specified min/max ranges
- No thermal damage to components
- Stable operation for 4+ hours
- Interface meets all functional requirements

## 6. Interface Compatibility Analysis
{compatibility_analysis}

## 7. Risk Assessment
{risk_assessment}

## 8. Design Considerations

### 8.1 Safety Requirements
- All electrical interfaces must meet IEC 61010-1 safety standards
- Thermal interfaces require overheat protection
- Mechanical interfaces must have fail-safe mounting

### 8.2 Environmental Conditions
- Operating Temperature: 15-35°C ambient
- Relative Humidity: 20-80% non-condensing
- Vibration: <0.5g RMS

### 8.3 Maintenance Access
- All connectors accessible within 30 seconds
- Test points marked and accessible
- Service documentation required for each interface

## 9. Change History
| Date | Revision | Description | Author |
|------|----------|-------------|--------|
| {date} | {revision} | Initial release | System Engineer |

---
*This ICD was auto-generated from component specifications on {timestamp}*
"""
    
    def generate_icd(self, interface: Interface) -> str:
        """Generate complete ICD document"""
        
        # Get component specifications
        side_a_specs = self._get_component_specs(interface.side_a_components)
        side_b_specs = self._get_component_specs(interface.side_b_components)
        
        # Format requirements table
        req_rows = []
        for req in interface.requirements:
            req_rows.append(
                f"| {req.parameter} | {req.nominal} | {req.min_value} | "
                f"{req.max_value} | {req.units} | {req.verification_method} |"
            )
        
        # Perform compatibility analysis
        compatibility = self._analyze_compatibility(interface, side_a_specs, side_b_specs)
        
        # Assess risks
        risks = self._assess_risks(interface, compatibility)
        
        # Format the document
        doc = self.template.format(
            icd_number=interface.icd_number,
            name=interface.name,
            revision=interface.revision,
            date=interface.date,
            status=interface.status,
            criticality=interface.criticality.value.upper(),
            side_a_subsystem=interface.side_a_subsystem,
            side_b_subsystem=interface.side_b_subsystem,
            interface_types=", ".join([t.value for t in interface.interface_types]),
            side_a_components=", ".join(interface.side_a_components),
            side_b_components=", ".join(interface.side_b_components),
            requirements_table="\n".join(req_rows),
            mechanical_details=self._format_dict_section(interface.mechanical_details),
            thermal_details=self._format_dict_section(interface.thermal_details),
            electrical_details=self._format_dict_section(interface.electrical_details),
            side_a_specs=side_a_specs,
            side_b_specs=side_b_specs,
            test_equipment=self._format_list(interface.test_equipment),
            test_procedure=self._generate_test_procedure(interface),
            compatibility_analysis=compatibility,
            risk_assessment=risks,
            timestamp="Current version"
        )
        
        return doc
    
    def _get_component_specs(self, component_names: List[str]) -> str:
        """Extract component specifications from registry"""
        specs = []
        for name in component_names:
            for component in self.registry.components:
                if component.name == name:
                    specs.append(f"**{name}**")
                    if component.tech_specs:
                        ts = component.tech_specs
                        if ts.power_consumption:
                            specs.append(f"- Power Consumption: {ts.power_consumption}W")
                        if ts.power_supply:
                            specs.append(f"- Power Supply: {ts.power_supply}W")
                        if ts.operating_temp:
                            specs.append(f"- Operating Temp: {ts.operating_temp[0]}-{ts.operating_temp[1]}°C")
                        if ts.max_temp:
                            specs.append(f"- Max Temp: {ts.max_temp}°C")
                        if ts.weight:
                            specs.append(f"- Weight: {ts.weight}kg")
                        if ts.frequency:
                            specs.append(f"- Frequency: {ts.frequency}Hz")
                        if ts.efficiency:
                            specs.append(f"- Efficiency: {ts.efficiency}%")
                        if ts.dimensions:
                            dims = ts.dimensions
                            if 'L' in dims and 'W' in dims and 'H' in dims:
                                specs.append(f"- Dimensions: {dims['L']}×{dims['W']}×{dims['H']}mm")
                            elif 'D' in dims and 'H' in dims:
                                specs.append(f"- Dimensions: Ø{dims['D']}×{dims['H']}mm")
                    specs.append(f"- Cost: ${component.total_cost}")
                    specs.append(f"- Supplier: {component.supplier}")
                    specs.append("")
                    break
            else:
                specs.append(f"**{name}**")
                specs.append("- ⚠️ Component not in registry - needs definition")
                specs.append("- Specification: [TO BE DEFINED]")
                specs.append("- Cost: [TBD]")
                specs.append("- Supplier: [TBD]")
                specs.append("- **ACTION REQUIRED**: Add to component_registry.py")
                specs.append("")
        
        return "\n".join(specs)
    
    def _analyze_compatibility(self, interface: Interface, side_a_specs: str, side_b_specs: str) -> str:
        """Analyze interface compatibility"""
        issues = []
        warnings = []
        
        # Check thermal compatibility
        if InterfaceType.THERMAL in interface.interface_types:
            side_a_max_temp = 0
            side_b_max_temp = 0
            
            for comp_name in interface.side_a_components:
                for component in self.registry.components:
                    if component.name == comp_name and component.tech_specs:
                        if component.tech_specs.max_temp:
                            side_a_max_temp = max(side_a_max_temp, component.tech_specs.max_temp)
                            if component.tech_specs.max_temp < 100:  # Low temp component
                                warnings.append(
                                    f"⚠️ {comp_name} has max temp of {component.tech_specs.max_temp}°C - ensure adequate thermal isolation"
                                )
            
            for comp_name in interface.side_b_components:
                for component in self.registry.components:
                    if component.name == comp_name and component.tech_specs:
                        if component.tech_specs.max_temp:
                            side_b_max_temp = max(side_b_max_temp, component.tech_specs.max_temp)
            
            # Check for extreme thermal mismatch
            if side_a_max_temp > 0 and side_b_max_temp > 0:
                temp_diff = abs(side_a_max_temp - side_b_max_temp)
                if temp_diff > 500:
                    issues.append(
                        f"❌ Extreme thermal mismatch: {temp_diff}°C difference between sides"
                    )
        
        # Check power compatibility
        if InterfaceType.ELECTRICAL in interface.interface_types:
            total_power_demand = 0
            total_power_supply = 0
            
            for comp_name in interface.side_a_components + interface.side_b_components:
                for component in self.registry.components:
                    if component.name == comp_name and component.tech_specs:
                        if component.tech_specs.power_consumption:
                            total_power_demand += component.tech_specs.power_consumption * (component.quantity or 1)
                        if component.tech_specs.power_supply:
                            total_power_supply += component.tech_specs.power_supply * (component.quantity or 1)
            
            if total_power_demand > total_power_supply:
                issues.append(f"❌ Insufficient power supply: {total_power_demand}W demand vs {total_power_supply}W supply")
            elif total_power_demand > total_power_supply * 0.8:
                warnings.append(f"⚠️ Low power margin: {total_power_demand}W demand vs {total_power_supply}W supply")
        
        # Check frequency compatibility
        if InterfaceType.ACOUSTIC in interface.interface_types:
            frequencies = []
            for comp_name in interface.side_a_components + interface.side_b_components:
                for component in self.registry.components:
                    if component.name == comp_name and component.tech_specs:
                        if component.tech_specs.frequency:
                            frequencies.append((comp_name, component.tech_specs.frequency))
            
            # Check for frequency mismatches
            if len(frequencies) > 1:
                base_freq = frequencies[0][1]
                for comp_name, freq in frequencies[1:]:
                    if abs(freq - base_freq) > base_freq * 0.05:  # >5% difference
                        warnings.append(f"⚠️ Frequency mismatch: {comp_name} at {freq}Hz vs reference {base_freq}Hz")
        
        # Generate result
        result = "### Compatibility Status: "
        if not issues:
            result += "✅ COMPATIBLE\n\n"
        else:
            result += "❌ INCOMPATIBLE\n\n**Critical Issues:**\n"
            result += "\n".join(f"- {issue}" for issue in issues) + "\n\n"
        
        if warnings:
            result += "**Warnings:**\n"
            result += "\n".join(f"- {warning}" for warning in warnings) + "\n\n"
        
        if not issues and not warnings:
            result += "No compatibility issues identified.\n"
        
        return result
    
    def _assess_risks(self, interface: Interface, compatibility: str) -> str:
        """Assess interface risks"""
        risks = []
        
        # High criticality risks
        if interface.criticality.value == "high":
            risks.append({
                'risk': 'Critical interface failure causing system shutdown',
                'probability': 'Low',
                'impact': 'High',
                'mitigation': 'Redundant monitoring, fail-safe design, regular testing'
            })
        
        # Type-specific risks
        if InterfaceType.THERMAL in interface.interface_types:
            risks.append({
                'risk': 'Thermal damage to components',
                'probability': 'Medium',
                'impact': 'High',
                'mitigation': 'Active cooling, thermal monitoring, temperature limits'
            })
        
        if InterfaceType.ACOUSTIC in interface.interface_types:
            risks.append({
                'risk': 'Acoustic coupling loss affecting process quality',
                'probability': 'Medium',
                'impact': 'Medium',
                'mitigation': 'Regular calibration, field mapping, backup transducers'
            })
        
        if InterfaceType.ELECTRICAL in interface.interface_types:
            risks.append({
                'risk': 'Electrical fault causing component damage',
                'probability': 'Low',
                'impact': 'High',
                'mitigation': 'Circuit protection, isolation, ground fault detection'
            })
        
        if InterfaceType.DATA in interface.interface_types:
            risks.append({
                'risk': 'Data corruption or communication loss',
                'probability': 'Medium',
                'impact': 'Medium',
                'mitigation': 'Error checking, redundant paths, watchdog timers'
            })
        
        if not risks:
            return "No significant risks identified."
        
        result = "| Risk | Probability | Impact | Mitigation |\n"
        result += "|------|-------------|--------|------------|\n"
        for risk in risks:
            result += f"| {risk['risk']} | {risk['probability']} | {risk['impact']} | {risk['mitigation']} |\n"
        
        return result
    
    def _format_dict_section(self, data: Optional[Dict]) -> str:
        """Format dictionary as markdown section"""
        if not data:
            return "Not specified"
        
        lines = []
        for key, value in data.items():
            formatted_key = key.replace('_', ' ').title()
            lines.append(f"- **{formatted_key}**: {value}")
        return "\n".join(lines)
    
    def _format_list(self, items: List[str]) -> str:
        """Format list as markdown bullets"""
        if not items:
            return "- None specified"
        return "\n".join(f"- {item}" for item in items)
    
    def _generate_test_procedure(self, interface: Interface) -> str:
        """Generate test procedure outline"""
        proc = []
        proc.append("1. **Pre-Test Setup**")
        proc.append("   - Verify all components installed correctly")
        proc.append("   - Check electrical connections and continuity")
        proc.append("   - Calibrate test equipment")
        proc.append("   - Document baseline conditions")
        proc.append("")
        
        proc.append("2. **Baseline Measurements**")
        for req in interface.requirements:
            proc.append(f"   - Measure {req.parameter} using {req.verification_method}")
            proc.append(f"     * Expected: {req.nominal} {req.units} (±{((req.max_value-req.min_value)/2):.1f})")
        proc.append("")
        
        proc.append("3. **Functional Verification**")
        proc.append("   - Power on system incrementally")
        proc.append("   - Monitor all interface parameters")
        proc.append("   - Verify normal operation for 30 minutes")
        proc.append("   - Check for error conditions or alarms")
        proc.append("")
        
        proc.append("4. **Stress Testing**")
        proc.append("   - Gradually increase to maximum rated conditions")
        proc.append("   - Monitor for parameter drift or instability")
        proc.append("   - Verify parameters remain within specification")
        proc.append("   - Document any degradation or warnings")
        proc.append("")
        
        proc.append("5. **Acceptance Testing**")
        proc.append("   - Run full 4-hour endurance test")
        proc.append("   - Verify all requirements continuously met")
        proc.append("   - Document final measurements")
        proc.append("   - Generate acceptance report")
        
        return "\n".join(proc)
    
    def generate_all_icds(self, output_dir: str = "icds/generated"):
        """Generate all system ICDs"""
        os.makedirs(output_dir, exist_ok=True)
        
        print(f"Generating {len(SYSTEM_INTERFACES)} Interface Control Documents...")
        
        for interface in SYSTEM_INTERFACES:
            icd_content = self.generate_icd(interface)
            
            filename = f"{interface.icd_number}_{interface.name.replace(' ', '_').replace('-', '_')}.md"
            filepath = os.path.join(output_dir, filename)
            
            with open(filepath, 'w') as f:
                f.write(icd_content)
            
            print(f"✓ Generated {filename}")
        
        # Generate summary
        self._generate_summary(output_dir)
        print(f"\n✅ Generated {len(SYSTEM_INTERFACES)} ICDs in {output_dir}/")
    
    def _generate_summary(self, output_dir: str):
        """Generate ICD summary document"""
        summary = ["# Interface Control Document Summary\n"]
        summary.append(f"**Generated**: Current version")
        summary.append(f"**System**: Acoustic Manufacturing System L1")
        summary.append(f"**Total Interfaces**: {len(SYSTEM_INTERFACES)}\n")
        
        summary.append("## Interface Overview\n")
        summary.append("| ICD # | Interface | Criticality | Status | Types |")
        summary.append("|-------|-----------|-------------|--------|-------|")
        
        for interface in SYSTEM_INTERFACES:
            types = ", ".join([t.value for t in interface.interface_types])
            summary.append(
                f"| [{interface.icd_number}]({interface.icd_number}_{interface.name.replace(' ', '_').replace('-', '_')}.md) | "
                f"{interface.name} | {interface.criticality.value.upper()} | "
                f"{interface.status} | {types} |"
            )
        
        # Add component traceability
        summary.append("\n## Component-Interface Traceability\n")
        component_interfaces = {}
        
        for interface in SYSTEM_INTERFACES:
            for comp in interface.side_a_components + interface.side_b_components:
                if comp not in component_interfaces:
                    component_interfaces[comp] = []
                component_interfaces[comp].append(interface.icd_number)
        
        summary.append("| Component | Interfaces |")
        summary.append("|-----------|------------|")
        for comp, icds in sorted(component_interfaces.items()):
            summary.append(f"| {comp} | {', '.join(icds)} |")
        
        # Add interface matrix
        summary.append("\n## Interface Matrix\n")
        summary.append("```mermaid")
        summary.append("graph LR")
        
        # Create subsystem nodes
        subsystems = set()
        for interface in SYSTEM_INTERFACES:
            subsystems.add(interface.side_a_subsystem)
            subsystems.add(interface.side_b_subsystem)
        
        # Add connections
        for interface in SYSTEM_INTERFACES:
            side_a = interface.side_a_subsystem.replace(' ', '_')
            side_b = interface.side_b_subsystem.replace(' ', '_')
            summary.append(f"    {side_a} ---|{interface.icd_number}| {side_b}")
        
        summary.append("```")
        
        summary_path = os.path.join(output_dir, "ICD_Summary.md")
        with open(summary_path, 'w') as f:
            f.write("\n".join(summary))
        
        print(f"✓ Generated ICD_Summary.md")

if __name__ == "__main__":
    generator = ICDGenerator()
    generator.generate_all_icds()