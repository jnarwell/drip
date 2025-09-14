"""
Design Verification Matrix for Acoustic Manufacturing System
Maps requirements to test methods and acceptance criteria
"""

from dataclasses import dataclass
from typing import List, Dict
from datetime import datetime
import pandas as pd

@dataclass
class VerificationItem:
    """Single verification requirement"""
    subsystem: str
    requirement_id: str
    requirement_desc: str
    test_method: str
    test_equipment: List[str]
    acceptance_criteria: str
    responsible_engineer: str
    test_phase: str
    status: str = "Not Started"
    test_date: str = ""
    results: str = ""
    notes: str = ""

# Define verification matrix
verification_matrix = [
    # Acoustic Array Verification
    VerificationItem(
        subsystem="Acoustic Array",
        requirement_id="SR001",
        requirement_desc="10kHz operation frequency",
        test_method="Frequency spectrum analysis",
        test_equipment=["Oscilloscope", "Spectrum analyzer", "Hydrophone"],
        acceptance_criteria="9.9-10.1 kHz measured frequency",
        responsible_engineer="Acoustic Engineer",
        test_phase="Level 1"
    ),
    VerificationItem(
        subsystem="Acoustic Array",
        requirement_id="SR002",
        requirement_desc="Droplet steering accuracy ±0.3mm",
        test_method="High-speed optical tracking",
        test_equipment=["High-speed camera >1000fps", "Telecentric lens", "Image analysis software"],
        acceptance_criteria="<0.3mm deviation from target over 100 droplets",
        responsible_engineer="Test Engineer",
        test_phase="Level 1"
    ),
    VerificationItem(
        subsystem="Acoustic Array",
        requirement_id="SR011",
        requirement_desc="Transducer array scaling",
        test_method="Phased array uniformity test",
        test_equipment=["Acoustic field scanner", "Phase meter"],
        acceptance_criteria="Phase uniformity <5°, amplitude uniformity <10%",
        responsible_engineer="Acoustic Engineer",
        test_phase="Level 2"
    ),
    
    # Thermal System Verification
    VerificationItem(
        subsystem="Thermal System",
        requirement_id="SR003",
        requirement_desc="Temperature range 700-1580°C",
        test_method="Calibrated thermocouple measurement",
        test_equipment=["Type B thermocouples", "Data logger", "Optris PI 1M camera"],
        acceptance_criteria=">1580°C achieved and maintained for 30 min",
        responsible_engineer="Thermal Engineer",
        test_phase="Level 2"
    ),
    VerificationItem(
        subsystem="Thermal System",
        requirement_id="SR009",
        requirement_desc="Chamber temperature <300°C",
        test_method="Multi-point temperature mapping",
        test_equipment=["Type K thermocouples (x12)", "Thermal camera"],
        acceptance_criteria="All points <300°C during operation",
        responsible_engineer="Thermal Engineer",
        test_phase="Level 1"
    ),
    VerificationItem(
        subsystem="Thermal System",
        requirement_id="SR010",
        requirement_desc="Cooling rate >1000°C/s",
        test_method="Pyrometer measurement of droplet",
        test_equipment=["High-speed pyrometer", "Optris PI 1M"],
        acceptance_criteria=">1000°C/s measured on 10 consecutive droplets",
        responsible_engineer="Process Engineer",
        test_phase="Level 2"
    ),
    
    # Material Quality Verification
    VerificationItem(
        subsystem="Material Quality",
        requirement_id="SR006",
        requirement_desc="Material density >95%",
        test_method="Archimedes density measurement",
        test_equipment=["Precision scale", "Density kit", "Optical microscope"],
        acceptance_criteria=">95% theoretical density, <5% porosity",
        responsible_engineer="Materials Engineer",
        test_phase="Level 1"
    ),
    VerificationItem(
        subsystem="Material Quality",
        requirement_id="SR007",
        requirement_desc="Build rate 25 cm³/hr (Level 4)",
        test_method="Volumetric measurement",
        test_equipment=["Precision scale", "3D scanner", "Timer"],
        acceptance_criteria="25±2 cm³/hr over 4-hour test",
        responsible_engineer="Process Engineer",
        test_phase="Level 4"
    ),
    
    # Control System Verification
    VerificationItem(
        subsystem="Control System",
        requirement_id="SR014",
        requirement_desc="FPGA + STM32 + PC architecture",
        test_method="Communication latency test",
        test_equipment=["Logic analyzer", "Oscilloscope"],
        acceptance_criteria="<1ms control loop, <100μs phase update",
        responsible_engineer="Controls Engineer",
        test_phase="Level 1"
    ),
    VerificationItem(
        subsystem="Control System",
        requirement_id="SR013",
        requirement_desc="Thermal camera integration",
        test_method="Closed-loop tracking test",
        test_equipment=["Optris PI 1M", "Test droplet generator"],
        acceptance_criteria="Track 100 droplets with <5% loss",
        responsible_engineer="Software Engineer",
        test_phase="Level 1"
    ),
    
    # System Integration Verification
    VerificationItem(
        subsystem="System Integration",
        requirement_id="SR004",
        requirement_desc="Power budget compliance",
        test_method="Power consumption measurement",
        test_equipment=["Power analyzer", "Current probes"],
        acceptance_criteria="Level 1: <12kW, Level 2: <25kW, Level 4: <45kW",
        responsible_engineer="Systems Engineer",
        test_phase="All Levels"
    ),
    VerificationItem(
        subsystem="System Integration",
        requirement_id="SR005",
        requirement_desc="Build volume capability",
        test_method="Working envelope verification",
        test_equipment=["CMM", "Test artifacts"],
        acceptance_criteria="Level 1: 125cm³, Level 4: 8000cm³ accessible",
        responsible_engineer="Mechanical Engineer",
        test_phase="Level 1, 4"
    ),
    
    # Multi-Material Verification (Level 3)
    VerificationItem(
        subsystem="Multi-Material",
        requirement_id="SR003.1",
        requirement_desc="Al-Steel bonding interface",
        test_method="Destructive tensile test",
        test_equipment=["Tensile tester", "SEM", "EDS"],
        acceptance_criteria=">70% base material strength",
        responsible_engineer="Materials Engineer",
        test_phase="Level 3"
    ),
    VerificationItem(
        subsystem="Multi-Material",
        requirement_id="SR010.1",
        requirement_desc="Interface cooling control",
        test_method="Thermal gradient measurement",
        test_equipment=["Multi-channel pyrometer", "Thermal model"],
        acceptance_criteria="Controlled gradient <500°C/mm",
        responsible_engineer="Process Engineer",
        test_phase="Level 3"
    )
]

