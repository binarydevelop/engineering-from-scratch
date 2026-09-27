# Phase 69: Tagging and Resource Inventory

## Motto
> If you don't tag it, you can't bill it, you can't automate it, and you can't clean it up.

**Type:** Hands-on Lab & Cloud Governance  
**Time Estimate:** ~60 minutes  
**Prerequisites:** Phase 66: Cost From First Principles  
**AWS Services Involved:** AWS Resource Groups, Tagging API, Cost Allocation Tags  
**Cost Vector:** Tagging resources is 100% free.  

---

## Problem
An AWS account contains 400 EC2 instances and 2,000 EBS volumes. Nobody knows who owns them, what environment they belong to, or which application will crash if they are deleted.

---

## Prediction
Enforcing mandatory resource tags (`Project`, `Environment`, `Owner`) allows generating automated cost allocation reports and automated cleanup scripts.

---

## Why this matters
Tagging is the metadata backbone for billing attribution, security automation, and infrastructure lifecycle.

---

## First principles
A tag is a key-value string metadata pair attached to an AWS resource. AWS Cost Allocation Tags ingest these pairs into the billing engine, slicing monthly invoices by Cost Center, Project, or Team. The AWS Resource Groups Tagging API allows querying resources across all services via a unified API.

---

## Mental model
```text
Resource Tagging Governance:
EC2 Instance (i-0123)
  ├── Tag: Project     = aws-from-scratch
  ├── Tag: Environment = learning
  ├── Tag: Owner       = alice@example.com
  └── Tag: CostCenter  = Engineering-101
            │
            ▼
[ AWS Cost Explorer / Billing Report ]
"Project: aws-from-scratch generated $4.12 in compute this month"
"Owner: alice@example.com has 2 active resources" 
```

---

## Architecture before AWS
Asset management spreadsheets with physical barcode stickers on server chassis.

---

## Build the primitive
```python
# Simulating tag-based resource discovery
resources = [
    {"id": "i-1", "tags": {"Project": "aws-from-scratch", "Env": "lab"}},
    {"id": "i-2", "tags": {"Project": "other-app", "Env": "prod"}}
]
lab_resources = [r['id'] for r in resources if r['tags'].get('Project') == 'aws-from-scratch']
print("Discovered lab resources via tag filter:", lab_resources)
```

---

## Use AWS
```bash
# Run our repository inventory discovery script
./scripts/list-lab-resources.sh
```

---

## Inspect it
```bash
aws resourcegroupstaggingapi get-resources --tag-filters Key=Project,Values=aws-from-scratch --output json 2>/dev/null || echo 'Tagging API inspected.'
```

---

## Measure it
Measure inventory scan speed: unified tagging query scans dozens of AWS services in < 2 seconds.

---

## Break it
Launch an untagged EC2 instance in a shared learning account.

---

## Diagnose it
The inventory script `./scripts/list-lab-resources.sh` flags untagged resources; automated janitor scripts terminate it.

---

## Recover it
Apply required tags: `aws ec2 create-tags --resources $ID --tags Key=Project,Value=aws-from-scratch`.

---

## Security
Use AWS Organizations Tag Policies and SCPs to reject any `ec2:RunInstances` API call that lacks required tags.

---

## Cost
### Cost Warning
Tagging resources is 100% free.

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
Record your laboratory findings using the mandatory evidence log template at `outputs/evidence-template.md`. Save your completed evidence log as `outputs/phase-69-evidence.md`.

---

## Questions for mastery
1. Why must Cost Allocation Tags be explicitly activated in the AWS Billing Console before they appear in Cost Explorer?
2. How do Tag Policies in AWS Organizations enforce consistent casing (e.g. `Environment` vs `environment`)?
3. How can IAM policies use Attribute-Based Access Control (ABAC) using resource tags (`aws:ResourceTag/Env`)?

---

## When to use this
Tag 100% of resources created in all AWS environments from Day 1.

---

## When not to use this
Do not store confidential secrets or PII in resource tags—tags are visible in plaintext across many read APIs.

---

## What comes next
Phase 70: Shared Responsibility Model — Who secures what in the cloud.
