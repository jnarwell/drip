# API Reference

## Component Registry API

### Classes

#### `ComponentRegistry`
Main registry containing all system components.

```python
class ComponentRegistry:
    def __init__(self):
        """Initialize registry with all components"""
    
    def get_components_by_category(self, category: ComponentCategory) -> List[Component]:
        """Get all components in a category"""
    
    def calculate_power_budget(self) -> Dict[str, Dict[str, float]]:
        """Calculate power consumption by subsystem"""
    
    def validate_thermal_design(self) -> Dict[str, Any]:
        """Validate thermal management requirements"""
```

#### `Component`
Individual component data structure.

```python
@dataclass
class Component:
    name: str
    category: ComponentCategory
    type: ComponentType
    specification: str
    quantity: int
    unit_cost: float
    total_cost: float
    supplier: str
    tech_specs: Optional[TechnicalSpecs] = None
```

#### `TechnicalSpecs`
Detailed technical specifications.

```python
@dataclass
class TechnicalSpecs:
    # Electrical
    power_consumption: Optional[float] = None  # Watts
    power_supply: Optional[float] = None  # Watts (for PSUs)
    voltage_nominal: Optional[float] = None  # V
    
    # Physical
    weight: Optional[float] = None  # kg
    dimensions: Optional[Dict[str, float]] = None  # mm
    
    # Thermal
    operating_temp: Optional[Tuple[float, float]] = None  # (min, max) °C
    max_temp: Optional[float] = None  # °C
    
    # Performance
    efficiency: Optional[float] = None  # %
    frequency: Optional[float] = None  # Hz
```

### Enumerations

#### `ComponentCategory`
```python
class ComponentCategory(Enum):
    FRAME = "Frame Subsystem"
    HEATED_BED = "Heated Bed Subsystem"
    ACOUSTIC = "Acoustic Cylinder Subsystem"
    CRUCIBLE = "Crucible Subsystem"
    POWER_CONTROL = "Power/Control Subsystem"
```

#### `ComponentType`
```python
class ComponentType(Enum):
    COTS = "Commercial Off-The-Shelf"
    CUSTOM = "Custom Fabricated"
```

### Usage Examples

#### Getting Components
```python
from models.component_registry import ComponentRegistry, ComponentCategory

# Initialize registry
registry = ComponentRegistry()

# Get all acoustic components
acoustic_components = [
    c for c in registry.components 
    if c.category == ComponentCategory.ACOUSTIC
]

# Get total cost
total_cost = sum(c.total_cost for c in registry.components)
```

#### Power Analysis
```python
# Calculate power budget
power_budget = registry.calculate_power_budget()

# Get net power consumption
net_power = power_budget['TOTAL']['net_power']
print(f"Net power consumption: {net_power}W")

# Check thermal dissipation
thermal_validation = registry.validate_thermal_design()
total_heat = thermal_validation['total_heat_generation']
```

## Interface Registry API

### Classes

#### `Interface`
Interface Control Document data structure.

```python
@dataclass
class Interface:
    icd_number: str
    name: str
    side_a_subsystem: str
    side_a_components: List[str]
    side_b_subsystem: str
    side_b_components: List[str]
    interface_types: List[InterfaceType]
    criticality: InterfaceCriticality
    requirements: List[InterfaceRequirement] = field(default_factory=list)
```

#### `InterfaceRequirement`
```python
@dataclass
class InterfaceRequirement:
    parameter: str
    nominal: float
    min_value: float
    max_value: float
    units: str
    verification_method: str
```

### Functions

#### `get_interface(icd_number: str) -> Optional[Interface]`
Retrieve interface by ICD number.

#### `get_interfaces_by_subsystem(subsystem: str) -> List[Interface]`
Get all interfaces involving a subsystem.

### Usage Examples

```python
from models.interfaces.interface_registry import get_interface, SYSTEM_INTERFACES

# Get specific interface
icd = get_interface("ICD-001")
print(f"Interface: {icd.name}")
print(f"Criticality: {icd.criticality.value}")

# Check requirements
for req in icd.requirements:
    print(f"{req.parameter}: {req.nominal} {req.units}")
```

## ICD Generator API

### Classes

#### `ICDGenerator`
Generate Interface Control Documents.

```python
class ICDGenerator:
    def generate_icd(self, interface: Interface) -> str:
        """Generate complete ICD document"""
    
    def generate_all_icds(self, output_dir: str = "icds/generated"):
        """Generate all system ICDs"""
```

### Usage Examples

```python
from models.interfaces.icd_generator import ICDGenerator
from models.interfaces.interface_registry import get_interface

# Generate single ICD
generator = ICDGenerator()
icd = get_interface("ICD-001")
content = generator.generate_icd(icd)

# Generate all ICDs
generator.generate_all_icds()
```

## Interface Validator API

### Classes

#### `InterfaceValidator`
Validate interface compatibility.

```python
class InterfaceValidator:
    def validate_interface(self, interface: Interface) -> Tuple[bool, List[str]]:
        """Validate single interface"""
    
    def validate_all_interfaces(self) -> Tuple[bool, List[Dict]]:
        """Validate all system interfaces"""
    
    def generate_validation_report(self) -> str:
        """Generate validation report"""
```

### Usage Examples

```python
from models.interfaces.interface_validator import InterfaceValidator

# Validate all interfaces
validator = InterfaceValidator()
valid, results = validator.validate_all_interfaces()

if not valid:
    for result in results:
        if not result['valid']:
            print(f"{result['icd']}: {len(result['issues'])} issues")

# Generate report
report = validator.generate_validation_report()
```

## Utility Functions

### Power Calculations
```python
def calculate_net_power(consumption: float, supply: float) -> float:
    """Calculate net power requirement"""
    return consumption - supply
```

### Temperature Conversions
```python
def celsius_to_fahrenheit(celsius: float) -> float:
    """Convert Celsius to Fahrenheit"""
    return celsius * 9/5 + 32

def fahrenheit_to_celsius(fahrenheit: float) -> float:
    """Convert Fahrenheit to Celsius"""
    return (fahrenheit - 32) * 5/9
```

### Acoustic Calculations
```python
def wavelength(frequency: float, speed: float = 343) -> float:
    """Calculate wavelength from frequency"""
    return speed / frequency

def pressure_to_db(pressure: float, reference: float = 20e-6) -> float:
    """Convert pressure to decibels"""
    return 20 * math.log10(pressure / reference)
```
