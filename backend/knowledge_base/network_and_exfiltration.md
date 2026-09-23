# Network Anomalies & Data Exfiltration Defense Guide

## 1. Data Exfiltration Tactics (TA0010)
Adversaries target sensitive intellectual property, customer databases, and credential stores to exfiltrate outside the enterprise boundary:
- **Exfiltration Over C2 Channel (T1041)**: Stealing data through established command and control protocols (e.g., encoded HTTP POST requests, encrypted TLS tunnels).
- **Exfiltration Over Web Service (T1567)**: Transferring data to public cloud storage (AWS S3, Dropbox, Mega, paste sites) to blend in with legitimate business traffic.
- **Data Encrypted Before Exfiltration**: Compressing and password-protecting archives (e.g., zip, 7z, tar.gz) in staging directories prior to outbound burst.

## 2. Key Indicators of Compromise (IoCs)
- Sudden spike in outbound bytes (e.g. > 10 MB in a single connection from a workstation or internal database server).
- Outbound connections established on unusual non-standard high ports (e.g. 4444, 8888, 31337) or direct IP connections without DNS resolution.
- Unscheduled bulk queries executed against high-value SQL databases followed immediately by outbound egress traffic.

## 3. Containment Strategy
1. Restrict outbound egress on perimeter firewall for destination IP.
2. Isolate internal host to stop ongoing multi-gigabyte data transfer.
3. Review firewall NetFlow logs to measure total volume of exfiltrated data.
