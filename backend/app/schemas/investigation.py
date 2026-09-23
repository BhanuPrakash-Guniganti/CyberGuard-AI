from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class InvestigationChatMessage(BaseModel):
    role: str # "user" | "assistant" | "system"
    content: str
    timestamp: Optional[str] = None
    grounding: Optional[Dict[str, Any]] = None

class InvestigationRequest(BaseModel):
    query: Optional[str] = None
    force_refresh: bool = False

class StructuredInvestigationResult(BaseModel):
    summary: str
    evidence: List[str]
    timeline_analysis: List[str]
    possible_attack_behaviors: List[Dict[str, str]]
    affected_assets: List[str]
    risk_explanation: str
    recommendations: List[Dict[str, Any]]
    uncertainty: List[str]
    tool_executions: Optional[List[Dict[str, Any]]] = []
    rag_sources: Optional[List[Dict[str, Any]]] = []

class InvestigationResponse(BaseModel):
    incident_id: str
    status: str
    result: StructuredInvestigationResult
