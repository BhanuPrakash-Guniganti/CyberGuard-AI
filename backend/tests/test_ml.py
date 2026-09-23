import pytest
from backend.app.ml.predict import ml_service

def test_ml_prediction_normal():
    normal_event = {
        "event_type": "DNS Query",
        "username": "alice",
        "source_ip": "10.0.1.20",
        "destination_ip": "10.0.1.1",
        "bytes_transferred": 200,
        "status": "Success"
    }
    res = ml_service.predict_event(normal_event)
    assert res is not None
    assert "attack_type" in res
    assert "anomaly_score" in res
    assert 0.0 <= res["confidence"] <= 1.0

def test_ml_prediction_brute_force():
    brute_event = {
        "event_type": "Failed Login",
        "username": "admin",
        "source_ip": "198.51.100.12",
        "destination_ip": "10.0.4.15",
        "status": "Failure",
        "failed_attempts_count": 25,
        "bytes_transferred": 1500
    }
    history = [brute_event] * 8
    res = ml_service.predict_event(brute_event, history=history)
    assert res is not None
    assert res["is_suspicious"] is True
    assert res["attack_type"] in ["Brute Force", "Behavioral Anomaly", "Privilege Escalation"]
