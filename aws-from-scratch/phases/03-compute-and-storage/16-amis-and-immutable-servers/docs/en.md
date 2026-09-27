# Phase 16: AMIs and Immutable Servers

## Motto
> Treat servers like cattle, not pets. Never patch in production: bake a new image and replace the fleet.

**Type:** Hands-on Lab & Immutable Infrastructure  
**Time Estimate:** ~60 minutes  
**Prerequisites:** Phase 15: EBS  
**AWS Services Involved:** Amazon Machine Images (AMI), EC2 Image Builder  
**Cost Vector:** AMI storage is billed at standard EBS snapshot rates (~$0.05/GB-month). Deregister AMIs and delete their associated snapshots when done!  

---

## Problem
Maintaining servers by SSHing into them and applying updates manually leads to 'snowflake servers' with undocumented configurations that crash when duplicated.

---

## Prediction
Creating an AMI from a configured instance takes a snapshot of the EBS root disk and metadata, allowing you to launch 50 identical clones in parallel.

---

## Why this matters
Immutable infrastructure is the foundation of autoscaling and continuous deployment. New code is shipped as a new AMI.

---

## First principles
An Amazon Machine Image (AMI) consists of: (1) an EBS snapshot of the root filesystem, (2) architecture metadata (x86_64 or arm64), (3) block device mappings, and (4) virtualization type (HVM). Launching an instance from an AMI clones the snapshot onto a new EBS volume via lazy loading.

---

## Mental model
```text
Golden AMI Pipeline:
[ Base OS AMI ] ──► Launch EC2 ──► Install App Dependencies ──► Create AMI Snapshot
                                                                       │
             ┌─────────────────────────────────────────────────────────┘
             ▼
[ Golden AMI (v1.2.0) ] ──► Auto Scaling Group Launches 100 Identical Cattle Instances
```

---

## Architecture before AWS
Creating golden disk images using Norton Ghost or VMware VM templates.

---

## Build the primitive
```python
# Simulating immutable version manifest
manifest = {"version": "v1.2.0", "ami_name": "app-golden-2026", "packages": ["nginx", "python3.12", "app-daemon"]}
print(f"Baking immutable server artifact: {manifest['ami_name']} ({manifest['version']})")
```

---

## Use AWS
```bash
aws ec2 create-image --instance-id $INSTANCE_ID --name 'aws-from-scratch-golden-ami' --no-reboot --tag-specifications 'ResourceType=image,Tags=[{Key=Project,Value=aws-from-scratch}]'
```

---

## Inspect it
```bash
aws ec2 describe-images --filters 'Name=tag:Project,Values=aws-from-scratch' --output json
```

---

## Measure it
Compare launch boot time: AMI pre-baked app (30 seconds) vs User Data installing from scratch (5 minutes).

---

## Break it
Attempt to launch an ARM64-compiled AMI on an x86 instance type (e.g. `t3.micro`).

---

## Diagnose it
The API call fails with architecture incompatibility: ARM64 binaries cannot execute on x86 instruction sets.

---

## Recover it
Launch on compatible architecture (`t4g.micro` for Graviton ARM64).

---

## Security
Golden AMIs allow security teams to pre-scan for vulnerabilities and CVEs before instances reach production.

---

## Cost
### Cost Warning
AMI storage is billed at standard EBS snapshot rates (~$0.05/GB-month). Deregister AMIs and delete their associated snapshots when done!

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
for id in $(aws ec2 describe-images --filters 'Name=tag:Project,Values=aws-from-scratch' --query 'Images[].ImageId' --output text); do aws ec2 deregister-image --image-id $id; done
```

---

## Verify cleanup
```bash
echo 'AMIs cleaned.'
```

---

## Evidence
Record your laboratory findings using the mandatory evidence log template at `outputs/evidence-template.md`. Save your completed evidence log as `outputs/phase-16-evidence.md`.

---

## Questions for mastery
1. Why does launching an instance from a newly created AMI sometimes exhibit high initial disk latency? (Hint: EBS Lazy Loading / Fast Snapshot Restore).
2. Why is immutable infrastructure safer than running `apt-get upgrade` in production?
3. What happens to the underlying EBS snapshot when you deregister an AMI?

---

## When to use this
Use pre-baked AMIs when auto-scaling needs to launch and register healthy instances in under 60 seconds.

---

## When not to use this
Do not bake dynamic configurations (database passwords, API keys) into AMIs; fetch secrets dynamically at boot time.

---

## What comes next
Phase 17: S3 From First Principles — Distributed object storage.
