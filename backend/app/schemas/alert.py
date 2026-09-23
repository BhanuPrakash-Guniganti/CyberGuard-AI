from pydantic import BaseModel
from typing import Optional, Dict, Any, List

class AlertBase(BaseModel):
    event_id: str
    prediction: str
    attack_type: str
    confidence: float
    severity: str
    source: str
    device: str
    timestamp: str
    status: str = "Open"
    raw_event: Optional[Dict[str, Any]] = None

class AlertCreate(AlertBase):
    alert_id: Optional[str] = None

class AlertResponse(AlertBase):
    id: str
    alert_id: str
    incident_id: Optional[str] = None
