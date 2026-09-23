import pytest
from backend.app.correlation.engine import correlation_engine
from backend.app.correlation.risk_scorer import calculate_incident_risk_score

def test_risk_scoring():
    events = [
        {"severity": "Critical", "bytes_transferred": 50000000},
        {"severity": "High", "bytes_transferred": 1000}
    ]
    alerts = [{"confidence": 0.95}, {"confidence": 0.88}]
    res = calculate_incident_risk_score(events, alerts, ["endpoint-03", "server-02"], 4)
    assert res["score"] >= 60
    assert res["level"] in ["High", "Critical"]

def test_mitre_mapping():
    events = [
        {"event_type": "Failed Login", "status": "Failure", "source_ip": "198.51.100.42", "username": "user01", "timestamp": "2026-09-22T10:00:00Z"},
        {"event_type": "Successful Login", "status": "Success", "source_ip": "198.51.100.42", "username": "user01", "timestamp": "2026-09-22T10:03:00Z"},
        {"event_type": "Privileged Activity", "command": "sudo cat /etc/shadow", "device": "endpoint-03", "timestamp": "2026-09-22T10:05:00Z"}
    ]
    stages = correlation_engine.map_mitre_stages(events)
    assert len(stages) >= 2
    tactics = [s["tactic"] for s in stages]
    assert any("Credential Access" in t for t in tactics)
