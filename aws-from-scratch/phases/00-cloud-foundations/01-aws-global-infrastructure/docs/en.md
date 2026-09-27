# Phase 01: AWS Global Infrastructure

## Motto
> Region != Availability Zone. Latency is the speed of light in optical fiber.

**Type:** Systems Experiment & Measurement  
**Time Estimate:** ~45 minutes  
**Prerequisites:** Phase 00: Cloud Before AWS  
**AWS Services Involved:** AWS Global Regions, Availability Zones, Edge Locations  
**Cost Vector:** Cross-AZ data transfer: ~$0.01/GB in each direction. Cross-region data transfer: ~$0.02/GB. Inter-AZ communication within the same AZ is $0.00.  

---

## Problem
Deploying an entire application into a single physical building means a municipal power grid failure, flood, or fiber cut causes 100% downtime. Furthermore, users on the other side of the planet experience 200ms+ round-trip latency.

---

## Prediction
Querying an AWS endpoint across the continent will exhibit a minimum baseline latency bounded by the speed of light (~5ms per 1,000 km of glass fiber).

---

## Why this matters
Conflating an AWS Region with an Availability Zone leads to single-point-of-failure architectures that fail completely when one datacenter suffers an outage.

---

## First principles
Light travels through glass fiber optic cables at ~200,000 km/s (~5 microseconds per kilometer). An Availability Zone is one or more discrete physical datacenters separated by 10-50 km to ensure independent flood/earthquake blast radiuses while keeping round-trip latency under 1-2 milliseconds.

---

## Mental model
```text
AWS Global Topology:
AWS Global Backbone
├── Region A (e.g., us-east-1: N. Virginia)
│   ├── AZ 1 (us-east-1a) ──(Sub-2ms Dark Fiber)──► AZ 2 (us-east-1b)
│   │   └── Physical DC Campus 1                    └── Physical DC Campus 2
│   └── AZ 3 (us-east-1c)
└── Region B (e.g., eu-central-1: Frankfurt)
    └── Bounded by Transatlantic Undersea Cables (~70ms latency)
```

---

## Architecture before AWS
Global enterprises leased synchronous MPLS circuits between private datacenters in New York, London, and Tokyo, paying tens of thousands of dollars monthly.

---

## Build the primitive
```python
import time, urllib.request
def measure(url):
    t0 = time.perf_counter()
    urllib.request.urlopen(url, timeout=5)
    return (time.perf_counter() - t0) * 1000
print(f"Latency to us-east-1: {measure('https://ec2.us-east-1.amazonaws.com'):.1f}ms")
print(f"Latency to eu-central-1: {measure('https://ec2.eu-central-1.amazonaws.com'):.1f}ms")
```

---

## Use AWS
```bash
aws ec2 describe-availability-zones --query 'AvailabilityZones[].[ZoneName,ZoneId,State]' --output table
```

---

## Inspect it
```bash
aws ec2 describe-regions --query 'Regions[].RegionName' --output text
```

---

## Measure it
Compare same-AZ ping (< 1ms), cross-AZ ping (1-2ms), and cross-region ping (70-150ms).

---

## Break it
Attempt to synchronously replicate database transactions across transatlantic regions.

---

## Diagnose it
Observe database write commit latency balloon from 2ms to 120ms due to speed-of-light round trips.

---

## Recover it
Use asynchronous replication across regions and synchronous replication only within Multi-AZ boundaries.

---

## Security
Data sovereignty and legal compliance (GDPR, HIPAA, CCPA) strictly mandate which geographic region data may physically reside in.

---

## Cost
### Cost Warning
Cross-AZ data transfer: ~$0.01/GB in each direction. Cross-region data transfer: ~$0.02/GB. Inter-AZ communication within the same AZ is $0.00.

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
# No infrastructure provisioned. Zero cleanup needed.
```

---

## Verify cleanup
```bash
echo 'Account clean.'
```

---

## Evidence
Record your laboratory findings using the mandatory evidence log template at `outputs/evidence-template.md`. Save your completed evidence log as `outputs/phase-01-evidence.md`.

---

## Questions for mastery
1. Why does AWS map the logical AZ name 'us-east-1a' to different physical Zone IDs across different AWS accounts?
2. Why can an application synchronously commit transactions across AZs in the same region, but must use asynchronous replication across regions?
3. Under what circumstances does deploying across two AZs actually REDUCE overall availability?

---

## When to use this
Use Multi-AZ for high availability within a region. Use Multi-Region only for disaster recovery or extreme global data residency requirements.

---

## When not to use this
Do not build multi-region active-active architectures prematurely—cross-region consensus is one of the hardest distributed systems problems.

---

## What comes next
Phase 02: AWS CLI, APIs, and Console — Stripping away the UI magic to see signed REST API requests.
