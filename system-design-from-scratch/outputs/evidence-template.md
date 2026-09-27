# Architecture Evidence & Observation Log

> Record your empirical measurements, failure observations, and architectural decisions here.

---

## 1. System Metadata
- **System / Problem Name**:
- **Date**:
- **Baseline Architecture**:
- **Target Scale**:

---

## 2. Requirements & Constraints
- **Functional Requirements**:
- **Non-Functional Requirements (SLAs)**:
- **Assumptions**:
- **Explicit Non-Goals**:

---

## 3. Back-of-the-Envelope Estimates
- **Daily Active Users**:
- **Read QPS / Write QPS**:
- **Peak Factor**:
- **Storage Growth (1 day / 5 years)**:
- **Bandwidth (Ingress / Egress)**:
- **Cache Memory Requirements**:

---

## 4. Empirical Experiment Log
- **Baseline Measurement (p50 / p95 / p99 Latency)**:
- **Failure Injected**:
- **Observed System Behavior & Error Codes**:
- **Root Cause & Bottleneck**:
- **Architectural Modification Applied**:
- **Verification Measurement Post-Fix**:

---

## 5. Architectural Tradeoffs & Justification
- **What component was added?**
- **What concrete failure did it prevent?**
- **What new failure mode or operational cost did it introduce?**
- **What simpler alternative was rejected and why?**
- **What would you change at 10x higher scale?**
- **What would you remove at 1/100th scale?**
