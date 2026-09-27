# Architectural Decision Record / Decision Journal Template

Use this template to record high-stakes architectural, organizational, and product decisions. The goal is to document the context, alternatives, and reasoning at the moment the decision is made, establishing accountability and preventing historical revisionism.

---

# ADR-[NNN]: [Title of Decision]

* **Status:** Proposed | Accepted | Deprecated | Superseded by [ADR-XXX]
* **Date:** YYYY-MM-DD
* **Decision Owner:** [Staff Engineer / Tech Lead]
* **Key Stakeholders:** [EM, PM, Principal Architect, SRE Lead]
* **Revisit Date:** YYYY-MM-DD

---

## 1. Context
Describe the forces at play:
* What technical, product, or organizational situation necessitated this decision?
* What business or customer pressures exist right now?
* What is the current system baseline, and what constraints are binding us?

## 2. Problem Statement
Clearly articulate the exact problem being solved.
* Avoid embedding solutions into the problem statement.
* Define what breaks, degrades, or stalls if no decision is made.

## 3. Options Considered

### Option A: [Name of Option]
* **Description:** [Brief architectural overview]
* **Pros:** [Benefits, strengths, leverage]
* **Cons:** [Drawbacks, complexity, operational cost]
* **Effort / Time to Value:** [S / M / L / XL]

### Option B: [Name of Option]
* **Description:** [Brief architectural overview]
* **Pros:** [Benefits, strengths, leverage]
* **Cons:** [Drawbacks, complexity, operational cost]
* **Effort / Time to Value:** [S / M / L / XL]

### Option C: [Minimal Intervention or Do Nothing]
* **Description:** [Living with the constraint or applying simple tactical patch]
* **Pros:** [Immediate, zero-to-low migration effort]
* **Cons:** [Accumulated debt, recurring operational pain]
* **Effort / Time to Value:** [Minimal]

## 4. Evidence
What empirical facts, benchmarks, prototypes, or user data informed this evaluation?
* Traces, metrics, or profiling data.
* Prototype spike results.
* Production incident history.

## 5. Assumptions
What beliefs are we treating as true for this decision to make sense?
* Assumption 1: [e.g., Traffic will not exceed 5x over the next 18 months].
* Assumption 2: [e.g., Team B will complete their API contract by Q3].

## 6. Unknowns & Blind Spots
What could we NOT know at the time of writing?
* [e.g., Long-term latency characteristics under multi-region replication].

## 7. Tradeoff Analysis
Compare the options against critical dimensions:
| Dimension | Option A | Option B | Option C |
| :--- | :--- | :--- | :--- |
| Initial Implementation Cost | | | |
| Ongoing Operational Maintenance | | | |
| Reversibility (Two-Way vs One-Way Door)| | | |
| Alignment with Technical Strategy | | | |
| Team Cognitive Load | | | |

## 8. Decision & Rationale
State the chosen option clearly:
* **Selected Option:** Option [X]
* **Why:** Explain why the advantages of this option decisively outweigh its drawbacks under current constraints.
* **What We Are Choosing NOT to Do:** Explicitly document the rejected alternatives and non-goals.

## 9. Expected Outcomes & Success Metrics
* **Primary Target Metric:** [e.g., p99 latency drops below 200ms within 60 days of launch].
* **Guardrail Metric:** [e.g., Error rate does not exceed 0.05%; compute cost remains under $2,000/mo].

## 10. Risks & Mitigations
| Identified Risk | Severity (H/M/L) | Likelihood (H/M/L) | Mitigation Strategy |
| :--- | :--- | :--- | :--- |
| | | | |

## 11. Revisit Conditions & "What Would Change My Mind?"
Under what specific circumstances should future engineers reconsider this decision?
* "If monthly active users exceed 10 million before Q4..."
* "If the managed vendor price increases by more than 40%..."
* "If team ownership shifts to a centralized platform group..."
