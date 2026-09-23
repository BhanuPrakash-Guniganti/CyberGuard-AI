# CyberGuard AI: Generative AI Framework for Cyber Threat Detection, Incident Investigation & Response Simulation

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688.svg?style=flat&logo=fastapi)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/Frontend-React%20%2B%20Vite-61DAFB.svg?style=flat&logo=react)](https://react.dev)
[![TailwindCSS](https://img.shields.io/badge/Styling-Tailwind%20CSS-38B2AC.svg?style=flat&logo=tailwind-css)](https://tailwindcss.com)
[![Machine Learning](https://img.shields.io/badge/ML-Random%20Forest%20%2B%20IsoForest-F7931E.svg?style=flat&logo=scikit-learn)](https://scikit-learn.org)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB.svg?style=flat&logo=python)](https://python.org)

**CyberGuard AI** is a comprehensive, production-grade cybersecurity decision-support framework combining Machine Learning threat classification, temporal & entity incident correlation, RAG-grounded Generative AI investigation, MITRE ATT&CK kill-chain mapping, safe defensive response simulation, and a dark SOC analyst dashboard.

---

## 🌟 Key Features

1. **Dual Machine Learning Engine**:
   - Supervised **Random Forest Classifier** trained on realistic multi-class cybersecurity telemetry (*Brute Force, Privilege Escalation, Data Exfiltration, Lateral Movement, Normal*).
   - Unsupervised **Isolation Forest** scoring real-time behavioral anomalies (0.05–0.99 normalized score).
2. **Incident Correlation & Composite Risk Scorer**:
   - Clusters related telemetry across sliding time-windows, usernames, source IPs, and devices into high-confidence Incident records.
   - Computes 0–100 risk score incorporating event severity weights, ML confidence, multi-stage attack depth, and asset criticality.
3. **RAG Knowledge Base & Semantic Search**:
   - Embedded cybersecurity playbooks, NIST SP 800-61 incident response guidelines, and MITRE ATT&CK reference matrices.
   - Vector indexing with cosine similarity matching and source citations.
4. **Agentic AI Investigator**:
   - Multi-step investigation workflow invoking tools: `get_incident()`, `get_related_events()`, `get_asset_info()`, `search_knowledge()`, and `ai_synthesis_engine()`.
   - Distinguishes *Observed Evidence* from *Inferences* and highlights *Uncertainties*.
   - Interactive Q&A chat assistant for SOC analysts.
5. **Defensive Response Simulator & Policy Sandbox**:
   - Rule-based policy matrix verifying response impact levels.
   - Mandatory analyst sign-off for critical server isolation.
   - Safe simulated state mutations with the safety guarantee:
     > **"Simulation Only — Actual Infrastructure Not Modified."**
6. **Executive Incident Reporting & Audit Trail**:
   - Full printable/exportable incident report with timeline, attack chains, and policy decisions.
   - Timestamped compliance audit trail logging all analyst actions.
7. **SOC-Grade Dark Theme Workbench**:
   - Built with React, Vite, Tailwind CSS, Recharts, and Lucide React.
   - Information-dense, interactive charts, timeline visualizers, and MITRE kill-chain graphs.

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- Python 3.10+
- Node.js 18+ and npm

### 2. Backend Setup
```bash
# Navigate to project root
cd CYBER-GUARD-AI

# Install Python dependencies
pip install -r backend/requirements.txt

# Train ML Models & Ingest RAG Knowledge Base
python -m backend.app.ml.train
python -m backend.app.rag.ingestion

# Seed Realistic Scenarios & Incident CG-1021
python -m backend.scripts.seed_demo_data

# Start FastAPI Backend Server
python -m backend.app.main
```
Backend API will be live at `http://localhost:8000` (Swagger docs at `http://localhost:8000/docs`).

### 3. Frontend Setup
```bash
# In a new terminal, navigate to frontend directory
cd frontend

# Install dependencies (if not already installed)
npm install

# Start Vite Development Server
npm run dev
```
Frontend SOC Dashboard will be accessible at `http://localhost:5173`.

---

## 🔐 Default Demo Credentials
- **Email**: `analyst@cyberguard.ai`
- **Password**: `CyberGuard2026!`

---

## 🧪 Testing
Run the automated test suite covering ML inference, correlation, RAG retrieval, and policy sandboxes:
```bash
pytest
```

---

## 📂 Project Architecture

```text
CYBER-GUARD-AI/
├── backend/
│   ├── app/
│   │   ├── api/            # FastAPI REST endpoints (auth, dashboard, events, alerts, incidents, rag, etc.)
│   │   ├── core/           # Database manager, configuration, JWT security
│   │   ├── ml/             # Feature engineering, training pipeline, prediction service
│   │   ├── correlation/    # Incident clustering engine & 0-100 risk scorer
│   │   ├── rag/            # Document chunking, vector embeddings, retriever
│   │   ├── agents/         # Agentic investigator workflow & tool callers
│   │   ├── simulator/      # Policy engine & defensive response sandbox
│   │   ├── services/       # AI service abstraction & report compiler
│   │   ├── schemas/        # Pydantic validation models
│   │   └── main.py         # FastAPI application entrypoint
│   ├── datasets/           # Generated training datasets
│   ├── knowledge_base/     # Authoritative markdown cybersecurity playbooks
│   ├── scripts/            # Database seed script for 4 demo scenarios
│   ├── tests/              # Pytest unit & integration test suite
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/     # Severity badges, banner, navbar, sidebar
│   │   ├── pages/          # Login, Dashboard, Events, Alerts, Incidents, Incident Details, Simulator, Audit, Reports
│   │   ├── context/        # Authentication context
│   │   ├── services/       # Centralized Axios API client
│   │   └── App.jsx
│   ├── package.json
│   └── tailwind.config.js
├── docs/                   # Architecture, API, and demo walkthrough guides
├── docker-compose.yml
├── pytest.ini
└── README.md
```

---

## 🛡️ Safety & Academic Compliance Disclaimer
CyberGuard AI is an academic prototype designed for cybersecurity decision support. Under no circumstances does this platform execute real-world destructive payloads, unauthorized network scans, or live infrastructure modifications. All defensive actions operate strictly within a localized simulation sandbox.
