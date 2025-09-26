#!/usr/bin/env python3
"""
Test Management System - Main entry point for test tracking and verification
"""
import sys
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from test_management.data_models import TestStatus, TestResult, VerificationStatus
from test_management.verification_logic import VerificationEngine
from test_management.report_generator import ReportGenerator
from test_management.dashboard_generator import DashboardGenerator
from test_management.test_registry import TestRegistry
from test_management.component_test_mapping import ComponentTestMapper

class TestManagementSystem:
    """Main test management system interface"""
    
    def __init__(self):
        self.engine = VerificationEngine()
        self.report_generator = ReportGenerator()
        self.dashboard_generator = DashboardGenerator()
        self.test_registry = TestRegistry()
        self.component_mapper = ComponentTestMapper()
        
        print("Test Management System Initialized")
        print(f"Tests Loaded: {len(self.test_registry.tests)}")
        print(f"Components Tracked: {len(self.engine.component_verifications)}")
    
    def check_gateway_test(self):
        """Check if TE-000 physics validation has passed"""
        te000_execution = self.engine.test_executions.get('TE-000')
        if not te000_execution or te000_execution.result != TestResult.PASS:
            print("⚠️ WARNING: TE-000 Physics Validation MUST PASS before other testing!")
            if not te000_execution:
                print("Current Status: NOT STARTED")
                print("➡️ START WITH TE-000 IMMEDIATELY")
            else:
                print(f"Current Status: {te000_execution.status.value}")
                print(f"Result: {te000_execution.result.value}")
            return False
        return True
    
    def update_test(self, test_id: str, status: str, result: str = None, 
                    engineer: str = "", notes: str = ""):
        """Update test status and result"""
        try:
            # Check gateway test for all tests except TE-000
            if test_id != "TE-000" and not self.check_gateway_test():
                print(f"❌ Cannot proceed with {test_id} until TE-000 passes!")
                print("   All testing is blocked by the gateway physics validation test.")
                return
            
            test_status = TestStatus[status.upper()]
            test_result = TestResult[result.upper()] if result else None
            
            success = self.engine.update_test_status(
                test_id=test_id,
                status=test_status,
                result=test_result,
                test_engineer=engineer,
                notes=notes
            )
            
            if success:
                print(f"✅ Updated {test_id}: {status}")
                self._show_affected_components(test_id)
            else:
                print(f"❌ Failed to update {test_id}")
                
        except KeyError as e:
            print(f"❌ Invalid status or result: {e}")
    
    def _show_affected_components(self, test_id: str):
        """Show components affected by test update"""
        affected = self.component_mapper.get_components_for_test(test_id)
        if affected:
            print(f"   Affected components: {', '.join(affected)}")
    
    def show_component_status(self, component_name: str = None):
        """Display component verification status"""
        if component_name:
            comp_id = component_name.replace(" ", "_").upper()
            verification = self.engine.component_verifications.get(comp_id)
            
            if verification:
                print(f"\n{'='*60}")
                print(f"Component: {verification.component_name}")
                print(f"Status: {self._get_status_emoji(verification.verification_status)} {verification.verification_status.value}")
                print(f"Progress: {verification.get_completion_percentage():.1f}%")
                print(f"Required Tests: {len(verification.required_tests)}")
                print(f"Completed: {len(verification.completed_tests)}")
                print(f"Failed: {len(verification.failed_tests)}")
                
                if verification.required_tests:
                    print("\nTest Details:")
                    for test_id in verification.required_tests:
                        execution = self.engine.test_executions.get(test_id)
                        test_def = self.test_registry.get_test(test_id)
                        if execution and test_def:
                            status_emoji = self._get_test_emoji(execution.status)
                            print(f"  {status_emoji} {test_id}: {test_def.test_name[:40]}... - {execution.status.value}")
                print('='*60)
            else:
                print(f"Component '{component_name}' not found")
        else:
            # Show all components
            self._show_all_components()
    
    def _show_all_components(self):
        """Display all component statuses grouped by subsystem"""
        subsystems = self.component_mapper.get_subsystem_components()
        
        print("\nComponent Verification Status by Subsystem")
        print("="*80)
        
        for subsystem, components in subsystems.items():
            print(f"\n{subsystem} Subsystem:")
            print("-"*40)
            
            for comp_name in components:
                comp_id = comp_name.replace(" ", "_").upper()
                verification = self.engine.component_verifications.get(comp_id)
                
                if verification:
                    status_emoji = self._get_status_emoji(verification.verification_status)
                    progress = verification.get_completion_percentage()
                    print(f"  {status_emoji} {comp_name:<30} {progress:>5.1f}% ({len(verification.completed_tests)}/{len(verification.required_tests)})")
    
    def show_next_tests(self, limit: int = 10):
        """Show next tests to execute"""
        # Check if TE-000 needs to be done first
        te000_execution = self.engine.test_executions.get('TE-000')
        if not te000_execution or te000_execution.result != TestResult.PASS:
            print("\n🚨 CRITICAL: TE-000 Physics Validation MUST be completed first!")
            print("="*80)
            print("\n1. TE-000: Acoustic Steering Physics Validation")
            print("   Purpose: Validate lateral steering forces on falling droplets are achievable")
            print("   Duration: 16.0h")
            print("   Components: 40kHz Transducers")
            print("   Equipment: Single 40kHz transducer, Function generator, Audio amplifier (100W)")
            print("\n⚠️ All other tests are BLOCKED until TE-000 passes!")
            return
        
        next_tests = self.engine.get_next_required_tests(limit)
        
        print(f"\nNext {limit} Tests to Execute:")
        print("="*80)
        
        if next_tests:
            total_hours = 0
            for i, (test_id, test_def) in enumerate(next_tests, 1):
                print(f"\n{i}. {test_id}: {test_def.test_name}")
                print(f"   Purpose: {test_def.test_purpose}")
                print(f"   Duration: {test_def.estimated_duration_hours}h")
                print(f"   Components: {', '.join(test_def.target_components)}")
                print(f"   Equipment: {', '.join(test_def.required_equipment[:3])}")
                
                total_hours += test_def.estimated_duration_hours
            
            print(f"\nTotal Duration: {total_hours:.1f} hours ({total_hours/8:.1f} days)")
        else:
            print("No tests available. Check blocked tests.")
    
    def show_blocked_tests(self):
        """Show tests blocked by prerequisites"""
        blocked = self.engine.get_blocked_tests()
        
        if blocked:
            print("\nBlocked Tests:")
            print("="*60)
            
            for test_id, blocking_tests in blocked:
                test_def = self.test_registry.get_test(test_id)
                if test_def:
                    print(f"\n{test_id}: {test_def.test_name}")
                    print(f"  Blocked by: {', '.join(blocking_tests)}")
        else:
            print("\nNo tests are currently blocked.")
    
    def show_summary(self):
        """Show overall verification summary"""
        summary = self.engine.get_verification_summary()
        subsystem_status = self.engine.get_subsystem_status()
        
        print("\nDRIP System Verification Summary")
        print("="*60)
        print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Check gateway test status first
        if not self.check_gateway_test():
            print("🚨 CRITICAL: TE-000 Physics Validation MUST PASS before any other testing!")
            print("="*60)
            print()
        
        # Component summary
        print("Component Status:")
        print(f"  ✅ Verified: {summary['components']['verified']}/{summary['components']['total']}")
        print(f"  🔄 In Testing: {summary['components']['in_testing']}")
        print(f"  ❌ Failed: {summary['components']['failed']}")
        print(f"  ⬜ Not Started: {summary['components']['not_tested']}")
        
        # Test summary
        print("\nTest Status:")
        print(f"  ✅ Complete: {summary['tests']['complete']}/{summary['tests']['total']}")
        print(f"  🔄 In Progress: {summary['tests']['in_progress']}")
        print(f"  ❌ Failed: {summary['tests']['failed']}")
        print(f"  🚫 Blocked: {summary['tests']['blocked']}")
        print(f"  ⬜ Not Started: {summary['tests']['not_started']}")
        
        # Subsystem summary
        print("\nSubsystem Progress:")
        for subsystem, status in subsystem_status.items():
            bar = self._create_mini_progress_bar(status['completion_percentage'])
            print(f"  {subsystem:<12} {bar} {status['completion_percentage']:>5.1f}%")
    
    def generate_dashboards(self):
        """Generate all verification dashboards"""
        print("\nGenerating verification dashboards...")
        self.dashboard_generator.generate_all_dashboards()
        print("✅ Dashboards generated successfully")
    
    def create_test_report(self, test_id: str):
        """Create a test report template"""
        if self.report_generator.generate_test_report_template(test_id):
            print(f"✅ Created template for {test_id}")
            template_path = self.report_generator.get_template_path(test_id)
            if template_path:
                print(f"   Template: {template_path}")
        else:
            print(f"❌ Failed to create template for {test_id}")
    
    def batch_update_tests(self, updates: List[Dict]):
        """Update multiple tests at once"""
        print(f"\nBatch updating {len(updates)} tests...")
        
        for update in updates:
            self.update_test(**update)
    
    # Helper methods
    def _get_status_emoji(self, status: VerificationStatus) -> str:
        """Get emoji for verification status"""
        emojis = {
            VerificationStatus.NOT_TESTED: "⬜",
            VerificationStatus.IN_TESTING: "🔄",
            VerificationStatus.VERIFIED: "✅",
            VerificationStatus.FAILED: "❌",
            VerificationStatus.NOT_APPLICABLE: "➖"
        }
        return emojis.get(status, "❓")
    
    def _get_test_emoji(self, status: TestStatus) -> str:
        """Get emoji for test status"""
        emojis = {
            TestStatus.NOT_STARTED: "⬜",
            TestStatus.IN_PROGRESS: "🔄",
            TestStatus.COMPLETE: "✅",
            TestStatus.FAILED: "❌",
            TestStatus.BLOCKED: "🚫"
        }
        return emojis.get(status, "❓")
    
    def _create_mini_progress_bar(self, percentage: float) -> str:
        """Create a mini progress bar"""
        filled = int(percentage / 10)
        bar = "█" * filled + "░" * (10 - filled)
        return f"[{bar}]"


