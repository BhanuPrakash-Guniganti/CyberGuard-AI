from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime

class SecurityEventBase(BaseModel):
    timestamp: str
    source_ip: str
    destination_ip: str
    username: str
    device: str
    event_type: str
    status: str
    severity: str
    port: Optional[int] = None
    protocol: Optional[str] = "TCP"
    bytes_transferred: Optional[int] = 0
    failed_attempts_count: Optional[int] = 0
    command: Optional[str] = None
    process_name: Optional[str] = None
    details: Optional[Dict[str, Any]] = None

class SecurityEventCreate(SecurityEventBase):
    pass

class SecurityEventResponse(SecurityEventBase):
    id: str
    is_anomaly: Optional[bool] = False
    anomaly_score: Optional[float] = 0.0
    predicted_attack_type: Optional[str] = None
    prediction_confidence: Optional[float] = None
    correlated_incident_id: Optional[str] = None

class EventFilter(BaseModel):
    severity: Optional[str] = None
    event_type: Optional[str] = None
    status: Optional[str] = None
    search: Optional[str] = None
    limit: int = 50
    offset: int = 0
