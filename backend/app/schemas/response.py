from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class PolicyCheckRequest(BaseModel):
    incident_id: str
    action: str # "REVOKE_SESSION" | "ISOLATE_ENDPOINT" | "BLOCK_SOURCE" | "INCREASE_MONITORING" | "ESCALATE_INCIDENT"
    target: str
    risk_score: int

class PolicyCheckResponse(BaseModel):
    action: str
    target: str
    allowed: bool
    requires_approval: bool
    reason: str
    impact_level: str # "LOW" | "MEDIUM" | "HIGH" | "CRITICAL"

class SimulationRequest(BaseModel):
    incident_id: str
    action: str
    target: str
    approved: bool
    analyst_notes: Optional[str] = "Approved by SOC Analyst"

class SimulationResponse(BaseModel):
    simulation_id: str
    incident_id: str
    action: str
    target: str
    status: str # "SIMULATED_SUCCESS" | "REJECTED_BY_POLICY" | "PENDING_APPROVAL"
    execution_time: str
    policy_validation: Dict[str, Any]
    simulated_state_change: Dict[str, Any]
    actual_infrastructure_modified: bool = False
    message: str = "Simulation Only — Actual Infrastructure Not Modified."
