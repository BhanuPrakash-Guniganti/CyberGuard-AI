from fastapi import APIRouter, Depends, Query
from typing import List, Optional, Dict, Any
from backend.app.core.database import get_db
from backend.app.schemas.event import SecurityEventResponse, SecurityEventCreate
from backend.app.ml.predict import ml_service

router = APIRouter(prefix="/events", tags=["Security Events"])

@router.get("", response_model=List[SecurityEventResponse])
async def list_security_events(
    severity: Optional[str] = None,
    event_type: Optional[str] = None,
    status: Optional[str] = None,
    search: Optional[str] = None,
    limit: int = Query(50, le=200),
    offset: int = 0,
    db = Depends(get_db)
):
    coll = db.get_collection("security_events")
    events = await coll.find()

    # Filter in memory for robust multi-field search
    filtered = []
    for e in events:
        if severity and severity.lower() != "all" and e.get("severity", "").lower() != severity.lower():
            continue
        if event_type and event_type.lower() != "all" and e.get("event_type", "").lower() != event_type.lower():
            continue
        if status and status.lower() != "all" and e.get("status", "").lower() != status.lower():
            continue
        if search:
            q = search.lower()
            match = any(
                q in str(e.get(k, "")).lower() 
                for k in ["source_ip", "destination_ip", "username", "device", "event_type", "id", "command"]
            )
            if not match:
                continue
        filtered.append(e)

    # Sort descending by timestamp
    filtered.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
    sliced = filtered[offset:offset+limit]

    res = []
    for e in sliced:
        res.append(SecurityEventResponse(
            id=e.get("id") or e.get("_id", ""),
            timestamp=e.get("timestamp", ""),
            source_ip=e.get("source_ip", ""),
            destination_ip=e.get("destination_ip", ""),
            username=e.get("username", ""),
            device=e.get("device", ""),
            event_type=e.get("event_type", ""),
            status=e.get("status", ""),
            severity=e.get("severity", "Medium"),
            port=e.get("port"),
            protocol=e.get("protocol", "TCP"),
            bytes_transferred=e.get("bytes_transferred", 0),
            failed_attempts_count=e.get("failed_attempts_count", 0),
            command=e.get("command"),
            process_name=e.get("process_name"),
            is_anomaly=e.get("is_anomaly", False),
            anomaly_score=e.get("anomaly_score", 0.0),
            predicted_attack_type=e.get("predicted_attack_type"),
            prediction_confidence=e.get("prediction_confidence"),
            correlated_incident_id=e.get("correlated_incident_id")
        ))
    return res

@router.post("", response_model=SecurityEventResponse)
async def ingest_security_event(event_in: SecurityEventCreate, db = Depends(get_db)):
    coll = db.get_collection("security_events")
    event_dict = event_in.dict()
    
    # Run ML prediction on the fly
    ml_res = ml_service.predict_event(event_dict)
    event_dict["is_anomaly"] = ml_res["is_anomaly"]
    event_dict["anomaly_score"] = ml_res["anomaly_score"]
    event_dict["predicted_attack_type"] = ml_res["attack_type"]
    event_dict["prediction_confidence"] = ml_res["confidence"]
    
    if "id" not in event_dict or not event_dict["id"]:
        import uuid
        event_dict["id"] = f"EVT-{uuid.uuid4().hex[:6].upper()}"

    await coll.insert_one(event_dict)

    # If suspicious, generate alert
    if ml_res["is_suspicious"] or event_dict.get("severity") in ["High", "Critical"]:
        alerts_coll = db.get_collection("alerts")
        alert_doc = {
            "id": f"ALT-{event_dict['id'].replace('EVT-', '')}",
            "alert_id": f"ALT-{event_dict['id'].replace('EVT-', '')}",
            "event_id": event_dict["id"],
            "prediction": ml_res["prediction"],
            "attack_type": ml_res["attack_type"] if ml_res["attack_type"] != "Normal" else "Behavioral Anomaly",
            "confidence": ml_res["confidence"],
            "severity": event_dict["severity"],
            "source": event_dict["source_ip"],
            "device": event_dict["device"],
            "timestamp": event_dict["timestamp"],
            "status": "Open",
            "incident_id": None,
            "raw_event": event_dict
        }
        await alerts_coll.insert_one(alert_doc)

    return SecurityEventResponse(**event_dict)
