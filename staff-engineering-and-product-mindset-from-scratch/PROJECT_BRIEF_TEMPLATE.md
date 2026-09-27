# Project Brief Template

Use this template to frame, shape, and de-risk a major multi-team technical initiative before committing engineering teams to sprint backlogs.

---

# Project Brief: [Initiative Name]

* **Staff Tech Lead:** [Name]
* **Product Lead:** [Name]
* **Engineering Manager Partner:** [Name]
* **Target Quarter:** [e.g., Q3 202X]
* **Status:** In Shaping | Ready for Review | Committed | In Flight | Completed

---

## 1. Problem Framing
* What concrete problem are we solving?
* Who experiences this problem?
* What is the evidence that this is a critical problem to solve right now?

## 2. Desired Outcomes & Success Metrics
* **Primary Business / Product Outcome:** (e.g., checkout completion rate improves by 2.5%).
* **Primary Technical Outcome:** (e.g., p99 API latency decreases from 850ms to 200ms).
* **Guardrail Metrics:** (e.g., cloud spend does not increase by more than $500/mo; zero customer regressions).

## 3. Scope Boundaries
* **In Scope:**
  * Concrete features, systems, and interfaces modified or created.
* **Non-Goals (Explicitly Out of Scope):**
  * Adjacent capabilities, premature optimizations, or unrelated technical debt cleanup that will be deferred.

## 4. Key Constraints
* Hard calendar delivery commitments or market events.
* Resource caps (number of engineers available).
* Legacy compatibility and customer SLA commitments.

## 5. Stakeholder Alignment & Ownership
| Workstream | Accountable Owner | Contributing Teams | Key Stakeholder |
| :--- | :--- | :--- | :--- |
| API Contracts & Gateway | [Lead Engineer] | Platform, Payments | Product Manager |
| Data Layer & Migration | [Lead Engineer] | Data Infra, Core Store| SRE Lead |
| Frontend Checkout UX | [Lead Engineer] | Web Checkout, Mobile | UX Designer |

## 6. Major Unknowns & Risk Retirement Strategy
What are the highest-risk assumptions, and how will we de-risk them in Week 1 rather than Week 10?
* **Risk 1:** Unproven third-party payment gateway latency under peak load.
  * *Early Retirement Action:* Run a 48-hour load testing spike against their sandbox environment prior to signing contract.
* **Risk 2:** Cross-table locking during database migration.
  * *Early Retirement Action:* Prototype online schema migration on staging cluster with replicated production volume.

## 7. Milestone Slicing (Thin End-to-End Capabilities)
Structure work into thin, vertical, risk-retiring milestones rather than horizontal architectural layers:
* **Milestone 0 (Week 2): Risk Retirement & Architecture Proof**
  * Spikes completed; architectural decision records signed off.
* **Milestone 1 (Week 4): Internal Dark Launch**
  * End-to-end shadow traffic routed through new pipeline; telemetry validated.
* **Milestone 2 (Week 7): 5% Canary User Traffic**
  * First real customer traffic served; conversion metrics monitored.
* **Milestone 3 (Week 10): 100% Traffic & Legacy Decommissioning**
  * Full cutover completed; legacy code and database tables removed.

## 8. Communication Cadence
* Weekly written async status report distributed to [Slack Channel / Mailing List].
* Bi-weekly steering check-in with executive sponsors.
