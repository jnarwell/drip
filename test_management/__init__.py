"""
Test Management System for DRIP Acoustic Manufacturing
"""
from .data_models import (
    VerificationStatus, TestStatus, TestResult, VerificationType,
    TestDefinition, TestExecution, ComponentTestMapping, ComponentVerification
)
from .test_registry import TestRegistry
from .component_test_mapping import ComponentTestMapper
from .verification_logic import VerificationEngine
from .report_generator import ReportGenerator
from .dashboard_generator import DashboardGenerator
from .test_management_system import TestManagementSystem

__version__ = "1.0.0"
__all__ = [
    "TestManagementSystem",
    "VerificationEngine",
    "ReportGenerator", 
    "DashboardGenerator",
    "TestRegistry",
    "ComponentTestMapper",
    "VerificationStatus",
    "TestStatus",
    "TestResult",
    "VerificationType"
]