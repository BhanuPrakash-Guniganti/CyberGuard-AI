import uuid
from typing import Dict, Any, Optional
from datetime import datetime
from backend.app.simulator.policy import policy_engine
from backend.app.core.database import get_db

class ResponseSimulator:
    def __init__(self):
        self.policy = policy_engine
        self.db = get_db()
        # Simulated environment state
        self.simulated_state = {
            "isolated_endpoints": set(),
            "revoked_sessions": set(),
            "blocked_ips": set(),
            "monitored_targets": set(),
            "escalated_incidents": set()
        }

    async def simulate_response(
        self,
        incident_id: str,
        action: str,
        target: str,
        approved: bool,
        user_email: str = "analyst@cyberguard.ai",
        analyst_notes: str = "Authorized defensive simulation"
    ) -> Dict[str, Any]:
        """
        Executes safe simulation of the defensive response.
        Mutates ONLY simulated sandbox state.
        Guarantees: Actual infrastructure is NEVER modified.
        """
        # Retrieve incident to get risk score
        inc_coll = self.db.get_collection("incidents")
        incident = await inc_coll.find_one({"incident_id": incident_id}) or {}
        risk_score = incident.get("risk_score", 75)

        # Validate against policy engine
        validation = self.policy.validate_action(action=action, target=target, risk_score=risk_score)

        sim_id = f"SIM-{uuid.uuid4().hex[:8].upper()}"
        timestamp = datetime.utcnow().isoformat()

        # Check approval requirement
        if validation["requires_approval"] and not approved:
            status = "PENDING_APPROVAL"
            state_change = {"effect": "Awaiting human analyst authorization"}
            message = "Action requires human approval before simulation can execute."
        elif not validation["allowed"]:
            status = "REJECTED_BY_POLICY"
            state_change = {"effect": "None - action violates policy"}
            message = f"Simulation rejected: {validation['reason']}"
        else:
            status = "SIMULATED_SUCCESS"
            action_clean = action.upper().strip()
            
            # Apply to sandbox memory
            if action_clean == "ISOLATE_ENDPOINT":
                self.simulated_state["isolated_endpoints"].add(target)
                state_change = {
                    "isolated_host": target,
                    "simulated_network_status": "DISCONNECTED_EXCEPT_EDR",
                    "simulated_firewall_rule": f"DROP ALL EXCEPT TCP:8443 TO EDR-CONSOLE FROM {target}"
                }
            elif action_clean == "REVOKE_SESSION":
                self.simulated_state["revoked_sessions"].add(target)
                state_change = {
                    "revoked_user": target,
                    "simulated_token_status": "INVALIDATED",
                    "simulated_mfa_requirement": "ENFORCED_NEXT_LOGON"
                }
            elif action_clean == "BLOCK_SOURCE":
                self.simulated_state["blocked_ips"].add(target)
                state_change = {
                    "blocked_ip": target,
                    "simulated_perimeter_rule": f"REJECT INBOUND PACKETS FROM {target} DROP SILENT"
                }
            elif action_clean == "INCREASE_MONITORING":
                self.simulated_state["monitored_targets"].add(target)
                state_change = {
                    "monitored_target": target,
                    "simulated_sampling_rate": "100%_FULL_PACKET_CAPTURE",
                    "retention_days": 30
                }
            elif action_clean == "ESCALATE_INCIDENT":
                self.simulated_state["escalated_incidents"].add(incident_id)
                state_change = {
                    "escalated_incident_id": incident_id,
                    "simulated_tier": "TIER_3_RED_TEAM_LEAD"
                }
            else:
                state_change = {"effect": "Generic sandbox action applied"}

            message = "Simulation Only — Actual Infrastructure Not Modified."

        # Save simulation record
        sim_record = {
            "simulation_id": sim_id,
            "incident_id": incident_id,
            "action": action,
            "target": target,
            "status": status,
            "execution_time": timestamp,
            "policy_validation": validation,
            "simulated_state_change": state_change,
            "actual_infrastructure_modified": False,
            "analyst_notes": analyst_notes,
            "user": user_email,
            "message": message
        }

        sim_coll = self.db.get_collection("response_simulations")
        await sim_coll.insert_one(sim_record)

        # Audit Log Entry
        audit_coll = self.db.get_collection("audit_logs")
        await audit_coll.insert_one({
            "timestamp": timestamp,
            "user": user_email,
            "action": f"SIMULATE_{action.upper()}",
            "incident_id": incident_id,
            "target": target,
            "reason": analyst_notes,
            "approval_status": "APPROVED" if approved else "NOT_APPROVED",
            "simulation_status": status,
            "details": {
                "simulation_id": sim_id,
                "impact_level": validation["impact_level"],
                "actual_infrastructure_modified": False
            }
        })

        # Update Incident status
        if status == "SIMULATED_SUCCESS":
            await inc_coll.update_one(
                {"incident_id": incident_id},
                {"$set": {"response_simulation_status": "SIMULATED", "status": "Contained (Simulated)"}}
            )

        return sim_record

response_simulator = ResponseSimulator()
