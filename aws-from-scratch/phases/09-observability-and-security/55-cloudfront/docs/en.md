# Phase 55: CloudFront

## Motto
> Move computation and caching to the edge. Bring data closer to the user.

**Type:** Hands-on Lab & Edge Caching  
**Time Estimate:** ~60 minutes  
**Prerequisites:** Phase 20: Static Website / Object Delivery  
**AWS Services Involved:** Amazon CloudFront, Cache Behaviors, TTLs  
**Cost Vector:** First 1 TB of Data Transfer Out and 10,000,000 HTTP/HTTPS requests per month are permanently free.  

---

## Problem
Users in Singapore accessing a web application hosted in Virginia experience 240ms latency on every single image and API request due to speed-of-light travel across the Pacific Ocean.

---

## Prediction
Deploying a CloudFront CDN distribution caches static assets at local edge Points of Presence (PoPs), dropping round-trip latency to under 20ms.

---

## Why this matters
CloudFront accelerates both static assets and dynamic APIs by terminating TLS at the edge and proxying traffic over AWS's private optical network.

---

## First principles
Anycast BGP routing directs user DNS queries to the geographically closest CloudFront edge location (out of 450+ PoPs worldwide). The edge terminates the TLS handshake locally, avoiding multi-hop cross-ocean handshakes. If cached, it returns the file; if a cache miss occurs, it routes across AWS private fiber to the origin.

---

## Mental model
```text
CloudFront Edge Acceleration:
[ User in Tokyo ] ──(20ms Local Fiber)──► [ CloudFront Tokyo Edge PoP ]
                                                   │
                                                   ├── (Cache Hit) ──► Return in 20ms!
                                                   │
                                                   ▼ (Cache Miss)
                                       [ AWS Private Backbone Fiber ]
                                       (Accelerated TCP / BBR Congestion Control)
                                                   │
                                                   ▼
                                       [ Origin Server in Virginia ]
```

---

## Architecture before AWS
Akamai CDN contracts or maintaining edge reverse-proxy servers in multiple global colocation centers.

---

## Build the primitive
```python
# Simulating Cache-Control header evaluation
def get_ttl(cache_control_header):
    for directive in cache_control_header.split(','):
        directive = directive.strip()
        if directive.startswith('max-age='):
            return int(directive.split('=')[1])
    return 86400 # Default 24h
print("TTL for asset:", get_ttl("public, max-age=31536000, immutable"), "seconds")
```

---

## Use AWS
```bash
# Inspect CloudFront distributions
aws cloudfront list-distributions --output table
```

---

## Inspect it
```bash
curl -I https://d111111abcdef8.cloudfront.net/logo.png 2>&1 | grep -iE '(x-cache|age|content-type)'
```

---

## Measure it
Measure latency: Cache Miss (`X-Cache: Miss from cloudfront`) = 180ms vs Cache Hit (`X-Cache: Hit from cloudfront`) = 14ms.

---

## Break it
Deploy an updated `index.html` file to S3, but forget to invalidate the CloudFront cache.

---

## Diagnose it
Users continue seeing the old website version because CloudFront's edge cache still holds the old object until TTL expires.

---

## Recover it
Issue an invalidation: `aws cloudfront create-invalidation --distribution-id $DIST_ID --paths '/index.html'`.

---

## Security
Attach AWS WAF directly to CloudFront to block DDoS and malicious traffic at the edge before it hits your origin.

---

## Cost
### Cost Warning
First 1 TB of Data Transfer Out and 10,000,000 HTTP/HTTPS requests per month are permanently free.

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
# Disable and delete test distributions
```

---

## Verify cleanup
```bash
echo 'CloudFront clean.'
```

---

## Evidence
Record your laboratory findings using the mandatory evidence log template at `outputs/evidence-template.md`. Save your completed evidence log as `outputs/phase-55-evidence.md`.

---

## Questions for mastery
1. Why does CloudFront accelerate dynamic non-cacheable API requests (e.g. POST requests)?
2. What is the difference between CloudFront Invalidation and Cache-Control Cache Busting (hashed filenames)?
3. How do CloudFront Functions differ from Lambda@Edge in terms of execution location and performance?

---

## When to use this
Use CloudFront for global web asset delivery, video streaming, API acceleration, and edge security.

---

## When not to use this
Do not use CloudFront for purely internal private intranet applications that have no external internet users.

---

## What comes next
Phase 56: WAF and Edge Security — Application layer firewalling.
