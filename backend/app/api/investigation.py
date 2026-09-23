from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any, Optional
from backend.app.schemas.investigation import InvestigationRequest, InvestigationResponse, StructuredInvestigationResult
from backend.app.agents.investigator import investigator_agent
from backend.app.core.database import get_db

router = APIRouter(prefix="/investigate", tags=["AI Investigation"])

@router.post("/{incident_id}", response_model=InvestigationResponse)
async def trigger_investigation(incident_id: str, req: Optional[InvestigationRequest] = None, db = Depends(get_db)):
    query = req.query if req else None
    
    # Check if existing cached investigation exists and force_refresh is False
    if req and not req.force_refresh and not query:
        inv_coll = db.get_collection("investigations")
        existing = await inv_coll.find_one({"incident_id": incident_id})
        if existing and existing.get("result"):
            return InvestigationResponse(
                incident_id=incident_id,
                status="CACHED",
                result=StructuredInvestigationResult(**existing["result"])
            )

    result = await investigator_agent.investigate_incident(incident_id=incident_id, query=query)
    
    if result.get("status") == "NOT_FOUND":
        raise HTTPException(status_code=404, detail=f"Incident {incident_id} not found.")

    return InvestigationResponse(
        incident_id=incident_id,
        status="SUCCESS",
        result=StructuredInvestigationResult(**result["result"])
    )
