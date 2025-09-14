"""
Unified Component Registry for Acoustic Manufacturing System
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Tuple, Any
from enum import Enum


class ComponentCategory(Enum):
    FRAME = "Frame Subsystem"
    HEATED_BED = "Heated Bed Subsystem"
    ACOUSTIC = "Acoustic Cylinder Subsystem"
    CRUCIBLE = "Crucible Subsystem"
    POWER_CONTROL = "Power/Control Subsystem"


class ComponentType(Enum):
    COTS = "Commercial Off-The-Shelf"
    CUSTOM = "Custom Fabricated"


@dataclass
class TechnicalSpecs:
    """Detailed technical specifications for components"""
    # Electrical
    power_consumption: Optional[float] = None  # Watts
    voltage_nominal: Optional[float] = None  # V
    voltage_range: Optional[Tuple[float, float]] = None  # (min, max) V
    current_draw: Optional[float] = None  # A
    
    # Physical
    weight: Optional[float] = None  # kg
    dimensions: Optional[Dict[str, float]] = None  # {'L': mm, 'W': mm, 'H': mm, 'D': mm}
    mounting_type: Optional[str] = None
    material_spec: Optional[str] = None
    
    # Thermal
    operating_temp: Optional[Tuple[float, float]] = None  # (min, max) °C
    max_temp: Optional[float] = None  # °C
    thermal_dissipation: Optional[float] = None  # W
    cooling_required: Optional[str] = None  # "none", "passive", "forced air", "liquid"
    
    # Performance
    efficiency: Optional[float] = None  # %
    frequency: Optional[float] = None  # Hz (for acoustic/electrical components)
    accuracy: Optional[float] = None  # ± value
    flow_rate: Optional[float] = None  # L/min or CFM
    
    # Interfaces
    connections: Optional[List[str]] = None
    control_signal: Optional[str] = None


@dataclass
class Component:
    """Base component class for all system components"""
    name: str
    category: ComponentCategory
    type: ComponentType
    specification: str
    quantity: int
    unit_cost: float
    total_cost: float
    notes: str
    
    # Expansion tracking parameters
    requires_expansion: bool = False
    expansion_notes: str = ""
    
    # Additional metadata
    part_number: Optional[str] = None
    supplier: Optional[str] = None
    lead_time_weeks: Optional[int] = None
    material: Optional[str] = None
    process: Optional[str] = None
    
    # Technical specifications
    tech_specs: TechnicalSpecs = field(default_factory=TechnicalSpecs)


class ComponentRegistry:
    """Central registry for all system components"""
    
    def __init__(self):
        self.components: List[Component] = []
        self._initialize_components()
    
    def _initialize_components(self):
        """Initialize all components from Level 1 BOM"""
        
        # FRAME SUBSYSTEM - COTS
        self.components.extend([
            Component(
                name="Kapton Tubes",
                category=ComponentCategory.FRAME,
                type=ComponentType.COTS,
                specification="DuPont HN, 4\" dia, 0.005\" wall, 400°C",
                quantity=2,
                unit_cost=90,
                total_cost=180,
                notes="Thermal isolation barrier",
                requires_expansion=False,
                expansion_notes="",
                tech_specs=TechnicalSpecs(
                    power_consumption=0,  # Passive component
                    weight=0.045,  # kg per tube
                    dimensions={'D': 101.6, 'wall': 0.127, 'L': 150},  # mm
                    operating_temp=(-269, 400),  # °C
                    max_temp=400,
                    material_spec="DuPont Kapton HN polyimide film",
                    thermal_dissipation=0,
                    cooling_required="none"
                )
            ),
            Component(
                name="Assembly Rails",
                category=ComponentCategory.FRAME,
                type=ComponentType.COTS,
                specification="1/2\" zinc threaded rod, 12\" length",
                quantity=4,
                unit_cost=2.50,
                total_cost=10,
                notes="For mounting acoustic rings",
                requires_expansion=False,
                expansion_notes="",
                tech_specs=TechnicalSpecs(
                    power_consumption=0,
                    weight=0.15,  # kg per rod
                    dimensions={'D': 12.7, 'L': 304.8},  # mm (1/2" x 12")
                    material_spec="Zinc-plated steel, Grade 5",
                    operating_temp=(-40, 200),
                    mounting_type="M12 threaded full length"
                )
            ),
        ])
        
        # FRAME SUBSYSTEM - Custom
        self.components.extend([
            Component(
                name="Frame",
                category=ComponentCategory.FRAME,
                type=ComponentType.CUSTOM,
                specification="Steel weldment, powder coated",
                quantity=1,
                unit_cost=800,
                total_cost=800,
                notes="Main structural support",
                material="Steel",
                process="Welding",
                requires_expansion=False,
                expansion_notes="",
                tech_specs=TechnicalSpecs(
                    power_consumption=0,
                    weight=25.0,  # kg
                    dimensions={'L': 500, 'W': 500, 'H': 800},  # mm
                    material_spec="Steel tube 40x40x3mm, powder coated",
                    operating_temp=(-20, 150),
                    mounting_type="Floor standing with leveling feet"
                )
            ),
            Component(
                name="Baseplate",
                category=ComponentCategory.FRAME,
                type=ComponentType.CUSTOM,
                specification="1/2\" aluminum, machined",
                quantity=1,
                unit_cost=400,
                total_cost=400,
                notes="Precision mounting surface",
                material="Aluminum",
                process="CNC Machining",
                requires_expansion=False,
                expansion_notes="",
                tech_specs=TechnicalSpecs(
                    power_consumption=0,
                    weight=8.5,  # kg
                    dimensions={'L': 400, 'W': 400, 'H': 12.7},  # mm
                    material_spec="6061-T6 Aluminum, flatness 0.05mm",
                    operating_temp=(-50, 200),
                    mounting_type="M8 tapped holes on 50mm grid"
                )
            ),
            Component(
                name="SS Tube",
                category=ComponentCategory.FRAME,
                type=ComponentType.CUSTOM,
                specification="316 SS, 120mm ID × 150mm",
                quantity=1,
                unit_cost=350,
                total_cost=350,
                notes="Chamber cylinder",
                material="316 Stainless Steel",
                requires_expansion=False,
                expansion_notes="",
                tech_specs=TechnicalSpecs(
                    power_consumption=0,
                    weight=3.2,  # kg
                    dimensions={'D': 120, 'wall': 3, 'H': 150},  # mm (ID x wall x height)
                    material_spec="316L Stainless Steel, 2B finish",
                    operating_temp=(-196, 870),
                    max_temp=870,
                    mounting_type="Flange mount top and bottom"
                )
            ),
            Component(
                name="Top Plate",
                category=ComponentCategory.FRAME,
                type=ComponentType.CUSTOM,
                specification="1/4\" aluminum, machined",
                quantity=1,
                unit_cost=250,
                total_cost=250,
                notes="Chamber top with ports",
                material="Aluminum",
                process="CNC Machining",
                requires_expansion=False,
                expansion_notes="",
                tech_specs=TechnicalSpecs(
                    power_consumption=0,
                    weight=2.1,  # kg
                    dimensions={'L': 300, 'W': 300, 'H': 6.35},  # mm
                    material_spec="6061-T6 Aluminum",
                    operating_temp=(-50, 200),
                    mounting_type="M6 countersunk holes",
                    connections=["25x outlet ports", "4x cable glands"]
                )
            ),
            Component(
                name="Access Panel",
                category=ComponentCategory.FRAME,
                type=ComponentType.CUSTOM,
                specification="Acrylic/polycarbonate window",
                quantity=1,
                unit_cost=150,
                total_cost=150,
                notes="Observation window",
                material="Acrylic/Polycarbonate",
                requires_expansion=False,
                expansion_notes="",
                tech_specs=TechnicalSpecs(
                    power_consumption=0,
                    weight=0.8,  # kg
                    dimensions={'L': 200, 'W': 150, 'H': 10},  # mm
                    material_spec="Polycarbonate, optical grade, AR coated",
                    operating_temp=(-40, 120),
                    max_temp=140,
                    mounting_type="Gasket sealed, 8x M4 bolts"
                )
            ),
            Component(
                name="Build Volume",
                category=ComponentCategory.FRAME,
                type=ComponentType.CUSTOM,
                specification="Insulated chamber assembly",
                quantity=1,
                unit_cost=600,
                total_cost=600,
                notes="Includes seals",
                requires_expansion=False,
                expansion_notes="",
                tech_specs=TechnicalSpecs(
                    power_consumption=0,
                    weight=5.0,  # kg
                    dimensions={'D': 120, 'H': 150, 'volume': 125000},  # mm, mm³
                    material_spec="Insulated 316 SS with ceramic liner",
                    operating_temp=(20, 300),
                    max_temp=400,
                    cooling_required="passive"
                )
            ),
            Component(
                name="Thermal Isolation Layer",
                category=ComponentCategory.FRAME,
                type=ComponentType.CUSTOM,
                specification="Ceramic fiber composite",
                quantity=1,
                unit_cost=200,
                total_cost=200,
                notes="High-temp insulation",
                material="Ceramic fiber composite",
                requires_expansion=False,
                expansion_notes="",
                tech_specs=TechnicalSpecs(
                    power_consumption=0,
                    weight=0.5,  # kg
                    dimensions={'thickness': 25, 'area': 0.15},  # mm, m²
                    material_spec="Ceramic fiber blanket, 128kg/m³ density",
                    operating_temp=(-200, 1260),
                    max_temp=1260,
                    thermal_dissipation=0.5  # W/m²K thermal conductivity
                )
            ),
            Component(
                name="Air/Gas Border",
                category=ComponentCategory.FRAME,
                type=ComponentType.CUSTOM,
                specification="Silicone/Viton seals",
                quantity=1,
                unit_cost=100,
                total_cost=100,
                notes="Chamber sealing",
                material="Silicone/Viton",
                requires_expansion=False,
                expansion_notes="",
                tech_specs=TechnicalSpecs(
                    power_consumption=0,
                    weight=0.2,  # kg
                    dimensions={'thickness': 3, 'shore_hardness': 70},  # mm, Shore A
                    material_spec="Viton fluoroelastomer O-rings and gaskets",
                    operating_temp=(-26, 205),
                    max_temp=205,
                    mounting_type="Groove mount per AS568A"
                )
            ),
        ])
        
        # HEATED BED SUBSYSTEM - COTS
        self.components.extend([
            Component(
                name="Heating Rods",
                category=ComponentCategory.HEATED_BED,
                type=ComponentType.COTS,
                specification="1kW cartridge, 12mm×150mm, 220V",
                quantity=4,
                unit_cost=25,
                total_cost=100,
                notes="Platform heating",
                requires_expansion=False,
                expansion_notes="",
                tech_specs=TechnicalSpecs(
                    power_consumption=1000,  # W per rod
                    voltage_nominal=220,
                    voltage_range=(200, 240),
                    current_draw=4.5,  # A per rod
                    weight=0.12,  # kg per rod
                    dimensions={'D': 12, 'L': 150},  # mm
                    operating_temp=(0, 800),
                    max_temp=800,
                    efficiency=95,
                    connections=["2-wire with ground", "M4 terminal"],
                    control_signal="PWM or SSR"
                )
            ),
            Component(
                name="Thermocouples",
                category=ComponentCategory.HEATED_BED,
                type=ComponentType.COTS,
                specification="Type K, M6 thread, 800°C",
                quantity=2,
                unit_cost=12,
                total_cost=24,
                notes="Bed temperature sensing",
                requires_expansion=False,
                expansion_notes="",
                tech_specs=TechnicalSpecs(
                    power_consumption=0,
                    weight=0.02,  # kg
                    dimensions={'D': 6, 'L': 100, 'thread': 'M6x1'},  # mm
                    material_spec="Type K, Inconel sheath",
                    operating_temp=(-200, 1250),
                    accuracy=2.2,  # ±°C
                    connections=["2-wire", "miniature connector"],
                    control_signal="1-100mV analog"
                )
            ),
        ])
        
        # HEATED BED SUBSYSTEM - Custom
        self.components.extend([
            Component(
                name="Heated Bed Assembly",
                category=ComponentCategory.HEATED_BED,
                type=ComponentType.CUSTOM,
                specification="Aluminum block with channels",
                quantity=1,
                unit_cost=450,
                total_cost=450,
                notes="Includes mounting",
                material="Aluminum",
                process="CNC Machining",
                requires_expansion=False,
                expansion_notes="",
                tech_specs=TechnicalSpecs(
                    power_consumption=4000,  # 4 heating rods
                    weight=12.0,  # kg
                    dimensions={'L': 300, 'W': 300, 'H': 50},  # mm
                    material_spec="6061-T6 Aluminum, hard anodized",
                    operating_temp=(20, 800),
                    max_temp=850,
                    thermal_dissipation=200,  # W to environment
                    cooling_required="passive",
                    mounting_type="Standoffs with thermal isolation"
                )
            ),
            Component(
                name="Conductive Block",
                category=ComponentCategory.HEATED_BED,
                type=ComponentType.CUSTOM,
                specification="Copper/aluminum composite",
                quantity=1,
                unit_cost=300,
                total_cost=300,
                notes="Heat distribution",
                material="Copper/Aluminum composite",
                requires_expansion=False,
                expansion_notes="",
                tech_specs=TechnicalSpecs(
                    power_consumption=0,  # Passive component
                    weight=5.0,  # kg
                    dimensions={'L': 250, 'W': 250, 'H': 25},  # mm
                    material_spec="Copper core with aluminum cladding",
                    operating_temp=(20, 850),
                    max_temp=900,
                    thermal_dissipation=50,  # W/m²K conductivity
                    mounting_type="Direct contact with thermal paste"
                )
            ),
            Component(
                name="Distribution Channels",
                category=ComponentCategory.HEATED_BED,
                type=ComponentType.CUSTOM,
                specification="CNC machined pathways",
                quantity=1,
                unit_cost=200,
                total_cost=200,
                notes="Integrated in bed",
                process="CNC Machining",
                requires_expansion=False,
                expansion_notes="",
                tech_specs=TechnicalSpecs(
                    power_consumption=0,
                    dimensions={'channel_width': 10, 'channel_depth': 5, 'pitch': 50},  # mm
                    material_spec="Part of aluminum bed assembly",
                    operating_temp=(20, 850),
                    efficiency=90,  # % heat distribution uniformity
                    accuracy=5  # ±°C temperature uniformity
                )
            ),
            Component(
                name="Thermal Isolation Tube",
                category=ComponentCategory.HEATED_BED,
                type=ComponentType.CUSTOM,
                specification="Multi-layer insulation",
                quantity=1,
                unit_cost=350,
                total_cost=350,
                notes="Includes air gaps, thermal breaks",
                requires_expansion=False,
                expansion_notes="",
                tech_specs=TechnicalSpecs(
                    power_consumption=0,
                    weight=2.5,  # kg
                    dimensions={'D_outer': 350, 'D_inner': 300, 'H': 100},  # mm
                    material_spec="Ceramic fiber with stainless steel shield",
                    operating_temp=(-50, 1000),
                    max_temp=1200,
                    thermal_dissipation=0.02,  # W/m·K (very low conductivity)
                    cooling_required="none"
                )
            ),
        ])
        
        # ACOUSTIC CYLINDER SUBSYSTEM - COTS
        self.components.extend([
            Component(
                name="40kHz Transducers",
                category=ComponentCategory.ACOUSTIC,
                type=ComponentType.COTS,
                specification="16mm ultrasonic, waterproof",
                quantity=18,
                unit_cost=2,
                total_cost=36,
                notes="6 per ring × 3 rings",
                requires_expansion=False,
                expansion_notes="",
                tech_specs=TechnicalSpecs(
                    power_consumption=10,  # W per transducer
                    voltage_nominal=12,
                    voltage_range=(10, 15),
                    current_draw=0.8,  # A per transducer
                    weight=0.015,  # kg per transducer
                    dimensions={'D': 16, 'H': 12},  # mm
                    material_spec="PZT ceramic with aluminum housing",
                    operating_temp=(0, 60),
                    max_temp=80,
                    frequency=40000,  # Hz
                    efficiency=80,  # %
                    connections=["2-pin JST"],
                    control_signal="PWM 40kHz"
                )
            ),
            Component(
                name="Cable Ties",
                category=ComponentCategory.ACOUSTIC,
                type=ComponentType.COTS,
                specification="8\" nylon, standard temp",
                quantity=18,
                unit_cost=0.22,
                total_cost=4,
                notes="Harbor Freight 100-pack",
                supplier="Harbor Freight",
                requires_expansion=False,
                expansion_notes="",
                tech_specs=TechnicalSpecs(
                    power_consumption=0,
                    weight=0.002,  # kg per tie
                    dimensions={'L': 203, 'W': 4.8},  # mm (8" length)
                    material_spec="Nylon 66, UV resistant",
                    operating_temp=(-40, 85),
                    max_temp=105
                )
            ),
        ])
        
        # ACOUSTIC CYLINDER SUBSYSTEM - Custom
        self.components.extend([
            Component(
                name="Acoustic Cylinder",
                category=ComponentCategory.ACOUSTIC,
                type=ComponentType.CUSTOM,
                specification="Aluminum tube, machined",
                quantity=1,
                unit_cost=600,
                total_cost=600,
                notes="Precision bore for waves",
                material="Aluminum",
                process="CNC Machining",
                requires_expansion=False,
                expansion_notes="",
                tech_specs=TechnicalSpecs(
                    power_consumption=0,
                    weight=8.0,  # kg
                    dimensions={'D_outer': 150, 'D_inner': 120, 'H': 200},  # mm
                    material_spec="6061-T6 Aluminum, ±0.05mm tolerance",
                    operating_temp=(-50, 200),
                    mounting_type="Flange mount with O-ring seal",
                    accuracy=0.05  # mm bore tolerance
                )
            ),
            Component(
                name="Transducer Array Layer",
                category=ComponentCategory.ACOUSTIC,
                type=ComponentType.CUSTOM,
                specification="Custom PCB with mounting",
                quantity=1,
                unit_cost=400,
                total_cost=400,
                notes="Includes connectors",
                process="PCB Fabrication",
                requires_expansion=False,
                expansion_notes="",
                tech_specs=TechnicalSpecs(
                    power_consumption=5,  # W for control circuitry
                    voltage_nominal=12,
                    weight=0.5,  # kg
                    dimensions={'D': 140, 'thickness': 2.4},  # mm
                    material_spec="FR4 4-layer PCB, HASL finish",
                    operating_temp=(0, 85),
                    connections=["DB25 control", "Power terminal"],
                    control_signal="SPI bus, 10MHz"
                )
            ),
            Component(
                name="Transducer Rings",
                category=ComponentCategory.ACOUSTIC,
                type=ComponentType.CUSTOM,
                specification="Aluminum, CNC machined",
                quantity=3,
                unit_cost=150,
                total_cost=450,
                notes="$450 total",
                material="Aluminum",
                process="CNC Machining",
                requires_expansion=False,
                expansion_notes="",
                tech_specs=TechnicalSpecs(
                    power_consumption=0,
                    weight=1.2,  # kg per ring
                    dimensions={'D_outer': 140, 'D_inner': 122, 'H': 30},  # mm
                    material_spec="6061-T6 Aluminum, black anodized",
                    operating_temp=(-50, 150),
                    mounting_type="6x M4 tapped holes @ 60°",
                    accuracy=0.1  # mm positioning tolerance
                )
            ),
            Component(
                name="Transducer Housing",
                category=ComponentCategory.ACOUSTIC,
                type=ComponentType.CUSTOM,
                specification="3D printed or machined",
                quantity=6,
                unit_cost=50,
                total_cost=300,
                notes="$300 total",
                process="3D Printing/Machining",
                requires_expansion=False,
                expansion_notes="",
                tech_specs=TechnicalSpecs(
                    power_consumption=0,
                    weight=0.08,  # kg per housing
                    dimensions={'L': 40, 'W': 40, 'H': 25},  # mm
                    material_spec="PETG or machined Delrin",
                    operating_temp=(-20, 80),
                    mounting_type="Snap-fit with backup screws"
                )
            ),
            Component(
                name="Cooling Channels",
                category=ComponentCategory.ACOUSTIC,
                type=ComponentType.CUSTOM,
                specification="Integrated water passages",
                quantity=1,
                unit_cost=200,
                total_cost=200,
                notes="Built into housing",
                requires_expansion=False,
                expansion_notes="",
                tech_specs=TechnicalSpecs(
                    power_consumption=0,
                    dimensions={'channel_dia': 6, 'total_length': 2000},  # mm
                    material_spec="Machined into aluminum rings",
                    flow_rate=2.0,  # L/min
                    operating_temp=(5, 60),
                    connections=["1/4\" NPT in/out"],
                    cooling_required="liquid"
                )
            ),
            Component(
                name="Cooling Layer",
                category=ComponentCategory.ACOUSTIC,
                type=ComponentType.CUSTOM,
                specification="Heat sink assembly",
                quantity=1,
                unit_cost=250,
                total_cost=250,
                notes="With fins",
                requires_expansion=False,
                expansion_notes="",
                tech_specs=TechnicalSpecs(
                    power_consumption=0,
                    weight=3.5,  # kg
                    dimensions={'L': 300, 'W': 300, 'H': 50},  # mm
                    material_spec="Aluminum extrusion with 40 fins",
                    thermal_dissipation=500,  # W at 50°C rise
                    cooling_required="forced air",
                    flow_rate=100  # CFM required airflow
                )
            ),
            Component(
                name="Air/Water Jacket",
                category=ComponentCategory.ACOUSTIC,
                type=ComponentType.CUSTOM,
                specification="Welded aluminum",
                quantity=1,
                unit_cost=300,
                total_cost=300,
                notes="Cooling manifold",
                material="Aluminum",
                process="Welding",
                requires_expansion=False,
                expansion_notes="",
                tech_specs=TechnicalSpecs(
                    power_consumption=0,
                    weight=2.0,  # kg
                    dimensions={'D_outer': 160, 'D_inner': 150, 'H': 200},  # mm
                    material_spec="5052 Aluminum, TIG welded",
                    operating_temp=(5, 80),
                    flow_rate=5.0,  # L/min
                    connections=["1/2\" NPT in/out", "drain valve"],
                    cooling_required="liquid"
                )
            ),
        ])
        
        # CRUCIBLE SUBSYSTEM - COTS
        self.components.extend([
            Component(
                name="Induction Heater",
                category=ComponentCategory.CRUCIBLE,
                type=ComponentType.COTS,
                specification="DaWei 15kW, 30-80kHz",
                quantity=1,
                unit_cost=700,
                total_cost=700,
                notes="Run at 3kW for L1",
                supplier="DaWei",
                requires_expansion=False,
                expansion_notes="",
                tech_specs=TechnicalSpecs(
                    power_consumption=3000,  # W (derated for L1)
                    voltage_nominal=220,
                    voltage_range=(200, 240),
                    current_draw=15,  # A at 3kW
                    weight=12.0,  # kg
                    dimensions={'L': 400, 'W': 300, 'H': 200},  # mm
                    operating_temp=(0, 45),
                    max_temp=50,
                    thermal_dissipation=300,  # W
                    cooling_required="forced air",
                    frequency=50000,  # Hz typical
                    efficiency=85,  # %
                    connections=["3-phase power", "water cooling"],
                    control_signal="0-10V analog or RS485"
                )
            ),
            Component(
                name="Pellet Hopper",
                category=ComponentCategory.CRUCIBLE,
                type=ComponentType.COTS,
                specification="3D printed PLA + hardware",
                quantity=1,
                unit_cost=20,
                total_cost=20,
                notes="Includes stepper motor",
                requires_expansion=False,
                expansion_notes="",
                tech_specs=TechnicalSpecs(
                    power_consumption=5,  # W for stepper
                    voltage_nominal=12,
                    weight=0.5,  # kg including motor
                    dimensions={'D': 100, 'H': 150, 'capacity': 500},  # mm, mL
                    material_spec="PLA body, NEMA17 stepper",
                    operating_temp=(10, 50),
                    flow_rate=10,  # pellets/min
                    connections=["4-wire stepper"],
                    control_signal="Step/Dir signals"
                )
            ),
            Component(
                name="Feedrate Controller",
                category=ComponentCategory.CRUCIBLE,
                type=ComponentType.COTS,
                specification="TB6600 stepper driver, 4A",
                quantity=1,
                unit_cost=25,
                total_cost=25,
                notes="Single axis control",
                requires_expansion=False,
                expansion_notes="",
                tech_specs=TechnicalSpecs(
                    power_consumption=10,  # W max
                    voltage_nominal=24,
                    voltage_range=(9, 42),
                    current_draw=4,  # A max output
                    weight=0.2,  # kg
                    dimensions={'L': 96, 'W': 71, 'H': 37},  # mm
                    operating_temp=(0, 50),
                    connections=["6-pin control", "4-pin motor"],
                    control_signal="5V TTL Step/Dir/Enable"
                )
            ),
            Component(
                name="Temperature Controller",
                category=ComponentCategory.CRUCIBLE,
                type=ComponentType.COTS,
                specification="REX-C100 PID clone",
                quantity=1,
                unit_cost=15,
                total_cost=15,
                notes="SSR output for induction",
                requires_expansion=False,
                expansion_notes="",
                tech_specs=TechnicalSpecs(
                    power_consumption=3,  # W
                    voltage_nominal=100,
                    voltage_range=(90, 240),
                    weight=0.15,  # kg
                    dimensions={'L': 48, 'W': 48, 'H': 100},  # mm
                    operating_temp=(0, 50),
                    accuracy=0.5,  # % FS
                    connections=["Thermocouple input", "SSR output"],
                    control_signal="12V DC SSR drive"
                )
            ),
            Component(
                name="Thermocouples",
                category=ComponentCategory.CRUCIBLE,
                type=ComponentType.COTS,
                specification="Type K, ceramic sheath",
                quantity=2,
                unit_cost=12,
                total_cost=24,
                notes="Crucible monitoring",
                requires_expansion=False,
                expansion_notes="",
                tech_specs=TechnicalSpecs(
                    power_consumption=0,
                    weight=0.03,  # kg
                    dimensions={'D': 8, 'L': 150},  # mm
                    material_spec="Type K, alumina sheath",
                    operating_temp=(-50, 1350),
                    max_temp=1400,
                    accuracy=2.2,  # ±°C
                    connections=["2-wire", "standard connector"],
                    control_signal="1-50mV analog"
                )
            ),
            Component(
                name="Micro Heaters",
                category=ComponentCategory.CRUCIBLE,
                type=ComponentType.COTS,
                specification="12V 40W cartridge, 6mm×20mm",
                quantity=25,
                unit_cost=8,
                total_cost=200,
                notes="Feed line heating",
                requires_expansion=False,
                expansion_notes="",
                tech_specs=TechnicalSpecs(
                    power_consumption=40,  # W per heater
                    voltage_nominal=12,
                    current_draw=3.3,  # A per heater
                    weight=0.01,  # kg per heater
                    dimensions={'D': 6, 'L': 20},  # mm
                    operating_temp=(0, 300),
                    max_temp=350,
                    efficiency=95,  # %
                    connections=["2-wire with fiberglass leads"],
                    control_signal="PWM or on/off"
                )
            ),
        ])
        
        # CRUCIBLE SUBSYSTEM - Custom
        self.components.extend([
            Component(
                name="Crucible Assembly",
                category=ComponentCategory.CRUCIBLE,
                type=ComponentType.CUSTOM,
                specification="Graphite + insulation",
                quantity=1,
                unit_cost=400,
                total_cost=400,
                notes="Complete unit",
                material="Graphite",
                requires_expansion=False,
                expansion_notes="",
                tech_specs=TechnicalSpecs(
                    power_consumption=0,  # Heated by induction
                    weight=2.5,  # kg
                    dimensions={'D_outer': 80, 'D_inner': 60, 'H': 100},  # mm
                    material_spec="High-purity graphite with ceramic insulation",
                    operating_temp=(20, 1800),
                    max_temp=2000,
                    thermal_dissipation=100,  # W at operating temp
                    cooling_required="none",
                    mounting_type="Ceramic standoffs"
                )
            ),
            Component(
                name="Material Feed System",
                category=ComponentCategory.CRUCIBLE,
                type=ComponentType.CUSTOM,
                specification="Machined aluminum",
                quantity=1,
                unit_cost=350,
                total_cost=350,
                notes="Includes guides",
                material="Aluminum",
                process="CNC Machining",
                requires_expansion=False,
                expansion_notes="",
                tech_specs=TechnicalSpecs(
                    power_consumption=0,
                    weight=3.0,  # kg
                    dimensions={'L': 200, 'W': 150, 'H': 100},  # mm
                    material_spec="6061-T6 Aluminum with PTFE liners",
                    operating_temp=(20, 150),
                    flow_rate=100,  # pellets/min max
                    mounting_type="Bolt-on frame mount",
                    connections=["Hopper interface", "Crucible feed"]
                )
            ),
            Component(
                name="Induction Coil Assembly",
                category=ComponentCategory.CRUCIBLE,
                type=ComponentType.CUSTOM,
                specification="Copper tube + mounting",
                quantity=1,
                unit_cost=250,
                total_cost=250,
                notes="Custom wound",
                material="Copper",
                requires_expansion=False,
                expansion_notes="",
                tech_specs=TechnicalSpecs(
                    power_consumption=0,  # Passive component
                    weight=1.5,  # kg
                    dimensions={'D': 100, 'H': 80, 'turns': 8},  # mm
                    material_spec="6mm OD copper tube, water cooled",
                    operating_temp=(20, 80),
                    max_temp=100,
                    cooling_required="liquid",
                    flow_rate=1.0,  # L/min cooling water
                    connections=["1/4\" compression fittings"],
                    frequency=50000  # Hz operating frequency
                )
            ),
            Component(
                name="Material Delivery System",
                category=ComponentCategory.CRUCIBLE,
                type=ComponentType.CUSTOM,
                specification="Multi-channel manifold",
                quantity=1,
                unit_cost=400,
                total_cost=400,
                notes="25 outlets",
                requires_expansion=False,
                expansion_notes="",
                tech_specs=TechnicalSpecs(
                    power_consumption=1000,  # W for micro heaters
                    weight=4.0,  # kg
                    dimensions={'L': 200, 'W': 200, 'H': 150},  # mm
                    material_spec="316 SS manifold with PTFE liners",
                    operating_temp=(20, 400),
                    max_temp=450,
                    flow_rate=0.1,  # kg/min total material flow
                    connections=["25x 2mm outlets", "1x 10mm inlet"],
                    accuracy=5  # % flow distribution uniformity
                )
            ),
            Component(
                name="Outlet Array",
                category=ComponentCategory.CRUCIBLE,
                type=ComponentType.CUSTOM,
                specification="Precision drilled plate",
                quantity=1,
                unit_cost=300,
                total_cost=300,
                notes="5×5 grid, 2mm spacing",
                process="Precision Drilling",
                requires_expansion=False,
                expansion_notes="",
                tech_specs=TechnicalSpecs(
                    power_consumption=0,
                    weight=0.5,  # kg
                    dimensions={'L': 100, 'W': 100, 'H': 10},  # mm
                    material_spec="316 SS, electro-polished",
                    operating_temp=(20, 500),
                    max_temp=600,
                    accuracy=0.05,  # mm hole position tolerance
                    connections=["25x 2mm dia outlets"]
                )
            ),
            Component(
                name="Splitter Plate",
                category=ComponentCategory.CRUCIBLE,
                type=ComponentType.CUSTOM,
                specification="Stainless steel",
                quantity=1,
                unit_cost=200,
                total_cost=200,
                notes="Flow distribution",
                material="Stainless Steel",
                requires_expansion=False,
                expansion_notes="",
                tech_specs=TechnicalSpecs(
                    power_consumption=0,
                    weight=0.8,  # kg
                    dimensions={'D': 150, 'H': 20},  # mm
                    material_spec="316L SS with micro-channels",
                    operating_temp=(20, 500),
                    efficiency=95,  # % flow splitting uniformity
                    connections=["1x central inlet", "25x outlets"]
                )
            ),
            Component(
                name="Feed Lines",
                category=ComponentCategory.CRUCIBLE,
                type=ComponentType.CUSTOM,
                specification="PTFE/SS tubing",
                quantity=25,
                unit_cost=10,
                total_cost=250,
                notes="High-temp rated",
                material="PTFE/Stainless Steel",
                requires_expansion=False,
                expansion_notes="",
                tech_specs=TechnicalSpecs(
                    power_consumption=0,
                    weight=0.02,  # kg per line
                    dimensions={'D_outer': 3, 'D_inner': 2, 'L': 300},  # mm
                    material_spec="PTFE lined SS tubing",
                    operating_temp=(20, 260),
                    max_temp=300,
                    connections=["Compression fittings both ends"]
                )
            ),
            Component(
                name="Thermal Pulse Formation",
                category=ComponentCategory.CRUCIBLE,
                type=ComponentType.CUSTOM,
                specification="Control valves",
                quantity=1,
                unit_cost=350,
                total_cost=350,
                notes="Droplet timing",
                requires_expansion=False,
                expansion_notes="",
                tech_specs=TechnicalSpecs(
                    power_consumption=50,  # W for solenoids
                    voltage_nominal=24,
                    weight=2.0,  # kg
                    dimensions={'L': 150, 'W': 100, 'H': 80},  # mm
                    operating_temp=(10, 80),
                    frequency=10,  # Hz max pulse rate
                    accuracy=1,  # ms timing precision
                    connections=["25x solenoid valves"],
                    control_signal="24V DC PWM"
                )
            ),
            Component(
                name="Ceramic Isolation",
                category=ComponentCategory.CRUCIBLE,
                type=ComponentType.CUSTOM,
                specification="Moldable ceramic",
                quantity=1,
                unit_cost=150,
                total_cost=150,
                notes="Thermal protection",
                material="Moldable Ceramic",
                requires_expansion=False,
                expansion_notes="",
                tech_specs=TechnicalSpecs(
                    power_consumption=0,
                    weight=1.0,  # kg
                    dimensions={'thickness': 50, 'coverage': 0.5},  # mm, m²
                    material_spec="Alumina-silicate moldable refractory",
                    operating_temp=(20, 1400),
                    max_temp=1600,
                    thermal_dissipation=0.15,  # W/m·K conductivity
                    cooling_required="none"
                )
            ),
        ])
        
        # POWER/CONTROL SUBSYSTEM - COTS
        self.components.extend([
            Component(
                name="10kW PSU",
                category=ComponentCategory.POWER_CONTROL,
                type=ComponentType.COTS,
                specification="Mean Well RSP-10000-48",
                quantity=1,
                unit_cost=1850,
                total_cost=1850,
                notes="Main power supply",
                supplier="Mean Well",
                requires_expansion=False,
                expansion_notes="",
                tech_specs=TechnicalSpecs(
                    power_consumption=900,  # W input power consumption (10kW * (1-0.91 efficiency))
                    voltage_nominal=48,
                    voltage_range=(43.2, 52.8),  # ±10% adjustment
                    current_draw=48,  # A input at full load
                    weight=7.5,  # kg
                    dimensions={'L': 280, 'W': 140, 'H': 90},  # mm
                    operating_temp=(0, 50),
                    max_temp=70,
                    thermal_dissipation=900,  # W heat generated = power consumed
                    cooling_required="forced air",
                    efficiency=91,  # % (10kW output / 10.9kW input)
                    connections=["AC input terminal", "DC output terminal"],
                    control_signal="Remote on/off, voltage adjust"
                )
            ),
            Component(
                name="FPGA Board",
                category=ComponentCategory.POWER_CONTROL,
                type=ComponentType.COTS,
                specification="Cyclone IV EP4CE6",
                quantity=1,
                unit_cost=75,
                total_cost=75,
                notes="Per VDATP reference",
                requires_expansion=False,
                expansion_notes="",
                tech_specs=TechnicalSpecs(
                    power_consumption=2,  # W
                    voltage_nominal=3.3,
                    voltage_range=(3.0, 3.6),
                    weight=0.05,  # kg
                    dimensions={'L': 70, 'W': 50, 'H': 15},  # mm
                    operating_temp=(0, 85),
                    connections=["JTAG", "GPIO headers", "USB"],
                    control_signal="3.3V LVTTL I/O"
                )
            ),
            Component(
                name="6-Channel Amp Modules",
                category=ComponentCategory.POWER_CONTROL,
                type=ComponentType.COTS,
                specification="TDA2030 DIY boards",
                quantity=4,
                unit_cost=15,
                total_cost=60,
                notes="Build from kits",
                requires_expansion=False,
                expansion_notes="",
                tech_specs=TechnicalSpecs(
                    power_consumption=100,  # W per module (6ch)
                    voltage_nominal=24,
                    voltage_range=(12, 36),
                    current_draw=4,  # A per module
                    weight=0.3,  # kg per module
                    dimensions={'L': 120, 'W': 80, 'H': 40},  # mm
                    operating_temp=(0, 70),
                    thermal_dissipation=20,  # W
                    cooling_required="passive",
                    efficiency=70,  # %
                    connections=["6x speaker outputs", "6x signal inputs"],
                    control_signal="1Vpp audio input"
                )
            ),
            Component(
                name="8-Channel Relays",
                category=ComponentCategory.POWER_CONTROL,
                type=ComponentType.COTS,
                specification="Generic relay modules, 10A",
                quantity=5,
                unit_cost=8,
                total_cost=40,
                notes="eBay/AliExpress",
                supplier="eBay/AliExpress",
                requires_expansion=False,
                expansion_notes="",
                tech_specs=TechnicalSpecs(
                    power_consumption=2,  # W per module
                    voltage_nominal=5,  # V control
                    current_draw=0.4,  # A for all relays on
                    weight=0.15,  # kg per module
                    dimensions={'L': 140, 'W': 70, 'H': 20},  # mm
                    operating_temp=(0, 60),
                    connections=["8x NO/NC/COM", "Control header"],
                    control_signal="5V TTL active low"
                )
            ),
            Component(
                name="STM32 Dev Board",
                category=ComponentCategory.POWER_CONTROL,
                type=ComponentType.COTS,
                specification="STM32F4 Discovery",
                quantity=1,
                unit_cost=25,
                total_cost=25,
                notes="Real STM32 for development",
                requires_expansion=False,
                expansion_notes="",
                tech_specs=TechnicalSpecs(
                    power_consumption=0.5,  # W
                    voltage_nominal=3.3,
                    voltage_range=(2.0, 3.6),
                    weight=0.04,  # kg
                    dimensions={'L': 95, 'W': 64, 'H': 15},  # mm
                    operating_temp=(-40, 85),
                    frequency=168000000,  # Hz (168 MHz)
                    connections=["USB", "SWD", "GPIO headers"],
                    control_signal="3.3V I/O, 5V tolerant"
                )
            ),
            Component(
                name="Industrial PC",
                category=ComponentCategory.POWER_CONTROL,
                type=ComponentType.COTS,
                specification="User-provided",
                quantity=0,
                unit_cost=0,
                total_cost=0,
                notes="Min specs: i5, 8GB RAM",
                requires_expansion=False,
                expansion_notes="",
                tech_specs=TechnicalSpecs(
                    power_consumption=65,  # W typical
                    voltage_nominal=12,  # V DC typical
                    weight=2.0,  # kg estimated
                    operating_temp=(0, 50),
                    connections=["USB 3.0", "Ethernet", "DisplayPort"],
                    control_signal="USB/Ethernet communication"
                )
            ),
        ])
        
        # POWER/CONTROL SUBSYSTEM - Custom
        self.components.extend([
            Component(
                name="Control Bus PCB",
                category=ComponentCategory.POWER_CONTROL,
                type=ComponentType.CUSTOM,
                specification="4-layer board",
                quantity=1,
                unit_cost=350,
                total_cost=350,
                notes="Main interconnect",
                process="PCB Fabrication",
                requires_expansion=False,
                expansion_notes="",
                tech_specs=TechnicalSpecs(
                    power_consumption=10,  # W for onboard regulators
                    voltage_nominal=48,  # V main bus
                    weight=0.8,  # kg
                    dimensions={'L': 300, 'W': 200, 'thickness': 1.6},  # mm
                    material_spec="FR4 4-layer, 2oz copper, ENIG",
                    operating_temp=(0, 85),
                    connections=["Power distribution", "Control signals"],
                    control_signal="Mixed voltage domains"
                )
            ),
            Component(
                name="Acoustic Bus PCB",
                category=ComponentCategory.POWER_CONTROL,
                type=ComponentType.CUSTOM,
                specification="2-layer board",
                quantity=1,
                unit_cost=200,
                total_cost=200,
                notes="Transducer routing",
                process="PCB Fabrication",
                requires_expansion=False,
                expansion_notes="",
                tech_specs=TechnicalSpecs(
                    power_consumption=5,  # W
                    voltage_nominal=24,
                    weight=0.4,  # kg
                    dimensions={'L': 200, 'W': 150, 'thickness': 1.6},  # mm
                    material_spec="FR4 2-layer, 1oz copper",
                    operating_temp=(0, 70),
                    frequency=40000,  # Hz signal routing
                    connections=["18x transducer outputs", "FPGA interface"],
                    control_signal="Differential 40kHz drives"
                )
            ),
            Component(
                name="Thermal Bus PCB",
                category=ComponentCategory.POWER_CONTROL,
                type=ComponentType.CUSTOM,
                specification="2-layer board with relays",
                quantity=1,
                unit_cost=250,
                total_cost=250,
                notes="Heater control",
                process="PCB Fabrication",
                requires_expansion=False,
                expansion_notes="",
                tech_specs=TechnicalSpecs(
                    power_consumption=15,  # W including relays
                    voltage_nominal=220,  # V switching
                    current_draw=20,  # A total switching capacity
                    weight=0.6,  # kg
                    dimensions={'L': 250, 'W': 180, 'thickness': 2.4},  # mm
                    material_spec="FR4 2-layer, 2oz copper, high voltage spacing",
                    operating_temp=(0, 60),
                    connections=["Heater outputs", "Thermocouple inputs"],
                    control_signal="SSR drives, analog TC inputs"
                )
            ),
            Component(
                name="Wiring Harness",
                category=ComponentCategory.POWER_CONTROL,
                type=ComponentType.CUSTOM,
                specification="Custom cables",
                quantity=1,
                unit_cost=300,
                total_cost=300,
                notes="All interconnects",
                requires_expansion=False,
                expansion_notes="",
                tech_specs=TechnicalSpecs(
                    power_consumption=0,
                    weight=3.0,  # kg total
                    material_spec="Silicone insulated wire, various gauges",
                    operating_temp=(-40, 200),
                    connections=["Power cables", "Signal cables", "Sensor cables"],
                    mounting_type="Cable management channels"
                )
            ),
            Component(
                name="Control Enclosure",
                category=ComponentCategory.POWER_CONTROL,
                type=ComponentType.CUSTOM,
                specification="Sheet metal box",
                quantity=1,
                unit_cost=200,
                total_cost=200,
                notes="Electronics housing",
                material="Sheet Metal",
                process="Metal Fabrication",
                requires_expansion=False,
                expansion_notes="",
                tech_specs=TechnicalSpecs(
                    power_consumption=0,
                    weight=5.0,  # kg
                    dimensions={'L': 500, 'W': 400, 'H': 200},  # mm
                    material_spec="16ga steel, powder coated",
                    operating_temp=(0, 50),
                    cooling_required="forced air",
                    flow_rate=200,  # CFM ventilation
                    mounting_type="19\" rack mount or standalone",
                    connections=["Cable glands", "ventilation grilles"]
                )
            ),
        ])
    
    def get_components_by_category(self, category: ComponentCategory) -> List[Component]:
        """Get all components in a specific category"""
        return [c for c in self.components if c.category == category]
    
    def get_components_by_type(self, comp_type: ComponentType) -> List[Component]:
        """Get all components of a specific type (COTS or Custom)"""
        return [c for c in self.components if c.type == comp_type]
    
    def get_components_requiring_expansion(self) -> List[Component]:
        """Get all components marked as requiring expansion"""
        return [c for c in self.components if c.requires_expansion]
    
    def get_total_cost_by_category(self) -> Dict[ComponentCategory, Dict[str, float]]:
        """Calculate total costs broken down by category and type"""
        totals = {}
        for category in ComponentCategory:
            totals[category] = {
                'COTS': sum(c.total_cost for c in self.components 
                           if c.category == category and c.type == ComponentType.COTS),
                'Custom': sum(c.total_cost for c in self.components 
                             if c.category == category and c.type == ComponentType.CUSTOM),
                'Total': 0
            }
            totals[category]['Total'] = totals[category]['COTS'] + totals[category]['Custom']
        return totals
    
    def get_grand_totals(self) -> Dict[str, float]:
        """Calculate grand totals for the entire system"""
        return {
            'COTS': sum(c.total_cost for c in self.components if c.type == ComponentType.COTS),
            'Custom': sum(c.total_cost for c in self.components if c.type == ComponentType.CUSTOM),
            'Total': sum(c.total_cost for c in self.components)
        }
    
    def mark_for_expansion(self, component_name: str, notes: str = ""):
        """Mark a component as requiring expansion"""
        for component in self.components:
            if component.name == component_name:
                component.requires_expansion = True
                component.expansion_notes = notes
                return True
        return False
    
    def update_expansion_notes(self, component_name: str, notes: str):
        """Update expansion notes for a component"""
        for component in self.components:
            if component.name == component_name:
                component.expansion_notes = notes
                return True
        return False
    
    def get_component_by_name(self, name: str) -> Optional[Component]:
        """Get a specific component by name"""
        for component in self.components:
            if component.name == name:
                return component
        return None
    
    def print_summary(self):
        """Print a summary of the component registry"""
        print("COMPONENT REGISTRY SUMMARY")
        print("=" * 80)
        
        # Category breakdown
        totals = self.get_total_cost_by_category()
        for category in ComponentCategory:
            print(f"\n{category.value}:")
            print(f"  COTS: ${totals[category]['COTS']:,.2f}")
            print(f"  Custom: ${totals[category]['Custom']:,.2f}")
            print(f"  Subtotal: ${totals[category]['Total']:,.2f}")
        
        # Grand totals
        grand = self.get_grand_totals()
        print(f"\nGRAND TOTALS:")
        print(f"  COTS: ${grand['COTS']:,.2f}")
        print(f"  Custom: ${grand['Custom']:,.2f}")
        print(f"  TOTAL: ${grand['Total']:,.2f}")
        
        # Components requiring expansion
        expansion_needed = self.get_components_requiring_expansion()
        if expansion_needed:
            print(f"\nCOMPONENTS REQUIRING EXPANSION: {len(expansion_needed)}")
            for comp in expansion_needed:
                print(f"  - {comp.name}: {comp.expansion_notes}")
    
    def calculate_power_budget(self) -> Dict[str, Dict[str, float]]:
        """Calculate total power consumption by subsystem"""
        power_budget = {}
        
        for category in ComponentCategory:
            category_power = {
                'active_power': 0,  # W - actual power consumption
                'thermal_load': 0,  # W - heat generated
                'component_count': 0
            }
            
            for component in self.components:
                if component.category == category and component.tech_specs.power_consumption:
                    # Calculate based on quantity
                    total_power = component.tech_specs.power_consumption * component.quantity
                    category_power['active_power'] += total_power
                    
                    # Calculate thermal load (inefficiency)
                    if component.tech_specs.efficiency:
                        thermal_load = total_power * (1 - component.tech_specs.efficiency / 100)
                    elif component.tech_specs.thermal_dissipation:
                        thermal_load = component.tech_specs.thermal_dissipation * component.quantity
                    else:
                        # Assume 20% loss for components without efficiency data
                        thermal_load = total_power * 0.2
                    
                    category_power['thermal_load'] += thermal_load
                    category_power['component_count'] += component.quantity
            
            power_budget[category.value] = category_power
        
        # Calculate totals
        power_budget['TOTAL'] = {
            'active_power': sum(pb['active_power'] for pb in power_budget.values()),
            'thermal_load': sum(pb['thermal_load'] for pb in power_budget.values()),
            'component_count': sum(pb['component_count'] for pb in power_budget.values())
        }
        
        return power_budget
    
    def validate_thermal_design(self) -> Dict[str, Any]:
        """Validate thermal management requirements"""
        validation_results = {
            'total_heat_generation': 0,  # W
            'cooling_requirements': {},
            'critical_components': [],
            'warnings': [],
            'recommendations': []
        }
        
        # Categorize cooling needs
        cooling_types = {
            'none': [],
            'passive': [],
            'forced air': [],
            'liquid': []
        }
        
        for component in self.components:
            if not component.tech_specs.power_consumption:
                continue
                
            # Calculate heat generation
            if component.tech_specs.thermal_dissipation:
                heat_gen = component.tech_specs.thermal_dissipation * component.quantity
            elif component.tech_specs.efficiency:
                power = component.tech_specs.power_consumption * component.quantity
                heat_gen = power * (1 - component.tech_specs.efficiency / 100)
            else:
                heat_gen = component.tech_specs.power_consumption * component.quantity * 0.2
            
            validation_results['total_heat_generation'] += heat_gen
            
            # Categorize by cooling requirement
            cooling_req = component.tech_specs.cooling_required or 'passive'
            cooling_types[cooling_req].append({
                'component': component.name,
                'heat_load': heat_gen,
                'max_temp': component.tech_specs.max_temp
            })
            
            # Check for critical temperature components
            if component.tech_specs.max_temp and component.tech_specs.max_temp < 100:
                validation_results['critical_components'].append({
                    'name': component.name,
                    'max_temp': component.tech_specs.max_temp,
                    'cooling': cooling_req
                })
        
        # Summarize cooling requirements
        for cooling_type, components in cooling_types.items():
            if components:
                total_heat = sum(c['heat_load'] for c in components)
                validation_results['cooling_requirements'][cooling_type] = {
                    'component_count': len(components),
                    'total_heat_load': total_heat,
                    'components': components
                }
        
        # Generate warnings and recommendations
        total_heat = validation_results['total_heat_generation']
        
        if total_heat > 5000:
            validation_results['warnings'].append(
                f"High total heat generation: {total_heat:.0f}W requires substantial cooling"
            )
        
        if 'liquid' in validation_results['cooling_requirements']:
            validation_results['recommendations'].append(
                "Implement liquid cooling system with minimum 5L/min flow rate"
            )
        
        if 'forced air' in validation_results['cooling_requirements']:
            cfm_required = validation_results['cooling_requirements']['forced air']['total_heat_load'] / 3
            validation_results['recommendations'].append(
                f"Provide forced air cooling with minimum {cfm_required:.0f} CFM airflow"
            )
        
        # Check acoustic subsystem specifically
        acoustic_heat = sum(
            c.tech_specs.power_consumption * c.quantity * 0.2
            for c in self.components
            if c.category == ComponentCategory.ACOUSTIC and c.tech_specs.power_consumption
        )
        if acoustic_heat > 100:
            validation_results['warnings'].append(
                f"Acoustic subsystem generates {acoustic_heat:.0f}W - ensure transducer cooling"
            )
        
        return validation_results


# Example usage
if __name__ == "__main__":
    registry = ComponentRegistry()
    registry.print_summary()
    
    # Calculate power budget
    print("\n" + "=" * 80)
    print("POWER BUDGET ANALYSIS")
    print("=" * 80)
    power_budget = registry.calculate_power_budget()
    for subsystem, power_data in power_budget.items():
        if power_data['active_power'] > 0:
            print(f"\n{subsystem}:")
            print(f"  Active Power: {power_data['active_power']:.1f}W")
            print(f"  Thermal Load: {power_data['thermal_load']:.1f}W")
            print(f"  Components: {power_data['component_count']}")
    
    # Validate thermal design
    print("\n" + "=" * 80)
    print("THERMAL VALIDATION")
    print("=" * 80)
    thermal_validation = registry.validate_thermal_design()
    print(f"\nTotal Heat Generation: {thermal_validation['total_heat_generation']:.1f}W")
    
    print("\nCooling Requirements:")
    for cooling_type, data in thermal_validation['cooling_requirements'].items():
        print(f"  {cooling_type.title()}: {data['component_count']} components, "
              f"{data['total_heat_load']:.1f}W heat load")
    
    if thermal_validation['warnings']:
        print("\nWarnings:")
        for warning in thermal_validation['warnings']:
            print(f"  ⚠️  {warning}")
    
    if thermal_validation['recommendations']:
        print("\nRecommendations:")
        for rec in thermal_validation['recommendations']:
            print(f"  • {rec}")