def main():
    """Main CLI interface"""
    system = TestManagementSystem()
    
    print("\nTest Management System CLI")
    print("Commands: summary, components, next, blocked, update, dashboard, quit")
    
    while True:
        try:
            command = input("\n> ").strip().lower()
            
            if command == "quit" or command == "exit":
                break
            
            elif command == "summary":
                system.show_summary()
            
            elif command == "components":
                system.show_component_status()
            
            elif command.startswith("component "):
                comp_name = command[10:].strip()
                system.show_component_status(comp_name)
            
            elif command == "next":
                system.show_next_tests()
            
            elif command == "blocked":
                system.show_blocked_tests()
            
            elif command.startswith("update "):
                parts = command[7:].split()
                if len(parts) >= 2:
                    test_id = parts[0].upper()
                    status = parts[1]
                    result = parts[2] if len(parts) > 2 else None
                    system.update_test(test_id, status, result)
                else:
                    print("Usage: update TEST_ID STATUS [RESULT]")
            
            elif command == "dashboard":
                system.generate_dashboards()
            
            elif command == "help":
                print("\nAvailable commands:")
                print("  summary - Show overall verification summary")
                print("  components - List all component statuses")
                print("  component NAME - Show specific component status")
                print("  next - Show next tests to execute")
                print("  blocked - Show blocked tests")
                print("  update TEST_ID STATUS [RESULT] - Update test status")
                print("  dashboard - Generate verification dashboards")
                print("  quit - Exit the system")
            
            else:
                print(f"Unknown command: {command}. Type 'help' for commands.")
                
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()