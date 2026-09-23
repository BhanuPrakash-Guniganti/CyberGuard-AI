from typing import List, Dict, Any

def calculate_incident_risk_score(
    events: List[Dict[str, Any]],
    alerts: List[Dict[str, Any]],
    affected_assets: List[str],
    attack_stages_count: int
) -> Dict[str, Any]:
    """
    Calculates a normalized 0-100 composite risk score for an incident based on:
    1. Maximum & average event severity weights (0-30 pts)
    2. ML Confidence & Anomaly scores (0-25 pts)
    3. Multi-stage attack progression (0-25 pts)
    4. Asset criticality & scope of impact (0-20 pts)
    """
    if not events and not alerts:
        return {
            "score": 10,
            "level": "Low",
            "explanation": "Minimal telemetry data present."
        }

    # 1. Severity weight
    severity_weights = {"Critical": 30, "High": 22, "Medium": 14, "Low": 6, "Info": 2}
    max_sev_score = max([severity_weights.get(e.get("severity", "Low"), 6) for e in events] or [10])
    
    # 2. ML confidence & anomaly scores
    conf_sum = sum(a.get("confidence", 0.7) for a in alerts)
    avg_conf = (conf_sum / len(alerts)) if alerts else 0.65
    ml_factor = int(avg_conf * 25)

    # 3. Multi-stage progression factor (e.g. Auth -> Priv -> Exfil)
    stage_factor = min(25, attack_stages_count * 8)

    # 4. Scope / Asset Criticality
    critical_assets = ["server-02", "dc-primary", "prod-db-01", "vault-prod", "ad-controller"]
    has_critical_asset = any(a.lower() in [ca.lower() for ca in critical_assets] for a in affected_assets)
    asset_scope = min(20, len(affected_assets) * 5 + (10 if has_critical_asset else 0))

    # Total composite score
    total_score = min(100, max(5, int(max_sev_score + ml_factor + stage_factor + asset_scope)))

    # Level classification
    if total_score >= 81:
        level = "Critical"
    elif total_score >= 61:
        level = "High"
    elif total_score >= 31:
        level = "Medium"
    else:
        level = "Low"

    explanation = (
        f"Incident scored {total_score}/100 ({level}) based on {attack_stages_count} correlated attack stages, "
        f"{len(affected_assets)} affected assets, and an average ML detection confidence of {int(avg_conf * 100)}%."
    )

    return {
        "score": total_score,
        "level": level,
        "explanation": explanation,
        "breakdown": {
            "severity_component": max_sev_score,
            "ml_confidence_component": ml_factor,
            "attack_stages_component": stage_factor,
            "asset_scope_component": asset_scope
        }
    }
