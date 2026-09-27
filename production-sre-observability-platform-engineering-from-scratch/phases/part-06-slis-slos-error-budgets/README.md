# Part 06: SLIs, SLOs & Error Budgets (Phases 73 – 83)

> **Motto**: Understand it. Instrument it. Measure it. Break it. Detect it. Debug it. Recover it. Automate it. Improve it. Operate it.

---

## Overview

Part 06 moves reliability from subjective opinions to mathematical rigor. We define Critical User Journeys (CUJs), construct Service Level Indicators (SLIs), establish Service Level Objectives (SLOs), compute error budgets, and implement Multi-Window Multi-Burn-Rate alerting.

---

## Key Formulas & Concepts

### 1. Service Level Indicator (SLI)
$$\text{SLI} = \frac{\text{Good Events}}{\text{Total Events}} \times 100\%$$
* Good Event: `http.response.status_code < 500 AND duration_seconds <= 0.500`
* Total Event: All valid eligible user checkout requests.

### 2. Error Budget
$$\text{Error Budget} = 100\% - \text{SLO Target}$$
* For a 99.9% SLO over 10,000,000 monthly requests:
  - Allowed Failures: $10,000,000 \times 0.001 = \mathbf{10,000\text{ requests}}$.

### 3. Burn Rate Mathematics (Phase 78)
$$\text{Burn Rate} = \frac{\text{Observed Error Rate}}{\text{Allowable Error Rate}}$$
* Burn Rate = 1.0 -> 100% of error budget consumed exactly at day 30.
* Burn Rate = 14.4 -> 2% of total monthly error budget consumed in 1 hour.
* Burn Rate = 20.0 -> Total budget exhausted in 36 hours.

### 4. Multi-Window Multi-Burn-Rate Alerting (Phase 79)
Alerts fire ONLY when BOTH the long window (verifying significant budget consumption) AND the short window (verifying the outage is actively continuing) cross threshold, eliminating false alarms on transient spikes!
