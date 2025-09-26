"""
Data models for test management system
"""
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict
import json

class VerificationStatus(Enum):
    NOT_TESTED = "NOT_TESTED"
    IN_TESTING = "IN_TESTING"
    VERIFIED = "VERIFIED"
    FAILED = "FAILED"
    NOT_APPLICABLE = "NOT_APPLICABLE"

class TestStatus(Enum):
    NOT_STARTED = "NOT_STARTED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETE = "COMPLETE"
    FAILED = "FAILED"
    BLOCKED = "BLOCKED"

class TestResult(Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    CONDITIONAL = "CONDITIONAL"
    NOT_TESTED = "NOT_TESTED"
    ABORTED = "ABORTED"

class VerificationType(Enum):
    FEASIBILITY = "FEASIBILITY"
    FUNCTIONAL = "FUNCTIONAL"
    PERFORMANCE = "PERFORMANCE"
    INTEGRATION = "INTEGRATION"
    ACCEPTANCE = "ACCEPTANCE"
    ENVIRONMENTAL = "ENVIRONMENTAL"
    ENDURANCE = "ENDURANCE"
    SAFETY = "SAFETY"

@dataclass
class TestDefinition:
    test_id: str
    test_name: str
    test_purpose: str
    target_components: List[str]
    verification_type: VerificationType
    prerequisite_tests: List[str] = field(default_factory=list)
    enables_tests: List[str] = field(default_factory=list)
    estimated_duration_hours: float = 1.0
    required_equipment: List[str] = field(default_factory=list)
    test_procedure_ref: str = ""
    acceptance_criteria: str = ""
    
    def to_dict(self):
        return {
            'test_id': self.test_id,
            'test_name': self.test_name,
            'test_purpose': self.test_purpose,
            'target_components': self.target_components,
            'verification_type': self.verification_type.value,
            'prerequisite_tests': self.prerequisite_tests,
            'enables_tests': self.enables_tests,
            'estimated_duration_hours': self.estimated_duration_hours,
            'required_equipment': self.required_equipment,
            'test_procedure_ref': self.test_procedure_ref,
            'acceptance_criteria': self.acceptance_criteria
        }

@dataclass
class TestExecution:
    test_id: str
    status: TestStatus = TestStatus.NOT_STARTED
    result: TestResult = TestResult.NOT_TESTED
    date_executed: Optional[datetime] = None
    test_engineer: str = ""
    report_path: str = ""
    notes: str = ""
    issues_found: List[str] = field(default_factory=list)
    
    def to_dict(self):
        return {
            'test_id': self.test_id,
            'status': self.status.value,
            'result': self.result.value,
            'date_executed': self.date_executed.isoformat() if self.date_executed else None,
            'test_engineer': self.test_engineer,
            'report_path': self.report_path,
            'notes': self.notes,
            'issues_found': self.issues_found
        }

@dataclass
class ComponentTestMapping:
    component_id: str
    test_id: str
    verification_type: VerificationType
    is_required: bool = True
    is_critical: bool = False
    
    def to_dict(self):
        return {
            'component_id': self.component_id,
            'test_id': self.test_id,
            'verification_type': self.verification_type.value,
            'is_required': self.is_required,
            'is_critical': self.is_critical
        }

@dataclass
class ComponentVerification:
    component_id: str
    component_name: str
    part_number: str
    verification_status: VerificationStatus = VerificationStatus.NOT_TESTED
    required_tests: List[str] = field(default_factory=list)
    completed_tests: List[str] = field(default_factory=list)
    passed_tests: List[str] = field(default_factory=list)
    failed_tests: List[str] = field(default_factory=list)
    verification_date: Optional[datetime] = None
    notes: str = ""
    
    def update_status(self):
        """Update verification status based on test results"""
        if not self.required_tests:
            self.verification_status = VerificationStatus.NOT_APPLICABLE
        elif not self.completed_tests:
            self.verification_status = VerificationStatus.NOT_TESTED
        elif self.failed_tests:
            self.verification_status = VerificationStatus.FAILED
        elif set(self.required_tests).issubset(set(self.passed_tests)):
            self.verification_status = VerificationStatus.VERIFIED
            self.verification_date = datetime.now()
        else:
            self.verification_status = VerificationStatus.IN_TESTING
    
    def get_completion_percentage(self):
        """Calculate test completion percentage"""
        if not self.required_tests:
            return 100.0
        return (len(self.completed_tests) / len(self.required_tests)) * 100.0
    
    def to_dict(self):
        return {
            'component_id': self.component_id,
            'component_name': self.component_name,
            'part_number': self.part_number,
            'verification_status': self.verification_status.value,
            'required_tests': self.required_tests,
            'completed_tests': self.completed_tests,
            'passed_tests': self.passed_tests,
            'failed_tests': self.failed_tests,
            'verification_date': self.verification_date.isoformat() if self.verification_date else None,
            'notes': self.notes,
            'completion_percentage': self.get_completion_percentage()
        }