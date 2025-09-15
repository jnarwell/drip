"""
Integration module to connect test management system with component registry
"""
import sys
from pathlib import Path
from typing import Dict, List, Optional

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

# Placeholder imports until component registry is properly integrated
class ComponentRegistry:
    pass

class Component:
    pass
from test_management.verification_logic import VerificationEngine
from test_management.data_models import ComponentVerification, VerificationStatus

class ComponentRegistryIntegration:
    """Integrates test management with existing component registry"""
    
    def __init__(self, verification_engine: VerificationEngine):
        self.verification_engine = verification_engine
        self.component_registry = ComponentRegistry()
        
        # Sync components
        self._sync_components()
    
    def _sync_components(self):
        """Synchronize component registry with verification system"""
        # Get all components from registry
        all_components = []
        
        # Update verification engine with actual component data
        for component in all_components:
            # Convert component name to ID format used in verification system
            comp_id = component.name.replace(" ", "_").upper()
            
            if comp_id in self.verification_engine.component_verifications:
                # Update with actual part number and details
                verification = self.verification_engine.component_verifications[comp_id]
                verification.part_number = component.part_number
                
                # Add any missing components to verification system
            else:
                # Create new verification entry for components not in test mapping
                verification = ComponentVerification(
                    component_id=comp_id,
                    component_name=component.name,
                    part_number=component.part_number,
                    verification_status=VerificationStatus.NOT_APPLICABLE,
                    required_tests=[],  # Will be populated if tests are defined
                    notes=f"Component from registry, category: {component.category.value}"
                )
                self.verification_engine.component_verifications[comp_id] = verification
        
        # Save updated state
        self.verification_engine.save_state()
    
    def get_component_details(self, component_name: str) -> Optional[Component]:
        """Get detailed component information from registry"""
        return self.component_registry.search_by_name(component_name)
    
    def get_components_by_subsystem(self, subsystem: str) -> List[any]:
        """Get all components in a subsystem"""
        # Map subsystem names to component categories
        category_mapping = {
            "Acoustic": "ACOUSTIC",
            "Thermal": "HEATED_BED",
            "Crucible": "CRUCIBLE",
            "Power": "POWER_CONTROL",
            "Control": "POWER_CONTROL",
            "Chamber": "FRAME",
            "Frame": "FRAME"
        }
        
        category_name = category_mapping.get(subsystem)
        if category_name:
            return self.component_registry.get_by_category(category_name)
        return []
    
    def update_component_cost_impact(self, component_name: str, test_failures: List[str]) -> Dict[str, float]:
        """Calculate cost impact of component failure"""
        component = self.get_component_details(component_name)
        if not component:
            return {}
        
        impact = {
            "component_cost": component.cost,
            "potential_rework_cost": component.cost * 0.5,  # Estimate 50% for rework
            "schedule_impact_days": len(test_failures) * 2,  # 2 days per failed test
            "total_impact": component.cost * 1.5
        }
        
        # Factor in dependencies
        if component.dependencies:
            dependency_cost = sum(
                self.component_registry.search_by_name(dep).cost 
                for dep in component.dependencies 
                if self.component_registry.search_by_name(dep)
            )
            impact["dependency_impact"] = dependency_cost
            impact["total_impact"] += dependency_cost * 0.2  # 20% risk factor
        
        return impact
    
    def generate_bom_verification_report(self) -> Dict[str, any]:
        """Generate a BOM with verification status"""
        report = {
            "total_components": 0,
            "verified_components": 0,
            "total_cost": 0.0,
            "verified_cost": 0.0,
            "subsystems": {}
        }
        
        # Process each category
        for category in ["FRAME", "HEATED_BED", "ACOUSTIC", "CRUCIBLE", "POWER_CONTROL"]:
            components = self.component_registry.get_by_category(category)
            
            subsystem_data = {
                "components": [],
                "total_cost": 0.0,
                "verified_cost": 0.0,
                "verification_percentage": 0.0
            }
            
            for component in components:
                comp_id = component.name.replace(" ", "_").upper()
                verification = self.verification_engine.component_verifications.get(comp_id)
                
                comp_data = {
                    "name": component.name,
                    "part_number": component.part_number,
                    "cost": component.cost,
                    "quantity": component.quantity,
                    "total_cost": component.cost * component.quantity,
                    "verification_status": "NOT_TRACKED",
                    "test_progress": "N/A"
                }
                
                if verification:
                    comp_data["verification_status"] = verification.verification_status.value
                    comp_data["test_progress"] = f"{len(verification.completed_tests)}/{len(verification.required_tests)}"
                    
                    if verification.verification_status == VerificationStatus.VERIFIED:
                        subsystem_data["verified_cost"] += comp_data["total_cost"]
                
                subsystem_data["components"].append(comp_data)
                subsystem_data["total_cost"] += comp_data["total_cost"]
            
            if subsystem_data["total_cost"] > 0:
                subsystem_data["verification_percentage"] = (
                    subsystem_data["verified_cost"] / subsystem_data["total_cost"] * 100
                )
            
            report["subsystems"][category] = subsystem_data
            report["total_components"] += len(components)
            report["total_cost"] += subsystem_data["total_cost"]
            report["verified_cost"] += subsystem_data["verified_cost"]
        
        if report["total_cost"] > 0:
            report["overall_verification_percentage"] = (
                report["verified_cost"] / report["total_cost"] * 100
            )
        else:
            report["overall_verification_percentage"] = 0.0
        
        return report
    
    def check_component_specifications(self, component_name: str, test_results: Dict[str, any]) -> Dict[str, bool]:
        """Check if test results meet component specifications"""
        component = self.get_component_details(component_name)
        if not component or not component.tech_specs:
            return {"specifications_available": False}
        
        specs = component.tech_specs
        compliance = {"specifications_available": True}
        
        # Check operating temperature
        if specs.operating_temp and "temperature" in test_results:
            temp = test_results["temperature"]
            compliance["temperature_in_range"] = (
                specs.operating_temp[0] <= temp <= specs.operating_temp[1]
            )
        
        # Check power consumption
        if specs.power_consumption and "power_measured" in test_results:
            power = test_results["power_measured"]
            compliance["power_within_spec"] = (
                power <= specs.power_consumption * 1.1  # 10% tolerance
            )
        
        # Check frequency (for acoustic components)
        if specs.frequency and "frequency_measured" in test_results:
            freq = test_results["frequency_measured"]
            compliance["frequency_within_spec"] = (
                abs(freq - specs.frequency) <= 100  # ±100Hz tolerance
            )
        
        # Check efficiency
        if specs.efficiency and "efficiency_measured" in test_results:
            eff = test_results["efficiency_measured"]
            compliance["efficiency_meets_spec"] = (
                eff >= specs.efficiency * 0.95  # 5% tolerance
            )
        
        return compliance
    
    def get_critical_components(self) -> List[Dict[str, any]]:
        """Get components critical to system operation"""
        critical_components = []
        
        # Define critical component criteria
        critical_names = [
            "40kHz Transducers",
            "Phase Array Controller",
            "Thermal Cameras",
            "Mean Well RSP-10000-48",
            "STM32F7 Controllers",
            "Graphite Crucibles",
            "Induction Heater Module"
        ]
        
        for name in critical_names:
            component = self.component_registry.search_by_name(name)
            if component:
                comp_id = name.replace(" ", "_").upper()
                verification = self.verification_engine.component_verifications.get(comp_id)
                
                critical_components.append({
                    "name": component.name,
                    "part_number": component.part_number,
                    "cost": component.cost,
                    "quantity": component.quantity,
                    "lead_time_weeks": component.lead_time_weeks,
                    "verification_status": verification.verification_status.value if verification else "NOT_TRACKED",
                    "risk_level": self._assess_risk_level(component, verification)
                })
        
        return sorted(critical_components, key=lambda x: x["risk_level"], reverse=True)
    
    def _assess_risk_level(self, component: Component, verification: Optional[ComponentVerification]) -> str:
        """Assess risk level for a component"""
        risk_score = 0
        
        # Lead time risk
        if component.lead_time_weeks > 8:
            risk_score += 3
        elif component.lead_time_weeks > 4:
            risk_score += 2
        elif component.lead_time_weeks > 2:
            risk_score += 1
        
        # Cost risk
        if component.cost > 1000:
            risk_score += 2
        elif component.cost > 500:
            risk_score += 1
        
        # Verification risk
        if verification:
            if verification.verification_status == VerificationStatus.FAILED:
                risk_score += 5
            elif verification.verification_status == VerificationStatus.NOT_TESTED:
                risk_score += 3
            elif verification.verification_status == VerificationStatus.IN_TESTING:
                risk_score += 1
        else:
            risk_score += 2  # Not tracked
        
        # Map score to risk level
        if risk_score >= 7:
            return "HIGH"
        elif risk_score >= 4:
            return "MEDIUM"
        else:
            return "LOW"