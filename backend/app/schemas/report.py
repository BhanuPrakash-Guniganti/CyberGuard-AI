from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class IncidentReportResponse(BaseModel):
    report_id: str
    incident_id: str
    generated_at: str
    analyst_name: str
    title: str
    severity: str
    risk_score: int
    executive_summary: str
    evidence_summary: List[str]
    affected_assets: List[str]
    timeline: List[Dict[str, Any]]
    possible_attack_behaviors: List[Dict[str, Any]]
    ai_investigation_findings: Dict[str, Any]
    recommendations: List[Dict[str, Any]]
    policy_decision: Optional[Dict[str, Any]] = None
    response_simulations: List[Dict[str, Any]] = []
    audit_trail: List[Dict[str, Any]] = []
    disclaimer: str = "Simulation Only — Academic Prototype. Actual Infrastructure Not Modified."
