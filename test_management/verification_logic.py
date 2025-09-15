"""
Verification Logic Engine
Manages component verification status based on test results
"""
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import json
from pathlib import Path

from .data_models import (
    VerificationStatus, TestStatus, TestResult, TestExecution,
    ComponentVerification, TestDefinition
)
from .test_registry import TestRegistry
from .component_test_mapping import ComponentTestMapper

class VerificationEngine:
    def __init__(self, data_dir: str = "verification_status"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        self.test_registry = TestRegistry()
        self.component_mapper = ComponentTestMapper()
        
        # Load or initialize state
        self.component_verifications = self._load_component_verifications()
        self.test_executions = self._load_test_executions()
    
    def _load_component_verifications(self) -> Dict[str, ComponentVerification]:
        """Load component verification status from disk"""
        file_path = self.data_dir / "component_status.json"
        if file_path.exists():
            with open(file_path, 'r') as f:
                data = json.load(f)
                verifications = {}
                for comp_id, comp_data in data.items():
                    verifications[comp_id] = ComponentVerification(**comp_data)
                return verifications
        else:
            # Initialize from component mapper
            return self._initialize_component_verifications()
    
    def _initialize_component_verifications(self) -> Dict[str, ComponentVerification]:
        """Initialize verification status for all components"""
        verifications = {}
        
        # Get all components from the mapping
        for component_name, requirements in self.component_mapper.component_test_requirements.items():
            # Create a simple component ID (could be enhanced with actual registry)
            component_id = component_name.replace(" ", "_").upper()
            
            verification = ComponentVerification(
                component_id=component_id,
                component_name=component_name,
                part_number="TBD",  # Would come from component registry
                required_tests=requirements["required_tests"],
                verification_status=VerificationStatus.NOT_TESTED
            )
            verifications[component_id] = verification
        
        return verifications
    
    def _load_test_executions(self) -> Dict[str, TestExecution]:
        """Load test execution status from disk"""
        file_path = self.data_dir / "test_status.json"
        if file_path.exists():
            with open(file_path, 'r') as f:
                data = json.load(f)
                executions = {}
                for test_id, test_data in data.items():
                    # Handle datetime conversion
                    if test_data.get('date_executed'):
                        test_data['date_executed'] = datetime.fromisoformat(test_data['date_executed'])
                    executions[test_id] = TestExecution(**test_data)
                return executions
        else:
            # Initialize all tests as not started
            return self._initialize_test_executions()
    
    def _initialize_test_executions(self) -> Dict[str, TestExecution]:
        """Initialize execution status for all tests"""
        executions = {}
        for test_id in self.test_registry.tests:
            executions[test_id] = TestExecution(
                test_id=test_id,
                status=TestStatus.NOT_STARTED,
                result=TestResult.NOT_TESTED
            )
        return executions
    
    def save_state(self):
        """Save current state to disk"""
        # Save component verifications
        comp_data = {}
        for comp_id, verification in self.component_verifications.items():
            comp_data[comp_id] = verification.to_dict()
        
        with open(self.data_dir / "component_status.json", 'w') as f:
            json.dump(comp_data, f, indent=2)
        
        # Save test executions
        test_data = {}
        for test_id, execution in self.test_executions.items():
            test_data[test_id] = execution.to_dict()
        
        with open(self.data_dir / "test_status.json", 'w') as f:
            json.dump(test_data, f, indent=2)
    
    def update_test_status(self, test_id: str, status: TestStatus, 
                          result: Optional[TestResult] = None,
                          test_engineer: str = "",
                          notes: str = "",
                          issues: List[str] = None) -> bool:
        """Update test execution status and trigger component verification check"""
        if test_id not in self.test_executions:
            return False
        
        execution = self.test_executions[test_id]
        execution.status = status
        
        if result:
            execution.result = result
        
        if status == TestStatus.COMPLETE:
            execution.date_executed = datetime.now()
            if not result:
                # Default to PASS if completed without explicit result
                execution.result = TestResult.PASS
        
        if test_engineer:
            execution.test_engineer = test_engineer
        
        if notes:
            execution.notes = notes
            
        if issues:
            execution.issues_found.extend(issues)
        
        # Update affected components
        self._update_affected_components(test_id)
        
        # Save state
        self.save_state()
        
        return True
    
    def _update_affected_components(self, test_id: str):
        """Update verification status for components affected by test"""
        affected_components = self.component_mapper.get_components_for_test(test_id)
        
        for component_name in affected_components:
            component_id = component_name.replace(" ", "_").upper()
            if component_id in self.component_verifications:
                self._update_component_verification(component_id)
    
    def _update_component_verification(self, component_id: str):
        """Update verification status for a specific component"""
        verification = self.component_verifications[component_id]
        
        # Get all tests for this component
        all_tests = self.component_mapper.get_all_tests_for_component(verification.component_name)
        required_tests = all_tests["required"]
        integration_tests = all_tests["integration"]
        
        # Update test lists based on execution status
        verification.completed_tests = []
        verification.passed_tests = []
        verification.failed_tests = []
        
        for test_id in required_tests + integration_tests:
            if test_id in self.test_executions:
                execution = self.test_executions[test_id]
                
                if execution.status == TestStatus.COMPLETE:
                    verification.completed_tests.append(test_id)
                    
                    if execution.result == TestResult.PASS:
                        verification.passed_tests.append(test_id)
                    elif execution.result == TestResult.FAIL:
                        verification.failed_tests.append(test_id)
        
        # Update verification status
        verification.update_status()
    
    def get_component_status(self, component_id: str) -> Optional[ComponentVerification]:
        """Get verification status for a component"""
        return self.component_verifications.get(component_id)
    
    def get_test_status(self, test_id: str) -> Optional[TestExecution]:
        """Get execution status for a test"""
        return self.test_executions.get(test_id)
    
    def get_next_required_tests(self, limit: int = 10) -> List[Tuple[str, TestDefinition]]:
        """Get prioritized list of tests needed for critical path"""
        next_tests = []
        
        # Get critical path components
        critical_components = self.component_mapper.get_critical_path_components()
        
        # First priority: Required tests for critical components that haven't started
        for component_name in critical_components:
            component_id = component_name.replace(" ", "_").upper()
            if component_id in self.component_verifications:
                verification = self.component_verifications[component_id]
                
                for test_id in verification.required_tests:
                    execution = self.test_executions.get(test_id)
                    if execution and execution.status == TestStatus.NOT_STARTED:
                        # Check if prerequisites are met
                        test_def = self.test_registry.get_test(test_id)
                        if test_def and self._prerequisites_met(test_def):
                            next_tests.append((test_id, test_def))
                            if len(next_tests) >= limit:
                                return next_tests
        
        # Second priority: Integration tests for components with completed required tests
        for component_name in critical_components:
            tests = self.component_mapper.get_all_tests_for_component(component_name)
            component_id = component_name.replace(" ", "_").upper()
            verification = self.component_verifications.get(component_id)
            
            if verification:
                # Check if all required tests are complete
                required_complete = all(
                    test_id in verification.completed_tests 
                    for test_id in tests["required"]
                )
                
                if required_complete:
                    for test_id in tests["integration"]:
                        execution = self.test_executions.get(test_id)
                        if execution and execution.status == TestStatus.NOT_STARTED:
                            test_def = self.test_registry.get_test(test_id)
                            if test_def and self._prerequisites_met(test_def):
                                next_tests.append((test_id, test_def))
                                if len(next_tests) >= limit:
                                    return next_tests
        
        return next_tests
    
    def _prerequisites_met(self, test: TestDefinition) -> bool:
        """Check if all prerequisite tests are completed"""
        for prereq_id in test.prerequisite_tests:
            execution = self.test_executions.get(prereq_id)
            if not execution or execution.status != TestStatus.COMPLETE:
                return False
        return True
    
    def get_blocked_tests(self) -> List[Tuple[str, List[str]]]:
        """Get tests blocked by incomplete prerequisites"""
        blocked = []
        
        for test_id, test_def in self.test_registry.tests.items():
            execution = self.test_executions.get(test_id)
            
            if execution and execution.status == TestStatus.NOT_STARTED:
                if test_def.prerequisite_tests and not self._prerequisites_met(test_def):
                    # Find which prerequisites are blocking
                    blocking_tests = []
                    for prereq_id in test_def.prerequisite_tests:
                        prereq_exec = self.test_executions.get(prereq_id)
                        if not prereq_exec or prereq_exec.status != TestStatus.COMPLETE:
                            blocking_tests.append(prereq_id)
                    
                    blocked.append((test_id, blocking_tests))
        
        return blocked
    
    def get_verification_summary(self) -> Dict[str, Dict[str, int]]:
        """Get summary of verification status across all components"""
        summary = {
            "components": {
                "total": len(self.component_verifications),
                "verified": 0,
                "in_testing": 0,
                "failed": 0,
                "not_tested": 0
            },
            "tests": {
                "total": len(self.test_executions),
                "complete": 0,
                "in_progress": 0,
                "failed": 0,
                "not_started": 0,
                "blocked": 0
            }
        }
        
        # Count component statuses
        for verification in self.component_verifications.values():
            if verification.verification_status == VerificationStatus.VERIFIED:
                summary["components"]["verified"] += 1
            elif verification.verification_status == VerificationStatus.IN_TESTING:
                summary["components"]["in_testing"] += 1
            elif verification.verification_status == VerificationStatus.FAILED:
                summary["components"]["failed"] += 1
            elif verification.verification_status == VerificationStatus.NOT_TESTED:
                summary["components"]["not_tested"] += 1
        
        # Count test statuses
        blocked_tests = self.get_blocked_tests()
        blocked_test_ids = {t[0] for t in blocked_tests}
        
        for test_id, execution in self.test_executions.items():
            if execution.status == TestStatus.COMPLETE:
                summary["tests"]["complete"] += 1
                if execution.result == TestResult.FAIL:
                    summary["tests"]["failed"] += 1
            elif execution.status == TestStatus.IN_PROGRESS:
                summary["tests"]["in_progress"] += 1
            elif execution.status == TestStatus.NOT_STARTED:
                if test_id in blocked_test_ids:
                    summary["tests"]["blocked"] += 1
                else:
                    summary["tests"]["not_started"] += 1
        
        return summary
    
    def get_subsystem_status(self) -> Dict[str, Dict[str, float]]:
        """Get verification status by subsystem"""
        subsystems = self.component_mapper.get_subsystem_components()
        subsystem_status = {}
        
        for subsystem_name, components in subsystems.items():
            total_required = 0
            total_completed = 0
            total_passed = 0
            
            for component_name in components:
                component_id = component_name.replace(" ", "_").upper()
                verification = self.component_verifications.get(component_id)
                
                if verification:
                    total_required += len(verification.required_tests)
                    total_completed += len(verification.completed_tests)
                    total_passed += len(verification.passed_tests)
            
            if total_required > 0:
                subsystem_status[subsystem_name] = {
                    "completion_percentage": (total_completed / total_required) * 100,
                    "pass_percentage": (total_passed / total_required) * 100,
                    "total_tests": total_required,
                    "completed_tests": total_completed,
                    "passed_tests": total_passed
                }
            else:
                subsystem_status[subsystem_name] = {
                    "completion_percentage": 100.0,
                    "pass_percentage": 100.0,
                    "total_tests": 0,
                    "completed_tests": 0,
                    "passed_tests": 0
                }
        
        return subsystem_status
    
    def generate_verification_matrix(self) -> List[Dict[str, any]]:
        """Generate verification matrix for reporting"""
        matrix = []
        
        for component_id, verification in self.component_verifications.items():
            component_data = {
                "component_id": component_id,
                "component_name": verification.component_name,
                "part_number": verification.part_number,
                "verification_status": verification.verification_status.value,
                "completion_percentage": verification.get_completion_percentage(),
                "required_tests": len(verification.required_tests),
                "completed_tests": len(verification.completed_tests),
                "passed_tests": len(verification.passed_tests),
                "failed_tests": len(verification.failed_tests),
                "verification_date": verification.verification_date.isoformat() if verification.verification_date else None
            }
            matrix.append(component_data)
        
        return matrix