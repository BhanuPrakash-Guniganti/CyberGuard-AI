from fastapi import APIRouter, Depends
from typing import List
from backend.app.core.database import get_db
from backend.app.schemas.audit import AuditLogResponse

router = APIRouter(prefix="/audit", tags=["Audit Log"])

@router.get("", response_model=List[AuditLogResponse])
async def get_audit_logs(db = Depends(get_db)):
    coll = db.get_collection("audit_logs")
    logs = await coll.find()
    logs.sort(key=lambda x: x.get("timestamp", ""), reverse=True)

    res = []
    for l in logs:
        res.append(AuditLogResponse(
            id=l.get("id") or l.get("_id", ""),
            timestamp=l.get("timestamp", ""),
            user=l.get("user", "analyst"),
            action=l.get("action", "SOC_ACTION"),
            incident_id=l.get("incident_id"),
            target=l.get("target"),
            reason=l.get("reason"),
            approval_status=l.get("approval_status"),
            simulation_status=l.get("simulation_status"),
            details=l.get("details")
        ))
    return res
