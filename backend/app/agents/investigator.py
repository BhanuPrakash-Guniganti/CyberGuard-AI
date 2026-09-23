import time
from typing import Dict, Any, List, Optional
from datetime import datetime
from backend.app.agents.tools import investigator_tools
from backend.app.services.ai_service import ai_service
from backend.app.core.database import get_db

class IncidentInvestigatorAgent:
    def __init__(self):
        self.tools = investigator_tools
        self.ai = ai_service
        self.db = get_db()

    async def investigate_incident(self, incident_id: str, query: Optional[str] = None) -> Dict[str, Any]:
        """
        Executes controlled, deterministic multi-step agentic workflow:
        1. Tool: get_incident()
        2. Tool: get_related_events()
        3. Tool: get_asset_info()
        4. Tool: search_knowledge() [RAG Retrieval]
        5. AI Analysis Engine (Grounding & MITRE Mapping)
        6. Persist Investigation & Tool Execution Record
        """
        tool_executions = []
        
        # Step 1: Retrieve Incident
        t0 = time.time()
        incident = await self.tools.get_incident(incident_id)
        tool_executions.append({
            "step": 1,
            "tool_name": "get_incident",
            "input": {"incident_id": incident_id},
            "output_summary": f"Retrieved incident {incident_id} ({incident.get('title') if incident else 'Not Found'})",
            "duration_ms": round((time.time() - t0) * 1000, 2),
            "status": "SUCCESS" if incident else "FAILED"
        })

        if not incident:
            return {
                "incident_id": incident_id,
                "status": "NOT_FOUND",
                "result": {
                    "summary": f"Incident {incident_id} not found in database.",
                    "evidence": [],
                    "timeline_analysis": [],
                    "possible_attack_behaviors": [],
                    "affected_assets": [],
                    "risk_explanation": "No incident record available.",
                    "recommendations": [],
                    "uncertainty": ["Incident ID does not exist."]
                }
            }

        # Step 2: Retrieve Related Events
        t1 = time.time()
        event_ids = incident.get("event_ids", [])
        events = await self.tools.get_related_events(event_ids=event_ids, incident_id=incident_id)
        tool_executions.append({
            "step": 2,
            "tool_name": "get_related_events",
            "input": {"event_count": len(event_ids), "incident_id": incident_id},
            "output_summary": f"Retrieved {len(events)} correlated security telemetry events",
            "duration_ms": round((time.time() - t1) * 1000, 2),
            "status": "SUCCESS"
        })

        # Step 3: Identify & Inspect Assets
        t2 = time.time()
        assets_info = []
        for asset in incident.get("affected_assets", []):
            info = await self.tools.get_asset_info(asset)
            assets_info.append(info)
        tool_executions.append({
            "step": 3,
            "tool_name": "get_asset_info",
            "input": {"assets": incident.get("affected_assets", [])},
            "output_summary": f"Inspected {len(assets_info)} endpoint host profiles",
            "duration_ms": round((time.time() - t2) * 1000, 2),
            "status": "SUCCESS"
        })

        # Step 4: Search Knowledge Base (RAG)
        t3 = time.time()
        rag_query = f"{incident.get('title')} {incident.get('category')} incident response recommendations containment"
        rag_results = await self.tools.search_knowledge(rag_query, top_k=4)
        tool_executions.append({
            "step": 4,
            "tool_name": "search_knowledge",
            "input": {"query": rag_query, "top_k": 4},
            "output_summary": f"Retrieved {len(rag_results)} relevant knowledge base playbooks & MITRE references",
            "duration_ms": round((time.time() - t3) * 1000, 2),
            "status": "SUCCESS"
        })

        # Step 5: Run Grounded AI Synthesis
        t4 = time.time()
        investigation_findings = await self.ai.generate_incident_investigation(
            incident=incident,
            related_events=events,
            rag_context=rag_results,
            user_query=query
        )
        tool_executions.append({
            "step": 5,
            "tool_name": "ai_synthesis_engine",
            "input": {"evidence_count": len(events), "rag_chunks": len(rag_results)},
            "output_summary": "Generated structured evidence attribution, MITRE mappings, and containment playbooks",
            "duration_ms": round((time.time() - t4) * 1000, 2),
            "status": "SUCCESS"
        })

        investigation_findings["tool_executions"] = tool_executions
        
        # Persist investigation
        inv_collection = self.db.get_collection("investigations")
        inv_record = {
            "incident_id": incident_id,
            "investigated_at": datetime.utcnow().isoformat(),
            "query": query,
            "result": investigation_findings
        }
        await inv_collection.insert_one(inv_record)

        # Update incident with summary & recommendations
        inc_collection = self.db.get_collection("incidents")
        await inc_collection.update_one(
            {"incident_id": incident_id},
            {
                "$set": {
                    "summary": investigation_findings.get("summary"),
                    "recommendations": investigation_findings.get("recommendations", []),
                    "status": "Investigated"
                }
            }
        )

        return {
            "incident_id": incident_id,
            "status": "SUCCESS",
            "result": investigation_findings
        }

investigator_agent = IncidentInvestigatorAgent()
