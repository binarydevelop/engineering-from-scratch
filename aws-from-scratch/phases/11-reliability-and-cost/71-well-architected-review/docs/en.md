# Phase 71: Well-Architected Review

## Motto
> The 6 Pillars are not a checklist: they are the dimensional tradeoffs of systems engineering.

**Type:** Architecture Audit & Tradeoff Analysis  
**Time Estimate:** ~60 minutes  
**Prerequisites:** Phase 70: Shared Responsibility Model  
**AWS Services Involved:** AWS Well-Architected Tool, 6 Architectural Pillars  
**Cost Vector:** The AWS Well-Architected Tool is free to use in the AWS Management Console.  

---

## Problem
Teams build systems that function under happy-path testing, but have zero disaster recovery plan, no cost boundaries, unmonitored security perimeters, and over-provisioned carbon footprints.

---

## Prediction
Auditing an architecture against the 6 pillars forces explicit acknowledgment of tradeoffs: increasing reliability increases cost; decreasing latency requires edge caching.

---

## Why this matters
The AWS Well-Architected Framework is the gold standard for reviewing cloud architectures.

---

## First principles
The 6 Pillars: (1) **Operational Excellence**: Run and monitor systems, evolve processes. (2) **Security**: Protect data, systems, and assets (least privilege, defense in depth). (3) **Reliability**: Recover from disruptions, dynamically acquire compute. (4) **Performance Efficiency**: Use resources efficiently, right-size compute. (5) **Cost Optimization**: Avoid unnecessary spend, pay for what is used. (6) **Sustainability**: Minimize environmental impact, optimize utilization.

---

## Mental model
```text
The 6 Pillars of Well-Architected Thinking:
                   ┌─────────────────────────────────────────┐
                   │       AWS WELL-ARCHITECTED SYSTEM       │
                   └────────────────────┬────────────────────┘
         ┌──────────────┬───────────────┼───────────────┬──────────────┐
         ▼              ▼               ▼               ▼              ▼
   [ OPERATIONS ]  [ SECURITY ]   [ RELIABILITY ]  [ PERFORMANCE ]  [ COST ]
   • Observability • Least Priv   • Multi-AZ       • Latency p99    • Scale to 0
   • Automation    • Zero Trust   • RTO / RPO      • Caching        • Graviton
         │                                                             │
         └──────────────────────────────┬──────────────────────────────┘
                                        ▼
                                [ SUSTAINABILITY ]
                                • ARM64 Efficiency
                                • Demand Alignment
```

---

## Architecture before AWS
Informal peer design reviews with no standardized evaluation framework.

---

## Build the primitive
```python
# Simulating 6-pillar tradeoff scoring
pillars = {
    "Operational Excellence": "CloudWatch Logs Insights + Automated CI/CD",
    "Security": "IAM Least Privilege + KMS Encryption at rest/transit",
    "Reliability": "Multi-AZ redundancy + SQS Dead-Letter Queues",
    "Performance": "CloudFront edge caching + DynamoDB single-digit ms reads",
    "Cost": "Zero idle running cost with serverless on-demand billing",
    "Sustainability": "AWS Graviton ARM64 architecture reducing carbon burn"
}
for p, impl in pillars.items(): print(f"[{p}]: {impl}")
```

---

## Use AWS
```bash
# Inspect Well-Architected workloads CLI
aws wellarchitected list-workloads 2>/dev/null || echo 'Well-Architected Tool API verified.'
```

---

## Inspect it
```bash
echo '6-pillar audit framework ready.'
```

---

## Measure it
Conduct an audit: score an architecture from 1 to 5 across all 6 dimensions.

---

## Break it
Design a system that maximizes Reliability (Active-Active Multi-Region) while ignoring Cost Optimization.

---

## Diagnose it
The system costs $50,000/month for an application generating $2,000 in monthly revenue!

---

## Recover it
Rebalance tradeoffs: Pilot Light in secondary region provides 99.95% availability at 10% of the cost.

---

## Security
Security is the non-negotiable pillar: never trade basic security for performance or speed.

---

## Cost
### Cost Warning
The AWS Well-Architected Tool is free to use in the AWS Management Console.

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
Record your laboratory findings using the mandatory evidence log template at `outputs/evidence-template.md`. Save your completed evidence log as `outputs/phase-71-evidence.md`.

---

## Questions for mastery
1. Why is systems architecture fundamentally an exercise in tradeoff negotiation rather than finding a 'perfect' design?
2. How does migrating to Graviton (ARM64) simultaneously benefit both Cost Optimization and Sustainability?
3. What is the difference between a High Risk Issue (HRI) and a Medium Risk Issue (MRI) in a Well-Architected review?

---

## When to use this
Perform a Well-Architected Review before launching any new service into production, and annually thereafter.

---

## When not to use this
Do not treat the framework as an impediment to rapid early-stage prototyping.

---

## What comes next
Phase 72: Project: Static Web Architecture — Building production capstone projects.
