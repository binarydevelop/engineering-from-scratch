#!/usr/bin/env python3
"""
scripts/generate_broken_labs.py
Generates the 32 broken-network scenario directories with decoupled README.md (symptoms)
and solution.md (root cause, layer identification, fix).
"""

import os
import sys

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BROKEN_DIR = os.path.join(REPO_ROOT, "broken-networks")

sys.path.insert(0, BROKEN_DIR)
from verify_all_broken_labs import LAB_DATABASE


def generate_labs():
    os.makedirs(BROKEN_DIR, exist_ok=True)

    for lab in LAB_DATABASE:
        folder_name = f"{lab.lab_id}-{lab.title.lower().replace(' ', '-').replace('/', '-').replace('(', '').replace(')', '').replace('---', '-')}"
        lab_path = os.path.join(BROKEN_DIR, folder_name)
        os.makedirs(lab_path, exist_ok=True)

        readme_content = f"""# {lab.lab_id.upper()}: {lab.title}

> **Motto**: Never guess when troubleshooting a network failure. Start from the symptom, hypothesize which layer is broken, collect empirical proof, and verify.

---

## 1. Observed Symptom
A developer or monitoring system reports the following alert:
```text
{lab.primary_symptom}
```

## 2. Investigation Protocol
Do **NOT** consult `solution.md` yet. Use the command line to answer these questions:
1. What layer does this error message originate from?
2. Which tool provides direct visibility into this state? (Hint: `{lab.key_tool}`)
3. Did any packet leave the sender? Did a reply arrive?
4. What does the kernel state table show?

## 3. Evidence Checklist
Record your observations in `outputs/evidence-template.md`:
- [ ] Command executed and raw output
- [ ] Layer identified: `{lab.failing_layer}`
- [ ] Packet capture or kernel state proof
- [ ] Surgical fix applied and post-fix verification
"""

        solution_content = f"""# Solution: {lab.lab_id.upper()} — {lab.title}

---

## 1. Failing Layer
**{lab.failing_layer}**

## 2. Root Cause Analysis
The failure occurs because:
> **{lab.solution_summary}**

When the client initiates communication, the expected protocol interaction fails at the {lab.failing_layer} boundary. 

## 3. Diagnostic Trace
Using `{lab.key_tool}`, we observe the definitive proof of failure:
- **Diagnostic Command**:
  ```bash
  {lab.key_tool}
  ```
- **Evidence**:
  The output directly confirms that the target endpoint or route cannot be reached or resolved due to a state mismatch.

## 4. Surgical Remediation
To permanently resolve this issue:
```bash
# Remediation:
{lab.solution_summary}
```

## 5. Production Connection
This incident pattern frequently manifests in production environments:
- **Cloud (AWS/GCP)**: Misconfigured Security Groups, missing VPC route table entries, or incorrect NAT gateways.
- **Containers (Docker/Kubernetes)**: Binding services to `127.0.0.1` inside containers, CNI routing table desynchronization, or kube-proxy iptables rules dropping packets.
- **Microservices**: DNS resolver timeouts, ephemeral port exhaustion during connection spikes, or stale client connection pools.
"""

        with open(os.path.join(lab_path, "README.md"), "w") as f:
            f.write(readme_content.strip() + "\n")

        with open(os.path.join(lab_path, "solution.md"), "w") as f:
            f.write(solution_content.strip() + "\n")

    print(f"Successfully generated all {len(LAB_DATABASE)} broken network lab directories!")


if __name__ == "__main__":
    generate_labs()
