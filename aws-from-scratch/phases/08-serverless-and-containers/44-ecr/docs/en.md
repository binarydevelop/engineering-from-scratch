# Phase 44: ECR

## Motto
> ECR is an S3-backed OCI image registry authenticated by IAM.

**Type:** Hands-on Lab & Container Registry  
**Time Estimate:** ~60 minutes  
**Prerequisites:** Phase 43: Containers on AWS  
**AWS Services Involved:** Amazon Elastic Container Registry (ECR)  
**Cost Vector:** ECR storage costs $0.10 per GB-month. Configure Lifecycle Policies to automatically purge untagged images!  

---

## Problem
Storing proprietary corporate container images in public Docker Hub repositories exposes proprietary code and risks Docker Hub rate limits.

---

## Prediction
Amazon ECR provides a private, encrypted OCI registry integrated with IAM permissions and automated vulnerability scanning.

---

## Why this matters
ECS and EKS clusters pull images from ECR. Understanding ECR authentication tokens (`get-login-password`) prevents pull failures.

---

## First principles
An OCI container image is a manifest JSON file referencing a collection of gzipped tarballs (layers) addressed by SHA256 content hashes. ECR stores these layer blobs in S3 and uses IAM to authorize Docker `push` and `pull` operations.

---

## Mental model
```text
ECR Image Storage Mechanics:
[ Developer / CI/CD ] ──(docker push)──► [ Amazon ECR API ]
                                                │
                                                ▼ Stores Layers as Blobs
                                 [ Private S3 Storage Vault ]
                                 ├── Layer 1: Python Runtime (SHA256: e3b0...)
                                 └── Layer 2: App Code (SHA256: 7a8f...)
```

---

## Architecture before AWS
Self-hosted Docker Registry (v2) or Nexus / Artifactory servers on EC2.

---

## Build the primitive
```python
# ECR Docker Login Helper Command
login_cmd = "aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 123456789012.dkr.ecr.us-east-1.amazonaws.com"
print("ECR Login command pattern:", login_cmd)
```

---

## Use AWS
```bash
aws ecr create-repository --repository-name lab-app --image-scanning-configuration scanOnPush=true --tags Key=Project,Value=aws-from-scratch
```

---

## Inspect it
```bash
aws ecr describe-repositories --repository-names lab-app --output json
```

---

## Measure it
Measure image pull latency inside the same AWS region: ECR pulls over AWS backbone at 100+ MB/s.

---

## Break it
Attempt to docker push to ECR without logging in with `aws ecr get-login-password`.

---

## Diagnose it
Docker CLI outputs: `no basic auth credentials`.

---

## Recover it
Authenticate Docker CLI using short-lived ECR authorization tokens (valid for 12 hours).

---

## Security
Enable **Enhanced Scanning** with Amazon Inspector to automatically detect CVEs in container packages.

---

## Cost
### Cost Warning
ECR storage costs $0.10 per GB-month. Configure Lifecycle Policies to automatically purge untagged images!

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
aws ecr delete-repository --repository-name lab-app --force
```

---

## Verify cleanup
```bash
echo 'ECR repository deleted.'
```

---

## Evidence
Record your laboratory findings using the mandatory evidence log template at `outputs/evidence-template.md`. Save your completed evidence log as `outputs/phase-44-evidence.md`.

---

## Questions for mastery
1. Why does an ECR login token expire after exactly 12 hours?
2. How does ECR image layer deduplication save storage costs when pushing 50 versions of an application?
3. What is the difference between mutable image tags and immutable image tags in ECR?

---

## When to use this
Use ECR for all container images deployed to ECS, EKS, Lambda Container Images, and App Runner.

---

## When not to use this
Do not store generic non-container file archives in ECR (use Amazon S3).

---

## What comes next
Phase 45: ECS — Orchestrating container tasks across clusters.
