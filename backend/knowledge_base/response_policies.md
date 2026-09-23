# Enterprise Defensive Response Policy & Safety Guidelines

## 1. Safety Sandbox Policy
CyberGuard AI operates under strict academic and simulation safeguards:
- **Simulation Guarantee**: Under NO circumstances should real-world API hooks modify production infrastructure, firewalls, or physical endpoint network adapters directly without simulation gating.
- **Safety Banner Requirement**: Every simulated outcome must explicitly include: *"Simulation Only — Actual Infrastructure Not Modified."*

## 2. Policy Enforcement Matrix
| Action ID | Target Type | Risk Level | Requires Approval | Max Blast Radius |
| :--- | :--- | :--- | :--- | :--- |
| `REVOKE_SESSION` | User Account | Low/Medium | No (Auto-allowed) | Single User Session |
| `INCREASE_MONITORING` | Host / User / IP | Low | No (Auto-allowed) | Telemetry Stream Only |
| `BLOCK_SOURCE` | External IP | Medium | No (Auto-allowed) | Perimeter Ingress Rule |
| `ISOLATE_ENDPOINT` | Standard Endpoint (`endpoint-01..10`) | High | Yes (Analyst Sign-off) | Single Workstation |
| `ISOLATE_ENDPOINT` | Critical Server (`server-02`, `dc-primary`) | Critical | Yes (Senior Approval) | Infrastructure Service Impact |
| `ESCALATE_INCIDENT` | Incident Record | Medium | No (Auto-allowed) | Tier-3 SOC Escalation |

## 3. Human-in-the-Loop Protocol
For any high-impact action (`ISOLATE_ENDPOINT` or actions on risk scores > 75), the Policy Engine must reject unapproved execution requests and prompt the SOC analyst for cryptographic/session confirmation with reasoning notes.
