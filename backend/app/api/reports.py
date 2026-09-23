from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any
from backend.app.schemas.report import IncidentReportResponse
from backend.app.services.report_service import report_service
from backend.app.core.database import get_db

router = APIRouter(prefix="/reports", tags=["Incident Reports"])

@router.get("/{incident_id}", response_model=IncidentReportResponse)
async def get_incident_report(incident_id: str, db = Depends(get_db)):
    report = await report_service.generate_incident_report(incident_id=incident_id)
    if not report:
        raise HTTPException(status_code=404, detail=f"Incident {incident_id} not found for report generation")

    return IncidentReportResponse(**report)
