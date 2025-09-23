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
    power_consumption: Optional[float] = None  # Watts (power consumed by component)
    power_supply: Optional[float] = None  # Watts (power supplied by component, e.g., PSU)
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
    
    # Power Domain
    power_type: Optional[str] = None  # 'AC', 'DC', or 'DUAL'
    power_voltage: Optional[float] = None  # Operating voltage (120, 240, 48, 24, 12, 5)


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
    
    # Level scaling factors derived from current projections
    LEVEL_MULTIPLIERS = {
        1: {'cost': 1.0, 'power': 1.0, 'transducers': 18, 'build_volume': 125},
        2: {'cost': 1.55, 'power': 1.78, 'transducers': 36, 'build_volume': 1000},
        3: {'cost': 2.73, 'power': 2.72, 'transducers': 36, 'build_volume': 1000},
        4: {'cost': 5.70, 'power': 4.07, 'transducers': 72, 'build_volume': 8000}
    }
    
    # Level-specific capabilities
    LEVEL_CAPABILITIES = {
        1: {'materials': ['Al'], 'build_rate': 1},  # cm³/hr
        2: {'materials': ['Al', 'Steel'], 'build_rate': 5},
        3: {'materials': ['Al', 'Steel'], 'build_rate': 10, 'feature': 'Dual simultaneous'},
        4: {'materials': ['Al', 'Steel', 'Ti', 'Cu', 'Ni'], 'build_rate': 25}
    }
    
    def __init__(self, level=1):
        self.level = level
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
            Component(
                name="Chamber Assembly",
                category=ComponentCategory.FRAME,
                type=ComponentType.CUSTOM,
                specification="Complete chamber with ports and seals",
                quantity=1,
                unit_cost=1200,
                total_cost=1200,
                notes="Main process chamber - thermal control",
                material="316 Stainless Steel",
                process="Welding and Machining",
                requires_expansion=False,
                expansion_notes="",
                tech_specs=TechnicalSpecs(
                    power_consumption=0,  # Passive component
                    weight=15.0,  # kg
                    dimensions={'L': 400, 'W': 400, 'H': 300},  # mm
                    material_spec="316L SS chamber with viewing ports",
                    operating_temp=(20, 300),  # Per SR009 - max chamber temp 300°C
                    max_temp=400,  # With safety margin
                    thermal_dissipation=50,  # W to environment
                    cooling_required="passive",
                    mounting_type="Frame mounted with vibration isolation",
                    connections=["Multiple sensor ports", "Gas inlet/outlet", "Access door"]
                )
            ),
        ])
        
        # HEATED BED SUBSYSTEM - COTS
        self.components.extend([
            Component(
                name="Cartridge Heaters 120V (4-pack)",
                category=ComponentCategory.HEATED_BED,
                type=ComponentType.COTS,
                specification="1/2 inch × 8 inch, 1000W, 120V",
                quantity=4,
                unit_cost=8,
                total_cost=32,
                notes="2 active + 2 spare/redundancy, 2-zone operation",
                supplier="https://oemheaters.com/product/5429/",
                requires_expansion=False,
                expansion_notes="",
                tech_specs=TechnicalSpecs(
                    power_consumption=1000,  # W per heater
                    power_type='AC',  # Direct from mains
                    power_voltage=120,
                    voltage_nominal=120,
                    voltage_range=(110, 130),
                    current_draw=8.3,  # A per heater at 120V
                    weight=0.15,  # kg per heater
                    dimensions={'D': 12.7, 'L': 203},  # mm (1/2" × 8")
                    material_spec="304 SS sheath, MgO insulation",
                    operating_temp=(20, 600),
                    max_temp=677,  # 1250°F
                    efficiency=95,
                    connections=["12 inch fiberglass leads"],
                    control_signal="SSR controlled"
                )
            ),
            Component(
                name="Thermocouples",
                category=ComponentCategory.HEATED_BED,
                type=ComponentType.COTS,
                specification="Type K, M6 thread, 3mm probe, 800°C rated",
                quantity=2,
                unit_cost=12.00,
                total_cost=24.00,
                notes="Bed temperature sensing - 2-zone control",
                part_number="Generic-K-M6-800C",
                supplier="Amazon (Meter Star or equivalent)",
                lead_time_weeks=1,
                requires_expansion=False,
                expansion_notes="",
                tech_specs=TechnicalSpecs(
                    power_consumption=0,
                    weight=0.02,  # kg each
                    dimensions={'D': 3, 'L': 100},  # mm
                    material_spec="Type K (Chromel/Alumel), SS316 sheath",
                    operating_temp=(-50, 800),
                    max_temp=850,
                    accuracy=1.5,  # ±°C Class 1
                    connections=["M6x1.0 thread", "2m fiberglass cable", "Mini K-plug"],
                    control_signal="Type K millivolt output (0-33mV @ 800°C)"
                )
            ),
        ])
        
        # HEATED BED SUBSYSTEM - Custom
        self.components.extend([
            Component(
                name="Copper Heated Bed",
                category=ComponentCategory.HEATED_BED,
                type=ComponentType.CUSTOM,
                specification="C11000 copper, 150mm × 30mm, 4 heater holes",
                quantity=1,
                unit_cost=450,
                total_cost=450,
                notes="4× heater capability, 2-zone control",
                material="Copper C11000",
                process="CNC Machining",
                requires_expansion=False,
                expansion_notes="",
                tech_specs=TechnicalSpecs(
                    power_consumption=2000,  # Normal: 2 heaters active
                    power_type='AC',
                    power_voltage=120,
                    weight=4.75,  # kg (copper is denser than aluminum)
                    dimensions={'D': 150, 'H': 30},  # mm diameter × height
                    material_spec="C11000 oxygen-free copper",
                    operating_temp=(20, 600),
                    max_temp=650,
                    thermal_dissipation=370,  # W steady-state
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
                    power_type='DC',  # DC powered
                    power_voltage=48,  # 48V DC from amplifiers
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
                name="Induction Heater Module (OEM)",
                category=ComponentCategory.CRUCIBLE,
                type=ComponentType.COTS,
                specification="HCGF HCX-3000W-50K, 30-80kHz auto-tracking",
                quantity=1,
                unit_cost=420,
                total_cost=420,
                notes="Professional OEM module with control board",
                supplier="HCGF/DUANXU via Alibaba",
                requires_expansion=False,
                expansion_notes="",
                tech_specs=TechnicalSpecs(
                    power_consumption=3000,  # W continuous
                    power_type='AC',  # AC powered
                    power_voltage=220,  # 220V single phase
                    voltage_nominal=220,
                    voltage_range=(200, 240),
                    current_draw=15,  # A at 3kW
                    weight=2.8,  # kg
                    dimensions={'L': 280, 'W': 180, 'H': 60},  # mm board only
                    operating_temp=(0, 45),
                    max_temp=50,
                    thermal_dissipation=300,  # W
                    cooling_required="forced air",
                    frequency=50000,  # Hz typical
                    efficiency=85,  # %
                    connections=["AC input", "HF output to coil", "water cooling"],
                    control_signal="PWM control input, Enable signal"
                )
            ),
            # Induction Heater Integration Components
            Component(
                name="Induction Main Contactor",
                category=ComponentCategory.CRUCIBLE,
                type=ComponentType.COTS,
                specification="Schneider LC1D32P7, 32A 230V coil",
                quantity=1,
                unit_cost=85,
                total_cost=85,
                notes="Safety disconnect for induction power",
                supplier="Grainger #3210847",
                requires_expansion=False,
                expansion_notes="",
                tech_specs=TechnicalSpecs(
                    power_consumption=5,  # W coil power
                    power_type='AC',
                    voltage_nominal=230,
                    current_draw=0.02,  # A coil current
                    weight=0.5,  # kg
                    dimensions={'L': 55, 'W': 85, 'H': 95},  # mm
                    operating_temp=(-25, 60),
                    connections=["3 power poles", "NC aux contact"],
                    control_signal="230V coil with E-stop interlock"
                )
            ),
            Component(
                name="Induction EMI Filter",
                category=ComponentCategory.CRUCIBLE,
                type=ComponentType.COTS,
                specification="Schaffner FN2090-16-06, 16A medical",
                quantity=1,
                unit_cost=45,
                total_cost=45,
                notes="Reduces conducted EMI from induction",
                supplier="Mouser #448-FN2090-16-06",
                requires_expansion=False,
                expansion_notes="",
                tech_specs=TechnicalSpecs(
                    power_consumption=2,  # W losses
                    weight=0.45,  # kg
                    dimensions={'L': 130, 'W': 65, 'H': 55},  # mm
                    operating_temp=(-25, 100),
                    connections=["Line in", "Load out", "Ground"]
                )
            ),
            Component(
                name="Induction Work Coil",
                category=ComponentCategory.CRUCIBLE,
                type=ComponentType.CUSTOM,
                specification="6mm copper tube, 8 turns, 80mm dia",
                quantity=1,
                unit_cost=40,
                total_cost=40,
                notes="Water-cooled coil for crucible",
                material="C11000 copper refrigeration tubing",
                process="Hand wound to specifications",
                requires_expansion=False,
                expansion_notes="",
                tech_specs=TechnicalSpecs(
                    power_consumption=0,  # Passive component
                    weight=0.5,  # kg
                    dimensions={'D': 80, 'H': 80, 'tube_od': 6},  # mm
                    material_spec="6mm OD x 4mm ID copper tube",
                    operating_temp=(20, 60),  # Water cooled
                    max_temp=80,
                    cooling_required="2 L/min water flow",
                    connections=["6mm compression water fittings", "100A electrical lugs"]
                )
            ),
            Component(
                name="Induction Cooling Pump",
                category=ComponentCategory.CRUCIBLE,
                type=ComponentType.COTS,
                specification="Hygger HG-909, 800L/h submersible",
                quantity=1,
                unit_cost=25,
                total_cost=25,
                notes="Circulates cooling water for coil",
                supplier="Amazon #B07L54XBDL",
                requires_expansion=False,
                expansion_notes="",
                tech_specs=TechnicalSpecs(
                    power_consumption=10,  # W
                    power_type='DC',
                    power_voltage=12,
                    flow_rate=13.3,  # L/min max
                    weight=0.3,  # kg
                    dimensions={'L': 65, 'W': 45, 'H': 55},  # mm
                    operating_temp=(5, 35)
                )
            ),
            Component(
                name="Induction Radiator",
                category=ComponentCategory.CRUCIBLE,
                type=ComponentType.COTS,
                specification="120mm aluminum with fan",
                quantity=1,
                unit_cost=35,
                total_cost=35,
                notes="Heat dissipation for cooling loop",
                supplier="Amazon #B019OCLHKE",
                requires_expansion=False,
                expansion_notes="",
                tech_specs=TechnicalSpecs(
                    power_consumption=3,  # W fan power
                    power_type='DC',
                    power_voltage=12,
                    thermal_dissipation=500,  # W heat rejection capacity
                    weight=0.4,  # kg
                    dimensions={'L': 155, 'W': 120, 'H': 28},  # mm
                )
            ),
            Component(
                name="Induction Flow Sensor",
                category=ComponentCategory.CRUCIBLE,
                type=ComponentType.COTS,
                specification="YF-S201 Hall effect, 1-30L/min",
                quantity=1,
                unit_cost=8,
                total_cost=8,
                notes="Safety interlock for cooling flow",
                supplier="Amazon #B00VKAT7EE",
                requires_expansion=False,
                expansion_notes="",
                tech_specs=TechnicalSpecs(
                    power_consumption=0.05,  # W
                    power_type='DC',
                    power_voltage=5,
                    accuracy=10,  # % of reading
                    connections=["G1/2 thread", "3-wire: 5V, GND, pulse"],
                    control_signal="Square wave, 4.5 pulses/L"
                )
            ),
            Component(
                name="Induction Power Meter",
                category=ComponentCategory.CRUCIBLE,
                type=ComponentType.COTS,
                specification="PZEM-022 with 100A CT",
                quantity=1,
                unit_cost=18,
                total_cost=18,
                notes="Monitors actual power consumption",
                supplier="Amazon #B07J2Q4YWW",
                requires_expansion=False,
                expansion_notes="",
                tech_specs=TechnicalSpecs(
                    power_consumption=0.5,  # W
                    voltage_range=(80, 260),  # VAC measurement
                    accuracy=1,  # % of reading
                    connections=["UART TTL", "100A split-core CT"],
                    control_signal="9600 baud UART"
                )
            ),
            Component(
                name="Induction Interface PCB",
                category=ComponentCategory.CRUCIBLE,
                type=ComponentType.CUSTOM,
                specification="2-layer FR4, optoisolated I/O",
                quantity=1,
                unit_cost=30,
                total_cost=30,
                notes="Connects STM32 to induction system",
                material="FR4 PCB",
                process="JLCPCB fabrication",
                requires_expansion=False,
                expansion_notes="",
                tech_specs=TechnicalSpecs(
                    power_consumption=1,  # W
                    dimensions={'L': 100, 'W': 80, 'thickness': 1.6},  # mm
                    connections=["20-pin STM32", "8-pin Phoenix", "Sensor headers"]
                )
            ),
            Component(
                name="Induction Enclosure",
                category=ComponentCategory.CRUCIBLE,
                type=ComponentType.COTS,
                specification="BUD NBF-32026, 14×10×6 inch NEMA 12",
                quantity=1,
                unit_cost=95,
                total_cost=95,
                notes="Safety enclosure for induction system",
                supplier="DigiKey #377-1894-ND",
                requires_expansion=False,
                expansion_notes="",
                tech_specs=TechnicalSpecs(
                    weight=3.2,  # kg
                    dimensions={'L': 356, 'W': 254, 'H': 152},  # mm
                    material_spec="16 gauge steel, powder coated",
                    mounting_type="Wall mount with cooling clearance"
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
                    connections=["Type K/J/PT100 input", "SSR/Relay output"],
                    control_signal="12V DC SSR drive, 30mA max"
                )
            ),
            Component(
                name="Thermocouples",
                category=ComponentCategory.CRUCIBLE,
                type=ComponentType.COTS,
                specification="Type K MI cable, Inconel 600 sheath, 1/4\" x 12\"",
                quantity=2,
                unit_cost=75.00,
                total_cost=150.00,
                notes="Induction crucible monitoring - Primary + backup",
                part_number="KMQSS-062U-12",
                supplier="Omega Engineering",
                lead_time_weeks=2,
                requires_expansion=False,
                expansion_notes="Limited to 1350°C - consider Type R/S for 1580°C requirement",
                tech_specs=TechnicalSpecs(
                    power_consumption=0,
                    weight=0.05,  # kg each
                    dimensions={'D': 6.35, 'L': 300},  # mm (1/4" x 12")
                    material_spec="Type K, Mineral Insulated, Inconel 600 sheath",
                    operating_temp=(-200, 1350),
                    max_temp=1400,  # Short-term
                    accuracy=2.2,  # ±°C or 0.75% above 375°C
                    connections=["Standard K-type plug", "Ungrounded junction"],
                    control_signal="Type K millivolt output (0-54.9mV @ 1350°C)",
                    mounting_type="1/4\" compression fitting"
                )
            ),
            Component(
                name="TC Mounting Kit",
                category=ComponentCategory.CRUCIBLE,
                type=ComponentType.COTS,
                specification="Industrial TC mounting: fittings, thermowells, ceramic paste",
                quantity=1,
                unit_cost=95.00,
                total_cost=95.00,
                notes="Professional mounting hardware for high-temp thermocouples",
                part_number="KIT-TC-MOUNT",
                supplier="Swagelok/McMaster-Carr",
                lead_time_weeks=1,
                requires_expansion=False,
                expansion_notes="",
                tech_specs=TechnicalSpecs(
                    power_consumption=0,
                    weight=0.3,  # kg total
                    material_spec="316SS fittings, alumina thermowells, ceramic paste",
                    operating_temp=(0, 1600),
                    max_temp=1700,
                    connections=["1/4\" NPT process connection", "1/4\" tube compression"],
                    mounting_type="Weld-in or threaded"
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
                    power_type='DC',  # DC powered at 12V
                    power_voltage=12,  # 12V DC
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
                name="Mean Well RSP-1500-48",
                category=ComponentCategory.POWER_CONTROL,
                type=ComponentType.COTS,
                specification="48V 32A switching power supply with PFC",
                quantity=1,
                unit_cost=400,
                total_cost=400,
                notes="Right-sized for 1.3kW DC load, 83% utilization",
                supplier="https://www.mouser.com/ProductDetail/MEAN-WELL/RSP-1500-48",
                requires_expansion=False,
                expansion_notes="",
                tech_specs=TechnicalSpecs(
                    power_consumption=110,  # Input losses at 91% efficiency
                    power_supply=1536,      # Output capacity
                    power_type='DC',
                    power_voltage=48,
                    voltage_nominal=48,
                    voltage_range=(43.2, 52.8),  # ±10% adjustment
                    current_draw=14.4,  # A input at full load (1650W / 115V)
                    weight=1.8,  # kg
                    dimensions={'L': 295, 'W': 127, 'H': 41},  # mm
                    operating_temp=(-20, 70),  # °C with derating above 50°C
                    max_temp=70,
                    thermal_dissipation=110,  # W heat generated
                    cooling_required="forced air",
                    efficiency=91,  # %
                    connections=["AC input terminal", "DC output terminal"],
                    control_signal="Remote on/off, voltage adjust"
                )
            ),
            Component(
                name="FPGA Board",
                category=ComponentCategory.POWER_CONTROL,
                type=ComponentType.COTS,
                specification="ElectroPeak EP4CE6E22C8N Development Board (Cyclone IV)",
                quantity=1,
                unit_cost=62.00,
                total_cost=62.00,
                notes="Per VDATP reference - proven for acoustic steering control",
                part_number="EP4CE6E22C8N",
                supplier="ElectroPeak",
                lead_time_weeks=2,
                requires_expansion=False,
                expansion_notes="",
                tech_specs=TechnicalSpecs(
                    power_consumption=2.0,  # W typical operation
                    voltage_nominal=5.0,  # V DC input
                    voltage_range=(4.5, 5.5),  # V DC input range
                    weight=0.05,  # kg (board only)
                    dimensions={'L': 70, 'W': 50, 'H': 15},  # mm
                    operating_temp=(0, 85),  # °C
                    frequency=50000000,  # Hz (50 MHz crystal)
                    connections=[
                        "USB-Blaster JTAG",
                        "91 user I/O pins",
                        "USB power/programming",
                        "DC 5V jack",
                        "256Mbit SDRAM",
                        "Camera interface"
                    ],
                    control_signal="3.3V LVTTL I/O standard",
                    power_type='DC',
                    power_voltage=5.0,
                    mounting_type="Standoffs/breadboard compatible",
                    efficiency=85  # % typical for onboard regulators
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
                    power_type='DC',  # DC powered
                    power_voltage=48,  # 48V DC from PSU
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
                    power_type='DC',  # DC powered
                    power_voltage=12,  # 12V DC typical for industrial PC
                    voltage_nominal=12,  # V DC typical
                    weight=2.0,  # kg estimated
                    operating_temp=(0, 50),
                    connections=["USB 3.0", "Ethernet", "DisplayPort"],
                    control_signal="USB/Ethernet communication"
                )
            ),
            Component(
                name="Thermal Camera - FLIR A35",
                category=ComponentCategory.POWER_CONTROL,
                type=ComponentType.COTS,
                specification="A35, 320×256 pixels, 60Hz real-time tracking, 25°×20° FOV",
                quantity=1,
                unit_cost=3995,
                total_cost=3995,
                notes="Primary sensor for acoustic steering - enables real-time droplet position tracking at 60Hz",
                supplier="FLIR Systems",
                requires_expansion=False,
                expansion_notes="",
                tech_specs=TechnicalSpecs(
                    power_consumption=12,  # W via PoE+
                    voltage_nominal=48,  # V (Power over Ethernet Plus)
                    voltage_range=(44, 57),  # V PoE+ range
                    current_draw=0.25,  # A at 48V
                    weight=0.65,  # kg
                    dimensions={'L': 108, 'W': 108, 'H': 171},  # mm
                    operating_temp=(-15, 50),
                    max_temp=50,
                    thermal_dissipation=5,  # W
                    cooling_required="passive",
                    efficiency=58.3,  # % (7W useful / 12W consumed)
                    frequency=60,  # Hz frame rate - optimized for real-time droplet tracking
                    accuracy=2,  # ±°C or ±2% of reading
                    connections=["GigE Vision", "PoE+", "M12 connector"],
                    control_signal="GigE Vision protocol with real-time streaming",
                    material_spec="Ruggedized aluminum housing, IP67 rated"
                )
            ),
            Component(
                name="Emergency Stop System",
                category=ComponentCategory.POWER_CONTROL,
                type=ComponentType.COTS,
                specification="Safety relay module with mushroom buttons",
                quantity=1,
                unit_cost=350,
                total_cost=350,
                notes="Fail-safe emergency shutdown per safety requirements",
                supplier="Pilz/Banner/Similar",
                requires_expansion=False,
                expansion_notes="",
                tech_specs=TechnicalSpecs(
                    power_consumption=5,  # W for relay coils
                    voltage_nominal=24,  # V DC control
                    voltage_range=(20.4, 26.4),  # ±10%
                    current_draw=0.2,  # A
                    weight=2.0,  # kg including buttons and wiring
                    dimensions={'L': 200, 'W': 150, 'H': 100},  # mm control box
                    operating_temp=(-25, 55),
                    max_temp=70,
                    thermal_dissipation=5,  # W
                    cooling_required="none",
                    efficiency=100,  # % (relay efficiency)
                    accuracy=10,  # ms response time
                    connections=["4x mushroom buttons", "Safety relay", "Reset key"],
                    control_signal="Normally closed safety circuit",
                    material_spec="DIN rail mount safety relay, IP65 buttons"
                )
            ),
            Component(
                name="Inkbird ITC-100VH PID Kit",
                category=ComponentCategory.POWER_CONTROL,
                type=ComponentType.COTS,
                specification="PID controller with 25A SSR and K thermocouple",
                quantity=1,
                unit_cost=35,
                total_cost=35,
                notes="Complete kit for primary zone control",
                supplier="https://inkbird.com/products/itc-100vh-k-sensor-ssr",
                requires_expansion=False,
                expansion_notes="",
                tech_specs=TechnicalSpecs(
                    power_consumption=5,
                    power_type='DC',
                    power_voltage=12,  # Controller power
                    voltage_nominal=100,  # Can work 100-240VAC
                    voltage_range=(100, 240),
                    weight=0.4,  # kg for complete kit
                    dimensions={'L': 48, 'W': 48, 'H': 100},  # mm controller size
                    operating_temp=(0, 50),
                    accuracy=0.1,  # °C
                    connections=["K-type thermocouple", "SSR output", "Alarm relay"],
                    control_signal="SSR signal + alarm relay"
                )
            ),
            Component(
                name="SSR-25DA Solid State Relay",
                category=ComponentCategory.POWER_CONTROL,
                type=ComponentType.COTS,
                specification="25A DC-AC solid state relay",
                quantity=1,
                unit_cost=8,
                total_cost=8,
                notes="For second heater zone",
                supplier="Amazon/eBay generic",
                requires_expansion=False,
                expansion_notes="",
                tech_specs=TechnicalSpecs(
                    power_consumption=0.012,  # 12mA @ 5V control
                    power_type='DC',
                    power_voltage=5,  # Control signal
                    voltage_nominal=5,
                    voltage_range=(3, 32),  # VDC control range
                    current_draw=0.012,  # A control current
                    weight=0.125,  # kg
                    dimensions={'L': 60, 'W': 45, 'H': 23},  # mm
                    operating_temp=(-20, 80),
                    connections=["DC control input", "AC load output"],
                    control_signal="3-32VDC input"
                )
            ),
            Component(
                name="Type K Thermocouple (spare)",
                category=ComponentCategory.POWER_CONTROL,
                type=ComponentType.COTS,
                specification="Type K, 6mm probe, 2m cable, general purpose",
                quantity=2,  # Increase to 2 spares
                unit_cost=10.00,
                total_cost=20.00,  # Updated for 2 units
                notes="Spare thermocouples for general temperature monitoring",
                part_number="Generic-K-6mm",
                supplier="Amazon",
                lead_time_weeks=1,
                requires_expansion=False,
                expansion_notes="",
                tech_specs=TechnicalSpecs(
                    power_consumption=0,
                    weight=0.02,  # kg each
                    dimensions={'D': 6, 'L': 100},  # mm
                    material_spec="Type K, SS304 sheath",
                    operating_temp=(-50, 500),
                    max_temp=600,
                    accuracy=2.5,  # ±°C Class 2
                    connections=["Mini K-type plug", "2m PVC cable"],
                    control_signal="Type K millivolt output"
                )
            ),
            Component(
                name="2-Channel Relay Module",
                category=ComponentCategory.POWER_CONTROL,
                type=ComponentType.COTS,
                specification="5V 10A dual relay for zone selection",
                quantity=1,
                unit_cost=12,
                total_cost=12,
                notes="Switches heater pairs for 2-zone operation",
                supplier="https://robu.in/product/2-channel-isolated-5v-10a-relay-module/",
                requires_expansion=False,
                expansion_notes="",
                tech_specs=TechnicalSpecs(
                    power_consumption=0.16,  # 160mA @ 5V all on
                    power_type='DC',
                    power_voltage=5,
                    voltage_nominal=5,
                    current_draw=0.16,  # A
                    weight=0.055,  # kg
                    dimensions={'L': 50, 'W': 38, 'H': 19},  # mm
                    operating_temp=(0, 70),
                    connections=["5V power", "2× control inputs", "2× NO/NC contacts"],
                    control_signal="5V logic level"
                )
            ),
            Component(
                name="48V to 12V DC Converter",
                category=ComponentCategory.POWER_CONTROL,
                type=ComponentType.COTS,
                specification="48V to 12V 35A step-down converter",
                quantity=1,
                unit_cost=40,
                total_cost=40,
                notes="Powers PC, fans, PID controllers",
                supplier="Generic/Amazon",
                requires_expansion=False,
                expansion_notes="",
                tech_specs=TechnicalSpecs(
                    power_consumption=460,  # Input from 48V bus (accounting for efficiency)
                    power_supply=420,       # 12V @ 35A output
                    power_type='DC',
                    power_voltage=48,       # Input voltage
                    efficiency=91,
                    voltage_range=(36, 72),  # Input voltage range
                    voltage_nominal=12,      # Output voltage
                    current_draw=9.6,        # 460W/48V input current
                    weight=0.3,
                    dimensions={'L': 120, 'W': 60, 'H': 30},  # mm
                    operating_temp=(0, 60),
                    mounting_type="Chassis mount with heatsink",
                    connections=["48V input terminals", "12V output terminals"],
                    control_signal="None - always on"
                )
            ),
            Component(
                name="48V to 5V DC Converter",  
                category=ComponentCategory.POWER_CONTROL,
                type=ComponentType.COTS,
                specification="48V to 5V 15A step-down converter",
                quantity=1,
                unit_cost=30,
                total_cost=30,
                notes="Powers FPGA, STM32, logic circuits",
                supplier="Generic/Amazon",
                requires_expansion=False,
                expansion_notes="",
                tech_specs=TechnicalSpecs(
                    power_consumption=82,   # Input from 48V bus
                    power_supply=75,        # 5V @ 15A output
                    power_type='DC',
                    power_voltage=48,       # Input voltage
                    efficiency=91,
                    voltage_range=(36, 72),  # Input voltage range
                    voltage_nominal=5,       # Output voltage
                    current_draw=1.7,        # 82W/48V input current
                    weight=0.2,
                    dimensions={'L': 100, 'W': 50, 'H': 25},  # mm
                    operating_temp=(0, 60),
                    mounting_type="PCB mount",
                    connections=["48V input terminals", "5V output terminals"],
                    control_signal="None - always on"
                )
            ),
            Component(
                name="48V to 24V DC Converter",
                category=ComponentCategory.POWER_CONTROL,
                type=ComponentType.COTS,
                specification="48V to 24V 2A step-down converter",
                quantity=1,
                unit_cost=20,
                total_cost=20,
                notes="Powers stepper motors for material feed",
                supplier="Generic/Amazon",
                requires_expansion=False,
                expansion_notes="",
                tech_specs=TechnicalSpecs(
                    power_consumption=53,   # Input from 48V bus
                    power_supply=48,        # 24V @ 2A output
                    power_type='DC',
                    power_voltage=48,       # Input voltage
                    efficiency=90,
                    voltage_range=(36, 72),  # Input voltage range
                    voltage_nominal=24,      # Output voltage
                    current_draw=1.1,        # 53W/48V input current
                    weight=0.1,
                    dimensions={'L': 80, 'W': 40, 'H': 20},  # mm
                    operating_temp=(0, 60),
                    mounting_type="DIN rail",
                    connections=["48V input terminals", "24V output terminals"],
                    control_signal="None - always on"
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
    
    def get_level_scaled_cost(self) -> float:
        """Get total cost with level multiplier applied"""
        base_cost = sum(c.total_cost for c in self.components)
        return base_cost * self.LEVEL_MULTIPLIERS[self.level]['cost']
    
    def get_level_scaled_power(self) -> float:
        """Get power requirement with level multiplier applied"""
        power_budget = self.calculate_power_budget()
        base_power = power_budget['TOTAL']['net_power']
        return base_power * self.LEVEL_MULTIPLIERS[self.level]['power']
    
    def get_level_total_power(self) -> float:
        """Get total power consumption with level multiplier applied"""
        power_budget = self.calculate_power_budget()
        base_power = power_budget['TOTAL']['active_power']
        return base_power * self.LEVEL_MULTIPLIERS[self.level]['power']
    
    def get_level_transducer_count(self) -> int:
        """Get transducer count for current level"""
        return self.LEVEL_MULTIPLIERS[self.level]['transducers']
    
    def get_level_build_volume(self) -> int:
        """Get build volume for current level"""
        return self.LEVEL_MULTIPLIERS[self.level]['build_volume']
    
    def get_level_materials(self) -> List[str]:
        """Get supported materials for current level"""
        return self.LEVEL_CAPABILITIES[self.level]['materials']
    
    def get_level_build_rate(self) -> float:
        """Get build rate for current level"""
        return self.LEVEL_CAPABILITIES[self.level]['build_rate']
    
    def get_level_power_supply_required(self) -> float:
        """Calculate required power supply capacity for level"""
        # Base it on total consumption, not net
        power_budget = self.calculate_power_budget()
        base_consumption = power_budget['TOTAL']['active_power']
        scaled_consumption = base_consumption * self.LEVEL_MULTIPLIERS[self.level]['power']
        # Add 20% safety margin
        return scaled_consumption * 1.2
    
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
        """Calculate total power consumption and supply by subsystem"""
        power_budget = {}
        
        for category in ComponentCategory:
            category_power = {
                'active_power': 0,  # W - actual power consumption (positive)
                'power_supply': 0,  # W - power supplied (positive)
                'net_power': 0,     # W - net consumption (consumption - supply)
                'thermal_load': 0,  # W - heat generated
                'component_count': 0
            }
            
            for component in self.components:
                if component.category == category:
                    # Power consumption (what component uses)
                    if component.tech_specs.power_consumption:
                        total_power = component.tech_specs.power_consumption * component.quantity
                        category_power['active_power'] += total_power
                    
                    # Power supply (what component provides)
                    if component.tech_specs.power_supply:
                        supplied_power = component.tech_specs.power_supply * component.quantity
                        category_power['power_supply'] += supplied_power
                    
                    # Calculate thermal load (inefficiency)
                    if component.tech_specs.power_consumption:
                        total_power = component.tech_specs.power_consumption * component.quantity
                        if component.tech_specs.efficiency:
                            thermal_load = total_power * (1 - component.tech_specs.efficiency / 100)
                        elif component.tech_specs.thermal_dissipation:
                            thermal_load = component.tech_specs.thermal_dissipation * component.quantity
                        else:
                            # Assume 20% loss for components without efficiency data
                            thermal_load = total_power * 0.2
                        
                        category_power['thermal_load'] += thermal_load
                    
                    if component.tech_specs.power_consumption or component.tech_specs.power_supply:
                        category_power['component_count'] += component.quantity
            
            # Calculate net power (consumption - supply)
            category_power['net_power'] = category_power['active_power'] - category_power['power_supply']
            
            power_budget[category.value] = category_power
        
        # Calculate totals (only sum category values, not including TOTAL)
        category_values = list(power_budget.values())
        power_budget['TOTAL'] = {
            'active_power': sum(pb['active_power'] for pb in category_values),
            'power_supply': sum(pb['power_supply'] for pb in category_values),
            'net_power': sum(pb['net_power'] for pb in category_values),
            'thermal_load': sum(pb['thermal_load'] for pb in category_values),
            'component_count': sum(pb['component_count'] for pb in category_values)
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
    
    def calculate_dual_domain_power(self):
        """Calculate power split between AC and DC domains"""
        
        power_domains = {
            'AC': {
                'components': {},
                'total': 0,
                'voltage_groups': {120: 0, 240: 0}
            },
            'DC': {
                'components': {},
                'total': 0,
                'voltage_groups': {48: 0, 24: 0, 12: 0, 5: 0}
            },
            'PSU': {
                'capacity': 15000,  # 15kW PSU
                'dc_load': 0,
                'efficiency': 0.91,
                'margin': 0,
                'utilization': 0
            }
        }
        
        for component in self.components:
            if not component.tech_specs or not component.tech_specs.power_consumption:
                continue
                
            power = component.tech_specs.power_consumption * component.quantity
            power_type = component.tech_specs.power_type or 'DC'  # Default to DC if not specified
            voltage = component.tech_specs.power_voltage or 48
            
            if power_type == 'AC':
                power_domains['AC']['components'][component.name] = {
                    'power': power,
                    'voltage': voltage,
                    'quantity': component.quantity
                }
                power_domains['AC']['total'] += power
                if voltage in power_domains['AC']['voltage_groups']:
                    power_domains['AC']['voltage_groups'][voltage] += power
            else:  # DC or unspecified
                power_domains['DC']['components'][component.name] = {
                    'power': power,
                    'voltage': voltage,
                    'quantity': component.quantity
                }
                power_domains['DC']['total'] += power
                power_domains['PSU']['dc_load'] += power
                if voltage in power_domains['DC']['voltage_groups']:
                    power_domains['DC']['voltage_groups'][voltage] += power
        
        # Calculate PSU metrics
        power_domains['PSU']['margin'] = power_domains['PSU']['capacity'] - power_domains['PSU']['dc_load']
        power_domains['PSU']['utilization'] = (power_domains['PSU']['dc_load'] / power_domains['PSU']['capacity']) * 100
        
        return power_domains

    def get_power_architecture_note(self):
        """Return explanation of AC/DC separation"""
        return """
    POWER ARCHITECTURE - DUAL DOMAIN
    ================================
    
    DC DOMAIN (Through PSU):
    - Acoustic system: 585W
    - Control electronics: 250W
    - Cooling/sensors: 415W
    - Material feed: 30W
    - TOTAL DC: 1,280W
    - PSU: RSP-1500-48 (1,536W capacity)
    - Utilization: 83%
    
    AC DOMAIN (Direct from mains):
    - Bed heaters: 2,000W (SSR switched)
    - Induction heater: 3,000W (contactor)
    - Micro heaters: 1,000W (SSR bank)
    - TOTAL AC: 6,000W
    
    TOTAL WALL POWER: ~7.4kW (DC + AC)
    """


"""
Heater Installation Pattern (150mm diameter copper disc):
    
    Top View:
         37.5mm
           ↓
      H1 ─────── H2     
       │         │      H1,H2 = Zone 1 (Primary)
       │    ●    │      H3,H4 = Zone 2 (Secondary)
       │         │      
      H3 ─────── H4     
         50mm spacing
         
Drilling Specifications:
- Hole diameter: 12.7mm (0.500")  
- Hole depth: 25mm (leave 5mm bottom)
- Position: 37.5mm from center
- Pattern: Square, 50mm spacing
- Finish: Ream for tight fit
"""

"""
Electrical Architecture:

120V AC Mains
    │
    ├─[20A Breaker]─┬─[SSR-1]──[H1: Heater 1 - Zone 1]
    │               ├─[SSR-1]──[H2: Heater 2 - Zone 1]
    │               ├─[SSR-2]──[H3: Heater 3 - Zone 2]
    │               └─[SSR-2]──[H4: Heater 4 - Zone 2]
    │
    └─[5V PSU]──[Arduino/Control]
         │
         ├──[ITC-100VH PID]──[SSR-1 control]
         ├──[Relay Module]───[Zone switching]
         └──[Thermocouples]──[Temperature feedback]

Operating Modes:
1. Normal: H1+H2 active (2000W)
2. Boost: H1+H2+H3+H4 (4000W for fast heat-up)
3. Redundant: H3+H4 if H1 or H2 fails
4. Uniform: Alternate pairs for better distribution
"""

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