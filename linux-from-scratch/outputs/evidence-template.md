# Laboratory Evidence Log

## Session Details
- **Lesson**: Phase XX — [Lesson Title]
- **Date**: YYYY-MM-DD
- **Operator**: [Your Name / Handle]
- **Distribution**: [e.g. Ubuntu 24.04 LTS / Debian 12]
- **Kernel Version**: [Output of uname -r]
- **Shell**: [Output of echo "$BASH_VERSION"]

---

## 1. Initial State & Problem
- **Problem Statement**:
- **Initial Hypothesis / Prediction**:
- **Pre-execution System Metrics**:
  - Memory: `free -h`
  - Load: `uptime`
  - Relevant process or socket state:

---

## 2. Command Execution & State Transitions
- **Commands Executed**:
```bash
# Insert executed commands here
```
- **Significant Command Output**:
```text
# Insert raw terminal output here
```

---

## 3. Objects & Abstractions Involved
- **Processes Involved** (PIDs, PPIDs, command line):
- **Files & Inodes Involved** (Path, Inode number, permissions):
- **Users & Groups Involved** (UID, GID, username):
- **Sockets & Ports Involved** (Proto, Local Address, State, Inode):
- **Virtual Filesystem Interfaces Checked** (`/proc/<pid>/...`, `/sys/...`):

---

## 4. Failure Injection & Diagnostic Proof
- **What Was Intentionally Broken?**:
- **What Command/Tool Provided the Decisive Diagnostic Evidence?**:
```bash
# Diagnostic command (e.g. strace, ss, lsof, journalctl)
```
- **Root Cause Identified**:

---

## 5. Remediation & Verification
- **Remediation Commands Applied**:
- **Verification Proof (Post-Fix System State)**:
```text
# Verification output proving health
```

---

## 6. Automation Artifact
- **Automated Check or Remediation Script**:
```bash
#!/usr/bin/env bash
set -euo pipefail
# Script content
```

---

## 7. Production Reflection
- **How would this incident appear in a production monitoring system?**:
- **What alert should fire if this occurs in production?**:
- **Remaining Questions or Edge Cases**:
