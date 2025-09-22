"""Calculate accurate test counts per subsystem without double counting"""

from typing import Dict, Set, Tuple
from test_management.test_registry import TestRegistry
from test_management.component_test_mapping import ComponentTestMapper
from test_management.system_test_mapping import SystemTestMapper


class TestCountCalculator:
    """Calculates accurate test counts per subsystem"""
    
    def __init__(self):
        self.registry = TestRegistry()
        self.component_mapper = ComponentTestMapper()
        self.system_mapper = SystemTestMapper()
        
        # Define test ranges for each major category
        self.test_ranges = {
            "Acoustic": list(f"TE-{i:03d}" for i in range(1, 16)),      # TE-001 to TE-015
            "Thermal": list(f"TE-{i:03d}" for i in range(16, 31)),      # TE-016 to TE-030
            "Crucible": list(f"TE-{i:03d}" for i in range(31, 41)),     # TE-031 to TE-040
            "Power": list(f"TE-{i:03d}" for i in range(41, 51)),        # TE-041 to TE-050
            "Sensors": list(f"TE-{i:03d}" for i in range(51, 61)),      # TE-051 to TE-060
            "Control": list(f"TE-{i:03d}" for i in range(61, 71)),      # TE-061 to TE-070
            "Chamber": list(f"TE-{i:03d}" for i in range(71, 76)),      # TE-071 to TE-075
            "Integration": list(f"TE-{i:03d}" for i in range(76, 81)),  # TE-076 to TE-080
            "Performance": list(f"TE-{i:03d}" for i in range(81, 86)),  # TE-081 to TE-085
            "Endurance": list(f"TE-{i:03d}" for i in range(86, 96)),    # TE-086 to TE-095
            "Validation": list(f"TE-{i:03d}" for i in range(96, 101))   # TE-096 to TE-100
        }
        
        # Some subsystems don't have dedicated test ranges (use component mapping)
        self.derived_subsystems = {
            "Cooling": [],  # Will be calculated from component tests
            "Insulation": []  # Will be calculated from component tests
        }
    
    def get_subsystem_test_counts(self) -> Dict[str, int]:
        """Get accurate test count for each subsystem"""
        counts = {}
        
        # First, add the major test categories
        for subsystem, test_ids in self.test_ranges.items():
            # Filter to only include tests that actually exist
            valid_tests = [tid for tid in test_ids if tid in self.registry.tests]
            counts[subsystem] = len(valid_tests)
        
        # Cooling and Insulation tests are already counted within other categories
        # TE-023, TE-024, TE-025 are part of Thermal (TE-016 to TE-030)
        # TE-026, TE-027 are part of Thermal (TE-016 to TE-030)
        # So we don't add them separately to avoid double counting
        
        # Remove these subsystems from the count to avoid duplication
        # counts["Cooling"] = 0  # Tests counted in Thermal
        # counts["Insulation"] = 0  # Tests counted in Thermal
        
        return counts
    
    def get_display_names(self) -> Dict[str, str]:
        """Map internal names to display names"""
        return {
            "Acoustic": "Acoustic Array",
            "Thermal": "Thermal System",
            "Crucible": "Material Feed",
            "Power": "Power System",
            "Sensors": "Sensors",
            "Control": "Control System",
            "Chamber": "Chamber",
            "Integration": "Integration",
            "Performance": "Performance",
            "Endurance": "Endurance",
            "Validation": "Validation"
        }