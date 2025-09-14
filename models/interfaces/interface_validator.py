"""
Interface Validator - Validates interfaces against component specifications
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from typing import List, Dict, Tuple
from datetime import datetime
from models.component_registry import ComponentRegistry
from models.interfaces.interface_registry import SYSTEM_INTERFACES, Interface, InterfaceType

class InterfaceValidator:
    """Validate interface compatibility and requirements"""
    
    def __init__(self):
        self.registry = ComponentRegistry()
        self.validation_results = []
    
    def validate_all_interfaces(self) -> Tuple[bool, List[Dict]]:
        """Validate all system interfaces"""
        all_valid = True
        results = []
        
        print(f"Validating {len(SYSTEM_INTERFACES)} system interfaces...")
        
        for interface in SYSTEM_INTERFACES:
            valid, issues = self.validate_interface(interface)
            if not valid:
                all_valid = False
            
            results.append({
                'icd': interface.icd_number,
                'name': interface.name,
                'valid': valid,
                'issues': issues,
                'warnings': self._generate_warnings(interface)
            })
            
            status = "✅ VALID" if valid else "❌ INVALID"
            print(f"  {interface.icd_number}: {status} ({len(issues)} issues)")
        
        return all_valid, results
    
    def validate_interface(self, interface: Interface) -> Tuple[bool, List[str]]:
        """Validate single interface"""
        issues = []
        
        # Check component existence
        missing_components = []
        for comp_name in interface.side_a_components + interface.side_b_components:
            if not self._component_exists(comp_name):
                missing_components.append(comp_name)
        
        if missing_components:
            issues.append(f"Components not found in registry: {', '.join(missing_components)}")
        
        # Validate thermal compatibility
        if InterfaceType.THERMAL in interface.interface_types:
            thermal_issues = self._validate_thermal_compatibility(interface)
            issues.extend(thermal_issues)
        
        # Validate power requirements
        power_issues = self._validate_power_requirements(interface)
        issues.extend(power_issues)
        
        # Validate mechanical constraints
        if InterfaceType.MECHANICAL in interface.interface_types:
            mech_issues = self._validate_mechanical_constraints(interface)
            issues.extend(mech_issues)
        
        # Validate electrical compatibility
        if InterfaceType.ELECTRICAL in interface.interface_types:
            electrical_issues = self._validate_electrical_compatibility(interface)
            issues.extend(electrical_issues)
        
        # Validate data interface requirements
        if InterfaceType.DATA in interface.interface_types:
            data_issues = self._validate_data_compatibility(interface)
            issues.extend(data_issues)
        
        # Validate acoustic compatibility
        if InterfaceType.ACOUSTIC in interface.interface_types:
            acoustic_issues = self._validate_acoustic_compatibility(interface)
            issues.extend(acoustic_issues)
        
        return len(issues) == 0, issues
    
    def _component_exists(self, name: str) -> bool:
        """Check if component exists in registry"""
        return any(c.name == name for c in self.registry.components)
    
    def _get_component(self, name: str):
        """Get component by name"""
        for c in self.registry.components:
            if c.name == name:
                return c
        return None
    
    def _validate_thermal_compatibility(self, interface: Interface) -> List[str]:
        """Validate thermal requirements"""
        issues = []
        
        # Get max temps for both sides
        side_a_temps = []
        side_b_temps = []
        
        for comp_name in interface.side_a_components:
            comp = self._get_component(comp_name)
            if comp and comp.tech_specs and comp.tech_specs.max_temp:
                side_a_temps.append((comp_name, comp.tech_specs.max_temp))
        
        for comp_name in interface.side_b_components:
            comp = self._get_component(comp_name)
            if comp and comp.tech_specs and comp.tech_specs.max_temp:
                side_b_temps.append((comp_name, comp.tech_specs.max_temp))
        
        # Check for extreme thermal mismatches
        if side_a_temps and side_b_temps:
            max_a = max(temp for _, temp in side_a_temps)
            max_b = max(temp for _, temp in side_b_temps)
            min_a = min(temp for _, temp in side_a_temps)
            min_b = min(temp for _, temp in side_b_temps)
            
            # Check if high-temp component interfaces with low-temp component
            if max_a > 500 and min_b < 100:
                issues.append(f"High-temp component ({max_a}°C) directly interfaces with low-temp component ({min_b}°C)")
            
            if max_b > 500 and min_a < 100:
                issues.append(f"High-temp component ({max_b}°C) directly interfaces with low-temp component ({min_a}°C)")
        
        # Check thermal dissipation requirements
        total_thermal_load = 0
        for comp_name in interface.side_a_components + interface.side_b_components:
            comp = self._get_component(comp_name)
            if comp and comp.tech_specs:
                if comp.tech_specs.thermal_dissipation:
                    total_thermal_load += comp.tech_specs.thermal_dissipation * (comp.quantity or 1)
                elif comp.tech_specs.power_consumption and comp.tech_specs.efficiency:
                    # Estimate thermal load from power and efficiency
                    power = comp.tech_specs.power_consumption * (comp.quantity or 1)
                    thermal_load = power * (1 - comp.tech_specs.efficiency / 100)
                    total_thermal_load += thermal_load
        
        if total_thermal_load > 1000:  # High thermal load
            cooling_components = 0
            for comp_name in interface.side_a_components + interface.side_b_components:
                comp = self._get_component(comp_name)
                if comp and comp.tech_specs and comp.tech_specs.cooling_required in ["forced air", "liquid"]:
                    cooling_components += 1
            
            if cooling_components == 0:
                issues.append(f"High thermal load ({total_thermal_load:.0f}W) but no active cooling specified")
        
        return issues
    
    def _validate_power_requirements(self, interface: Interface) -> List[str]:
        """Validate power requirements"""
        issues = []
        
        total_consumption = 0
        total_supply = 0
        
        for comp_name in interface.side_a_components + interface.side_b_components:
            comp = self._get_component(comp_name)
            if comp and comp.tech_specs:
                if comp.tech_specs.power_consumption:
                    total_consumption += comp.tech_specs.power_consumption * (comp.quantity or 1)
                if comp.tech_specs.power_supply:
                    total_supply += comp.tech_specs.power_supply * (comp.quantity or 1)
        
        # Check power balance
        if total_consumption > total_supply:
            deficit = total_consumption - total_supply
            issues.append(f"Power deficit: {total_consumption:.0f}W demanded vs {total_supply:.0f}W supplied (deficit: {deficit:.0f}W)")
        
        # Check against interface requirements
        for req in interface.requirements:
            if 'current' in req.parameter.lower():
                # Could add more sophisticated current validation here
                pass
            elif 'power' in req.parameter.lower():
                # Could validate against actual power calculations
                pass
        
        return issues
    
    def _validate_mechanical_constraints(self, interface: Interface) -> List[str]:
        """Validate mechanical constraints"""
        issues = []
        
        # Check mounting compatibility
        mounting_types = []
        weights = []
        
        for comp_name in interface.side_a_components + interface.side_b_components:
            comp = self._get_component(comp_name)
            if comp and comp.tech_specs:
                if comp.tech_specs.mounting_type:
                    mounting_types.append((comp_name, comp.tech_specs.mounting_type))
                if comp.tech_specs.weight:
                    weights.append(comp.tech_specs.weight * (comp.quantity or 1))
        
        # Check for mounting incompatibilities
        if len(set(mt[1] for mt in mounting_types)) > 2:
            issues.append("Multiple incompatible mounting types in same interface")
        
        # Check weight considerations
        total_weight = sum(weights)
        if total_weight > 50:  # Heavy interface
            vibration_sensitive = []
            for comp_name in interface.side_a_components + interface.side_b_components:
                comp = self._get_component(comp_name)
                if comp and comp.tech_specs and comp.tech_specs.accuracy:
                    vibration_sensitive.append(comp_name)
            
            if vibration_sensitive:
                issues.append(f"Heavy interface ({total_weight:.1f}kg) with vibration-sensitive components: {', '.join(vibration_sensitive)}")
        
        return issues
    
    def _validate_electrical_compatibility(self, interface: Interface) -> List[str]:
        """Validate electrical compatibility"""
        issues = []
        
        # Check voltage compatibility
        voltages = []
        currents = []
        
        for comp_name in interface.side_a_components + interface.side_b_components:
            comp = self._get_component(comp_name)
            if comp and comp.tech_specs:
                if comp.tech_specs.voltage_nominal:
                    voltages.append((comp_name, comp.tech_specs.voltage_nominal))
                if comp.tech_specs.current_draw:
                    currents.append(comp.tech_specs.current_draw * (comp.quantity or 1))
        
        # Check for voltage mismatches
        unique_voltages = list(set(v[1] for v in voltages))
        if len(unique_voltages) > 1:
            # Allow for compatible voltage levels (e.g., 48V and 24V from same supply)
            high_voltages = [v for v in unique_voltages if v > 24]
            low_voltages = [v for v in unique_voltages if v <= 24]
            
            if len(high_voltages) > 1 or len(low_voltages) > 1:
                issues.append(f"Incompatible voltage levels: {unique_voltages}")
        
        # Check current capacity
        total_current = sum(currents)
        if total_current > 100:  # High current interface
            issues.append(f"High current interface ({total_current:.1f}A) - verify wire gauge and connector ratings")
        
        return issues
    
    def _validate_data_compatibility(self, interface: Interface) -> List[str]:
        """Validate data interface compatibility"""
        issues = []
        
        data_rates = []
        
        # Check for data rate requirements vs capabilities
        for req in interface.requirements:
            if 'data rate' in req.parameter.lower():
                if req.nominal > 1000000:  # >1MHz
                    issues.append(f"High-speed data interface ({req.nominal/1e6:.1f}MHz) requires careful signal integrity design")
        
        return issues
    
    def _validate_acoustic_compatibility(self, interface: Interface) -> List[str]:
        """Validate acoustic compatibility"""
        issues = []
        
        # Check frequency matching
        frequencies = []
        for comp_name in interface.side_a_components + interface.side_b_components:
            comp = self._get_component(comp_name)
            if comp and comp.tech_specs and comp.tech_specs.frequency:
                frequencies.append((comp_name, comp.tech_specs.frequency))
        
        # Check for frequency mismatches
        if len(frequencies) > 1:
            base_freq = frequencies[0][1]
            for comp_name, freq in frequencies[1:]:
                if abs(freq - base_freq) > base_freq * 0.1:  # >10% difference
                    issues.append(f"Acoustic frequency mismatch: {comp_name} at {freq}Hz vs reference {base_freq}Hz")
        
        return issues
    
    def _generate_warnings(self, interface: Interface) -> List[str]:
        """Generate non-critical warnings"""
        warnings = []
        
        # Check for missing specifications
        for comp_name in interface.side_a_components + interface.side_b_components:
            comp = self._get_component(comp_name)
            if comp and comp.tech_specs:
                if InterfaceType.THERMAL in interface.interface_types and not comp.tech_specs.max_temp:
                    warnings.append(f"{comp_name}: Missing thermal specifications")
                
                if InterfaceType.ELECTRICAL in interface.interface_types and not comp.tech_specs.power_consumption:
                    warnings.append(f"{comp_name}: Missing power specifications")
        
        # Check interface requirement coverage
        if len(interface.requirements) < 2:
            warnings.append("Interface has few requirements - consider additional verification parameters")
        
        return warnings
    
    def generate_validation_report(self) -> str:
        """Generate validation report"""
        valid, results = self.validate_all_interfaces()
        
        report = ["# Interface Validation Report\n"]
        report.append(f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"**System**: Acoustic Manufacturing System L1")
        report.append(f"**Total Interfaces**: {len(SYSTEM_INTERFACES)}")
        report.append(f"**Overall Status**: {'✅ ALL VALID' if valid else '❌ ISSUES FOUND'}\n")
        
        # Summary statistics
        valid_count = sum(1 for r in results if r['valid'])
        issue_count = sum(len(r['issues']) for r in results)
        warning_count = sum(len(r['warnings']) for r in results)
        
        report.append("## Validation Summary\n")
        report.append(f"- Valid Interfaces: {valid_count}/{len(results)}")
        report.append(f"- Total Issues: {issue_count}")
        report.append(f"- Total Warnings: {warning_count}\n")
        
        # Interface status table
        report.append("## Interface Status\n")
        report.append("| ICD | Interface | Status | Issues | Warnings |")
        report.append("|-----|-----------|--------|--------|----------|")
        
        for result in results:
            status = "✅ Valid" if result['valid'] else "❌ Invalid"
            issues = len(result['issues'])
            warnings = len(result['warnings'])
            report.append(f"| {result['icd']} | {result['name']} | {status} | {issues} | {warnings} |")
        
        # Detailed issues
        report.append("\n## Detailed Issues\n")
        has_issues = False
        for result in results:
            if result['issues']:
                has_issues = True
                report.append(f"### {result['icd']}: {result['name']}")
                for issue in result['issues']:
                    report.append(f"- ❌ {issue}")
                report.append("")
        
        if not has_issues:
            report.append("No critical issues found.\n")
        
        # Warnings
        report.append("## Warnings\n")
        has_warnings = False
        for result in results:
            if result['warnings']:
                has_warnings = True
                report.append(f"### {result['icd']}: {result['name']}")
                for warning in result['warnings']:
                    report.append(f"- ⚠️ {warning}")
                report.append("")
        
        if not has_warnings:
            report.append("No warnings generated.\n")
        
        # Recommendations
        report.append("## Recommendations\n")
        if not valid:
            report.append("1. **Critical**: Resolve all interface compatibility issues before system integration")
            report.append("2. **High**: Update component specifications to fill missing data")
            report.append("3. **Medium**: Address warnings to improve system robustness")
        else:
            report.append("1. **Good**: All interfaces are compatible with current specifications")
            report.append("2. **Maintain**: Continue validation as components are updated")
            report.append("3. **Monitor**: Track any specification changes that affect interfaces")
        
        report.append("\n## Validation Methodology\n")
        report.append("This validation checks:")
        report.append("- Component existence in registry")
        report.append("- Thermal compatibility and cooling requirements")
        report.append("- Power supply vs demand balance")
        report.append("- Mechanical mounting and weight considerations")
        report.append("- Electrical voltage and current compatibility")
        report.append("- Data interface signal integrity requirements")
        report.append("- Acoustic frequency matching")
        
        return "\n".join(report)
    
    def validate_single_interface(self, icd_number: str) -> Dict:
        """Validate a single interface by ICD number"""
        for interface in SYSTEM_INTERFACES:
            if interface.icd_number == icd_number:
                valid, issues = self.validate_interface(interface)
                return {
                    'icd': interface.icd_number,
                    'name': interface.name,
                    'valid': valid,
                    'issues': issues,
                    'warnings': self._generate_warnings(interface)
                }
        return None

if __name__ == "__main__":
    validator = InterfaceValidator()
    report = validator.generate_validation_report()
    print(report)
    
    # Save report
    os.makedirs("icds/generated", exist_ok=True)
    with open("icds/generated/validation_report.md", "w") as f:
        f.write(report)
    print(f"\n✓ Validation report saved to icds/generated/validation_report.md")