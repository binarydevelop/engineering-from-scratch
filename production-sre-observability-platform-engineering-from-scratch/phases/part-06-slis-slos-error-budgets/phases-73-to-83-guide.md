# Phases 73 – 83: SLIs, SLOs & Error Budget Engineering

> **Motto**: Understand it. Instrument it. Measure it. Break it. Detect it. Debug it. Recover it. Automate it. Improve it. Operate it.

---

## Phase 73: Reliability as a Product Requirement

### Motto
"Reliability is the most fundamental feature of any product. A feature that does not work is not a feature; it is an annoyance."

### The User Journey Lens
Users do not care how many CPU cores your cluster has. They care about their user journeys:
* *"Can I search for a product?"*
* *"Can I add an item to my shopping cart?"*
* *"Can I submit payment and receive an order confirmation?"*
SLOs must be anchored to Critical User Journeys (CUJs).

---

## Phase 74: Service Level Indicators (SLIs)

### The SLI Equation
$$\text{SLI} = \frac{\sum \text{Good Events}}{\sum \text{Total Eligible Events}} \times 100\%$$

### Concrete Request-Based SLI
* **Good Event**: HTTP request method = `POST`, route = `/checkout`, status code $< 500$, latency $\le 0.500\text{s}$.
* **Total Event**: All HTTP POST `/checkout` requests excluding client errors (HTTP 400, 401).

---

## Phase 75: Service Level Objectives (SLOs)

### Setting Targets and Windows
* **Target**: $99.9\%$ (Three nines).
* **Window**: Rolling 30-day compliance window.
A rolling 30-day window evaluates actual delivered reliability over the trailing 720 hours, smoothing out short transient blips while holding teams accountable for sustained quality.

---

## Phase 76: SLO vs SLA

| Dimension | SLO (Service Level Objective) | SLA (Service Level Agreement) |
|:---|:---|:---|
| **Audience** | Internal engineering and product teams | External customers, enterprise clients |
| **Purpose** | Guide release velocity and reliability investments | Establish legal and financial contracts |
| **Consequence of Breach** | Shift development focus to reliability tasks | Financial penalties, credit refunds, contract breach |
| **Target Setting** | Stricter (e.g. 99.9%) to create a safety margin | Looser (e.g. 99.5%) to absorb internal fluctuations |

---

## Phase 77: Error Budgets

### The Currency of Release Velocity
$$\text{Error Budget} = 100\% - \text{SLO Target}$$
* For a 99.9% target: Allowable unreliability is $0.1\%$ ($0.001$).
* For 10,000,000 monthly requests: **10,000 failed requests are permitted**.
* If 4,000 requests fail: Consumed budget is $40\%$; remaining budget is $60\%$.
* **The Error Budget is meant to be spent!** If a service finishes the quarter with 100% remaining error budget, the team was moving too slowly or over-engineering solutions.

---

## Phase 78: Burn Rate Intuition

### How Fast Are We Spending Our Budget?
$$\text{Burn Rate} = \frac{\text{Observed Error Rate}}{1 - \text{SLO Target}}$$
* **1.0x Burn Rate**: Error rate is $0.1\%$. The budget will last exactly 30 days.
* **14.4x Burn Rate**: Error rate is $1.44\%$. $2\%$ of the monthly budget is consumed in **1 hour**! Complete budget exhaustion in **48 hours**.
* **36.0x Burn Rate**: Error rate is $3.6\%$. Complete budget exhaustion in **20 hours**.

---

## Phase 79: Multi-Window Multi-Burn-Rate Alerting

### Why Single-Window Thresholds Fail
* A 1-hour window alert at 14.4x fires fast during a SEV-1 outage, but keeps firing for 50 minutes after the outage has been completely resolved.
* A 5-minute window alert fires on a 30-second transient network glitch and wakes up an engineer for no reason.

### The Multi-Window Solution
Alert ONLY when:
$$\text{Long Window (1h) Burn Rate} > 14.4 \quad \text{AND} \quad \text{Short Window (5m) Burn Rate} > 14.4$$
* The long window ensures sufficient budget is consumed.
* The short window confirms the failure is *still actively happening right now*.
* When the incident is mitigated, the 5-minute burn rate drops to zero, and the alert resolves immediately!

---

## Phase 80: Choosing Realistic SLOs

### The Cost of Nines
Each additional "nine" multiplies infrastructure complexity and cost by 5x–10x:
* **99% (Two Nines)**: 7.2 hours downtime/month. Single server, simple backups.
* **99.9% (Three Nines)**: 43.2 minutes downtime/month. Multi-instance, automated health checks.
* **99.99% (Four Nines)**: 4.3 minutes downtime/month. Multi-zone, automated failover, canaries.
* **99.999% (Five Nines)**: 26 seconds downtime/month. Multi-region active-active, zero-downtime schema evolution, massive architectural cost.

---

## Phases 81 – 83: Batch SLOs, Queue SLOs & Governance

### Batch Pipeline Freshness (Phase 81)
$$\text{SLI} = \text{Time elapsed since last successful data warehouse sync} \le 24\text{ hours}$$

### Queue Backlog Age (Phase 82)
$$\text{SLI} = \text{Age of oldest unacknowledged message in RabbitMQ/Redis} \le 60\text{ seconds}$$

### Error Budget Policy Enforcement (Phase 83)
When a service depletes its 30-day error budget:
1. Product feature deployments with non-zero risk are paused.
2. Sprint capacity shifts to addressing postmortem corrective actions.
3. Once the 30-day compliance recovers above target, normal feature delivery resumes.
