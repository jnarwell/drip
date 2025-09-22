"""System Test Mapping - Maps system-level tests not directly tied to individual components"""

from typing import Dict, List, Set
from dataclasses import dataclass

@dataclass
class SystemTestCategory:
    """Represents a category of system-level tests"""
    category_name: str
    test_ids: List[str]
    description: str
    
class SystemTestMapper:
    """Maps system-level tests to categories and provides lookup functions"""
    
    def __init__(self):
        self.system_test_categories = {
            # Acoustic subsystem tests not mapped to specific components
            "Acoustic_System": SystemTestCategory(
                category_name="Acoustic System Tests",
                test_ids=["TE-005", "TE-006", "TE-013", "TE-014", "TE-015"],
                description="System-level acoustic array and field tests"
            ),
            
            # Thermal subsystem tests not mapped to specific components  
            "Thermal_System": SystemTestCategory(
                category_name="Thermal System Tests",
                test_ids=["TE-021", "TE-022", "TE-028", "TE-029", "TE-030"],
                description="System-level thermal control and regulation tests"
            ),
            
            # Cooling subsystem tests
            "Cooling_System": SystemTestCategory(
                category_name="Cooling System Tests",
                test_ids=["TE-023", "TE-024", "TE-025"],
                description="System-level cooling performance tests"
            ),
            
            # Insulation tests
            "Insulation_System": SystemTestCategory(
                category_name="Insulation System Tests",
                test_ids=["TE-026", "TE-027"],
                description="Thermal insulation performance tests"
            ),
            
            # Material feed system tests
            "Material_Feed_System": SystemTestCategory(
                category_name="Material Feed System Tests",
                test_ids=["TE-033", "TE-035", "TE-037", "TE-040"],
                description="Droplet generation and material handling tests"
            ),
            
            # Power system tests not mapped to specific components
            "Power_System": SystemTestCategory(
                category_name="Power System Tests",
                test_ids=["TE-045", "TE-048", "TE-049", "TE-050"],
                description="Power distribution and quality tests"
            ),
            
            # Sensor system tests
            "Sensor_System": SystemTestCategory(
                category_name="Sensor System Tests",
                test_ids=["TE-055", "TE-056", "TE-057", "TE-058", "TE-059", "TE-060"],
                description="Sensor integration and data acquisition tests"
            ),
            
            # Control system tests
            "Control_System": SystemTestCategory(
                category_name="Control System Tests",
                test_ids=["TE-064", "TE-065", "TE-066", "TE-067", "TE-068", "TE-069", "TE-070"],
                description="System control, HMI, and software tests"
            ),
            
            # Chamber/Environmental tests
            "Chamber_System": SystemTestCategory(
                category_name="Chamber System Tests",
                test_ids=["TE-071", "TE-072", "TE-073", "TE-074", "TE-075"],
                description="Chamber environment and safety tests"
            ),
            
            # Integration tests
            "Integration": SystemTestCategory(
                category_name="Integration Tests",
                test_ids=["TE-076", "TE-077", "TE-078", "TE-079", "TE-080"],
                description="Multi-subsystem integration tests"
            ),
            
            # Performance tests
            "Performance": SystemTestCategory(
                category_name="Performance Tests",
                test_ids=["TE-081", "TE-082", "TE-083", "TE-084", "TE-085"],
                description="System performance validation tests"
            ),
            
            # Endurance tests
            "Endurance": SystemTestCategory(
                category_name="Endurance Tests",
                test_ids=["TE-086", "TE-087", "TE-088", "TE-089", "TE-090", 
                          "TE-091", "TE-092", "TE-093", "TE-094", "TE-095"],
                description="Long-duration reliability tests"
            ),
            
            # Validation tests
            "Validation": SystemTestCategory(
                category_name="Validation Tests",
                test_ids=["TE-096", "TE-097", "TE-098", "TE-099", "TE-100"],
                description="Final system acceptance tests"
            )
        }
        
        # Build reverse mapping for quick lookups
        self.test_to_category = {}
        for cat_key, category in self.system_test_categories.items():
            for test_id in category.test_ids:
                self.test_to_category[test_id] = cat_key
    
    def get_category_for_test(self, test_id: str) -> str:
        """Get the category name for a given test ID"""
        return self.test_to_category.get(test_id, "Unknown")
    
    def get_tests_for_category(self, category: str) -> List[str]:
        """Get all test IDs for a given category"""
        if category in self.system_test_categories:
            return self.system_test_categories[category].test_ids
        return []
    
    def get_all_system_tests(self) -> Set[str]:
        """Get all system-level test IDs"""
        all_tests = set()
        for category in self.system_test_categories.values():
            all_tests.update(category.test_ids)
        return all_tests
    
    def get_system_test_stats(self) -> Dict[str, Dict]:
        """Get test statistics for system-level test categories only"""
        stats = {}
        
        # Only return the truly system-level categories (not subsystem-specific)
        system_level_categories = {
            "Integration": ["Integration"],
            "Performance": ["Performance"],
            "Endurance": ["Endurance"],
            "Validation": ["Validation"]
        }
        
        for display_name, categories in system_level_categories.items():
            total_tests = 0
            test_ids = []
            
            for cat in categories:
                if cat in self.system_test_categories:
                    cat_tests = self.system_test_categories[cat].test_ids
                    total_tests += len(cat_tests)
                    test_ids.extend(cat_tests)
            
            stats[display_name] = {
                'total_tests': total_tests,
                'test_ids': test_ids,
                'completed_tests': 0,  # Will be updated by verification engine
                'completion_percentage': 0
            }
        
        return stats
    
    def get_unmapped_subsystem_tests(self) -> Dict[str, int]:
        """Get count of tests not mapped to components for each subsystem"""
        # These are tests that belong to subsystems but aren't mapped to specific components
        unmapped = {
            "Acoustic Array": 5,  # TE-005, TE-006, TE-013, TE-014, TE-015
            "Thermal System": 5,  # TE-021, TE-022, TE-028, TE-029, TE-030
            "Cooling": 3,         # TE-023, TE-024, TE-025  
            "Insulation": 2,      # TE-026, TE-027
            "Material Feed": 4,   # TE-033, TE-035, TE-037, TE-040
            "Power System": 4,    # TE-045, TE-048, TE-049, TE-050
            "Sensors": 6,         # TE-055 to TE-060
            "Control System": 7,  # TE-064 to TE-070
            "Chamber": 5          # TE-071 to TE-075
        }
        return unmapped
    
    def get_test_coverage_summary(self) -> Dict[str, int]:
        """Get a summary of test coverage by category type"""
        summary = {
            'component_tests': 0,
            'system_tests': 0,
            'integration_tests': len(self.system_test_categories['Integration'].test_ids),
            'performance_tests': len(self.system_test_categories['Performance'].test_ids),
            'endurance_tests': len(self.system_test_categories['Endurance'].test_ids),
            'validation_tests': len(self.system_test_categories['Validation'].test_ids)
        }
        
        # Count component vs system tests
        for cat_key, category in self.system_test_categories.items():
            if cat_key not in ['Integration', 'Performance', 'Endurance', 'Validation']:
                summary['system_tests'] += len(category.test_ids)
        
        return summary