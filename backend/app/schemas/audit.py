from pydantic import BaseModel
from typing import Optional, Dict, Any

class AuditLogResponse(BaseModel):
    id: str
    timestamp: str
    user: str
    action: str
    incident_id: Optional[str] = None
    target: Optional[str] = None
    reason: Optional[str] = None
    approval_status: Optional[str] = None
    simulation_status: Optional[str] = None
    details: Optional[Dict[str, Any]] = None
