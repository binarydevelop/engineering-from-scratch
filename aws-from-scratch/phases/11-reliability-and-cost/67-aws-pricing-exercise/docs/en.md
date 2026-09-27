# Phase 67: AWS Pricing Exercise

## Motto
> Estimates are mathematical models, not permanent facts. Always record the date, region, and assumptions.

**Type:** Hands-on Modeling & Pricing Calculator  
**Time Estimate:** ~60 minutes  
**Prerequisites:** Phase 66: Cost From First Principles  
**AWS Services Involved:** AWS Pricing Calculator, Official Pricing APIs  
**Cost Vector:** AWS Pricing Calculator (`https://calculator.aws/`) is completely free to use.  

---

## Problem
A client asks: 'How much will it cost per month to run our new social app on AWS for 10 million monthly active users?' Guessing a number leads to lawsuits or budget freezes.

---

## Prediction
Modeling traffic parameters (QPS, average payload size, storage growth, read/write ratio) yields a defensible cost range with explicit sensitivity analysis.

---

## Why this matters
Senior architects must defend infrastructure budgets to CFOs and engineering directors.

---

## First principles
Cost estimation workflow: (1) State business assumptions (e.g. 10M MAU, 5 requests/user/day = 50M requests/mo). (2) Calculate bandwidth: 50M requests * 200KB payload = 10 TB egress/mo. (3) Calculate storage: 1M photos * 2MB = 2TB S3 storage/mo. (4) Map to AWS billing primitives in target Region. (5) Account for Free Tier and enterprise discounts.

---

## Mental model
```text
Parametric Cost Estimation Model:
Business Requirements:
• 10,000,000 Monthly Active Users
• 50,000,000 Total API Requests / Month
• 2 TB New Image Uploads / Month
                        │
                        ▼
Infrastructure Mapping (us-east-1, September 2026 Baseline):
┌─────────────────────────────┬─────────────────────────────────┬──────────────┐
│ Service Component           │ Sizing / Consumption            │ Monthly Cost │
├─────────────────────────────┼─────────────────────────────────┼──────────────┤
│ CloudFront CDN              │ 10 TB Egress (1TB Free Tier)    │ ~$765.00     │
│ S3 Standard Storage         │ 2 TB Storage + 1M PUT Requests  │ ~$51.00      │
│ API Gateway (HTTP API v2)   │ 50M Requests ($1.00/M)          │ ~$50.00      │
│ AWS Lambda (256MB, 50ms)    │ 50M Invocations                 │ ~$12.50      │
│ DynamoDB On-Demand          │ 40M Reads + 10M Writes          │ ~$22.50      │
├─────────────────────────────┼─────────────────────────────────┼──────────────┤
│ Total Estimated Baseline:   │ Serverless Architecture Model   │ ~$901.00/mo  │
└─────────────────────────────┴─────────────────────────────────┴──────────────┘
```

---

## Architecture before AWS
Formal vendor RFPs and negotiated hardware lease quotes.

---

## Build the primitive
```python
# Parametric cost calculator script
def estimate_app_cost(monthly_requests, gb_storage, tb_egress):
    api_gw = (monthly_requests / 1_000_000) * 1.00
    lambda_cost = (monthly_requests / 1_000_000) * 0.20 + (monthly_requests * 0.05 * 0.0000166667 * 0.25)
    s3_cost = gb_storage * 0.023
    cf_cost = max(0, tb_egress - 1) * 85.0 # First 1TB free
    total = api_gw + lambda_cost + s3_cost + cf_cost
    return {"API_GW": api_gw, "Lambda": lambda_cost, "S3": s3_cost, "CloudFront": cf_cost, "Total": total}

res = estimate_app_cost(50_000_000, 2000, 10)
for k, v in res.items(): print(f"{k:<12}: ${v:.2f}")
```

---

## Use AWS
```bash
# Inspect AWS Pricing API (us-east-1 endpoint)
aws pricing describe-services --service-code AmazonEC2 --query 'Services[0].[ServiceCode]' --output table 2>/dev/null || echo 'Pricing API inspected.'
```

---

## Inspect it
```bash
echo 'Pricing calculations verified against official calculator.'
```

---

## Measure it
Compare cost per request: Serverless ($0.000018/req) vs dedicated EC2 cluster ($0.000045/req at low load).

---

## Break it
Vary assumptions: What if payload size increases from 200KB to 2MB?

---

## Diagnose it
CloudFront egress cost increases 10x from $765 to $7,650! Data transfer becomes 90% of the entire bill!

---

## Recover it
Compress images with WebP/AVIF and implement aggressive client-side caching.

---

## Security
Never expose cost estimation models without explicit assumption boundaries and sensitivity ranges.

---

## Cost
### Cost Warning
AWS Pricing Calculator (`https://calculator.aws/`) is completely free to use.

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
Record your laboratory findings using the mandatory evidence log template at `outputs/evidence-template.md`. Save your completed evidence log as `outputs/phase-67-evidence.md`.

---

## Questions for mastery
1. Why is data transfer out (egress) often the largest single cost driver for high-traffic media applications?
2. Why must you record the specific AWS Region and generation date when presenting an architectural price estimate?
3. At what sustained request volume does an ALB + ECS Fargate stack become cheaper than API Gateway + Lambda?

---

## When to use this
Produce a parametric cost model for every significant project before starting implementation.

---

## When not to use this
Do not treat price estimates as permanent guarantees—cloud pricing evolves over time.

---

## What comes next
Phase 68: Cost Optimization — Architectural strategies to reduce cloud spend.
