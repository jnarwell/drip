"""
Missing Interface Definitions
These interfaces need ICDs but were not in the original set
"""

from models.interfaces.interface_registry import Interface, InterfaceType, InterfaceCriticality

MISSING_INTERFACES = [
    Interface(
        icd_number="ICD-006",
        name="Crucible Material Feed Interface",
        side_a_subsystem="Crucible Subsystem",
        side_b_subsystem="Power/Control Subsystem",
        side_a_components=["Material Feed Motor", "Feed Controller"],
        side_b_components=["STM32 Dev Board", "Motor Driver"],
        interface_types=[InterfaceType.ELECTRICAL, InterfaceType.DATA, InterfaceType.MECHANICAL],
        criticality=InterfaceCriticality.HIGH
    ),
    
    Interface(
        icd_number="ICD-007",
        name="Thermal Camera Data Interface",
        side_a_subsystem="Power/Control Subsystem",
        side_b_subsystem="Power/Control Subsystem",
        side_a_components=["Optris PI 1M"],
        side_b_components=["Industrial PC", "FPGA Board"],
        interface_types=[InterfaceType.DATA],
        criticality=InterfaceCriticality.HIGH
    ),
    
    Interface(
        icd_number="ICD-008",
        name="Acoustic Array Phasing Interface",
        side_a_subsystem="Acoustic Cylinder Subsystem",
        side_b_subsystem="Power/Control Subsystem",
        side_a_components=["Transducer Array", "Phase Shifters"],
        side_b_components=["FPGA Board", "DAC Array"],
        interface_types=[InterfaceType.ELECTRICAL, InterfaceType.DATA],
        criticality=InterfaceCriticality.HIGH  # CRITICAL level
    ),
    
    Interface(
        icd_number="ICD-009",
        name="Multi-Outlet Distribution Interface",
        side_a_subsystem="Crucible Subsystem",
        side_b_subsystem="Crucible Subsystem",
        side_a_components=["25-Outlet Manifold", "Flow Controllers"],
        side_b_components=["Distribution Valves", "Pressure Sensors"],
        interface_types=[InterfaceType.MECHANICAL, InterfaceType.THERMAL],
        criticality=InterfaceCriticality.HIGH
    ),
    
    Interface(
        icd_number="ICD-010",
        name="Emergency Shutdown Interface",
        side_a_subsystem="Power/Control Subsystem",
        side_b_subsystem="All Subsystems",
        side_a_components=["E-Stop Controller", "Safety PLC"],
        side_b_components=["All Power Components"],
        interface_types=[InterfaceType.ELECTRICAL, InterfaceType.DATA],
        criticality=InterfaceCriticality.HIGH  # CRITICAL level
    )
]

def add_missing_interfaces():
    """Add missing interfaces to the system registry"""
    from models.interfaces.interface_registry import SYSTEM_INTERFACES
    
    # Add missing interfaces to the system list
    for interface in MISSING_INTERFACES:
        if not any(i.icd_number == interface.icd_number for i in SYSTEM_INTERFACES):
            SYSTEM_INTERFACES.append(interface)
    
    print(f"Added {len(MISSING_INTERFACES)} missing interfaces")
    print("Total system interfaces: ", len(SYSTEM_INTERFACES))
    
    return SYSTEM_INTERFACES