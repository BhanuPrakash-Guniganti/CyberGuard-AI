# CyberGuard AI: System Architecture

CyberGuard AI is a full-stack, AI-driven cybersecurity decision-support framework designed to bridge the gap between raw atomic telemetry, machine learning threat classification, agentic investigation, and safe defensive containment.

```mermaid
graph TD
    subgraph Ingestion & Telemetry
        E[Security Events Stream] --> FE[Feature Engineering Engine]
    end

    subgraph Machine Learning Layer
        FE --> RF[Random Forest Classifier]
        FE --> IF[Isolation Forest Anomaly Detector]
        RF --> AE[Alert Generation Service]
        IF --> AE
    end

    subgraph Correlation & Risk Engine
        AE --> CE[Temporal & Entity Correlation Engine]
        CE --> RS[0-100 Risk Scorer]
        RS --> DB[(Database Store)]
    end

    subgraph Agentic GenAI & RAG
        KB[Cybersecurity KB] --> RAG[RAG Vector Store]
        DB --> AG[Investigator Agent]
        RAG --> AG
        AG --> MM[MITRE ATT&CK Mapper]
        AG --> AI[GenAI Explanation Service]
    end

    subgraph Policy & Simulation Sandbox
        AI --> PE[Policy Engine & Human Approval Matrix]
        PE --> SIM[Defensive Response Simulator]
        SIM --> AUD[Audit Trail & Incident Reports]
    end

    subgraph SOC Dashboard
        DB --> UI[React + Tailwind SOC Workbench]
        AUD --> UI
    end
```

## Key Architectural Principles
1. **Real Supervised & Unsupervised ML**: No mocked values. Random Forest provides high-confidence multi-class attack categorization, and Isolation Forest scores anomalies.
2. **Grounded Agentic Investigation**: The AI investigator uses tools (`get_incident`, `get_related_events`, `get_asset_info`, `search_knowledge`) to anchor every conclusion in concrete telemetry.
3. **Safety Guarantee**: Defensive responses are strictly routed to the `simulator` module with simulated state mutations, audit logs, and prominent safety banners.
