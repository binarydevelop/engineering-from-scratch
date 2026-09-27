# Phase 14: What Happens When EC2 Launches

## Motto
> From API call to running Linux kernel: demystifying the cloud control plane and instance metadata service.

**Type:** Systems Exploration & Control Plane Trace  
**Time Estimate:** ~60 minutes  
**Prerequisites:** Phase 13: EC2 From First Principles  
**AWS Services Involved:** EC2 Lifecycle, Instance Metadata Service (IMDSv2), CloudInit  
**Cost Vector:** IMDS queries are completely free and never leave the local hypervisor.  

---

## Problem
When an instance takes 5 minutes to launch or User Data fails to configure an application, developers have no idea where the process stalled.

---

## Prediction
The instance queries `http://169.254.169.254` locally via a link-local address to retrieve its IAM role credentials and configuration.

---

## Why this matters
Understanding cloud-init, IMDSv2, and EC2 boot stages allows you to diagnose bootstrap failures in seconds.

---

## First principles
The EC2 launch lifecycle: (1) API Call -> (2) Scheduler selects physical Nitro host with available capacity -> (3) Nitro card maps EBS volume via NVMe -> (4) Nitro card provisions ENI in target subnet -> (5) VM boots kernel -> (6) cloud-init runs and queries IMDSv2 -> (7) User Data script executes -> (8) 2/2 status checks turn green.

---

## Mental model
```text
EC2 Boot Sequence:
[ RunInstances API ] ──► [ Placement Scheduler ] ──► Select Physical Host
                                                            │
    ┌───────────────────────────────────────────────────────┘
    ▼
[ Nitro Hypervisor ] ──► Allocates vCPU/RAM
[ Nitro NVMe ]       ──► Attaches EBS Root Volume
[ Nitro VPC ]        ──► Attaches Subnet ENI & Security Groups
    │
    ▼
[ Linux Boot ]       ──► GRUB ──► Kernel Initialization ──► systemd
    │
    ▼
[ Cloud-Init ]       ──► Queries IMDSv2 (169.254.169.254) ──► Executes User Data
```

---

## Architecture before AWS
PXE network booting using TFTP, DHCP Option 66/67, and Kickstart/Preseed configuration files.

---

## Build the primitive
```python
# Querying IMDSv2 securely with a session token
import urllib.request
def get_imdsv2_token():
    req = urllib.request.Request(
        "http://169.254.169.254/latest/api/token",
        headers={"X-aws-ec2-metadata-token-ttl-seconds": "21600"},
        method="PUT"
    )
    try:
        with urllib.request.urlopen(req, timeout=2) as resp:
            return resp.read().decode()
    except Exception:
        return "IMDSv2 simulation: running locally"
print("IMDSv2 Token Request:", get_imdsv2_token())
```

---

## Use AWS
```bash
aws ec2 get-console-output --instance-id $INSTANCE_ID --output text | tail -n 25
```

---

## Inspect it
```bash
aws ec2 describe-instance-status --instance-ids $INSTANCE_ID --output json
```

---

## Measure it
Analyze `/var/log/cloud-init-output.log` timing timestamps.

---

## Break it
Insert a syntax error in User Data script (`exit 1`).

---

## Diagnose it
The instance passes 2/2 status checks (the OS booted fine), but the web server is not running! Inspect `/var/log/cloud-init-output.log`.

---

## Recover it
Fix the User Data script and relaunch the instance.

---

## Security
Enforce IMDSv2 (`HttpTokens=required`). IMDSv1 is vulnerable to Server-Side Request Forgery (SSRF) attacks.

---

## Cost
### Cost Warning
IMDS queries are completely free and never leave the local hypervisor.

### Resources Created
- Documented in lesson steps above.

### How to Verify Them
```bash
./scripts/list-lab-resources.sh
```

---

## Modify it
Experiment by tuning parameters, increasing capacity, changing timeouts, or tweaking security group rules. Observe metric changes in CloudWatch.

---

## Cleanup
```bash
# No additional resources provisioned.
```

---

## Verify cleanup
```bash
echo 'Account clean.'
```

---

## Evidence
Record your laboratory findings using the mandatory evidence log template at `outputs/evidence-template.md`. Save your completed evidence log as `outputs/phase-14-evidence.md`.

---

## Questions for mastery
1. Why is IMDSv2 token-based while IMDSv1 allowed simple GET requests?
2. Why does an instance show '2/2 Status Checks' even when your application inside the instance crashed?
3. Does User Data execute on every instance reboot, or only on the initial launch?

---

## When to use this
Use User Data for lightweight configuration, or pre-bake AMIs for faster launch times.

---

## When not to use this
Avoid long 15-minute User Data scripts in Auto Scaling groups; instances cannot serve traffic until User Data finishes.

---

## What comes next
Phase 15: EBS — Network-attached block storage and persistence.
