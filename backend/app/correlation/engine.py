import uuid
import random
import numpy as np
from typing import List, Dict, Any, Optional
from datetime import datetime
from backend.app.correlation.risk_scorer import calculate_incident_risk_score
from backend.app.core.config import settings

class IncidentCorrelationEngine:
    def __init__(self, time_window_minutes: int = 60):
        self.time_window_minutes = time_window_minutes

    def map_mitre_stages(self, events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Maps correlated event sequences to MITRE ATT&CK tactics & techniques.
        """
        stages = []
        
        for idx, evt in enumerate(events):
            evt_type = evt.get("event_type", "").lower()
            cmd = str(evt.get("command", "")).lower()
            status = evt.get("status", "")
            time_str = evt.get("timestamp", "")
            
            stage_info = None
            
            if "failed login" in evt_type or "auth" in evt_type and status == "Failure":
                stage_info = {
                    "stage_id": f"stage_{idx+1}",
                    "stage_name": "Authentication Failure / Password Spraying",
                    "tactic": "Credential Access (TA0006)",
                    "technique": "Brute Force / Password Guessing",
                    "mitre_id": "T1110.001",
                    "timestamp": time_str,
                    "evidence": f"Multiple authentication failures from IP {evt.get('source_ip', 'unknown')} targeting user {evt.get('username', 'unknown')}",
                    "confidence": 0.94
                }
            elif "successful login" in evt_type or ("login" in evt_type and status == "Success"):
                stage_info = {
                    "stage_id": f"stage_{idx+1}",
                    "stage_name": "Initial Access via Valid Accounts",
                    "tactic": "Initial Access (TA0001)",
                    "technique": "Valid Accounts: Domain Accounts",
                    "mitre_id": "T1078.002",
                    "timestamp": time_str,
                    "evidence": f"Successful session established for {evt.get('username')} from {evt.get('source_ip')}",
                    "confidence": 0.91
                }
            elif "privilege" in evt_type or "sudo" in cmd or "admin" in cmd:
                stage_info = {
                    "stage_id": f"stage_{idx+1}",
                    "stage_name": "Privilege Escalation / Sudo Execution",
                    "tactic": "Privilege Escalation (TA0004)",
                    "technique": "Sudo and Sudo Caching / Token Manipulation",
                    "mitre_id": "T1548.003",
                    "timestamp": time_str,
                    "evidence": f"Elevated privileges requested on {evt.get('device')} via command: {evt.get('command') or 'sudo elevation'}",
                    "confidence": 0.88
                }
            elif "sensitive access" in evt_type or "database query" in evt_type or "shadow" in cmd or "read" in evt_type:
                stage_info = {
                    "stage_id": f"stage_{idx+1}",
                    "stage_name": "Discovery & Sensitive File Collection",
                    "tactic": "Collection (TA0009)",
                    "technique": "Data from Local System / Security Account Manager",
                    "mitre_id": "T1005",
                    "timestamp": time_str,
                    "evidence": f"Access to sensitive repository/database on {evt.get('device')}",
                    "confidence": 0.86
                }
            elif "exfiltrat" in evt_type or "transfer" in evt_type or int(evt.get("bytes_transferred", 0) or 0) > 1000000:
                stage_info = {
                    "stage_id": f"stage_{idx+1}",
                    "stage_name": "High-Volume Data Exfiltration",
                    "tactic": "Exfiltration (TA0010)",
                    "technique": "Exfiltration Over C2 Channel / Web Service",
                    "mitre_id": "T1041",
                    "timestamp": time_str,
                    "evidence": f"Anomalous outbound transfer of {evt.get('bytes_transferred', 0)} bytes to {evt.get('destination_ip')}",
                    "confidence": 0.95
                }
            elif "lateral" in evt_type or "smb" in evt_type or "ssh" in evt_type:
                stage_info = {
                    "stage_id": f"stage_{idx+1}",
                    "stage_name": "Lateral Movement across Endpoints",
                    "tactic": "Lateral Movement (TA0008)",
                    "technique": "Remote Services: SSH / SMB / Windows Admin Shares",
                    "mitre_id": "T1021.002",
                    "timestamp": time_str,
                    "evidence": f"Lateral connection established to {evt.get('destination_ip')}",
                    "confidence": 0.89
                }

            if stage_info:
                stages.append(stage_info)
                
        return stages

    def generate_timeline(self, events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        timeline = []
        for e in events:
            timeline.append({
                "time": e.get("timestamp", ""),
                "event_type": e.get("event_type", "Security Event"),
                "description": f"{e.get('event_type')} on {e.get('device', 'unknown')} by {e.get('username', 'system')} (Status: {e.get('status', 'OK')})",
                "severity": e.get("severity", "Medium"),
                "status": e.get("status", "Success"),
                "source_ip": e.get("source_ip"),
                "destination_ip": e.get("destination_ip"),
                "username": e.get("username"),
                "device": e.get("device")
            })
        return sorted(timeline, key=lambda x: x.get("time", ""))

    def correlate_cluster(self, cluster_events: List[Dict[str, Any]], cluster_alerts: List[Dict[str, Any]], incident_code: str = None) -> Dict[str, Any]:
        """
        Synthesizes a cluster of related events & alerts into a coherent Incident.
        """
        sorted_events = sorted(cluster_events, key=lambda x: x.get("timestamp", ""))
        
        affected_assets = list({e.get("device") for e in sorted_events if e.get("device")})
        affected_users = list({e.get("username") for e in sorted_events if e.get("username")})
        
        attack_chain = self.map_mitre_stages(sorted_events)
        timeline = self.generate_timeline(sorted_events)
        
        risk_data = calculate_incident_risk_score(
            events=sorted_events,
            alerts=cluster_alerts,
            affected_assets=affected_assets,
            attack_stages_count=len(attack_chain)
        )
        
        # Primary Title
        categories = list({a.get("attack_type") for a in cluster_alerts if a.get("attack_type") and a.get("attack_type") != "Normal"})
        primary_cat = categories[0] if categories else "Suspicious Activity"
        
        if len(attack_chain) >= 3:
            title = f"Multi-Stage Cyber Attack: Credential Compromise to Data Exfiltration"
            primary_cat = "Multi-Stage Attack"
        else:
            title = f"Potential {primary_cat} Detected on {affected_assets[0] if affected_assets else 'Endpoint'}"

        inc_id = incident_code or f"CG-{np.random.randint(1000, 9999)}"

        return {
            "incident_id": inc_id,
            "title": title,
            "category": primary_cat,
            "severity": risk_data["level"],
            "risk_score": risk_data["score"],
            "status": "Active",
            "description": f"Correlated incident involving {len(sorted_events)} events across {len(affected_assets)} endpoints and {len(affected_users)} user account(s).",
            "affected_assets": affected_assets,
            "affected_users": affected_users,
            "event_ids": [e.get("id") or e.get("_id") for e in sorted_events if e.get("id") or e.get("_id")],
            "alert_ids": [a.get("alert_id") or a.get("id") for a in cluster_alerts if a.get("alert_id") or a.get("id")],
            "timeline": timeline,
            "attack_chain": attack_chain,
            "risk_assessment": risk_data,
            "created_at": sorted_events[0].get("timestamp") if sorted_events else datetime.utcnow().isoformat(),
            "updated_at": sorted_events[-1].get("timestamp") if sorted_events else datetime.utcnow().isoformat()
        }

correlation_engine = IncidentCorrelationEngine()
