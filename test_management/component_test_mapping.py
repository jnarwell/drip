"""
Component-Test Mapping System
Maps components to their required tests for verification
"""
from typing import Dict, List, Set
from .data_models import VerificationType

class ComponentTestMapper:
    def __init__(self):
        self.component_test_requirements = self._initialize_mappings()
    
    def _initialize_mappings(self):
        """Define which tests are required for each component"""
        return {
            # Acoustic Subsystem Components
            "40kHz Transducers": {
                "required_tests": ["TE-001", "TE-002", "TE-003", "TE-004"],
                "integration_tests": ["TE-005", "TE-006", "TE-008", "TE-013"],
                "optional_tests": ["TE-015", "TE-056", "TE-076", "TE-087"],
                "verification_criteria": "ALL_REQUIRED_PASS"
            },
            "6-Channel Amplifiers": {
                "required_tests": ["TE-007", "TE-009"],
                "integration_tests": ["TE-008", "TE-015"],
                "optional_tests": ["TE-079"],
                "verification_criteria": "ALL_REQUIRED_PASS"
            },
            "Transducer Array Layer": {
                "required_tests": [],
                "integration_tests": ["TE-005", "TE-006"],
                "optional_tests": [],
                "verification_criteria": "ALL_INTEGRATION_PASS"
            },
            "Acoustic Cylinder": {
                "required_tests": ["TE-010"],
                "integration_tests": ["TE-006", "TE-011"],
                "optional_tests": [],
                "verification_criteria": "ALL_REQUIRED_PASS"
            },
            "Phase Array Controller": {
                "required_tests": ["TE-012", "TE-063"],
                "integration_tests": ["TE-013", "TE-014", "TE-015", "TE-056", "TE-078"],
                "optional_tests": [],
                "verification_criteria": "ALL_REQUIRED_PASS"
            },
            
            # Thermal Subsystem Components
            "Thermal Cameras": {
                "required_tests": ["TE-016", "TE-017"],
                "integration_tests": ["TE-018", "TE-030", "TE-057", "TE-058", "TE-059", "TE-076"],
                "optional_tests": ["TE-093"],
                "verification_criteria": "ALL_REQUIRED_PASS"
            },
            "Thermocouples Type K": {
                "required_tests": ["TE-019"],
                "integration_tests": ["TE-021", "TE-058"],
                "optional_tests": [],
                "verification_criteria": "ALL_REQUIRED_PASS"
            },
            "RTD PT100 Sensors": {
                "required_tests": ["TE-020"],
                "integration_tests": ["TE-028", "TE-029"],
                "optional_tests": [],
                "verification_criteria": "ALL_REQUIRED_PASS"
            },
            "Heated Build Platform": {
                "required_tests": ["TE-021", "TE-022"],
                "integration_tests": ["TE-029"],
                "optional_tests": [],
                "verification_criteria": "ALL_REQUIRED_PASS"
            },
            "Silicon Heating Plates": {
                "required_tests": [],
                "integration_tests": ["TE-022"],
                "optional_tests": [],
                "verification_criteria": "ALL_INTEGRATION_PASS"
            },
            "Temperature Controllers": {
                "required_tests": ["TE-028"],
                "integration_tests": ["TE-021", "TE-029", "TE-030"],
                "optional_tests": [],
                "verification_criteria": "ALL_REQUIRED_PASS"
            },
            "Pyrometers": {
                "required_tests": ["TE-040"],
                "integration_tests": ["TE-083"],
                "optional_tests": [],
                "verification_criteria": "ALL_REQUIRED_PASS"
            },
            
            # Cooling System Components
            "Water Pumps": {
                "required_tests": ["TE-024"],
                "integration_tests": ["TE-023", "TE-025"],
                "optional_tests": ["TE-089"],
                "verification_criteria": "ALL_REQUIRED_PASS"
            },
            "Radiator Fans": {
                "required_tests": [],
                "integration_tests": ["TE-023"],
                "optional_tests": ["TE-089"],
                "verification_criteria": "ALL_INTEGRATION_PASS"
            },
            "Water Cooling Blocks": {
                "required_tests": ["TE-025"],
                "integration_tests": ["TE-023"],
                "optional_tests": [],
                "verification_criteria": "ALL_REQUIRED_PASS"
            },
            "Flow Regulators": {
                "required_tests": [],
                "integration_tests": ["TE-024"],
                "optional_tests": [],
                "verification_criteria": "ALL_INTEGRATION_PASS"
            },
            "Fittings 1/2 NPT to 3/8 Barb": {
                "required_tests": [],
                "integration_tests": ["TE-025"],
                "optional_tests": [],
                "verification_criteria": "ALL_INTEGRATION_PASS"
            },
            
            # Insulation Components
            "Ceramic Fiber Blanket": {
                "required_tests": ["TE-026", "TE-027"],
                "integration_tests": ["TE-074"],
                "optional_tests": [],
                "verification_criteria": "ALL_REQUIRED_PASS"
            },
            "Ceramic Insulation Plates": {
                "required_tests": ["TE-026", "TE-027"],
                "integration_tests": [],
                "optional_tests": [],
                "verification_criteria": "ALL_REQUIRED_PASS"
            },
            "Thermal Isolation Tube": {
                "required_tests": [],
                "integration_tests": ["TE-011"],
                "optional_tests": [],
                "verification_criteria": "ALL_INTEGRATION_PASS"
            },
            
            # Crucible Subsystem Components
            "Graphite Crucibles": {
                "required_tests": ["TE-031", "TE-038"],
                "integration_tests": ["TE-033", "TE-036", "TE-037", "TE-040"],
                "optional_tests": ["TE-088"],
                "verification_criteria": "ALL_REQUIRED_PASS"
            },
            "Induction Heater Module": {
                "required_tests": ["TE-031", "TE-032", "TE-039"],
                "integration_tests": ["TE-036", "TE-048", "TE-049"],
                "optional_tests": [],
                "verification_criteria": "ALL_REQUIRED_PASS"
            },
            "Induction Coils": {
                "required_tests": [],
                "integration_tests": ["TE-032", "TE-036"],
                "optional_tests": [],
                "verification_criteria": "ALL_INTEGRATION_PASS"
            },
            "Piezo Droplet Dispensers": {
                "required_tests": ["TE-034"],
                "integration_tests": ["TE-033", "TE-059"],
                "optional_tests": ["TE-091"],
                "verification_criteria": "ALL_REQUIRED_PASS"
            },
            "Piezo Drivers": {
                "required_tests": [],
                "integration_tests": ["TE-034"],
                "optional_tests": [],
                "verification_criteria": "ALL_INTEGRATION_PASS"
            },
            "Material Wire Feeders": {
                "required_tests": ["TE-035"],
                "integration_tests": ["TE-037"],
                "optional_tests": [],
                "verification_criteria": "ALL_REQUIRED_PASS"
            },
            "Linear Actuators": {
                "required_tests": [],
                "integration_tests": ["TE-035"],
                "optional_tests": ["TE-094"],
                "verification_criteria": "ALL_INTEGRATION_PASS"
            },
            "Magnetic Shielding": {
                "required_tests": [],
                "integration_tests": ["TE-039"],
                "optional_tests": [],
                "verification_criteria": "ALL_INTEGRATION_PASS"
            },
            
            # Power System Components
            "Mean Well RSP-10000-48": {
                "required_tests": ["TE-041", "TE-042"],
                "integration_tests": ["TE-048", "TE-049", "TE-079"],
                "optional_tests": ["TE-086"],
                "verification_criteria": "ALL_REQUIRED_PASS"
            },
            "DC-DC Converters 48V to 24V": {
                "required_tests": ["TE-043"],
                "integration_tests": [],
                "optional_tests": [],
                "verification_criteria": "ALL_REQUIRED_PASS"
            },
            "DC-DC Converters 48V to 12V": {
                "required_tests": ["TE-043"],
                "integration_tests": [],
                "optional_tests": [],
                "verification_criteria": "ALL_REQUIRED_PASS"
            },
            "UPS Battery Backup 3kVA": {
                "required_tests": ["TE-044"],
                "integration_tests": [],
                "optional_tests": [],
                "verification_criteria": "ALL_REQUIRED_PASS"
            },
            "Circuit Breakers 3-phase 100A": {
                "required_tests": ["TE-045"],
                "integration_tests": ["TE-046", "TE-047"],
                "optional_tests": [],
                "verification_criteria": "ALL_REQUIRED_PASS"
            },
            "Fuses 250V 10A": {
                "required_tests": [],
                "integration_tests": ["TE-045"],
                "optional_tests": [],
                "verification_criteria": "ALL_INTEGRATION_PASS"
            },
            "Emergency Stop System": {
                "required_tests": ["TE-046"],
                "integration_tests": ["TE-047", "TE-069", "TE-080"],
                "optional_tests": [],
                "verification_criteria": "ALL_REQUIRED_PASS"
            },
            "Power Cables AWG 2": {
                "required_tests": ["TE-050"],
                "integration_tests": [],
                "optional_tests": [],
                "verification_criteria": "ALL_REQUIRED_PASS"
            },
            "Anderson Connectors 175A": {
                "required_tests": [],
                "integration_tests": ["TE-050"],
                "optional_tests": [],
                "verification_criteria": "ALL_INTEGRATION_PASS"
            },
            
            # Sensor Components
            "Load Cells 50kg": {
                "required_tests": ["TE-051"],
                "integration_tests": ["TE-055", "TE-056"],
                "optional_tests": [],
                "verification_criteria": "ALL_REQUIRED_PASS"
            },
            "Accelerometers 3-axis": {
                "required_tests": ["TE-052"],
                "integration_tests": ["TE-055"],
                "optional_tests": [],
                "verification_criteria": "ALL_REQUIRED_PASS"
            },
            "Humidity Sensors": {
                "required_tests": ["TE-053"],
                "integration_tests": ["TE-055"],
                "optional_tests": [],
                "verification_criteria": "ALL_REQUIRED_PASS"
            },
            "Gas Flow Sensors": {
                "required_tests": ["TE-054"],
                "integration_tests": ["TE-055", "TE-075"],
                "optional_tests": [],
                "verification_criteria": "ALL_REQUIRED_PASS"
            },
            
            # Control System Components
            "STM32F7 Controllers": {
                "required_tests": ["TE-061"],
                "integration_tests": ["TE-065", "TE-070"],
                "optional_tests": [],
                "verification_criteria": "ALL_REQUIRED_PASS"
            },
            "Raspberry Pi 4 8GB": {
                "required_tests": ["TE-062"],
                "integration_tests": ["TE-070"],
                "optional_tests": [],
                "verification_criteria": "ALL_REQUIRED_PASS"
            },
            "Control System": {
                "required_tests": ["TE-065", "TE-066", "TE-068", "TE-069"],
                "integration_tests": ["TE-013", "TE-014", "TE-018", "TE-030", "TE-055", 
                                    "TE-057", "TE-060", "TE-064", "TE-067", "TE-070", 
                                    "TE-076", "TE-077", "TE-078"],
                "optional_tests": ["TE-090"],
                "verification_criteria": "ALL_REQUIRED_PASS"
            },
            "Ethernet Switches": {
                "required_tests": [],
                "integration_tests": ["TE-064"],
                "optional_tests": [],
                "verification_criteria": "ALL_INTEGRATION_PASS"
            },
            "HMI Touch Screen 15 inch": {
                "required_tests": ["TE-067"],
                "integration_tests": ["TE-098"],
                "optional_tests": [],
                "verification_criteria": "ALL_REQUIRED_PASS"
            },
            "SSD 1TB Industrial": {
                "required_tests": [],
                "integration_tests": ["TE-068"],
                "optional_tests": [],
                "verification_criteria": "ALL_INTEGRATION_PASS"
            },
            
            # Chamber Components
            "Aluminum Chamber Walls": {
                "required_tests": ["TE-071"],
                "integration_tests": ["TE-074"],
                "optional_tests": [],
                "verification_criteria": "ALL_REQUIRED_PASS"
            },
            "Chamber Door Seals": {
                "required_tests": [],
                "integration_tests": ["TE-071"],
                "optional_tests": [],
                "verification_criteria": "ALL_INTEGRATION_PASS"
            },
            "HEPA Filters MERV 13": {
                "required_tests": ["TE-072"],
                "integration_tests": ["TE-073"],
                "optional_tests": ["TE-092"],
                "verification_criteria": "ALL_REQUIRED_PASS"
            },
            "Exhaust Blowers": {
                "required_tests": ["TE-073"],
                "integration_tests": [],
                "optional_tests": [],
                "verification_criteria": "ALL_REQUIRED_PASS"
            },
            "Dampers Motorized": {
                "required_tests": [],
                "integration_tests": ["TE-073"],
                "optional_tests": ["TE-094"],
                "verification_criteria": "ALL_INTEGRATION_PASS"
            },
            "Gas Manifolds": {
                "required_tests": [],
                "integration_tests": ["TE-075"],
                "optional_tests": [],
                "verification_criteria": "ALL_INTEGRATION_PASS"
            }
        }
    
    def get_required_tests(self, component_name: str) -> List[str]:
        """Get list of required tests for a component"""
        if component_name in self.component_test_requirements:
            return self.component_test_requirements[component_name]["required_tests"]
        return []
    
    def get_all_tests_for_component(self, component_name: str) -> Dict[str, List[str]]:
        """Get all test categories for a component"""
        if component_name in self.component_test_requirements:
            return {
                "required": self.component_test_requirements[component_name]["required_tests"],
                "integration": self.component_test_requirements[component_name]["integration_tests"],
                "optional": self.component_test_requirements[component_name]["optional_tests"]
            }
        return {"required": [], "integration": [], "optional": []}
    
    def get_components_for_test(self, test_id: str) -> List[str]:
        """Get all components that require a specific test"""
        components = []
        for component, requirements in self.component_test_requirements.items():
            all_tests = (requirements["required_tests"] + 
                        requirements["integration_tests"] + 
                        requirements["optional_tests"])
            if test_id in all_tests:
                components.append(component)
        return components
    
    def get_verification_criteria(self, component_name: str) -> str:
        """Get verification criteria for a component"""
        if component_name in self.component_test_requirements:
            return self.component_test_requirements[component_name]["verification_criteria"]
        return "UNDEFINED"
    
    def get_critical_path_components(self) -> List[str]:
        """Get components on the critical verification path"""
        # These are components that block system-level testing
        critical_components = [
            "40kHz Transducers",
            "Phase Array Controller", 
            "Thermal Cameras",
            "Control System",
            "Mean Well RSP-10000-48",
            "Graphite Crucibles",
            "Piezo Droplet Dispensers"
        ]
        return critical_components
    
    def calculate_component_test_coverage(self, component_name: str, 
                                        completed_tests: List[str]) -> Dict[str, float]:
        """Calculate test coverage percentages for a component"""
        tests = self.get_all_tests_for_component(component_name)
        
        coverage = {}
        for category, test_list in tests.items():
            if test_list:
                completed = len([t for t in test_list if t in completed_tests])
                coverage[category] = (completed / len(test_list)) * 100
            else:
                coverage[category] = 100.0  # No tests required
        
        # Calculate overall coverage based on required + integration
        total_tests = len(tests["required"]) + len(tests["integration"])
        if total_tests > 0:
            completed_total = len([t for t in tests["required"] + tests["integration"] 
                                 if t in completed_tests])
            coverage["overall"] = (completed_total / total_tests) * 100
        else:
            coverage["overall"] = 100.0
            
        return coverage
    
    def get_subsystem_components(self) -> Dict[str, List[str]]:
        """Group components by subsystem"""
        return {
            "Acoustic": [
                "40kHz Transducers", "6-Channel Amplifiers", "Transducer Array Layer",
                "Acoustic Cylinder", "Phase Array Controller"
            ],
            "Thermal": [
                "Thermal Cameras", "Thermocouples Type K", "RTD PT100 Sensors",
                "Heated Build Platform", "Silicon Heating Plates", "Temperature Controllers",
                "Pyrometers"
            ],
            "Cooling": [
                "Water Pumps", "Radiator Fans", "Water Cooling Blocks", 
                "Flow Regulators", "Fittings 1/2 NPT to 3/8 Barb"
            ],
            "Insulation": [
                "Ceramic Fiber Blanket", "Ceramic Insulation Plates", "Thermal Isolation Tube"
            ],
            "Crucible": [
                "Graphite Crucibles", "Induction Heater Module", "Induction Coils",
                "Piezo Droplet Dispensers", "Piezo Drivers", "Material Wire Feeders",
                "Linear Actuators", "Magnetic Shielding"
            ],
            "Power": [
                "Mean Well RSP-10000-48", "DC-DC Converters 48V to 24V", 
                "DC-DC Converters 48V to 12V", "UPS Battery Backup 3kVA",
                "Circuit Breakers 3-phase 100A", "Fuses 250V 10A", "Emergency Stop System",
                "Power Cables AWG 2", "Anderson Connectors 175A"
            ],
            "Sensors": [
                "Load Cells 50kg", "Accelerometers 3-axis", "Humidity Sensors",
                "Gas Flow Sensors"
            ],
            "Control": [
                "STM32F7 Controllers", "Raspberry Pi 4 8GB", "Control System",
                "Ethernet Switches", "HMI Touch Screen 15 inch", "SSD 1TB Industrial"
            ],
            "Chamber": [
                "Aluminum Chamber Walls", "Chamber Door Seals", "HEPA Filters MERV 13",
                "Exhaust Blowers", "Dampers Motorized", "Gas Manifolds"
            ]
        }
    
    def export_mapping_matrix(self) -> Dict[str, Dict[str, List[str]]]:
        """Export the complete mapping matrix"""
        return self.component_test_requirements