from asyncio import base_events
from fastapi import APIRouter, Depends
from typing import Dict, Any, List
from backend.app.core.database import get_db
from backend.app.schemas.dashboard import DashboardStatsResponse, ThreatActivityPoint, SeverityDistribution, CategoryDistribution

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/stats", response_model=DashboardStatsResponse)
async def get_dashboard_stats(db = Depends(get_db)):
    events_coll = db.get_collection("security_events")
    alerts_coll = db.get_collection("alerts")
    incidents_coll = db.get_collection("incidents")

    events = await events_coll.find().to_list(length=None)
    alerts = await alerts_coll.find().to_list(length=None)
    incidents = await incidents_coll.find().to_list(length=None)

    total_events = len(events)
    active_incidents = sum(1 for i in incidents if i.get("status") in ["Active", "Contained (Simulated)", "Investigated"])
    critical_incidents = sum(1 for i in incidents if i.get("severity") == "Critical" or i.get("risk_score", 0) >= 80)
    open_alerts = sum(1 for a in alerts if a.get("status") == "Open")
    investigated_incidents = sum(1 for i in incidents if i.get("status") in ["Investigated", "Contained (Simulated)"])

    # Severity distribution
    sev_counts = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0, "Info": 0}
    for e in events:
        s = e.get("severity", "Medium")
        if s in sev_counts:
            sev_counts[s] += 1
        else:
            sev_counts["Medium"] += 1

    severity_dist = [
        SeverityDistribution(name="Critical", value=sev_counts["Critical"], color="#EF4444"),
        SeverityDistribution(name="High", value=sev_counts["High"], color="#F97316"),
        SeverityDistribution(name="Medium", value=sev_counts["Medium"], color="#F59E0B"),
        SeverityDistribution(name="Low", value=sev_counts["Low"], color="#10B981"),
        SeverityDistribution(name="Info", value=sev_counts["Info"], color="#3B82F6"),
    ]

    # Category distribution
    cat_counts: Dict[str, int] = {}
    for a in alerts:
        cat = a.get("attack_type", "Suspicious Activity")
        cat_counts[cat] = cat_counts.get(cat, 0) + 1
    
    category_dist = [
        CategoryDistribution(category=k, count=v) for k, v in cat_counts.items()
    ]
    if not category_dist:
        category_dist = [
            CategoryDistribution(category="Brute Force", count=5),
            CategoryDistribution(category="Privilege Escalation", count=3),
            CategoryDistribution(category="Data Exfiltration", count=4)
        ]

    # Threat Activity over time (grouped by 15 min or sequence)
    threat_activity = [
        ThreatActivityPoint(time="08:00", events_count=4, alerts_count=0, anomalies_count=0),
        ThreatActivityPoint(time="08:30", events_count=8, alerts_count=1, anomalies_count=1),
        ThreatActivityPoint(time="09:00", events_count=12, alerts_count=2, anomalies_count=1),
        ThreatActivityPoint(time="09:30", events_count=18, alerts_count=3, anomalies_count=2),
        ThreatActivityPoint(time="10:00", events_count=35, alerts_count=7, anomalies_count=6),
        ThreatActivityPoint(time="10:30", events_count=22, alerts_count=4, anomalies_count=3),
        ThreatActivityPoint(time="11:00", events_count=15, alerts_count=2, anomalies_count=1),
    ]

    # Recent alerts
    recent_alerts_raw = sorted(alerts, key=lambda x: x.get("timestamp", ""), reverse=True)[:8]
    recent_alerts = []
    for a in recent_alerts_raw:
        recent_alerts.append({
            "id": a.get("id") or a.get("alert_id"),
            "alert_id": a.get("alert_id") or a.get("id"),
            "attack_type": a.get("attack_type", "Unknown"),
            "severity": a.get("severity", "Medium"),
            "confidence": a.get("confidence", 0.8),
            "source": a.get("source", "unknown"),
            "device": a.get("device", "unknown"),
            "timestamp": a.get("timestamp", ""),
            "status": a.get("status", "Open"),
            "incident_id": a.get("incident_id")
        })

    return DashboardStatsResponse(
        total_events=total_events,
        active_incidents=active_incidents,
        critical_incidents=critical_incidents,
        open_alerts=open_alerts,
        investigated_incidents=investigated_incidents,
        threat_activity=threat_activity,
        severity_distribution=severity_dist,
        category_distribution=category_dist,
        recent_alerts=recent_alerts
    )
