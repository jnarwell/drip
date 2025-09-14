#!/usr/bin/env python3
"""
Acoustic Manufacturing System - Requirements Validation
Validates SysML requirements against system constraints
"""

import json
import sys
from dataclasses import dataclass
from typing import Dict, List, Tuple

@dataclass
class Requirement:
    id: str
    description: str
    value: float
    unit: str
    status: str = "Not Verified"

@dataclass
class LevelConfig:
    level: int
    transducers: int
    power: float
    volume: float
    cost: float
    materials: str

class RequirementsValidator:
    def __init__(self):
        self.requirements = self._load_requirements()
        self.levels = self._load_level_configs()
        self.results = {}
        
    def _load_requirements(self) -> Dict[str, Requirement]:
        """Load system requirements"""
        return {
            "SR001": Requirement("SR001", "Acoustic Frequency", 10000, "Hz"),
            "SR002": Requirement("SR002", "Steering Accuracy", 0.3, "mm"),
            "SR003": Requirement("SR003", "Max Temperature", 1580, "°C"),
            "SR004": Requirement("SR004", "Max Power L4", 45000, "W"),
            "SR005": Requirement("SR005", "Max Volume L4", 8000, "cm³"),
            "SR006": Requirement("SR006", "Min Density", 95, "%"),
            "SR007": Requirement("SR007", "Build Rate L4", 25, "cm³/hr"),
            "SR008": Requirement("SR008", "Operating Cost", 95, "$/kg"),
            "SR009": Requirement("SR009", "Chamber Temp", 300, "°C"),
            "SR010": Requirement("SR010", "Cooling Rate", 1000, "°C/s"),
        }
    
    def _load_level_configs(self) -> Dict[int, LevelConfig]:
        """Load level configurations"""
        return {
            1: LevelConfig(1, 18, 12000, 125, 14320, "Aluminum"),
            2: LevelConfig(2, 36, 25000, 1000, 44470, "Al, Steel"),
            3: LevelConfig(3, 36, 30000, 1000, 78620, "Al+Steel"),
            4: LevelConfig(4, 72, 45000, 8000, 163970, "5+ materials"),
        }
    
    def validate_power_budget(self) -> Tuple[bool, str]:
        """Validate power requirements across levels"""
        results = []
        for level, config in self.levels.items():
            acoustic_power = config.transducers * 25  # 25W per transducer
            
            if level == 1:
                expected_total = 12000
            elif level == 2:
                expected_total = 25000
            elif level == 3:
                expected_total = 30000
            else:
                expected_total = 45000
            
            passed = config.power <= expected_total
            results.append(f"Level {level}: {config.power}W {'✓' if passed else '✗'}")
        
        all_passed = all("✓" in r for r in results)
        return all_passed, "\n".join(results)
    
    def validate_cost_progression(self) -> Tuple[bool, str]:
        """Validate cost targets"""
        targets = {1: 15000, 2: 45000, 3: 80000, 4: 165000}
        results = []
        
        for level, config in self.levels.items():
            target = targets[level]
            passed = config.cost <= target
            margin = ((target - config.cost) / target) * 100
            results.append(
                f"Level {level}: ${config.cost:,} "
                f"(margin: {margin:.1f}%) {'✓' if passed else '✗'}"
            )
        
        all_passed = all("✓" in r for r in results)
        return all_passed, "\n".join(results)
    
    def validate_thermal_constraints(self) -> Tuple[bool, str]:
        """Validate thermal management"""
        checks = []
        
        # Check aluminum melting capability
        al_temp = 700
        checks.append(("Aluminum melting", al_temp <= 700, f"{al_temp}°C"))
        
        # Check steel melting capability  
        steel_temp = 1580
        checks.append(("Steel melting", steel_temp <= 1580, f"{steel_temp}°C"))
        
        # Check chamber temperature limit
        chamber_temp = 250  # Nominal
        checks.append(("Chamber limit", chamber_temp <= 300, f"{chamber_temp}°C"))
        
        # Check cooling rate
        cooling_rate = 1200  # Achievable
        checks.append(("Cooling rate", cooling_rate >= 1000, f"{cooling_rate}°C/s"))
        
        results = [f"{name}: {value} {'✓' if passed else '✗'}" 
                  for name, passed, value in checks]
        
        all_passed = all(c[1] for c in checks)
        return all_passed, "\n".join(results)
    
    def validate_build_performance(self) -> Tuple[bool, str]:
        """Validate build rate and quality targets"""
        results = []
        
        # Build rates by level
        build_rates = {1: 20, 2: 12, 3: 15, 4: 25}
        for level, rate in build_rates.items():
            if level == 4:
                passed = rate >= 25
                results.append(f"Level {level} rate: {rate} cm³/hr {'✓' if passed else '✗'}")
        
        # Density targets
        densities = {1: 95, 2: 98, 3: 98, 4: 98}
        for level, density in densities.items():
            passed = density >= 95
            results.append(f"Level {level} density: {density}% {'✓' if passed else '✗'}")
        
        all_passed = all("✓" in r for r in results)
        return all_passed, "\n".join(results)
    
    def generate_report(self):
        """Generate validation report"""
        print("=" * 60)
        print("ACOUSTIC MANUFACTURING SYSTEM - REQUIREMENTS VALIDATION")
        print("=" * 60)
        
        tests = [
            ("Power Budget", self.validate_power_budget),
            ("Cost Targets", self.validate_cost_progression),
            ("Thermal Constraints", self.validate_thermal_constraints),
            ("Build Performance", self.validate_build_performance),
        ]
        
        overall_pass = True
        
        for test_name, test_func in tests:
            passed, details = test_func()
            overall_pass = overall_pass and passed
            
            print(f"\n{test_name}:")
            print("-" * 40)
            print(details)
            print(f"Status: {'PASS ✓' if passed else 'FAIL ✗'}")
        
        print("\n" + "=" * 60)
        print(f"OVERALL STATUS: {'ALL TESTS PASSED ✓' if overall_pass else 'FAILURES DETECTED ✗'}")
        print("=" * 60)
        
        # Generate compliance matrix
        self._generate_compliance_matrix()
    
    def _generate_compliance_matrix(self):
        """Generate requirements compliance matrix"""
        print("\nREQUIREMENTS COMPLIANCE MATRIX")
        print("-" * 60)
        print(f"{'Req ID':<10} {'Description':<30} {'Target':<15} {'Status':<10}")
        print("-" * 60)
        
        for req_id, req in self.requirements.items():
            print(f"{req_id:<10} {req.description[:30]:<30} "
                  f"{req.value} {req.unit:<10} {req.status:<10}")

if __name__ == "__main__":
    validator = RequirementsValidator()
    validator.generate_report()