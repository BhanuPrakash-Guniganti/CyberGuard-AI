import uuid
from typing import Dict, Any, Optional
from datetime import datetime
from backend.app.core.database import get_db

class ReportService:
    def __init__(self):
        self.db = get_db()

    async def generate_incident_report(self, incident_id: str, analyst_name: str = "Senior SOC Analyst") -> Optional[Dict[str, Any]]:
        inc_coll = self.db.get_collection("incidents")
        incident = await inc_coll.find_one({"incident_id": incident_id})
        if not incident:
            incident = await inc_coll.find_one({"id": incident_id})

        if not incident:
            return None

        # Fetch investigations
        inv_coll = self.db.get_collection("investigations")
        investigation = await inv_coll.find_one({"incident_id": incident_id}) or {}
        inv_res = investigation.get("result", {})

        # Fetch simulations
        sim_coll = self.db.get_collection("response_simulations")
        simulations = await sim_coll.find({"incident_id": incident_id})

        # Fetch audit logs
        audit_coll = self.db.get_collection("audit_logs")
        audit_trail = await audit_coll.find({"incident_id": incident_id})

        report_id = f"REP-{incident_id}-{uuid.uuid4().hex[:6].upper()}"
        generated_at = datetime.utcnow().isoformat()

        report_data = {
            "report_id": report_id,
            "incident_id": incident.get("incident_id", incident_id),
            "generated_at": generated_at,
            "analyst_name": analyst_name,
            "title": incident.get("title", "Security Incident"),
            "severity": incident.get("severity", "High"),
            "risk_score": incident.get("risk_score", 80),
            "executive_summary": inv_res.get("summary") or incident.get("description", "Security incident requiring SOC investigation."),
            "evidence_summary": inv_res.get("evidence") or [f"Event count: {len(incident.get('event_ids', []))}"],
            "affected_assets": incident.get("affected_assets", []),
            "timeline": incident.get("timeline", []),
            "possible_attack_behaviors": inv_res.get("possible_attack_behaviors") or incident.get("attack_chain", []),
            "ai_investigation_findings": {
                "timeline_analysis": inv_res.get("timeline_analysis", []),
                "risk_explanation": inv_res.get("risk_explanation", ""),
                "uncertainty": inv_res.get("uncertainty", []),
                "rag_sources": inv_res.get("rag_sources", [])
            },
            "recommendations": inv_res.get("recommendations") or incident.get("recommendations", []),
            "policy_decision": {
                "isolation_allowed": True,
                "requires_approval": True,
                "basis": "NIST SP 800-61 / Enterprise Response Policy"
            },
            "response_simulations": simulations,
            "audit_trail": audit_trail,
            "disclaimer": "Simulation Only — Academic Prototype. Actual Infrastructure Not Modified."
        }

        # Save to reports collection
        rep_coll = self.db.get_collection("reports")
        await rep_coll.insert_one(report_data)

        return report_data

report_service = ReportService()
