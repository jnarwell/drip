#!/usr/bin/env python3
"""
Script to generate all test report templates
"""
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from test_management.report_generator import ReportGenerator

def main():
    print("Generating test report templates...")
    
    # Create report generator
    generator = ReportGenerator()
    
    # Generate all templates
    results = generator.generate_all_templates()
    
    # Count successes
    successful = sum(1 for success in results.values() if success)
    total = len(results)
    
    print(f"\nGenerated {successful}/{total} test report templates")
    
    # List any failures
    failures = [test_id for test_id, success in results.items() if not success]
    if failures:
        print("\nFailed to generate templates for:")
        for test_id in failures:
            print(f"  - {test_id}")
    else:
        print("\nAll templates generated successfully!")
    
    # Show template location
    print(f"\nTemplates saved to: {generator.template_dir}")

if __name__ == "__main__":
    main()