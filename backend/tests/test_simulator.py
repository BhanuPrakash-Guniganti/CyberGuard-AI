import pytest
from backend.app.rag.retriever import rag_retriever
from backend.app.simulator.policy import policy_engine
from backend.app.simulator.simulator import response_simulator

def test_rag_retrieval():
    results = rag_retriever.search("brute force authentication password spraying", top_k=3)
    assert len(results) > 0
    assert any("authentication" in r["source"].lower() or "mitre" in r["source"].lower() for r in results)

def test_policy_engine():
    # ISOLATE_ENDPOINT on critical server should require approval
    val_crit = policy_engine.validate_action("ISOLATE_ENDPOINT", "server-02", risk_score=85)
    assert val_crit["allowed"] is True
    assert val_crit["requires_approval"] is True
    assert val_crit["impact_level"] == "CRITICAL"

    # REVOKE_SESSION on standard user
    val_session = policy_engine.validate_action("REVOKE_SESSION", "user01", risk_score=70)
    assert val_session["allowed"] is True
