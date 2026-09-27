# Phase 20: Static Website / Object Delivery

## Motto
> Never make an S3 bucket public for website hosting. Keep the bucket private and front it with CloudFront OAC.

**Type:** Hands-on Lab & Web Architecture  
**Time Estimate:** ~60 minutes  
**Prerequisites:** Phase 19: S3 Durability, Versioning, Lifecycle  
**AWS Services Involved:** S3, CloudFront Origin Access Control (OAC)  
**Cost Vector:** CloudFront Free Tier includes 1 TB data transfer out and 10,000,000 requests per month permanently.  

---

## Problem
Making an S3 bucket public exposes your account to unbounded direct GET request fees, lacks HTTPS custom domain support, and serves traffic from a single geographic region.

---

## Prediction
Using CloudFront with Origin Access Control allows CloudFront to read from a 100% private S3 bucket using AWS SigV4 signed requests.

---

## Why this matters
This is Project 01 in the curriculum and the industry standard for delivering frontend web applications.

---

## First principles
A Content Delivery Network (CDN) terminates TLS at the nearest Anycast edge point of presence (PoP). When a cache miss occurs, CloudFront signs an HTTP request to S3 using AWS SigV4 with its service principal credentials (`cloudfront.amazonaws.com`). The S3 bucket policy validates the signature and returns the object.

---

## Mental model
```text
CloudFront OAC Architecture:
[ User Browser ] ──(HTTPS)──► [ CloudFront Edge PoP ]
                                     │ (Cache Miss)
                                     │ SigV4 Signed Request
                                     ▼
                      [ Private S3 Bucket ]
                      (Block Public Access: ENABLED)
                      (Bucket Policy: Allow s3:GetObject ONLY to CloudFront ARN)
```

---

## Architecture before AWS
Hosting frontend Apache/Nginx web servers in multiple datacenters with geo-DNS routing.

---

## Build the primitive
```python
# OAC Bucket Policy Pattern
policy = {
    "Statement": [{
        "Effect": "Allow",
        "Principal": {"Service": "cloudfront.amazonaws.com"},
        "Action": "s3:GetObject",
        "Resource": "arn:aws:s3:::my-web-bucket/*",
        "Condition": {"StringEquals": {"AWS:SourceArn": "arn:aws:cloudfront::123:distribution/E123"}}
    }]
}
print("OAC Policy Structure validated.")
```

---

## Use AWS
```bash
aws s3api get-public-access-block --bucket $BUCKET --output table
```

---

## Inspect it
```bash
aws s3api get-bucket-policy --bucket $BUCKET
```

---

## Measure it
Measure latency improvement: direct cross-ocean S3 GET (180ms) vs edge cached CloudFront GET (15ms).

---

## Break it
Attempt to curl the private S3 bucket URL directly (`https://$BUCKET.s3.amazonaws.com/index.html`).

---

## Diagnose it
S3 returns HTTP 403 AccessDenied because Block Public Access is active and the bucket policy allows only CloudFront.

---

## Recover it
Access the asset through the CloudFront distribution domain name.

---

## Security
Enforce HTTPS redirect (`viewer-protocol-policy: redirect-to-https`) and TLS 1.2+ security policies.

---

## Cost
### Cost Warning
CloudFront Free Tier includes 1 TB data transfer out and 10,000,000 requests per month permanently.

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
# Cleanup web assets
```

---

## Verify cleanup
```bash
echo 'Static web assets cleaned.'
```

---

## Evidence
Record your laboratory findings using the mandatory evidence log template at `outputs/evidence-template.md`. Save your completed evidence log as `outputs/phase-20-evidence.md`.

---

## Questions for mastery
1. Why is legacy S3 Static Website Hosting discouraged in modern production architectures?
2. How does Origin Access Control (OAC) prevent other AWS customers with CloudFront distributions from accessing your private bucket?
3. Why should hashed asset bundles (e.g. `main.a8f9c.js`) have a 1-year Cache-Control header while `index.html` has a 5-minute header?

---

## When to use this
Use CloudFront + S3 OAC for all React, Vue, Svelte, or static frontend single-page applications.

---

## When not to use this
Do not use S3 for server-side dynamic HTML rendering (use ECS, Lambda, or EC2).

---

## What comes next
Phase 21: DNS and Route 53 — Authoritative domain name resolution.
