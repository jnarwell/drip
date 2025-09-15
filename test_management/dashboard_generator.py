"""
Dashboard Generator - Creates interactive verification status dashboards
"""
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import json

from .verification_logic import VerificationEngine
from .test_registry import TestRegistry
from .component_test_mapping import ComponentTestMapper
from .data_models import VerificationStatus, TestStatus

class DashboardGenerator:
    def __init__(self, output_dir: str = "docs/verification"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.engine = VerificationEngine()
        self.test_registry = TestRegistry()
        self.component_mapper = ComponentTestMapper()
    
    def generate_all_dashboards(self):
        """Generate all dashboard views"""
        print("Generating verification dashboards...")
        
        # Generate main dashboard
        self.generate_main_dashboard()
        
        # Generate component verification matrix
        self.generate_component_matrix()
        
        # Generate test execution tracker
        self.generate_test_tracker()
        
        # Generate subsystem status
        self.generate_subsystem_status()
        
        # Generate test planning view
        self.generate_test_planning()
        
        print(f"Dashboards generated in: {self.output_dir}")
    
    def generate_main_dashboard(self):
        """Generate main verification dashboard"""
        summary = self.engine.get_verification_summary()
        subsystem_status = self.engine.get_subsystem_status()
        
        content = f"""# DRIP System Verification Dashboard

*Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*

## Overall System Status

### Component Verification Progress
{self._create_progress_bar(
    summary['components']['verified'],
    summary['components']['total'],
    "Components Verified"
)}

- ✅ **Verified**: {summary['components']['verified']}/{summary['components']['total']}
- 🔄 **In Testing**: {summary['components']['in_testing']}
- ❌ **Failed**: {summary['components']['failed']}
- ⬜ **Not Started**: {summary['components']['not_tested']}

### Test Execution Progress
{self._create_progress_bar(
    summary['tests']['complete'],
    summary['tests']['total'],
    "Tests Complete"
)}

- ✅ **Complete**: {summary['tests']['complete']}/{summary['tests']['total']}
- 🔄 **In Progress**: {summary['tests']['in_progress']}
- ❌ **Failed**: {summary['tests']['failed']}
- 🚫 **Blocked**: {summary['tests']['blocked']}
- ⬜ **Not Started**: {summary['tests']['not_started']}

## Subsystem Status

"""
        # Add subsystem status table
        content += "| Subsystem | Progress | Tests Complete | Status |\n"
        content += "|-----------|----------|----------------|--------|\n"
        
        for subsystem, status in subsystem_status.items():
            progress_icon = self._get_progress_icon(status['completion_percentage'])
            content += f"| {subsystem} | {progress_icon} {status['completion_percentage']:.1f}% | "
            content += f"{status['completed_tests']}/{status['total_tests']} | "
            content += f"{self._get_subsystem_status_icon(status)} |\n"
        
        # Add critical path information
        content += "\n## Critical Path Status\n\n"
        critical_components = self.component_mapper.get_critical_path_components()
        
        content += "### Critical Components\n"
        content += "These components must be verified before system-level testing:\n\n"
        content += "| Component | Status | Progress | Next Test |\n"
        content += "|-----------|--------|----------|------------|\n"
        
        for comp_name in critical_components:
            comp_id = comp_name.replace(" ", "_").upper()
            verification = self.engine.component_verifications.get(comp_id)
            if verification:
                status_icon = self._get_status_icon(verification.verification_status)
                progress = verification.get_completion_percentage()
                
                # Find next test
                next_test = "Complete"
                for test_id in verification.required_tests:
                    if test_id not in verification.completed_tests:
                        next_test = test_id
                        break
                
                content += f"| {comp_name} | {status_icon} | {progress:.0f}% | {next_test} |\n"
        
        # Add quick links
        content += """
## Quick Links

- [Component Verification Matrix](component-matrix.md)
- [Test Execution Tracker](test-tracker.md)
- [Test Planning](test-planning.md)
- [Subsystem Details](subsystem-status.md)

## Actions Required

"""
        # Get next required tests
        next_tests = self.engine.get_next_required_tests(5)
        if next_tests:
            content += "### Next Tests to Execute\n"
            for test_id, test_def in next_tests:
                content += f"1. **{test_id}**: {test_def.test_name}\n"
                content += f"   - Duration: {test_def.estimated_duration_hours}h\n"
                content += f"   - Components: {', '.join(test_def.target_components)}\n"
        else:
            content += "No tests ready for execution. Check blocked tests.\n"
        
        # Save dashboard
        with open(self.output_dir / "index.md", 'w') as f:
            f.write(content)
    
    def generate_component_matrix(self):
        """Generate component verification matrix"""
        subsystems = self.component_mapper.get_subsystem_components()
        
        content = """# Component Verification Matrix

[← Back to Dashboard](index.md)

## Verification Status by Component

"""
        
        for subsystem_name, components in subsystems.items():
            content += f"\n### {subsystem_name} Subsystem\n\n"
            content += "| Component | P/N | Required Tests | Complete | Status | Action |\n"
            content += "|-----------|-----|----------------|----------|--------|--------|\n"
            
            for comp_name in components:
                comp_id = comp_name.replace(" ", "_").upper()
                verification = self.engine.component_verifications.get(comp_id)
                
                if verification:
                    status_icon = self._get_status_icon(verification.verification_status)
                    test_progress = f"{len(verification.completed_tests)}/{len(verification.required_tests)}"
                    
                    # Determine action
                    if verification.verification_status == VerificationStatus.VERIFIED:
                        action = "✅ Verified"
                    elif verification.failed_tests:
                        action = f"⚠️ Review Failed: {', '.join(verification.failed_tests)}"
                    elif len(verification.completed_tests) < len(verification.required_tests):
                        next_test = None
                        for test_id in verification.required_tests:
                            if test_id not in verification.completed_tests:
                                next_test = test_id
                                break
                        action = f"[Execute {next_test}](test-tracker.md#{next_test.lower()})" if next_test else "Continue"
                    else:
                        action = "Complete Integration Tests"
                    
                    content += f"| {comp_name} | {verification.part_number} | "
                    content += f"{', '.join(verification.required_tests) if verification.required_tests else 'None'} | "
                    content += f"{test_progress} | {status_icon} | {action} |\n"
            
            # Add progress bar for subsystem
            subsystem_status = self.engine.get_subsystem_status()
            if subsystem_name in subsystem_status:
                status = subsystem_status[subsystem_name]
                content += f"\n{self._create_progress_bar(status['completed_tests'], status['total_tests'], f'{subsystem_name} Progress')}\n"
        
        # Add legend
        content += """
## Legend

### Status Icons
- ⬜ Not Tested
- 🔄 In Testing  
- ✅ Verified
- ❌ Failed

### Actions
- **Execute [Test ID]**: Click to view test procedure
- **Review Failed**: Investigation required for failed tests
- **Complete Integration**: All required tests passed, integration testing needed

## Export Options

- [Download CSV](component-matrix.csv)
- [Download JSON](component-matrix.json)
"""
        
        with open(self.output_dir / "component-matrix.md", 'w') as f:
            f.write(content)
        
        # Also generate CSV and JSON exports
        self._export_component_matrix_csv()
        self._export_component_matrix_json()
    
    def generate_test_tracker(self):
        """Generate test execution tracker"""
        content = """# Test Execution Tracker

[← Back to Dashboard](index.md)

## Test Status Overview

"""
        
        # Group tests by subsystem
        test_groups = {
            "Acoustic Tests": ["TE-001", "TE-015"],
            "Thermal Tests": ["TE-016", "TE-030"],
            "Crucible Tests": ["TE-031", "TE-040"],
            "Power Tests": ["TE-041", "TE-050"],
            "Sensor Tests": ["TE-051", "TE-060"],
            "Control Tests": ["TE-061", "TE-070"],
            "Chamber Tests": ["TE-071", "TE-075"],
            "Integration Tests": ["TE-076", "TE-080"],
            "Performance Tests": ["TE-081", "TE-085"],
            "Endurance Tests": ["TE-086", "TE-095"],
            "Validation Tests": ["TE-096", "TE-100"]
        }
        
        for group_name, (start_id, end_id) in test_groups.items():
            content += f"\n### {group_name} ({start_id} to {end_id})\n\n"
            content += "| Test ID | Test Name | Status | Components | Duration | Report |\n"
            content += "|---------|-----------|---------|------------|----------|--------|\n"
            
            # Extract test numbers
            start_num = int(start_id.split('-')[1])
            end_num = int(end_id.split('-')[1])
            
            for i in range(start_num, end_num + 1):
                test_id = f"TE-{i:03d}"
                test_def = self.test_registry.get_test(test_id)
                execution = self.engine.test_executions.get(test_id)
                
                if test_def and execution:
                    status_icon = self._get_test_status_icon(execution.status)
                    
                    # Create report link
                    if execution.status == TestStatus.NOT_STARTED:
                        template_path = f"../../test_reports/templates/{test_id}_{test_def.test_name.replace(' ', '_').replace('/', '-')}.md"
                        report_link = f"[Create Report]({template_path})"
                    elif execution.status == TestStatus.COMPLETE:
                        if execution.report_path:
                            report_link = f"[View Report]({execution.report_path})"
                        else:
                            report_link = "[Report Missing]"
                    else:
                        report_link = "[In Progress]"
                    
                    content += f"| **{test_id}** | {test_def.test_name} | {status_icon} | "
                    content += f"{len(test_def.target_components)} | {test_def.estimated_duration_hours}h | "
                    content += f"{report_link} |\n"
            
            # Calculate group progress
            group_tests = [f"TE-{i:03d}" for i in range(start_num, end_num + 1)]
            completed = sum(1 for tid in group_tests 
                          if tid in self.engine.test_executions 
                          and self.engine.test_executions[tid].status == TestStatus.COMPLETE)
            total = len(group_tests)
            
            content += f"\n{self._create_progress_bar(completed, total, f'{group_name} Progress')}\n"
        
        # Add blocked tests section
        blocked_tests = self.engine.get_blocked_tests()
        if blocked_tests:
            content += "\n## ⚠️ Blocked Tests\n\n"
            content += "These tests cannot start until prerequisites are complete:\n\n"
            content += "| Test ID | Test Name | Blocked By | Action |\n"
            content += "|---------|-----------|------------|--------|\n"
            
            for test_id, blocking_tests in blocked_tests:
                test_def = self.test_registry.get_test(test_id)
                if test_def:
                    blockers = ", ".join(blocking_tests)
                    content += f"| {test_id} | {test_def.test_name} | {blockers} | "
                    content += f"Complete prerequisites |\n"
        
        with open(self.output_dir / "test-tracker.md", 'w') as f:
            f.write(content)
    
    def generate_subsystem_status(self):
        """Generate detailed subsystem status"""
        subsystems = self.component_mapper.get_subsystem_components()
        subsystem_status = self.engine.get_subsystem_status()
        
        content = """# Subsystem Verification Status

[← Back to Dashboard](index.md)

## Detailed Status by Subsystem

"""
        
        for subsystem_name, components in subsystems.items():
            status = subsystem_status.get(subsystem_name, {})
            
            content += f"\n## {subsystem_name} Subsystem\n\n"
            
            # Overall status
            content += f"### Overall Progress\n"
            content += f"{self._create_progress_bar(status.get('completed_tests', 0), status.get('total_tests', 0), 'Tests Complete')}\n\n"
            
            # Component details
            content += "### Component Status\n\n"
            content += "| Component | Verification | Required | Complete | Failed | Status |\n"
            content += "|-----------|--------------|----------|----------|---------|--------|\n"
            
            for comp_name in components:
                comp_id = comp_name.replace(" ", "_").upper()
                verification = self.engine.component_verifications.get(comp_id)
                
                if verification:
                    status_icon = self._get_status_icon(verification.verification_status)
                    content += f"| {comp_name} | {status_icon} | "
                    content += f"{len(verification.required_tests)} | "
                    content += f"{len(verification.completed_tests)} | "
                    content += f"{len(verification.failed_tests)} | "
                    content += f"{verification.verification_status.value} |\n"
            
            # Test details for subsystem
            content += f"\n### Test Coverage\n\n"
            
            # Collect all tests for this subsystem
            subsystem_tests = set()
            for comp_name in components:
                tests = self.component_mapper.get_all_tests_for_component(comp_name)
                subsystem_tests.update(tests['required'])
                subsystem_tests.update(tests['integration'])
            
            if subsystem_tests:
                content += "| Test ID | Name | Type | Status | Result |\n"
                content += "|---------|------|------|--------|--------|\n"
                
                for test_id in sorted(subsystem_tests):
                    test_def = self.test_registry.get_test(test_id)
                    execution = self.engine.test_executions.get(test_id)
                    
                    if test_def and execution:
                        status_icon = self._get_test_status_icon(execution.status)
                        result = execution.result.value if execution.result else "-"
                        
                        content += f"| {test_id} | {test_def.test_name[:40]}... | "
                        content += f"{test_def.verification_type.value} | "
                        content += f"{status_icon} | {result} |\n"
        
        with open(self.output_dir / "subsystem-status.md", 'w') as f:
            f.write(content)
    
    def generate_test_planning(self):
        """Generate test planning view"""
        content = """# Test Planning & Scheduling

[← Back to Dashboard](index.md)

## Test Execution Plan

### Next Available Tests
Tests ready for immediate execution (all prerequisites met):

"""
        
        next_tests = self.engine.get_next_required_tests(20)
        
        if next_tests:
            content += "| Priority | Test ID | Test Name | Duration | Equipment Required |\n"
            content += "|----------|---------|-----------|----------|-------------------|\n"
            
            for i, (test_id, test_def) in enumerate(next_tests, 1):
                equipment = ", ".join(test_def.required_equipment[:2])
                if len(test_def.required_equipment) > 2:
                    equipment += "..."
                
                content += f"| {i} | {test_id} | {test_def.test_name} | "
                content += f"{test_def.estimated_duration_hours}h | {equipment} |\n"
            
            # Calculate total time
            total_hours = sum(test_def.estimated_duration_hours for _, test_def in next_tests)
            content += f"\n**Total Duration**: {total_hours:.1f} hours ({total_hours/8:.1f} days at 8h/day)\n"
        else:
            content += "_No tests currently available. Check blocked tests below._\n"
        
        # Test dependencies visualization
        content += "\n### Test Dependencies\n\n"
        content += "Critical path tests and their dependencies:\n\n"
        content += "```mermaid\ngraph TD\n"
        
        # Add critical path dependencies
        critical_tests = ["TE-001", "TE-005", "TE-013", "TE-077", "TE-081"]
        for test_id in critical_tests:
            test_def = self.test_registry.get_test(test_id)
            if test_def:
                for prereq in test_def.prerequisite_tests:
                    content += f"    {prereq} --> {test_id}\n"
                for enabled in test_def.enables_tests:
                    content += f"    {test_id} --> {enabled}\n"
        
        content += "```\n"
        
        # Resource planning
        content += "\n### Resource Requirements\n\n"
        content += "#### Equipment Usage Schedule\n\n"
        
        # Group tests by equipment
        equipment_usage = {}
        for test_id, test_def in self.test_registry.tests.items():
            for equipment in test_def.required_equipment:
                if equipment not in equipment_usage:
                    equipment_usage[equipment] = []
                equipment_usage[equipment].append((test_id, test_def.estimated_duration_hours))
        
        # Show top equipment
        content += "| Equipment | Total Tests | Total Hours | Utilization |\n"
        content += "|-----------|-------------|-------------|-------------|\n"
        
        for equipment, tests in sorted(equipment_usage.items(), 
                                      key=lambda x: len(x[1]), 
                                      reverse=True)[:10]:
            total_hours = sum(hours for _, hours in tests)
            content += f"| {equipment} | {len(tests)} | {total_hours:.1f}h | "
            content += f"{(total_hours / (100 * 8)) * 100:.1f}% |\n"
        
        # Gantt chart placeholder
        content += """
### Proposed Schedule

#### Week 1-2: Critical Component Tests
- Focus on acoustic and thermal subsystems
- Establish baseline performance

#### Week 3-4: Integration Testing  
- System-level integration
- Control loop validation

#### Week 5-6: Performance & Endurance
- Full system characterization
- Long-duration testing

#### Week 7-8: Final Validation
- Customer acceptance tests
- Documentation completion

### Risk Mitigation

| Risk | Impact | Mitigation Strategy |
|------|--------|-------------------|
| Equipment failure | High | Maintain calibrated backup equipment |
| Test delays | Medium | Parallel test execution where possible |
| Failed tests | High | Root cause analysis process defined |
| Resource conflicts | Medium | Detailed scheduling and coordination |
"""
        
        with open(self.output_dir / "test-planning.md", 'w') as f:
            f.write(content)
    
    # Helper methods
    def _get_status_icon(self, status: VerificationStatus) -> str:
        """Get icon for verification status"""
        icons = {
            VerificationStatus.NOT_TESTED: "⬜",
            VerificationStatus.IN_TESTING: "🔄",
            VerificationStatus.VERIFIED: "✅",
            VerificationStatus.FAILED: "❌",
            VerificationStatus.NOT_APPLICABLE: "➖"
        }
        return icons.get(status, "❓")
    
    def _get_test_status_icon(self, status: TestStatus) -> str:
        """Get icon for test status"""
        icons = {
            TestStatus.NOT_STARTED: "⬜",
            TestStatus.IN_PROGRESS: "🔄",
            TestStatus.COMPLETE: "✅",
            TestStatus.FAILED: "❌",
            TestStatus.BLOCKED: "🚫"
        }
        return icons.get(status, "❓")
    
    def _get_progress_icon(self, percentage: float) -> str:
        """Get progress icon based on percentage"""
        if percentage >= 100:
            return "✅"
        elif percentage >= 75:
            return "🟢"
        elif percentage >= 50:
            return "🟡"
        elif percentage >= 25:
            return "🟠"
        else:
            return "🔴"
    
    def _get_subsystem_status_icon(self, status: Dict) -> str:
        """Get overall subsystem status icon"""
        if status['completion_percentage'] >= 100:
            return "✅ Complete"
        elif status['pass_percentage'] < status['completion_percentage']:
            return "⚠️ Issues Found"
        elif status['completion_percentage'] > 0:
            return "🔄 In Progress"
        else:
            return "⬜ Not Started"
    
    def _create_progress_bar(self, current: int, total: int, label: str) -> str:
        """Create a text progress bar"""
        if total == 0:
            percentage = 100
        else:
            percentage = (current / total) * 100
        
        bar_length = 30
        filled = int(bar_length * percentage / 100)
        bar = "█" * filled + "░" * (bar_length - filled)
        
        return f"**{label}**: [{bar}] {percentage:.1f}% ({current}/{total})"
    
    def _export_component_matrix_csv(self):
        """Export component verification matrix as CSV"""
        import csv
        
        with open(self.output_dir / "component-matrix.csv", 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Component', 'ID', 'Part Number', 'Status', 
                           'Required Tests', 'Completed Tests', 'Failed Tests',
                           'Completion %', 'Verification Date'])
            
            for comp_id, verification in self.engine.component_verifications.items():
                writer.writerow([
                    verification.component_name,
                    comp_id,
                    verification.part_number,
                    verification.verification_status.value,
                    len(verification.required_tests),
                    len(verification.completed_tests),
                    len(verification.failed_tests),
                    verification.get_completion_percentage(),
                    verification.verification_date.isoformat() if verification.verification_date else ''
                ])
    
    def _export_component_matrix_json(self):
        """Export component verification matrix as JSON"""
        matrix = self.engine.generate_verification_matrix()
        
        with open(self.output_dir / "component-matrix.json", 'w') as f:
            json.dump(matrix, f, indent=2)