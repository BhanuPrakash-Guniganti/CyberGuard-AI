from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from backend.app.core.database import get_db
from backend.app.schemas.alert import AlertResponse

router = APIRouter(prefix="/alerts", tags=["Alerts"])

@router.get("", response_model=List[AlertResponse])
async def list_alerts(
    severity: Optional[str] = None,
    status: Optional[str] = None,
    search: Optional[str] = None,
    db = Depends(get_db)
):
    coll = db.get_collection("alerts")
    alerts = await coll.find()

    filtered = []
    for a in alerts:
        if severity and severity.lower() != "all" and a.get("severity", "").lower() != severity.lower():
            continue
        if status and status.lower() != "all" and a.get("status", "").lower() != status.lower():
            continue
        if search:
            q = search.lower()
            if not any(q in str(a.get(k, "")).lower() for k in ["alert_id", "attack_type", "source", "device"]):
                continue
        filtered.append(a)

    filtered.sort(key=lambda x: x.get("timestamp", ""), reverse=True)

    res = []
    for a in filtered:
        res.append(AlertResponse(
            id=a.get("id") or a.get("alert_id", ""),
            alert_id=a.get("alert_id") or a.get("id", ""),
            event_id=a.get("event_id", ""),
            prediction=a.get("prediction", "Suspicious"),
            attack_type=a.get("attack_type", "Anomaly"),
            confidence=a.get("confidence", 0.8),
            severity=a.get("severity", "Medium"),
            source=a.get("source", "unknown"),
            device=a.get("device", "unknown"),
            timestamp=a.get("timestamp", ""),
            status=a.get("status", "Open"),
            incident_id=a.get("incident_id"),
            raw_event=a.get("raw_event")
        ))
    return res

@router.get("/{alert_id}", response_model=AlertResponse)
async def get_alert_detail(alert_id: str, db = Depends(get_db)):
    coll = db.get_collection("alerts")
    alert = await coll.find_one({"alert_id": alert_id})
    if not alert:
        alert = await coll.find_one({"id": alert_id})
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    return AlertResponse(
        id=alert.get("id") or alert.get("alert_id", ""),
        alert_id=alert.get("alert_id") or alert.get("id", ""),
        event_id=alert.get("event_id", ""),
        prediction=alert.get("prediction", "Suspicious"),
        attack_type=alert.get("attack_type", "Anomaly"),
        confidence=alert.get("confidence", 0.8),
        severity=alert.get("severity", "Medium"),
        source=alert.get("source", "unknown"),
        device=alert.get("device", "unknown"),
        timestamp=alert.get("timestamp", ""),
        status=alert.get("status", "Open"),
        incident_id=alert.get("incident_id"),
        raw_event=alert.get("raw_event")
    )
