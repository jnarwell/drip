"""
Setup imports for Jupyter notebooks
Run this first to ensure all imports work correctly
"""

import sys
import os

# Get the project root directory
notebook_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(notebook_dir)

# Add to Python path if not already there
if project_root not in sys.path:
    sys.path.insert(0, project_root)

print(f"Python path configured:")
print(f"  Project root: {project_root}")
print(f"  Notebook dir: {notebook_dir}")

# Test imports
try:
    from models.component_library import component_database
    from models.custom_parts_library import custom_parts_database
    from models.complete_bom_generator import generate_complete_bom
    print("\n✓ All imports successful!")
except ImportError as e:
    print(f"\n✗ Import error: {e}")
    print("\nTroubleshooting:")
    print(f"1. Check if files exist:")
    print(f"   - {os.path.join(project_root, 'models', 'component_library.py')}")
    print(f"   - {os.path.join(project_root, 'models', 'custom_parts_library.py')}")
    print(f"   - {os.path.join(project_root, 'models', 'complete_bom_generator.py')}")