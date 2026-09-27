# Phase 15: EBS

## Motto
> EBS is a network-attached hard drive. It lives in one AZ and survives instance termination.

**Type:** Hands-on Lab & Storage Persistence  
**Time Estimate:** ~60 minutes  
**Prerequisites:** Phase 13: EC2 From First Principles  
**AWS Services Involved:** Amazon Elastic Block Store (EBS gp3)  
**Cost Vector:** gp3 costs ~$0.08 per GB-month. A 100GB volume costs $8.00/month whether the instance is running, stopped, or deleted!  

---

## Problem
Instance-store storage is ephemeral: when an instance is stopped or hardware fails, all data is permanently lost. Relational databases need persistent, snapshot-capable block storage.

---

## Prediction
Stopping an EC2 instance will detach its compute, but writing data to an EBS volume guarantees that restarting the instance preserves every single byte.

---

## Why this matters
Unattached EBS volumes are one of the biggest sources of waste in AWS bills. Deleting an EC2 instance without deleting its volume leaves storage charges running forever.

---

## First principles
Elastic Block Store (EBS) is a distributed Storage Area Network (SAN). Volumes are replicated across multiple physical storage servers within a single Availability Zone. The instance communicates with EBS over a dedicated NVMe network bus.

---

## Mental model
```text
EBS Network-Attached Storage:
Physical Compute Host (AZ-A)
┌────────────────────────────────┐
│ EC2 Instance (Guest OS)        │
│ └── /dev/nvme1n1 (Block Device)│
└───────────────┬────────────────┘
                │ Dedicated 10Gbps+ Nitro Storage Network
┌───────────────▼────────────────────────────────────────┐
│ Amazon EBS Replicated Storage Cluster (Within AZ-A)    │
│ ┌─────────────────────────┐   ┌──────────────────────┐ │
│ │ Primary Storage Server  │═══│ Sync Replica Node    │ │
│ └─────────────────────────┘   └──────────────────────┘ │
└────────────────────────────────────────────────────────┘
```

---

## Architecture before AWS
Fibre Channel SANs, iSCSI arrays, and hardware RAID controllers (RAID 10/5).

---

## Build the primitive
```python
# Simulating block device persistence
import os
with open('/tmp/ebs_test.dat', 'wb') as f:
    f.write(b"PERSISTENT_DATABASE_TRANSACTION_LOG")
print("Wrote block data to disk. Verifying persistence:")
with open('/tmp/ebs_test.dat', 'rb') as f:
    print("Read back:", f.read().decode())
```

---

## Use AWS
```bash
aws ec2 create-volume --availability-zone us-east-1a --size 10 --volume-type gp3 --tag-specifications 'ResourceType=volume,Tags=[{Key=Project,Value=aws-from-scratch}]'
```

---

## Inspect it
```bash
aws ec2 describe-volumes --filters 'Name=tag:Project,Values=aws-from-scratch' --output table
```

---

## Measure it
Measure baseline gp3 performance: 3,000 baseline IOPS and 125 MB/s throughput regardless of volume size.

---

## Break it
Attempt to attach a volume created in `us-east-1a` to an EC2 instance running in `us-east-1b`.

---

## Diagnose it
The API call fails with `InvalidVolume.ZoneMismatch`: EBS volumes are strictly confined to a single Availability Zone!

---

## Recover it
Take an EBS snapshot of the volume and restore it as a new volume in `us-east-1b`.

---

## Security
Always enable default EBS encryption using AWS KMS so all newly created volumes are encrypted at rest.

---

## Cost
### Cost Warning
gp3 costs ~$0.08 per GB-month. A 100GB volume costs $8.00/month whether the instance is running, stopped, or deleted!

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
for id in $(aws ec2 describe-volumes --filters 'Name=tag:Project,Values=aws-from-scratch' --query 'Volumes[?State==`available`].VolumeId' --output text); do aws ec2 delete-volume --volume-id $id; done
```

---

## Verify cleanup
```bash
aws ec2 describe-volumes --filters 'Name=tag:Project,Values=aws-from-scratch' --query 'Volumes[]' --output text
```

---

## Evidence
Record your laboratory findings using the mandatory evidence log template at `outputs/evidence-template.md`. Save your completed evidence log as `outputs/phase-15-evidence.md`.

---

## Questions for mastery
1. Why can an EBS volume NOT be attached to instances across different Availability Zones?
2. What is the difference between `gp2` and `gp3` EBS volumes?
3. Why is an EBS volume faster for database boot disks than an S3 bucket?

---

## When to use this
Use EBS for operating system boot volumes, relational databases, and low-latency random block I/O.

---

## When not to use this
Do not use EBS as a shared multi-instance filesystem (use Amazon EFS) or for storing petabytes of static files (use Amazon S3).

---

## What comes next
Phase 16: AMIs and Immutable Servers — Freezing configured servers into golden reproducible images.
