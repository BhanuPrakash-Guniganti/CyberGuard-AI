from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any
from backend.app.schemas.response import PolicyCheckRequest, PolicyCheckResponse, SimulationRequest, SimulationResponse
from backend.app.simulator.policy import policy_engine
from backend.app.simulator.simulator import response_simulator
from backend.app.core.database import get_db

router = APIRouter(prefix="/response", tags=["Response & Simulation"])

@router.post("/validate", response_model=PolicyCheckResponse)
async def validate_policy(req: PolicyCheckRequest):
    val = policy_engine.validate_action(
        action=req.action,
        target=req.target,
        risk_score=req.risk_score
    )
    return PolicyCheckResponse(**val)

@router.post("/simulate", response_model=SimulationResponse)
async def simulate_response_action(req: SimulationRequest, db = Depends(get_db)):
    result = await response_simulator.simulate_response(
        incident_id=req.incident_id,
        action=req.action,
        target=req.target,
        approved=req.approved,
        analyst_notes=req.analyst_notes or "Analyst response simulation execution"
    )

    return SimulationResponse(
        simulation_id=result["simulation_id"],
        incident_id=result["incident_id"],
        action=result["action"],
        target=result["target"],
        status=result["status"],
        execution_time=result["execution_time"],
        policy_validation=result["policy_validation"],
        simulated_state_change=result["simulated_state_change"],
        actual_infrastructure_modified=False,
        message=result["message"]
    )
