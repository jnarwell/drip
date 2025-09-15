"""
Verification Status Tracker
Maintains single source of truth for all verification activities
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List, Dict
from enum import Enum

class VerificationStatus(Enum):
    NOT_STARTED = "Not Started"
    IN_PREPARATION = "In Preparation"
    IN_PROGRESS = "In Progress"
    COMPLETE_PASS = "Complete - Pass"
    COMPLETE_FAIL = "Complete - Fail"
    COMPLETE_CONDITIONAL = "Complete - Conditional"
    BLOCKED = "Blocked"
    DEFERRED = "Deferred"

@dataclass
class VerificationRecord:
    requirement_id: str
    requirement_desc: str
    verification_method: str
    status: VerificationStatus
    test_date: Optional[datetime] = None
    test_report_id: Optional[str] = None
    measured_value: Optional[str] = None
    pass_fail: Optional[bool] = None
    notes: Optional[str] = None
    evidence_files: List[str] = None
    
    def __post_init__(self):
        if self.evidence_files is None:
            self.evidence_files = []
    
    def can_claim_verified(self) -> bool:
        """Requirement can only be claimed as verified if test is complete with pass"""
        return (
            self.status == VerificationStatus.COMPLETE_PASS and
            self.test_date is not None and
            self.test_report_id is not None and
            len(self.evidence_files) > 0
        )

class VerificationTracker:
    def __init__(self):
        self.records: Dict[str, VerificationRecord] = {}
        self.initialize_requirements()
    
    def initialize_requirements(self):
        """Initialize all requirements with NOT_STARTED status"""
        requirements = [
            ("SR001", "40kHz ±100Hz acoustic frequency", "Spectrum analysis"),
            ("SR002", "±0.3-0.5mm steering accuracy", "Optical tracking"),
            ("SR003", "700-1580°C temperature range", "Thermocouple"),
            ("SR004", "Power scaling 12-45kW", "Power meter"),
            ("SR005", "Build volume 125-8000cm³", "CMM measurement"),
            ("SR006", ">95% material density", "Archimedes"),
            ("SR007", "25 cm³/hr build rate (L4)", "Volumetric"),
            ("SR008", "<$95/kg operating cost", "Cost analysis"),
            ("SR009", "Chamber temp <300°C", "Thermal mapping"),
            ("SR010", ">1000°C/s cooling rate", "Pyrometer"),
            ("SR011", "Scalable transducer array", "Field mapping"),
            ("SR012", "25 parallel outlets", "Visual inspection"),
            ("SR013", "Thermal camera integration", "Latency test"),
            ("SR014", "FPGA control architecture", "Logic analyzer"),
            ("SR015", "MERV 13 air filtration", "Flow measurement"),
        ]
        
        for req_id, desc, method in requirements:
            self.records[req_id] = VerificationRecord(
                requirement_id=req_id,
                requirement_desc=desc,
                verification_method=method,
                status=VerificationStatus.NOT_STARTED
            )
    
    def update_status(self, req_id: str, status: VerificationStatus, **kwargs):
        """Update verification status with evidence"""
        if req_id not in self.records:
            raise ValueError(f"Requirement {req_id} not found")
        
        record = self.records[req_id]
        record.status = status
        
        # Update additional fields if provided
        for key, value in kwargs.items():
            if hasattr(record, key):
                setattr(record, key, value)
    
    def get_verification_summary(self) -> Dict:
        """Get summary of verification status"""
        summary = {
            "total": len(self.records),
            "verified": 0,
            "in_progress": 0,
            "not_started": 0,
            "blocked": 0,
            "by_status": {}
        }
        
        for record in self.records.values():
            status_name = record.status.value
            summary["by_status"][status_name] = summary["by_status"].get(status_name, 0) + 1
            
            if record.can_claim_verified():
                summary["verified"] += 1
            elif record.status == VerificationStatus.IN_PROGRESS:
                summary["in_progress"] += 1
            elif record.status == VerificationStatus.NOT_STARTED:
                summary["not_started"] += 1
            elif record.status == VerificationStatus.BLOCKED:
                summary["blocked"] += 1
        
        summary["completion_percentage"] = (summary["verified"] / summary["total"]) * 100
        return summary
    
    def generate_verification_matrix(self) -> str:
        """Generate markdown verification matrix with accurate status"""
        lines = []
        lines.append("| ID | Requirement | Method | Status | Evidence |")
        lines.append("|----|-------------|--------|--------|----------|")
        
        for req_id, record in sorted(self.records.items()):
            status_icon = self._get_status_icon(record.status)
            evidence = "✅" if len(record.evidence_files) > 0 else "❌"
            
            lines.append(
                f"| {req_id} | {record.requirement_desc} | "
                f"{record.verification_method} | {status_icon} {record.status.value} | {evidence} |"
            )
        
        return "\n".join(lines)
    
    def _get_status_icon(self, status: VerificationStatus) -> str:
        """Get icon for status display"""
        icons = {
            VerificationStatus.NOT_STARTED: "📋",
            VerificationStatus.IN_PREPARATION: "🔧",
            VerificationStatus.IN_PROGRESS: "🔄",
            VerificationStatus.COMPLETE_PASS: "✅",
            VerificationStatus.COMPLETE_FAIL: "❌",
            VerificationStatus.COMPLETE_CONDITIONAL: "⚠️",
            VerificationStatus.BLOCKED: "🚫",
            VerificationStatus.DEFERRED: "⏸️"
        }
        return icons.get(status, "❓")

# Usage example
if __name__ == "__main__":
    tracker = VerificationTracker()
    
    # Example: Update a requirement that has actually been tested
    # tracker.update_status(
    #     "SR001",
    #     VerificationStatus.COMPLETE_PASS,
    #     test_date=datetime.now(),
    #     test_report_id="TR-001-2025",
    #     measured_value="40.02 kHz ± 0.08 kHz",
    #     pass_fail=True,
    #     evidence_files=["test_data/TR-001/spectrum_analysis.csv"],
    #     notes="All 18 transducers within specification"
    # )
    
    # Generate accurate status report
    summary = tracker.get_verification_summary()
    print("Verification Status Summary:")
    print(f"  Total Requirements: {summary['total']}")
    print(f"  Verified: {summary['verified']}")
    print(f"  In Progress: {summary['in_progress']}")
    print(f"  Not Started: {summary['not_started']}")
    print(f"  Completion: {summary['completion_percentage']:.1f}%")
    
    print("\n" + tracker.generate_verification_matrix())