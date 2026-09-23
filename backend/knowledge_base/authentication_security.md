# Authentication Security & Credential Access Playbook

## 1. Threat Overview: Brute Force & Password Spraying (T1110)
Adversaries frequently attempt to gain unauthorized initial access by guessing passwords against authentication interfaces (e.g., SSH, RDP, Kerberos, SAML, Active Directory, Web SSO). 
- **Brute Force (T1110.001)**: Systematically submitting multiple passwords against a single targeted user account.
- **Password Spraying (T1110.003)**: Submitting a small number of commonly used passwords against a large list of domain accounts to evade account lockout thresholds.

## 2. Suspicious Indicators & Detection Logic
- Rapid burst of failed authentication events (e.g., > 5 failures in 3 minutes) originating from external or non-standard source IP addresses.
- An authentication success immediately preceded by a cascade of failed authentication attempts from the same source IP.
- Unusual logon times (e.g., between 23:00 and 05:00 local time) without historical precedent.
- Logons from geographical locations or ASN blocks discordant with the user's regular profile.

## 3. Recommended Defensive Actions
1. **Revoke Active Sessions (REVOKE_SESSION)**: Force terminate all active OAuth/JWT tokens and Kerberos tickets for the compromised account.
2. **Mandatory Password Reset**: Invalidate current credentials and enforce immediate Multi-Factor Authentication (MFA) step-up challenge.
3. **Source IP Containment (BLOCK_SOURCE)**: Enforce temporary perimeter firewall block on the malicious source IP address.
4. **Enhanced Telemetry Monitoring (INCREASE_MONITORING)**: Place user account and origin IP in a high-priority SOC watch list for 72 hours.
