# Quick Start Guide

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Git
- 10GB free disk space

### Installation

```bash
# Clone the repository
git clone https://github.com/jnarwell/drip.git
cd drip/acoustic-sysml-v2

# Install dependencies
pip install -r requirements.txt

# Generate documentation
python generate_mkdocs.py

# Serve locally
mkdocs serve
```

### Project Structure

```
acoustic-sysml-v2/
├── models/              # Component and system models
│   ├── component_registry.py
│   └── interfaces/      # ICD definitions
├── icds/               # Generated ICDs
├── analysis/           # Analysis and simulations
├── verification/       # Test procedures
├── docs/              # Documentation source
└── site/              # Generated documentation
```

## 📋 Development Workflow

1. **Requirements Review** → [System Requirements](system/requirements.md)
2. **Component Selection** → [Component Registry](components/index.md)
3. **Interface Definition** → [ICDs](icds/index.md)
4. **Design Verification** → [Test Matrix](verification/matrix.md)
5. **Integration Testing** → [Test Reports](verification/reports.md)

## 🔧 Common Tasks

### Adding a Component

```python
from models.component_registry import Component, ComponentCategory, ComponentType

new_component = Component(
    name="New Part",
    category=ComponentCategory.ACOUSTIC,
    type=ComponentType.COTS,
    specification="Part Number",
    quantity=1,
    unit_cost=100.00,
    total_cost=100.00,
    supplier="Supplier Name"
)
```

### Generating ICDs

```bash
# Generate all ICDs
python generate_documentation.py

# Generate specific ICD
from models.interfaces.icd_generator import ICDGenerator
generator = ICDGenerator()
generator.generate_all_icds()
```

### Running Tests

```bash
# Run ICD system tests
python test_icd_system.py

# Validate interfaces
from models.interfaces.interface_validator import InterfaceValidator
validator = InterfaceValidator()
report = validator.generate_validation_report()
```

## 📚 Key Resources

- [Component Database](components/index.md)
- [Interface Specifications](icds/index.md)
- [Power Budget Analysis](analysis/power.md)
- [Thermal Analysis](analysis/thermal.md)
- [API Reference](api/index.md)
- [Glossary](resources/glossary.md)

## 🛠️ Troubleshooting

### Common Issues

**Import errors when running scripts**
: Add the project root to your Python path:
  ```python
  import sys
  sys.path.append('/path/to/acoustic-sysml-v2')
  ```

**MkDocs serve fails**
: Ensure all dependencies are installed:
  ```bash
  pip install -r requirements.txt
  ```

**Documentation not updating**
: Regenerate the documentation:
  ```bash
  python generate_mkdocs.py
  mkdocs build --clean
  ```
