"""
Interface Registry for Acoustic Manufacturing System
Links components from component_registry to formal interface definitions
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum
import json
from datetime import datetime

class InterfaceType(Enum):
    MECHANICAL = "mechanical"
    ELECTRICAL = "electrical"
    THERMAL = "thermal"
    DATA = "data"
    FLUID = "fluid"
    ACOUSTIC = "acoustic"

class InterfaceCriticality(Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

@dataclass
class InterfaceRequirement:
    """Single interface requirement"""
    parameter: str
    nominal: float
    min_value: float
    max_value: float
    units: str
    verification_method: str

@dataclass
class Interface:
    """Interface Control Document data structure"""
    icd_number: str
    name: str
    # Interface endpoints
    side_a_subsystem: str
    side_a_components: List[str]  # Component names from registry
    side_b_subsystem: str
    side_b_components: List[str]
    # Interface characteristics
    interface_types: List[InterfaceType]
    criticality: InterfaceCriticality
    
    revision: str = "1.0"
    date: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))
    
    # Requirements
    requirements: List[InterfaceRequirement] = field(default_factory=list)
    
    # Physical interface
    mechanical_details: Optional[Dict] = None
    electrical_details: Optional[Dict] = None
    thermal_details: Optional[Dict] = None
    
    # Verification
    verification_procedure: str = ""
    test_equipment: List[str] = field(default_factory=list)
    
    # Status tracking
    status: str = "Draft"
    approved_by: List[str] = field(default_factory=list)
    
    def to_dict(self) -> dict:
        """Convert to dictionary for serialization"""
        return {
            'icd_number': self.icd_number,
            'name': self.name,
            'revision': self.revision,
            'date': self.date,
            'side_a': {
                'subsystem': self.side_a_subsystem,
                'components': self.side_a_components
            },
            'side_b': {
                'subsystem': self.side_b_subsystem,
                'components': self.side_b_components
            },
            'interface_types': [t.value for t in self.interface_types],
            'criticality': self.criticality.value,
            'requirements': [
                {
                    'parameter': r.parameter,
                    'nominal': r.nominal,
                    'min': r.min_value,
                    'max': r.max_value,
                    'units': r.units,
                    'verification': r.verification_method
                } for r in self.requirements
            ],
            'status': self.status
        }

# Define all system interfaces
SYSTEM_INTERFACES = [
    Interface(
        icd_number="ICD-001",
        name="Acoustic-Thermal Interface",
        side_a_subsystem="Acoustic Cylinder Subsystem",
        side_a_components=["Acoustic Cylinder", "Transducer Array Layer", "40kHz Transducers"],
        side_b_subsystem="Heated Bed Subsystem",
        side_b_components=["Chamber Assembly", "Thermal Isolation Tube"],
        interface_types=[InterfaceType.MECHANICAL, InterfaceType.THERMAL, InterfaceType.ACOUSTIC],
        criticality=InterfaceCriticality.HIGH,
        requirements=[
            InterfaceRequirement(
                parameter="Acoustic Transmission",
                nominal=85, min_value=80, max_value=100,
                units="%",
                verification_method="Hydrophone measurement"
            ),
            InterfaceRequirement(
                parameter="Thermal Leakage",
                nominal=50, min_value=0, max_value=100,
                units="W",
                verification_method="Thermal imaging"
            ),
            InterfaceRequirement(
                parameter="Transducer Temperature",
                nominal=40, min_value=20, max_value=60,
                units="°C",
                verification_method="Thermocouple monitoring"
            ),
        ],
        mechanical_details={
            'mounting_plane': 'Z=150mm',
            'bolt_pattern': '6x M6 on 140mm PCD',
            'flatness': '0.05mm over 140mm',
            'alignment': '±0.1mm to centerline'
        },
        thermal_details={
            'barrier_material': 'Alumina ceramic',
            'barrier_thickness': '10mm',
            'max_gradient': '100°C/mm',
            'cooling_required': '2L/min water'
        },
        test_equipment=["Hydrophone array", "Thermal camera", "Thermocouples"]
    ),
    
    Interface(
        icd_number="ICD-002",
        name="Control-Power Interface",
        side_a_subsystem="Power/Control Subsystem",
        side_a_components=["Cyclone IV FPGA Board", "STM32 Dev Board"],
        side_b_subsystem="Power/Control Subsystem",
        side_b_components=["10kW PSU", "48V DC Power Supply", "12V DC Power Supply"],
        interface_types=[InterfaceType.ELECTRICAL, InterfaceType.DATA],
        criticality=InterfaceCriticality.HIGH,
        requirements=[
            InterfaceRequirement(
                parameter="Supply Voltage",
                nominal=48, min_value=45, max_value=52,
                units="VDC",
                verification_method="Multimeter measurement"
            ),
            InterfaceRequirement(
                parameter="Peak Current",
                nominal=100, min_value=0, max_value=125,
                units="A",
                verification_method="Current probe measurement"
            ),
            InterfaceRequirement(
                parameter="Data Rate",
                nominal=1000, min_value=100, max_value=2000,
                units="kbps",
                verification_method="Oscilloscope measurement"
            ),
        ],
        electrical_details={
            'connector_type': 'Phoenix Contact MSTB 2.5',
            'wire_gauge': 'AWG 12',
            'voltage_isolation': '2.5kV',
            'protection': 'Overcurrent, overvoltage'
        },
        test_equipment=["Digital multimeter", "Current probe", "Oscilloscope"]
    ),
    
    Interface(
        icd_number="ICD-003",
        name="Sensor-Control Interface",
        side_a_subsystem="Crucible Subsystem",
        side_a_components=["Optris PI 1M Thermal Camera"],
        side_b_subsystem="Power/Control Subsystem",
        side_b_components=["Industrial PC"],
        interface_types=[InterfaceType.DATA, InterfaceType.ELECTRICAL],
        criticality=InterfaceCriticality.MEDIUM,
        requirements=[
            InterfaceRequirement(
                parameter="Data Rate",
                nominal=32, min_value=30, max_value=1000,
                units="Hz",
                verification_method="Network analyzer"
            ),
            InterfaceRequirement(
                parameter="Latency",
                nominal=5, min_value=0, max_value=10,
                units="ms",
                verification_method="Oscilloscope measurement"
            ),
            InterfaceRequirement(
                parameter="Supply Voltage",
                nominal=24, min_value=20, max_value=28,
                units="VDC",
                verification_method="Multimeter measurement"
            ),
        ],
        electrical_details={
            'interface': 'Gigabit Ethernet',
            'connector': 'RJ45',
            'cable_type': 'Cat6A shielded',
            'max_distance': '100m'
        },
        test_equipment=["Network analyzer", "Ethernet tester", "Multimeter"]
    ),
    
    Interface(
        icd_number="ICD-004",
        name="Induction-Crucible Interface",
        side_a_subsystem="Crucible Subsystem",
        side_a_components=["Induction Heater", "Induction Coil Assembly"],
        side_b_subsystem="Crucible Subsystem",
        side_b_components=["Crucible Assembly", "Material Feed System"],
        interface_types=[InterfaceType.THERMAL, InterfaceType.ELECTRICAL, InterfaceType.MECHANICAL],
        criticality=InterfaceCriticality.HIGH,
        requirements=[
            InterfaceRequirement(
                parameter="Heating Power",
                nominal=3000, min_value=1000, max_value=3500,
                units="W",
                verification_method="Power meter measurement"
            ),
            InterfaceRequirement(
                parameter="Temperature Uniformity",
                nominal=5, min_value=0, max_value=10,
                units="°C",
                verification_method="Thermal mapping"
            ),
            InterfaceRequirement(
                parameter="Coil Current",
                nominal=15, min_value=5, max_value=20,
                units="A",
                verification_method="Current probe"
            ),
        ],
        thermal_details={
            'operating_temp': '1200-1500°C',
            'ramp_rate': '50°C/min max',
            'insulation': 'Ceramic fiber composite',
            'cooling': 'Water jacket required'
        },
        mechanical_details={
            'coil_clearance': '25mm minimum',
            'mounting': 'Fixed ceramic supports',
            'access_ports': '4x 50mm diameter'
        },
        test_equipment=["Power meter", "Thermal camera", "Current probe", "Thermocouples"]
    ),
    
    Interface(
        icd_number="ICD-005",
        name="Amplifier-Transducer Interface",
        side_a_subsystem="Power/Control Subsystem",
        side_a_components=["6-Channel Amp Modules", "Control Bus PCB"],
        side_b_subsystem="Acoustic Cylinder Subsystem",
        side_b_components=["40kHz Transducers", "Transducer Array Layer"],
        interface_types=[InterfaceType.ELECTRICAL, InterfaceType.ACOUSTIC],
        criticality=InterfaceCriticality.HIGH,
        requirements=[
            InterfaceRequirement(
                parameter="Drive Frequency",
                nominal=40000, min_value=39000, max_value=41000,
                units="Hz",
                verification_method="Frequency counter"
            ),
            InterfaceRequirement(
                parameter="Drive Voltage",
                nominal=120, min_value=100, max_value=150,
                units="Vrms",
                verification_method="Oscilloscope measurement"
            ),
            InterfaceRequirement(
                parameter="Acoustic Power",
                nominal=10, min_value=8, max_value=15,
                units="W/transducer",
                verification_method="Hydrophone calibration"
            ),
        ],
        electrical_details={
            'impedance': '50 ohms',
            'connector': 'BNC',
            'cable_type': 'RG-58 coaxial',
            'max_length': '3m'
        },
        test_equipment=["Function generator", "Oscilloscope", "Power meter", "Hydrophone"]
    ),
]

def get_interface(icd_number: str) -> Optional[Interface]:
    """Retrieve interface by ICD number"""
    for interface in SYSTEM_INTERFACES:
        if interface.icd_number == icd_number:
            return interface
    return None

def get_interfaces_by_subsystem(subsystem: str) -> List[Interface]:
    """Get all interfaces involving a subsystem"""
    interfaces = []
    for interface in SYSTEM_INTERFACES:
        if (interface.side_a_subsystem == subsystem or 
            interface.side_b_subsystem == subsystem):
            interfaces.append(interface)
    return interfaces

def get_interfaces_by_component(component_name: str) -> List[Interface]:
    """Get all interfaces involving a specific component"""
    interfaces = []
    for interface in SYSTEM_INTERFACES:
        if (component_name in interface.side_a_components or 
            component_name in interface.side_b_components):
            interfaces.append(interface)
    return interfaces