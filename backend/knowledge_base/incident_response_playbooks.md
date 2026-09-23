# NIST SP 800-61 Incident Handling & Containment Playbook

## 1. Incident Response Lifecycle
The standard incident response lifecycle adheres to four continuous phases:
1. **Preparation**: Maintaining sensor telemetry, EDR coverage, baseline behavioral profiles, and playbooks.
2. **Detection & Analysis**: Correlating atomic alerts, computing risk scores, determining attack vector, and establishing timeline reconstruction.
3. **Containment, Eradication & Recovery**: Limiting the blast radius, isolating affected assets, revoking privileges, eliminating persistence mechanisms, and restoring clean snapshots.
4. **Post-Incident Activity**: Lessons learned, MITRE ATT&CK coverage mapping, and signature tuning.

## 2. Containment Decision Criteria & Policy Matrix
Containment actions must balance attack containment speed with business continuity impact:
- **Endpoint Network Isolation (ISOLATE_ENDPOINT)**:
  - *Impact Level*: High. Cuts off network communication except for EDR management telemetry.
  - *Policy Requirement*: Mandatory analyst sign-off for critical infrastructure (e.g. `server-02`, domain controllers, database servers). Allowed for automated simulation on standard endpoints.
- **Session Revocation (REVOKE_SESSION)**:
  - *Impact Level*: Medium. Requires re-authentication. Safe to execute immediately upon confirmed credential anomaly.
- **Firewall IP Blocking (BLOCK_SOURCE)**:
  - *Impact Level*: Medium. Drops external inbound packets from attacker infrastructure.

## 3. Evidence Preservation Rules
Always capture ephemeral memory forensics and volatile process trees prior to physical power cycling or system rebuilds.
