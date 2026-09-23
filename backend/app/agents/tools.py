from typing import Dict, Any, List, Optional
from backend.app.core.database import get_db
from backend.app.rag.retriever import rag_retriever

class InvestigatorTools:
    def __init__(self):
        self.db = get_db()

    async def get_incident(self, incident_id: str) -> Optional[Dict[str, Any]]:
        collection = self.db.get_collection("incidents")
        inc = await collection.find_one({"incident_id": incident_id})
        if not inc:
            inc = await collection.find_one({"id": incident_id})
        return inc

    async def get_related_events(self, event_ids: List[str] = None, incident_id: str = None) -> List[Dict[str, Any]]:
        collection = self.db.get_collection("security_events")
        if event_ids:
            # Query by id or _id in list
            events = await collection.find()
            return [e for e in events if e.get("id") in event_ids or e.get("_id") in event_ids or e.get("correlated_incident_id") == incident_id]
        elif incident_id:
            events = await collection.find({"correlated_incident_id": incident_id})
            return events
        return []

    async def get_asset_info(self, device_name: str) -> Dict[str, Any]:
        return {
            "device_name": device_name,
            "asset_type": "Server / Workstation",
            "criticality": "Critical" if "server" in device_name.lower() or "dc" in device_name.lower() else "Medium",
            "os": "Linux Ubuntu 22.04 LTS / Windows Server 2022",
            "ip_address": "10.0.4.15",
            "status": "Monitored / Active"
        }

    async def search_knowledge(self, query: str, top_k: int = 4) -> List[Dict[str, Any]]:
        return rag_retriever.search(query=query, top_k=top_k)

investigator_tools = InvestigatorTools()
