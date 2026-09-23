from typing import Dict, Any

class PolicyEngine:
    def __init__(self):
        self.critical_assets = ["server-02", "dc-primary", "prod-db-01", "vault-prod", "ad-controller"]
        self.valid_actions = [
            "REVOKE_SESSION",
            "ISOLATE_ENDPOINT",
            "BLOCK_SOURCE",
            "INCREASE_MONITORING",
            "ESCALATE_INCIDENT"
        ]

    def validate_action(self, action: str, target: str, risk_score: int) -> Dict[str, Any]:
        """
        Evaluates organizational defensive policy for a given response action.
        """
        action_clean = action.upper().strip()
        if action_clean not in self.valid_actions:
            return {
                "action": action_clean,
                "target": target,
                "allowed": False,
                "requires_approval": True,
                "impact_level": "UNKNOWN",
                "reason": f"Action '{action_clean}' is not recognized in approved defensive taxonomy."
            }

        is_critical_asset = any(c.lower() in target.lower() for c in self.critical_assets)

        if action_clean == "ISOLATE_ENDPOINT":
            if is_critical_asset:
                return {
                    "action": action_clean,
                    "target": target,
                    "allowed": True,
                    "requires_approval": True,
                    "impact_level": "CRITICAL",
                    "reason": f"Target '{target}' is a mission-critical infrastructure server. Isolating will cause service degradation; Senior SOC Analyst sign-off is mandatory."
                }
            else:
                return {
                    "action": action_clean,
                    "target": target,
                    "allowed": True,
                    "requires_approval": True,
                    "impact_level": "HIGH",
                    "reason": f"Endpoint network isolation halts user operations on '{target}'. Requires analyst review before simulation."
                }

        elif action_clean == "REVOKE_SESSION":
            return {
                "action": action_clean,
                "target": target,
                "allowed": True,
                "requires_approval": False if risk_score > 60 else True,
                "impact_level": "MEDIUM",
                "reason": f"Revoking authentication session for '{target}' invalidates current access token without service disruption."
            }

        elif action_clean == "BLOCK_SOURCE":
            return {
                "action": action_clean,
                "target": target,
                "allowed": True,
                "requires_approval": False,
                "impact_level": "MEDIUM",
                "reason": f"Adding drop rule for malicious origin IP '{target}' at boundary firewall."
            }

        elif action_clean == "INCREASE_MONITORING":
            return {
                "action": action_clean,
                "target": target,
                "allowed": True,
                "requires_approval": False,
                "impact_level": "LOW",
                "reason": f"Increasing telemetry sampling rate for '{target}' has zero operational blast radius."
            }

        elif action_clean == "ESCALATE_INCIDENT":
            return {
                "action": action_clean,
                "target": target,
                "allowed": True,
                "requires_approval": False,
                "impact_level": "LOW",
                "reason": "Escalating incident ticket to Tier-3 incident response team."
            }

        return {
            "action": action_clean,
            "target": target,
            "allowed": True,
            "requires_approval": False,
            "impact_level": "LOW",
            "reason": "Standard automated containment action."
        }

policy_engine = PolicyEngine()
