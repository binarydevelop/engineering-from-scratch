# Phase 72: Project: Static Web Architecture

## Motto
> S3 stores the bits; CloudFront accelerates and secures the delivery. Zero servers to patch.

**Type:** Architecture Project & Production Deployment  
**Time Estimate:** ~90 minutes  
**Prerequisites:** Phase 20: Static Website / Object Delivery  
**AWS Services Involved:** S3, CloudFront OAC, Route 53, ACM  
**Cost Vector:** CloudFront Free Tier includes 1 TB data transfer out and 10M requests permanently.  

---

## Problem
Delivering static web assets directly from an S3 website endpoint causes global latency, exposes buckets to public scraping, and lacks custom TLS certificates.

---

## Prediction
Fronting a 100% private S3 bucket with CloudFront Origin Access Control delivers sub-20ms edge latency, enforces HTTPS, and prevents direct bucket access.

---

## Why this matters
This is Project 01: the production gold standard for hosting single-page web applications.

---

## First principles
The browser resolves Anycast DNS via Route 53 to the nearest CloudFront edge PoP. CloudFront terminates TLS 1.3 locally. On cache miss, CloudFront signs an authenticated AWS SigV4 request to the private S3 bucket via Origin Access Control (OAC).

---

## Mental model
```text
Project 01 Architecture:
[ User ] ──(HTTPS)──► [ Route 53 ] ──► [ CloudFront Edge (OAC) ]
                                                │ (Cache Miss)
                                                ▼ SigV4
                                 [ Private S3 Bucket (Block Public Access: ON) ]
```

---

## Architecture before AWS
Hosting Nginx/Apache servers in multiple colocation datacenters with GeoDNS.

---

## Build the primitive
```python
# Verify project implementation documentation
with open('projects/project-01-static-web/README.md') as f:
    print("Project 01 loaded:", "CloudFront + S3" in f.read())
```

---

## Use AWS
```bash
# Reference implementation in projects/project-01-static-web/README.md
```

---

## Inspect it
```bash
curl -I https://d111111abcdef8.cloudfront.net/index.html 2>&1 | grep -i x-cache
```

---

## Measure it
Measure latency improvement: direct transatlantic S3 (180ms) vs CloudFront edge cache hit (14ms).

---

## Break it
Attempt to access the S3 bucket directly via curl.

---

## Diagnose it
S3 returns HTTP 403 Forbidden because Block Public Access is active and the bucket policy allows only CloudFront.

---

## Recover it
Access through the CloudFront distribution domain.

---

## Security
Enforce response headers: HSTS, X-Content-Type-Options: nosniff, Content-Security-Policy.

---

## Cost
### Cost Warning
CloudFront Free Tier includes 1 TB data transfer out and 10M requests permanently.

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
Follow cleanup instructions in `projects/project-01-static-web/README.md`.
```

---

## Verify cleanup
```bash
./scripts/cleanup-check.sh
```

---

## Evidence
Record your laboratory findings using the mandatory evidence log template at `outputs/evidence-template.md`. Save your completed evidence log as `outputs/phase-72-evidence.md`.

---

## Questions for mastery
1. Why is keeping the S3 bucket 100% private with OAC superior to legacy public bucket website hosting?
2. How does CloudFront Origin Shield provide an additional caching layer between edge PoPs and S3?
3. Why should `index.html` have a short TTL (300s) while hashed assets have a 1-year immutable TTL?

---

## When to use this
Use for all production static websites, React/Vue frontends, and documentation portals.

---

## When not to use this
Do not use for dynamic server-rendered HTML applications (use ECS or Lambda).

---

## What comes next
Phase 73: Project: Highly Available Web App — Multi-AZ compute and managed databases.
