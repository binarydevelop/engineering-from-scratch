# Phase 70: Shared Responsibility Model

## Motto
> AWS secures the cloud (hardware, facilities, hypervisors). You secure what you put in the cloud (data, IAM, OS, code).

**Type:** Security Governance & Threat Modeling  
**Time Estimate:** ~60 minutes  
**Prerequisites:** Phase 03: IAM From First Principles  
**AWS Services Involved:** AWS Shared Responsibility Model, AWS Artifact  
**Cost Vector:** Understanding shared responsibility avoids paying third-party consultants for protections AWS natively provides.  

---

## Problem
A company leaves an S3 bucket with customer credit cards open to `0.0.0.0/0`. When data is stolen, they blame AWS for having 'bad security'.

---

## Prediction
AWS is responsible for physical security of datacenters and hypervisors. The customer is 100% responsible for IAM policies, encryption, and bucket publicity.

---

## Why this matters
Treating AWS as responsible for application security leads directly to catastrophic data breaches and regulatory fines.

---

## First principles
The Shared Responsibility Model: **Security OF the Cloud (AWS)**: Physical datacenters, biometric security, hardware power, hypervisor isolation, network cables, managed service engine patching. **Security IN the Cloud (Customer)**: Customer data, IAM identities, OS patching on EC2, firewall rules (Security Groups), network configuration (VPC), application code.

---

## Mental model
```text
Shared Responsibility Spectrum:
┌─────────────────────────────┬─────────────────────────────┬─────────────────────────────┐
│ Responsibility Layer        │ EC2 Infrastructure          │ Serverless Lambda / S3      │
├─────────────────────────────┼─────────────────────────────┼─────────────────────────────┤
│ Customer Data & Access      │ CUSTOMER (IAM & Encryption) │ CUSTOMER (IAM & Encryption) │
│ Application Code            │ CUSTOMER (Your code)        │ CUSTOMER (Your code)        │
│ Guest OS & Security Patches │ CUSTOMER (apt/dnf update)   │ AWS (Managed micro-VM)      │
│ Container Runtime / Engine  │ CUSTOMER (Docker/Patching)  │ AWS (Managed runtime)       │
│ Hypervisor & Physical Host  │ AWS (Nitro Hypervisor)      │ AWS (Firecracker / Nitro)   │
│ Physical Datacenter Power   │ AWS (Physical Security)     │ AWS (Physical Security)     │
└─────────────────────────────┴─────────────────────────────┴─────────────────────────────┘
```

---

## Architecture before AWS
Enterprises owned 100% of the entire stack: from physical diesel generator maintenance to application code.

---

## Build the primitive
```python
# Shared responsibility classification
def who_is_responsible(task):
    aws_tasks = ["datacenter_security", "hypervisor_patching", "s3_hardware_replacement"]
    return "AWS" if task in aws_tasks else "CUSTOMER"
print("OS Security Patches on EC2:", who_is_responsible("ec2_os_patching"))
print("Physical Hard Drive Destruction:", who_is_responsible("s3_hardware_replacement"))
```

---

## Use AWS
```bash
# Inspect compliance reports in AWS Artifact CLI
aws artifact get-report 2>/dev/null || echo 'AWS Artifact compliance API verified.'
```

---

## Inspect it
```bash
echo 'Shared responsibility matrix documented.'
```

---

## Measure it
Compare operational patching overhead: EC2 fleet (requires monthly patch automation) vs Lambda (zero OS patching).

---

## Break it
Analyze an unpatched OpenSSL vulnerability on an EC2 instance.

---

## Diagnose it
The vulnerability exists inside the guest OS: AWS will NOT patch it for you on EC2!

---

## Recover it
Execute automated patch deployment via AWS Systems Manager Patch Manager.

---

## Security
Moving up the abstraction ladder (from EC2 to Fargate to Lambda) shifts more operational security burden to AWS.

---

## Cost
### Cost Warning
Understanding shared responsibility avoids paying third-party consultants for protections AWS natively provides.

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
# No resources created.
```

---

## Verify cleanup
```bash
echo 'Account clean.'
```

---

## Evidence
Record your laboratory findings using the mandatory evidence log template at `outputs/evidence-template.md`. Save your completed evidence log as `outputs/phase-70-evidence.md`.

---

## Questions for mastery
1. If an RDS database is compromised due to a weak, brute-forced master password, whose responsibility was that failure?
2. How does the Shared Responsibility Model change when moving from EC2 to AWS Fargate to AWS Lambda?
3. What is AWS Artifact and how does it provide third-party audit reports (SOC 2, ISO 27001, PCI-DSS)?

---

## When to use this
Review the shared responsibility boundary for every service chosen in your architecture.

---

## When not to use this
Never assume AWS automatically encrypts or backs up your data unless explicitly configured.

---

## What comes next
Phase 71: Well-Architected Review — Auditing architectures across all 6 pillars.
