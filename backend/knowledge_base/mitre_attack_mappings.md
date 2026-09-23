# MITRE ATT&CK Matrix Reference & Behavioral Mappings

## 1. Tactical Progression in Targeted Intrusions
Real-world intrusions typically advance across the MITRE ATT&CK kill-chain:

1. **Initial Access (TA0001)**:
   - *T1078 (Valid Accounts)*: Exploiting compromised domain credentials obtained via phishing or brute force.
2. **Execution (TA0002)**:
   - *T1059 (Command and Scripting Interpreter)*: Utilizing PowerShell, bash, or cmd to execute malicious payloads.
3. **Privilege Escalation (TA0004)**:
   - *T1548 (Abuse Elevation Control Mechanism)*: Sudo caching, setuid binaries, or UAC bypass to gain administrative / root authority.
4. **Credential Access (TA0006)**:
   - *T1110 (Brute Force)*: Password spraying and dictionary attacks.
   - *T1003 (OS Credential Dumping)*: Reading SAM database or LSASS memory.
5. **Collection (TA0009)**:
   - *T1005 (Data from Local System)*: Searching for confidential customer records, source code, or internal database dumps.
6. **Exfiltration (TA0010)**:
   - *T1041 (Exfiltration Over C2)*: Sending sensitive assets to external adversary IP addresses.

## 2. Confidence Labeling Standards
In all CyberGuard AI investigations:
- Observed atomic events (e.g. 5 failed logons followed by 1 successful logon) must be stated as **Observed Evidence**.
- Suggested MITRE mappings must be explicitly documented as **Possible Mapping** to avoid false definitive attribution without forensic memory/kernel verification.
