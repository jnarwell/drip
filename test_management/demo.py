#!/usr/bin/env python3
"""
Demo script to showcase the test management system functionality
"""
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from test_management.test_management_system import TestManagementSystem
from test_management.component_registry_integration import ComponentRegistryIntegration

def main():
    print("="*80)
    print("DRIP Acoustic Manufacturing - Test Management System Demo")
    print("="*80)
    
    # Initialize the system
    print("\n1. Initializing Test Management System...")
    tms = TestManagementSystem()
    
    # Show summary
    print("\n2. System Summary:")
    tms.show_summary()
    
    # Show critical components
    print("\n3. Critical Component Status:")
    critical_components = [
        "40kHz Transducers",
        "Phase Array Controller",
        "Thermal Cameras",
        "Mean Well RSP-10000-48"
    ]
    
    for component in critical_components:
        tms.show_component_status(component)
    
    # Show next tests
    print("\n4. Next Tests to Execute:")
    tms.show_next_tests(5)
    
    # Simulate test updates
    print("\n5. Simulating Test Execution...")
    test_updates = [
        {"test_id": "TE-001", "status": "IN_PROGRESS", "engineer": "John Doe"},
        {"test_id": "TE-001", "status": "COMPLETE", "result": "PASS", 
         "notes": "All transducers within 40kHz ±100Hz"},
        {"test_id": "TE-007", "status": "COMPLETE", "result": "PASS",
         "notes": "All 6 channels verified at 500W"},
        {"test_id": "TE-016", "status": "IN_PROGRESS", "engineer": "Jane Smith"},
        {"test_id": "TE-041", "status": "COMPLETE", "result": "PASS",
         "notes": "10kW output verified, efficiency >94%"}
    ]
    
    print("\nUpdating test statuses:")
    for update in test_updates:
        tms.update_test(**update)
    
    # Show updated summary
    print("\n6. Updated System Summary:")
    tms.show_summary()
    
    # Check for blocked tests
    print("\n7. Checking for Blocked Tests:")
    tms.show_blocked_tests()
    
    # Generate dashboards
    print("\n8. Generating Verification Dashboards...")
    tms.generate_dashboards()
    
    # Component registry integration
    print("\n9. Component Registry Integration:")
    integration = ComponentRegistryIntegration(tms.engine)
    
    # Show BOM verification report
    bom_report = integration.generate_bom_verification_report()
    print(f"\nBOM Verification Summary:")
    print(f"  Total Components: {bom_report['total_components']}")
    print(f"  Total Cost: ${bom_report['total_cost']:,.2f}")
    print(f"  Verified Cost: ${bom_report['verified_cost']:,.2f}")
    print(f"  Overall Verification: {bom_report['overall_verification_percentage']:.1f}%")
    
    # Show critical components from registry
    print("\n10. Critical Component Risk Assessment:")
    critical = integration.get_critical_components()
    
    print("\n| Component | P/N | Lead Time | Cost | Risk Level |")
    print("|-----------|-----|-----------|------|------------|")
    for comp in critical:
        print(f"| {comp['name'][:20]} | {comp['part_number'][:15]} | "
              f"{comp['lead_time_weeks']}w | ${comp['cost']:,.0f} | {comp['risk_level']} |")
    
    print("\n" + "="*80)
    print("Demo Complete!")
    print(f"\nDashboards available at: docs/verification/")
    print(f"Test report templates at: test_reports/templates/")
    print(f"System state saved at: verification_status/")
    print("="*80)

if __name__ == "__main__":
    main()