# Stakeholder Map Template

A stakeholder map helps staff engineers navigate organizational complexity, align competing incentives, and communicate effectively without formal reporting authority.

---

# Stakeholder Map: [Initiative Name]

* **Initiative Lead:** [Staff Engineer]
* **Last Updated:** YYYY-MM-DD

---

## 1. Stakeholder Analysis Matrix

| Stakeholder / Group | Core Interest & Incentive | Organizational Influence (H/M/L) | Primary Fear / Concern | Decision Role (RACI) | Preferred Communication Cadence & Format |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Product Manager (PM)** | Conversion rate, feature launch velocity, user satisfaction | High | Launch delay, customer-facing regression, loss of competitive edge | Accountable / Consulted | Weekly 1:1, shared brief, async Slack |
| **Engineering Manager (EM)** | Team delivery throughput, developer morale, predictable sprints | High | Unplanned work, team burnout, sprint disruption | Responsible | Bi-weekly planning check-in |
| **Platform / SRE Lead** | System stability, low on-call paging, standardized tooling | High | Increased maintenance burden, uncontrolled failure modes | Consulted / Approver | Written RFC review, architectural sync |
| **Security / Compliance** | Zero data breach risk, regulatory adherence | High | Unencrypted sensitive data, non-compliant third-party vendor | Approver (Hard Gate) | Security design review document |
| **Contributing Dev Teams** | Clean API, minimal adoption friction, clear documentation | Med | Complicated migration, breaking changes in downstream contracts | Responsible / Informed | Tech demo, clear code samples, pair programming |
| **Executive Sponsor (VP/Dir)**| Business outcome delivery, strategic alignment, budget control | High | Missed quarterly commitment, budget overrun, cross-team gridlock | Informed | Monthly 3-sentence executive summary |

*RACI Legend: Responsible (R), Accountable (A), Consulted (C), Informed (I).*

---

## 2. Competing Incentives & Tension Points
Document the natural, rational points of conflict between stakeholder groups:
* **Tension 1 (Product vs SRE):** Product wants to ship the feature immediately to beat a competitor; SRE requires a 2-week canary verification and rollback runbook before enabling traffic.
  * *Resolution Strategy:* Implement an automated feature flag with instant kill-switch capability, enabling product testing while protecting SRE availability.
* **Tension 2 (Platform vs Feature Teams):** Platform team wants strict standardization on gRPC; Feature teams prefer REST for faster frontend prototyping.
  * *Resolution Strategy:* Provide an automated OpenAPI-to-gRPC transcoding gateway on the paved road, reducing friction for feature teams.

---

## 3. Communication & Alignment Plan
* **Before Major Decisions:** 1:1 alignment with high-influence stakeholders to gather input, identify objections early, and incorporate constraints prior to open meetings.
* **During RFC / Design Phase:** Asynchronous written review with a fixed 7-day feedback window.
* **During Rollout:** Transparent, automated dashboards and weekly outcome-focused status updates.
