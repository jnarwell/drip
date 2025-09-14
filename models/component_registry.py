"""
Unified Component Registry for Acoustic Manufacturing System
"""

from dataclasses import dataclass
from typing import Optional, List, Dict
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
                expansion_notes=""
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
                expansion_notes=""
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
                expansion_notes=""
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
                expansion_notes=""
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
                expansion_notes=""
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
                expansion_notes=""
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
                expansion_notes=""
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
                expansion_notes=""
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
                expansion_notes=""
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
                expansion_notes=""
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
                expansion_notes=""
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
                expansion_notes=""
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
                expansion_notes=""
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
                expansion_notes=""
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
                expansion_notes=""
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
                expansion_notes=""
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
                expansion_notes=""
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
                expansion_notes=""
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
                expansion_notes=""
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
                expansion_notes=""
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
                expansion_notes=""
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
                expansion_notes=""
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
                expansion_notes=""
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
                expansion_notes=""
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
                expansion_notes=""
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
                expansion_notes=""
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
                expansion_notes=""
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
                expansion_notes=""
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
                expansion_notes=""
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
                expansion_notes=""
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
                expansion_notes=""
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
                expansion_notes=""
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
                expansion_notes=""
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
                expansion_notes=""
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
                expansion_notes=""
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
                expansion_notes=""
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
                expansion_notes=""
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
                expansion_notes=""
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
                expansion_notes=""
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
                expansion_notes=""
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
                expansion_notes=""
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
                expansion_notes=""
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
                expansion_notes=""
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
                expansion_notes=""
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
                expansion_notes=""
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
                expansion_notes=""
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
                expansion_notes=""
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
                expansion_notes=""
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
                expansion_notes=""
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
                expansion_notes=""
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
                expansion_notes=""
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


# Example usage
if __name__ == "__main__":
    registry = ComponentRegistry()
    registry.print_summary()