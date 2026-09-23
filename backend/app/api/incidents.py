from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from backend.app.core.database import get_db
from backend.app.schemas.incident import IncidentResponse, IncidentCreate

router = APIRouter(prefix="/incidents", tags=["Incidents"])

@router.get("", response_model=List[IncidentResponse])
async def list_incidents(
    severity: Optional[str] = None,
    status: Optional[str] = None,
    category: Optional[str] = None,
    db = Depends(get_db)
):
    coll = db.get_collection("incidents")
    incidents = await coll.find()

    filtered = []
    for inc in incidents:
        if severity and severity.lower() != "all" and inc.get("severity", "").lower() != severity.lower():
            continue
        if status and status.lower() != "all" and inc.get("status", "").lower() != status.lower():
            continue
        if category and category.lower() != "all" and inc.get("category", "").lower() != category.lower():
            continue
        filtered.append(inc)

    # Sort by risk score descending
    filtered.sort(key=lambda x: x.get("risk_score", 0), reverse=True)

    res = []
    for inc in filtered:
        res.append(IncidentResponse(
            id=inc.get("id") or inc.get("incident_id", ""),
            incident_id=inc.get("incident_id", ""),
            title=inc.get("title", "Security Incident"),
            category=inc.get("category", "General"),
            severity=inc.get("severity", "High"),
            risk_score=inc.get("risk_score", 70),
            status=inc.get("status", "Active"),
            description=inc.get("description", ""),
            affected_assets=inc.get("affected_assets", []),
            affected_users=inc.get("affected_users", []),
            created_at=inc.get("created_at", ""),
            updated_at=inc.get("updated_at", ""),
            alert_ids=inc.get("alert_ids", []),
            event_ids=inc.get("event_ids", []),
            timeline=inc.get("timeline", []),
            attack_chain=inc.get("attack_chain", []),
            summary=inc.get("summary"),
            risk_assessment=inc.get("risk_assessment"),
            recommendations=inc.get("recommendations", []),
            response_simulation_status=inc.get("response_simulation_status", "PENDING")
        ))
    return res

@router.get("/{incident_id}", response_model=IncidentResponse)
async def get_incident_detail(incident_id: str, db = Depends(get_db)):
    coll = db.get_collection("incidents")
    inc = await coll.find_one({"incident_id": incident_id})
    if not inc:
        inc = await coll.find_one({"id": incident_id})
    if not inc:
        raise HTTPException(status_code=404, detail=f"Incident {incident_id} not found")

    return IncidentResponse(
        id=inc.get("id") or inc.get("incident_id", ""),
        incident_id=inc.get("incident_id", ""),
        title=inc.get("title", "Security Incident"),
        category=inc.get("category", "General"),
        severity=inc.get("severity", "High"),
        risk_score=inc.get("risk_score", 70),
        status=inc.get("status", "Active"),
        description=inc.get("description", ""),
        affected_assets=inc.get("affected_assets", []),
        affected_users=inc.get("affected_users", []),
        created_at=inc.get("created_at", ""),
        updated_at=inc.get("updated_at", ""),
        alert_ids=inc.get("alert_ids", []),
        event_ids=inc.get("event_ids", []),
        timeline=inc.get("timeline", []),
        attack_chain=inc.get("attack_chain", []),
        summary=inc.get("summary"),
        risk_assessment=inc.get("risk_assessment"),
        recommendations=inc.get("recommendations", []),
        response_simulation_status=inc.get("response_simulation_status", "PENDING")
    )
