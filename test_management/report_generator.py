"""
Test Report Template Generator
Creates standardized test report templates for all tests
"""
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import yaml

from .test_registry import TestRegistry
from .component_test_mapping import ComponentTestMapper
from .data_models import TestDefinition, VerificationType

class ReportGenerator:
    def __init__(self, template_dir: str = "test_reports/templates", 
                 completed_dir: str = "test_reports/completed"):
        self.template_dir = Path(template_dir)
        self.completed_dir = Path(completed_dir)
        self.template_dir.mkdir(parents=True, exist_ok=True)
        self.completed_dir.mkdir(parents=True, exist_ok=True)
        
        self.test_registry = TestRegistry()
        self.component_mapper = ComponentTestMapper()
    
    def generate_test_report_template(self, test_id: str) -> bool:
        """Generate a test report template for a specific test"""
        test_def = self.test_registry.get_test(test_id)
        if not test_def:
            return False
        
        template_content = self._create_template_content(test_def)
        
        # Create filename
        safe_name = test_def.test_name.replace(" ", "_").replace("/", "-")
        filename = f"{test_id}_{safe_name}.md"
        filepath = self.template_dir / filename
        
        with open(filepath, 'w') as f:
            f.write(template_content)
        
        return True
    
    def _create_template_content(self, test_def: TestDefinition) -> str:
        """Create the markdown content for a test report template"""
        
        # Create YAML frontmatter
        frontmatter = {
            'test_id': test_def.test_id,
            'test_name': test_def.test_name,
            'test_purpose': test_def.test_purpose,
            'verification_type': test_def.verification_type.value,
            'components_verified': [
                {
                    'name': comp,
                    'id': comp.replace(" ", "_").upper(),
                    'part_number': 'TBD'
                } for comp in test_def.target_components
            ],
            'prerequisite_tests': test_def.prerequisite_tests,
            'enables_tests': test_def.enables_tests,
            'estimated_duration': f"{test_def.estimated_duration_hours} hours",
            'required_equipment': test_def.required_equipment,
            'status': 'NOT_STARTED',
            'date_executed': None,
            'test_engineer': None,
            'result': None
        }
        
        # Create the template content
        content = f"""---
{yaml.dump(frontmatter, default_flow_style=False, sort_keys=False)}---

# Test Report: {test_def.test_id} - {test_def.test_name}

## 1.0 Test Information

### 1.1 Test Overview
- **Test ID**: {test_def.test_id}
- **Test Name**: {test_def.test_name}
- **Purpose**: {test_def.test_purpose}
- **Type**: {test_def.verification_type.value}
- **Duration**: {test_def.estimated_duration_hours} hours
- **Date Executed**: _[To be filled]_
- **Test Engineer**: _[To be filled]_

### 1.2 Components Under Test
{self._format_components_table(test_def.target_components)}

### 1.3 Prerequisites
{self._format_prerequisites(test_def.prerequisite_tests)}

### 1.4 Test Dependencies
This test enables the following tests:
{self._format_enables_list(test_def.enables_tests)}

## 2.0 Test Setup

### 2.1 Required Equipment
{self._format_equipment_list(test_def.required_equipment)}

### 2.2 Environmental Conditions
- **Temperature**: _[Record ambient temperature]_ °C
- **Humidity**: _[Record relative humidity]_ %
- **Other Conditions**: _[Note any relevant conditions]_

### 2.3 Test Configuration
_[Describe the specific test setup, including:]_
- Hardware configuration
- Software versions
- Calibration status
- Special fixtures or adapters

### 2.4 Pre-Test Checklist
- [ ] All equipment calibrated and within calibration date
- [ ] Test area cleared and safe
- [ ] Data recording systems ready
- [ ] Safety equipment available
- [ ] Test procedure reviewed
- [ ] Components inspected for damage

## 3.0 Test Procedure

### 3.1 Setup Steps
1. _[Step 1 description]_
2. _[Step 2 description]_
3. _[Continue as needed]_

### 3.2 Test Execution Steps
1. **Initial Baseline**
   - _[Measurement/observation]_
   - Expected: _[value/condition]_
   - Actual: _[to be filled]_

2. **Main Test Sequence**
   - _[Detailed step]_
   - Expected: _[value/condition]_
   - Actual: _[to be filled]_

3. **Additional Steps**
   - _[Continue as needed]_

### 3.3 Data Collection Points
| Parameter | Expected Value | Measured Value | Pass/Fail |
|-----------|---------------|----------------|-----------|
| _[Parameter 1]_ | _[Expected]_ | _[Actual]_ | _[P/F]_ |
| _[Parameter 2]_ | _[Expected]_ | _[Actual]_ | _[P/F]_ |
| _[Add rows as needed]_ | | | |

## 4.0 Test Results

### 4.1 Summary Results
- **Overall Result**: _[PASS/FAIL/CONDITIONAL]_
- **Test Completion**: _[Percentage of test completed]_
- **Major Findings**: _[Brief summary]_

### 4.2 Detailed Results
{self._create_results_table_template(test_def)}

### 4.3 Deviations and Anomalies
_[Document any deviations from expected results or test procedure]_

### 4.4 Issues Encountered
| Issue # | Description | Impact | Resolution |
|---------|-------------|--------|------------|
| 1 | _[Issue description]_ | _[Impact on test]_ | _[How resolved]_ |
| _[Add rows as needed]_ | | | |

## 5.0 Data Analysis

### 5.1 Performance Metrics
_[Analyze key performance indicators]_

### 5.2 Trends and Patterns
_[Identify any trends in the data]_

### 5.3 Comparison to Requirements
_[Compare results to specified requirements]_

### 5.4 Statistical Analysis
_[If applicable, include statistical analysis of results]_

## 6.0 Conclusions and Recommendations

### 6.1 Test Conclusions
_[Summarize what was learned from the test]_

### 6.2 Component Verification Status
{self._create_verification_status_table(test_def.target_components)}

### 6.3 Recommendations
1. _[Recommendation 1]_
2. _[Recommendation 2]_
3. _[Continue as needed]_

### 6.4 Follow-up Actions
- [ ] _[Action item 1]_
- [ ] _[Action item 2]_
- [ ] _[Continue as needed]_

### 6.5 Next Steps
_[Describe next tests or actions based on these results]_

---

## Appendices

### Appendix A: Raw Data
_[Reference to data files or include key data]_

### Appendix B: Calibration Certificates
_[Reference to equipment calibration records]_

### Appendix C: Photos/Screenshots
_[Include relevant visual documentation]_

### Appendix D: Additional Documentation
_[Reference any additional supporting documents]_

---

**Report Prepared By**: _[Name]_  
**Date**: _[Date]_  
**Reviewed By**: _[Name]_  
**Date**: _[Date]_  
**Approved By**: _[Name]_  
**Date**: _[Date]_
"""
        return content
    
    def _format_components_table(self, components: List[str]) -> str:
        """Format components as a markdown table"""
        if not components:
            return "_No components specified_"
        
        table = "| Component | ID | Part Number | Serial Number |\n"
        table += "|-----------|----|--------------|--------------|\n"
        
        for comp in components:
            comp_id = comp.replace(" ", "_").upper()
            table += f"| {comp} | {comp_id} | _[TBD]_ | _[Record S/N]_ |\n"
        
        return table
    
    def _format_prerequisites(self, prereqs: List[str]) -> str:
        """Format prerequisite tests"""
        if not prereqs:
            return "_No prerequisite tests required_"
        
        content = "The following tests must be completed before this test:\n"
        for prereq in prereqs:
            test_def = self.test_registry.get_test(prereq)
            if test_def:
                content += f"- **{prereq}**: {test_def.test_name}\n"
            else:
                content += f"- **{prereq}**: _Unknown test_\n"
        
        return content
    
    def _format_enables_list(self, enables: List[str]) -> str:
        """Format list of tests enabled by this test"""
        if not enables:
            return "_This test does not enable any other tests_"
        
        content = ""
        for test_id in enables:
            test_def = self.test_registry.get_test(test_id)
            if test_def:
                content += f"- **{test_id}**: {test_def.test_name}\n"
            else:
                content += f"- **{test_id}**: _Unknown test_\n"
        
        return content
    
    def _format_equipment_list(self, equipment: List[str]) -> str:
        """Format required equipment as a checklist"""
        if not equipment:
            return "_No special equipment required_"
        
        content = ""
        for item in equipment:
            content += f"- [ ] {item}\n"
        
        return content
    
    def _create_results_table_template(self, test_def: TestDefinition) -> str:
        """Create a results table template based on test type"""
        
        if test_def.verification_type == VerificationType.ACCEPTANCE:
            return """| Specification | Requirement | Measured | Pass/Fail |
|---------------|-------------|----------|-----------|
| _[Spec 1]_ | _[Requirement]_ | _[Actual]_ | _[P/F]_ |
| _[Spec 2]_ | _[Requirement]_ | _[Actual]_ | _[P/F]_ |
| _[Add rows as needed]_ | | | |"""
        
        elif test_def.verification_type == VerificationType.PERFORMANCE:
            return """| Parameter | Target | Minimum | Maximum | Measured | Pass/Fail |
|-----------|--------|---------|---------|----------|-----------|
| _[Param 1]_ | _[Target]_ | _[Min]_ | _[Max]_ | _[Actual]_ | _[P/F]_ |
| _[Param 2]_ | _[Target]_ | _[Min]_ | _[Max]_ | _[Actual]_ | _[P/F]_ |
| _[Add rows as needed]_ | | | | | |"""
        
        elif test_def.verification_type == VerificationType.INTEGRATION:
            return """| Interface | Signal/Data | Expected | Actual | Pass/Fail |
|-----------|-------------|----------|--------|-----------|
| _[Interface 1]_ | _[Signal]_ | _[Expected]_ | _[Actual]_ | _[P/F]_ |
| _[Interface 2]_ | _[Signal]_ | _[Expected]_ | _[Actual]_ | _[P/F]_ |
| _[Add rows as needed]_ | | | | |"""
        
        elif test_def.verification_type == VerificationType.SAFETY:
            return """| Safety Feature | Trigger Condition | Expected Response | Actual Response | Pass/Fail |
|----------------|-------------------|-------------------|-----------------|-----------|
| _[Feature 1]_ | _[Condition]_ | _[Expected]_ | _[Actual]_ | _[P/F]_ |
| _[Feature 2]_ | _[Condition]_ | _[Expected]_ | _[Actual]_ | _[P/F]_ |
| _[Add rows as needed]_ | | | | |"""
        
        else:  # Default table
            return """| Test Item | Expected Result | Actual Result | Pass/Fail |
|-----------|-----------------|---------------|-----------|
| _[Item 1]_ | _[Expected]_ | _[Actual]_ | _[P/F]_ |
| _[Item 2]_ | _[Expected]_ | _[Actual]_ | _[P/F]_ |
| _[Add rows as needed]_ | | | |"""
    
    def _create_verification_status_table(self, components: List[str]) -> str:
        """Create component verification status table"""
        if not components:
            return "_No components to verify_"
        
        table = "| Component | Verification Status | Notes |\n"
        table += "|-----------|--------------------|---------|\n"
        
        for comp in components:
            table += f"| {comp} | _[Status after test]_ | _[Any notes]_ |\n"
        
        return table
    
    def generate_all_templates(self) -> Dict[str, bool]:
        """Generate templates for all tests"""
        results = {}
        
        for test_id in self.test_registry.tests:
            success = self.generate_test_report_template(test_id)
            results[test_id] = success
            
        return results
    
    def get_template_path(self, test_id: str) -> Optional[Path]:
        """Get the path to a test template"""
        test_def = self.test_registry.get_test(test_id)
        if not test_def:
            return None
        
        safe_name = test_def.test_name.replace(" ", "_").replace("/", "-")
        filename = f"{test_id}_{safe_name}.md"
        filepath = self.template_dir / filename
        
        return filepath if filepath.exists() else None
    
    def list_templates(self) -> List[Dict[str, str]]:
        """List all available templates"""
        templates = []
        
        for template_file in self.template_dir.glob("*.md"):
            # Extract test ID from filename
            test_id = template_file.stem.split("_")[0]
            
            templates.append({
                "test_id": test_id,
                "filename": template_file.name,
                "path": str(template_file)
            })
        
        return sorted(templates, key=lambda x: x["test_id"])