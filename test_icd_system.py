#!/usr/bin/env python3
"""
Test ICD system functionality
"""

import os
import sys
from models.interfaces.interface_registry import SYSTEM_INTERFACES, get_interface, get_interfaces_by_subsystem, get_interfaces_by_component
from models.interfaces.icd_generator import ICDGenerator
from models.interfaces.interface_validator import InterfaceValidator

def test_interface_registry():
    """Test interface registry"""
    print("Testing Interface Registry...")
    
    # Test interface retrieval
    icd = get_interface("ICD-001")
    assert icd is not None, "Failed to retrieve ICD-001"
    assert icd.name == "Acoustic-Thermal Interface"
    
    # Test interfaces by subsystem
    acoustic_interfaces = get_interfaces_by_subsystem("Acoustic Cylinder Subsystem")
    assert len(acoustic_interfaces) > 0, "No interfaces found for Acoustic Cylinder Subsystem"
    
    # Test interfaces by component
    transducer_interfaces = get_interfaces_by_component("40kHz Transducers")
    assert len(transducer_interfaces) > 0, "No interfaces found for 40kHz Transducers"
    
    print("✓ Interface registry working")

def test_icd_generation():
    """Test ICD generation"""
    print("Testing ICD Generation...")
    
    generator = ICDGenerator()
    icd = get_interface("ICD-001")
    content = generator.generate_icd(icd)
    
    # Check for required content
    assert "ICD-001" in content, "ICD number missing from generated content"
    assert "Acoustic-Thermal Interface" in content, "Interface name missing from generated content"
    assert "Compatibility Status" in content, "Compatibility analysis missing"
    assert "Risk Assessment" in content, "Risk assessment missing"
    
    print("✓ ICD generation working")

def test_validation():
    """Test interface validation"""
    print("Testing Interface Validation...")
    
    validator = InterfaceValidator()
    valid, results = validator.validate_all_interfaces()
    
    assert isinstance(valid, bool), "Validation should return boolean"
    assert len(results) > 0, "Validation should return results"
    assert len(results) == len(SYSTEM_INTERFACES), "Should validate all interfaces"
    
    # Check result structure
    for result in results:
        assert 'icd' in result, "Result should contain ICD number"
        assert 'name' in result, "Result should contain interface name"
        assert 'valid' in result, "Result should contain validity flag"
        assert 'issues' in result, "Result should contain issues list"
        assert 'warnings' in result, "Result should contain warnings list"
    
    print("✓ Validation working")

def test_component_integration():
    """Test integration with component registry"""
    print("Testing Component Registry Integration...")
    
    # Test that components referenced in interfaces exist
    from models.component_registry import ComponentRegistry
    registry = ComponentRegistry()
    component_names = {c.name for c in registry.components}
    
    missing_components = []
    for interface in SYSTEM_INTERFACES:
        for comp_name in interface.side_a_components + interface.side_b_components:
            if comp_name not in component_names:
                missing_components.append((interface.icd_number, comp_name))
    
    if missing_components:
        print("⚠️  Missing components found:")
        for icd, comp in missing_components:
            print(f"   {icd}: {comp}")
    else:
        print("✓ All interface components exist in registry")

def test_file_generation():
    """Test actual file generation"""
    print("Testing File Generation...")
    
    # Create temporary directory
    test_dir = "test_output"
    os.makedirs(test_dir, exist_ok=True)
    
    try:
        # Generate ICDs
        generator = ICDGenerator()
        generator.generate_all_icds(test_dir)
        
        # Check files were created
        expected_files = [
            "ICD_Summary.md",
            "ICD-001_Acoustic_Thermal_Interface.md",
            "ICD-002_Control_Power_Interface.md",
            "ICD-003_Sensor_Control_Interface.md",
            "ICD-004_Induction_Crucible_Interface.md",
            "ICD-005_Amplifier_Transducer_Interface.md"
        ]
        
        for filename in expected_files:
            filepath = os.path.join(test_dir, filename)
            assert os.path.exists(filepath), f"File {filename} was not created"
            
            # Check file is not empty
            with open(filepath, 'r') as f:
                content = f.read()
                assert len(content) > 0, f"File {filename} is empty"
        
        # Generate validation report
        validator = InterfaceValidator()
        report = validator.generate_validation_report()
        
        report_path = os.path.join(test_dir, "validation_report.md")
        with open(report_path, "w") as f:
            f.write(report)
        
        assert os.path.exists(report_path), "Validation report was not created"
        
        print("✓ File generation working")
        
    finally:
        # Clean up test directory
        import shutil
        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)

def test_interface_completeness():
    """Test interface definition completeness"""
    print("Testing Interface Completeness...")
    
    issues = []
    
    for interface in SYSTEM_INTERFACES:
        # Check basic fields
        if not interface.name:
            issues.append(f"{interface.icd_number}: Missing name")
        
        if not interface.side_a_components:
            issues.append(f"{interface.icd_number}: No side A components")
            
        if not interface.side_b_components:
            issues.append(f"{interface.icd_number}: No side B components")
            
        if not interface.interface_types:
            issues.append(f"{interface.icd_number}: No interface types specified")
            
        if not interface.requirements:
            issues.append(f"{interface.icd_number}: No requirements specified")
        
        # Check requirement completeness
        for req in interface.requirements:
            if not req.verification_method:
                issues.append(f"{interface.icd_number}: Requirement '{req.parameter}' missing verification method")
            
            if req.min_value >= req.max_value:
                issues.append(f"{interface.icd_number}: Invalid range for '{req.parameter}'")
    
    if issues:
        print("⚠️  Interface definition issues found:")
        for issue in issues:
            print(f"   {issue}")
        return False
    else:
        print("✓ All interface definitions complete")
        return True

def run_all_tests():
    """Run all ICD system tests"""
    print("Running ICD System Tests...\n")
    
    tests = [
        test_interface_registry,
        test_icd_generation,
        test_validation,
        test_component_integration,
        test_file_generation,
        test_interface_completeness
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"❌ {test.__name__} failed: {e}")
            failed += 1
        print()
    
    print("=" * 50)
    print(f"Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("✅ All ICD system tests passed!")
        return True
    else:
        print("❌ Some tests failed")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)