def generate_verification_report(phase: str = None) -> pd.DataFrame:
    """Generate verification matrix report for specific phase or all"""
    data = []
    
    for item in verification_matrix:
        if phase is None or item.test_phase == phase or phase in item.test_phase:
            data.append({
                'Subsystem': item.subsystem,
                'Req ID': item.requirement_id,
                'Requirement': item.requirement_desc,
                'Test Method': item.test_method,
                'Acceptance': item.acceptance_criteria,
                'Phase': item.test_phase,
                'Status': item.status
            })
    
    return pd.DataFrame(data)

def generate_test_procedure(verification_item: VerificationItem) -> str:
    """Generate detailed test procedure document"""
    procedure = f"""
TEST PROCEDURE: {verification_item.requirement_id}
{'='*60}

REQUIREMENT: {verification_item.requirement_desc}
SUBSYSTEM: {verification_item.subsystem}
TEST PHASE: {verification_item.test_phase}

1. OBJECTIVE
   Verify that {verification_item.requirement_desc} meets the acceptance criteria:
   {verification_item.acceptance_criteria}

2. TEST EQUIPMENT
   Required equipment:
   {chr(10).join([f'   • {eq}' for eq in verification_item.test_equipment])}

3. TEST METHOD
   {verification_item.test_method}

4. PROCEDURE
   4.1 Pre-test Setup
       - Calibrate all test equipment
       - Document initial conditions
       - Verify safety protocols
   
   4.2 Test Execution
       - Implement {verification_item.test_method}
       - Record data at specified intervals
       - Monitor for anomalies
   
   4.3 Data Collection
       - Record all measurements
       - Document any deviations
       - Capture photographic evidence

5. ACCEPTANCE CRITERIA
   {verification_item.acceptance_criteria}

6. RESPONSIBLE ENGINEER
   {verification_item.responsible_engineer}

7. APPROVALS
   Test Engineer: _________________ Date: _______
   Quality Assurance: _____________ Date: _______
   Project Manager: _______________ Date: _______
"""
    return procedure

def calculate_verification_progress() -> Dict:
    """Calculate verification progress statistics"""
    total = len(verification_matrix)
    by_status = {}
    by_phase = {}
    
    for item in verification_matrix:
        # Count by status
        by_status[item.status] = by_status.get(item.status, 0) + 1
        
        # Count by phase
        by_phase[item.test_phase] = by_phase.get(item.test_phase, 0) + 1
    
    return {
        'total_tests': total,
        'by_status': by_status,
        'by_phase': by_phase,
        'completion_rate': by_status.get('Passed', 0) / total * 100 if total > 0 else 0
    }

if __name__ == "__main__":
    # Generate Level 1 verification report
    print("LEVEL 1 VERIFICATION MATRIX")
    print("="*80)
    level1_df = generate_verification_report("Level 1")
    print(level1_df.to_string(index=False))
    
    # Generate sample test procedure
    print("\n\nSAMPLE TEST PROCEDURE")
    print("="*80)
    print(generate_test_procedure(verification_matrix[0]))
    
    # Show progress statistics
    print("\n\nVERIFICATION PROGRESS")
    print("="*80)
    progress = calculate_verification_progress()
    print(f"Total Tests: {progress['total_tests']}")
    print(f"Status Breakdown: {progress['by_status']}")
    print(f"Phase Breakdown: {progress['by_phase']}")
    print(f"Completion Rate: {progress['completion_rate']:.1f}%")