import numpy as np
import pandas as pd
from typing import Dict, Any, List
from datetime import datetime

# Feature definitions for ML model training and inference
FEATURE_COLUMNS = [
    "failed_login_count",
    "unique_source_ips",
    "request_count",
    "connection_count",
    "bytes_transferred",
    "destination_count",
    "login_success_after_failures",
    "event_frequency_per_min",
    "unusual_time_indicator",
    "privileged_command_flag",
    "high_risk_port_flag",
    "internal_to_external_flag"
]

def extract_features_from_event(event: Dict[str, Any], history: List[Dict[str, Any]] = None) -> np.ndarray:
    """
    Extracts numerical feature vector from a single event in the context of recent entity history.
    """
    history = history or []
    
    # 1. Failed logins for this user / IP in history
    user = event.get("username", "")
    src_ip = event.get("source_ip", "")
    
    recent_user_events = [e for e in history if e.get("username") == user or e.get("source_ip") == src_ip]
    failed_login_count = sum(
        1 for e in recent_user_events 
        if e.get("event_type") in ["Failed Login", "Authentication Failure"] or e.get("status") == "Failure"
    )
    if event.get("event_type") in ["Failed Login", "Authentication Failure"] or event.get("status") == "Failure":
        failed_login_count += 1
    
    # 2. Unique source IPs accessing this user/device
    all_ips = {e.get("source_ip") for e in recent_user_events if e.get("source_ip")}
    if src_ip:
        all_ips.add(src_ip)
    unique_source_ips = max(1, len(all_ips))
    
    # 3. Request count
    request_count = len(recent_user_events) + 1
    
    # 4. Connection count
    connection_count = max(1, request_count)
    
    # 5. Bytes transferred
    bytes_transferred = float(event.get("bytes_transferred", 0) or 0)
    
    # 6. Destination count
    dest_ips = {e.get("destination_ip") for e in recent_user_events if e.get("destination_ip")}
    if event.get("destination_ip"):
        dest_ips.add(event.get("destination_ip"))
    destination_count = max(1, len(dest_ips))
    
    # 7. Login success after failure flag
    login_success_after_failures = 0
    if event.get("event_type") in ["Successful Login", "User Logon"] and failed_login_count > 0:
        login_success_after_failures = 1
        
    # 8. Event frequency per min
    event_frequency_per_min = float(min(120, len(recent_user_events) * 2 + 1))
    
    # 9. Unusual time indicator (Off hours: 22:00 to 06:00)
    unusual_time_indicator = 0
    ts_str = event.get("timestamp", "")
    try:
        if "T" in ts_str:
            dt = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
            if dt.hour < 6 or dt.hour >= 22:
                unusual_time_indicator = 1
        elif ":" in ts_str:
            hour = int(ts_str.split(":")[0][-2:].strip())
            if hour < 6 or hour >= 22:
                unusual_time_indicator = 1
    except Exception:
        unusual_time_indicator = 0
        
    # 10. Privileged command flag
    privileged_command_flag = 0
    cmd = str(event.get("command", "")).lower()
    proc = str(event.get("process_name", "")).lower()
    evt_type = str(event.get("event_type", "")).lower()
    if any(k in cmd or k in proc or k in evt_type for k in ["sudo", "admin", "privilege", "shadow", "powershell -enc", "whoami /priv", "chmod 777", "net group", "reg add"]):
        privileged_command_flag = 1
        
    # 11. High risk port flag (e.g., 4444, 1337, 3389, 445, 8888, 22)
    port = int(event.get("port", 0) or 0)
    high_risk_port_flag = 1 if port in [4444, 1337, 3389, 445, 8888, 6667, 31337] else 0
    
    # 12. Internal to external data transfer flag
    dest_ip = event.get("destination_ip", "")
    internal_to_external_flag = 0
    if dest_ip and not (dest_ip.startswith("10.") or dest_ip.startswith("192.168.") or dest_ip.startswith("172.16.")):
        if bytes_transferred > 500000 or "exfiltrat" in evt_type or "outbound" in evt_type:
            internal_to_external_flag = 1
            
    features = [
        failed_login_count,
        unique_source_ips,
        request_count,
        connection_count,
        bytes_transferred,
        destination_count,
        login_success_after_failures,
        event_frequency_per_min,
        unusual_time_indicator,
        privileged_command_flag,
        high_risk_port_flag,
        internal_to_external_flag
    ]
    return np.array(features, dtype=np.float32).reshape(1, -1)
