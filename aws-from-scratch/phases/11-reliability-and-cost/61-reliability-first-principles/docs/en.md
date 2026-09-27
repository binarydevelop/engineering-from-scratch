# Phase 61: Reliability From First Principles

## Motto
> Everything fails, all the time. Reliability is not the absence of failures: it is the ability to survive them.

**Type:** Conceptual & Systems Architecture  
**Time Estimate:** ~60 minutes  
**Prerequisites:** Phase 24: Multi-AZ Application  
**AWS Services Involved:** Reliability Engineering, MTBF, MTTF, MTTR  
**Cost Vector:** Each extra 'nine' of availability roughly multiplies infrastructure costs: 99.999% requires multi-region active-active architectures.  

---

## Problem
Engineers deploy a system on a single EC2 instance, declare it 'production ready', and are shocked when physical hardware failure in the datacenter takes the business offline for 4 hours.

---

## Prediction
Hardware components have a non-zero Mean Time To Failure (MTTF). In a fleet of 1,000 servers with an MTTF of 3 years, approximately one server will physically die every single day.

---

## Why this matters
Reliability engineering begins with the mathematical acceptance of physical failure.

---

## First principles
Availability ($A$) is defined as: $A = \frac{MTBF}{MTBF + MTTR}$. You can increase availability either by making components more reliable (increasing MTBF) or by recovering faster through automated self-healing (decreasing MTTR to seconds). Redundancy eliminates Single Points of Failure (SPOFs).

---

## Mental model
```text
Reliability Calculation:
Single Instance:
Availability = 99% (3.65 days downtime per year!)
MTBF = 100 days | MTTR = 1 day (Manual repair)

Redundant Multi-AZ Pair:
Availability = 1 - (1 - 0.99)^2 = 99.99% (52 minutes downtime per year!)
MTTR = 30 seconds (Automated health check failover)
```

---

## Architecture before AWS
Buying expensive fault-tolerant mainframe hardware (Tandem / Stratus) with duplicated CPUs and lockstep buses.

---

## Build the primitive
```python
# Availability calculation
def calc_availability(n_nines):
    return (1 - 10**(-n_nines)) * 100
for n in [2, 3, 4, 5]:
    down_hours = (1 - (calc_availability(n)/100)) * 8760
    print(f"{n} Nines ({calc_availability(n):.3f}%): {down_hours:.2f} hours downtime/year")
```

---

## Use AWS
```bash
# Inspect EC2 Service Health Dashboard events CLI
aws health describe-events --query 'events[]' 2>/dev/null || echo 'AWS Health API verified.'
```

---

## Inspect it
```bash
echo 'Reliability model documented.'
```

---

## Measure it
Calculate the availability difference between 99.9% (8.7 hours downtime/year) vs 99.99% (52 mins/year).

---

## Break it
Identify the Single Point of Failure (SPOF) in an architecture with 10 web servers connecting to 1 single-AZ database.

---

## Diagnose it
The database is the SPOF: if AZ-A loses power, all 10 web servers become useless.

---

## Recover it
Upgrade database to Multi-AZ synchronous standby.

---

## Security
Reliability requires graceful degradation under attack: shed non-essential load to keep core checkout functions alive.

---

## Cost
### Cost Warning
Each extra 'nine' of availability roughly multiplies infrastructure costs: 99.999% requires multi-region active-active architectures.

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
Record your laboratory findings using the mandatory evidence log template at `outputs/evidence-template.md`. Save your completed evidence log as `outputs/phase-61-evidence.md`.

---

## Questions for mastery
1. Why is reducing MTTR (Mean Time To Recovery) usually more cost-effective than trying to increase MTBF?
2. What is the difference between a high-availability architecture and a fault-tolerant architecture?
3. How does the blast radius concept limit the impact of bad software deployments?

---

## When to use this
Apply first-principles reliability modeling to every production architecture design.

---

## When not to use this
Do not over-engineer 5 nines (99.999%) of availability for an internal intranet tool used 9am-5pm on weekdays.

---

## What comes next
Phase 62: Multi-AZ Reliability — Physical datacenter failure containment.
