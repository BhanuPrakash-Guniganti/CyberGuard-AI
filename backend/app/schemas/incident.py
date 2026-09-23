from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class AttackStage(BaseModel):
    stage_id: str
    stage_name: str
    tactic: str
    technique: str
    mitre_id: str
    timestamp: str
    evidence: str
    confidence: float

class TimelineEvent(BaseModel):
    time: str
    event_type: str
    description: str
    severity: str
    status: str
    source_ip: Optional[str] = None
    destination_ip: Optional[str] = None
    username: Optional[str] = None
    device: Optional[str] = None

class IncidentBase(BaseModel):
    incident_id: str
    title: str
    category: str
    severity: str
    risk_score: int
    status: str = "Active"
    description: str
    affected_assets: List[str]
    affected_users: List[str]
    created_at: str
    updated_at: str

class IncidentCreate(IncidentBase):
    alert_ids: List[str] = []
    event_ids: List[str] = []
    timeline: List[TimelineEvent] = []
    attack_chain: List[AttackStage] = []

class IncidentResponse(IncidentBase):
    id: str
    alert_ids: List[str] = []
    event_ids: List[str] = []
    timeline: List[TimelineEvent] = []
    attack_chain: List[AttackStage] = []
    summary: Optional[str] = None
    risk_assessment: Optional[Dict[str, Any]] = None
    recommendations: Optional[List[Dict[str, Any]]] = []
    response_simulation_status: Optional[str] = "PENDING"
