# Project 08: Harden a Small Server

## Objective
Transform a default Linux installation into a secure, production-hardened bastion server:
1. SSH Daemon Hardening:
   - Disable root login (`PermitRootLogin no`)
   - Disable password authentication (`PasswordAuthentication no`)
   - Restrict to Ed25519 cryptographic keys
2. Firewall Configuration (UFW / nftables):
   - Default deny incoming policy
   - Permit only SSH and HTTP/HTTPS
3. Unprivileged Service Execution:
   - Verify no application daemons execute as UID 0
4. File Auditing & SUID Scans:
   - Identify and review all SUID/SGID binaries on disk
   - Restrict permissions on sensitive directories (`/tmp`, `/etc/shadow`)
