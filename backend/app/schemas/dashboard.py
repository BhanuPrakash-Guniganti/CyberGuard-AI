from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class ThreatActivityPoint(BaseModel):
    time: str
    events_count: int
    alerts_count: int
    anomalies_count: int

class SeverityDistribution(BaseModel):
    name: str
    value: int
    color: str

class CategoryDistribution(BaseModel):
    category: str
    count: int

class DashboardStatsResponse(BaseModel):
    total_events: int
    active_incidents: int
    critical_incidents: int
    open_alerts: int
    investigated_incidents: int
    threat_activity: List[ThreatActivityPoint]
    severity_distribution: List[SeverityDistribution]
    category_distribution: List[CategoryDistribution]
    recent_alerts: List[Dict[str, Any]]
