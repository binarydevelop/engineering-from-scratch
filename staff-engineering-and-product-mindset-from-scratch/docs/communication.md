# Technical & Executive Communication for Staff Engineers

> **Motto**: Clear writing creates clear thinking. High leverage belongs to those who communicate complex realities with brevity, precision, and empathy.

A staff engineer operates at the intersection of deep technical detail and executive strategy. Your impact is capped by your ability to tailor messages across engineering teams, cross-functional partners, and executive leadership.

---

## 1. The Core Communication Framework

Every written proposal, architectural update, or escalation must follow the **CPERTD** pipeline:

```text
 ┌─────────────────┐
 │     Context     │  Why are we talking about this right now? What changed?
 └────────┬────────┘
          │
          ▼
 ┌─────────────────┐
 │     Problem     │  What is broken, degrading, or blocking business outcomes?
 └────────┬────────┘
          │
          ▼
 ┌─────────────────┐
 │    Evidence     │  What verified data, metrics, or incident logs prove it?
 └────────┬────────┘
          │
          ▼
 ┌─────────────────┐
 │ Recommendation  │  What is our recommended technical / operational action?
 └────────┬────────┘
          │
          ▼
 ┌─────────────────┐
 │    Tradeoffs    │  What are the costs, risks, and explicit non-goals?
 └────────┬────────┘
          │
          ▼
 ┌─────────────────┐
 │ Decision Needed │  What explicit approval or ownership call is required?
 └────────┬────────┘
          │
          ▼
 ┌─────────────────┐
 │    Next Step    │  Who does what by when?
 └─────────────────┘
```

---

## 2. The 5-Sentence Executive Summary

Directors, VPs, and C-level executives read dozens of documents daily. They do not have time to read a 12-page RFC to extract the core business decision.

### The Five-Sentence Formula:
1. **Sentence 1 (Context & Problem):** *Due to a 4x increase in catalog traffic, our current synchronous search cluster breaches our 250ms p99 SLA on 12% of peak queries, dropping checkout conversion by 2.1%.*
2. **Sentence 2 (Current Evidence):** *Database telemetry confirms read lock saturation on the inventory table is the primary bottleneck.*
3. **Sentence 3 (Proposed Action):** *We propose introducing an asynchronous read-replica cluster with an event-driven cache invalidation layer over the next 4 weeks.*
4. **Sentence 4 (Tradeoffs & Cost):** *This requires an estimated $1,200/mo in additional cloud infrastructure and temporarily defers our internal analytics refactor.*
5. **Sentence 5 (Decision & Outcome):** *We request approval to begin the 4-week rollout, which will restore p99 latency below 180ms and recover an estimated $140k in monthly checkout revenue.*

---

## 3. Audience Adaptation: One Incident, Six Perspectives

When an outage occurs or an architectural pivot is made, explain the event to each audience without losing truth or overwhelming with irrelevant detail:

| Audience | What They Care About | Tone & Framing | What to Omit |
| :--- | :--- | :--- | :--- |
| **Software Engineers** | Root cause, stack traces, bytecode, fix verification, preventing recurrence | Technical, peer-to-peer, code-level precision | High-level financial impacts |
| **Engineering Manager** | Team capacity impact, sprint backlog disruption, on-call morale | Operational, resourcing-focused, process health | Raw SQL query execution plans |
| **Product Manager** | Customer user experience, feature roadmap delay, customer trust | User outcome, timeline, functional compromises | Thread dump analysis, JVM flags |
| **Support / Ops** | What to tell angry customers, workarounds, resolution ETA | Empathetic, actionable, clear timelines | Internal architectural debates |
| **Executive Leadership** | Revenue impact, SLA liabilities, brand risk, systemic prevention | Business-oriented, concise, risk-mitigated | Deep implementation mechanics |
| **External Customers** | Service availability, data security, apology, commitment to reliability | Humble, transparent, non-technical, reassuring | Internal team friction or blame |

---

## 4. Status Communication: Good vs. Bad

### The Bad Status Update (Task Checklist)
> *"This week we attended 6 meetings, reviewed 14 PRs, investigated the database, created a ticket for the indexing service, and wrote some unit tests. Next week we will continue working on the migration."*
* **Why it fails:** Lists activity rather than progress; hides risks; gives stakeholders zero visibility into whether the project is on track to deliver its outcome.

### The Good Status Update (Outcome & Risk)
> **Initiative:** Payment Gateway Modernization  
> **Status:** AMBER (Launch target: Oct 15)  
> **Outcome Delivered:** Completed shadow traffic test; processed 100k transactions through sandbox with 0.02% error rate (Target: < 0.05%).  
> **Key Risk:** Third-party gateway sandbox returns 450ms p99 latency during peak load tests, risking our 200ms checkout SLA.  
> **Decision Needed:** Product approval to implement an asynchronous webhook confirmation flow rather than synchronous response.  
> **Next Week:** Run 48-hour endurance test; finalize webhook RFC with Team Mobile.

---

## 5. Communicating Bad News Early

Hiding slippage or downplaying technical debt in the hope of a miracle is an amateur failure mode. A staff engineer delivers bad news with composure, evidence, and options:

### The 4 Rules of Delivering Bad News:
1. **Never Surprise Your Manager or Sponsor:** The moment a critical-path risk crosses a probability threshold, flag it.
2. **Bring Options, Not Just a Fire:** Never deliver a problem without at least two structured alternatives and a recommendation.
3. **Avoid Catastrophizing:** Stick strictly to observable facts and measured impact. Do not induce organizational panic.
4. **Take Responsibility for Next Steps:** Clarify who is investigating, what experiments are running, and when the next formal update will arrive.
