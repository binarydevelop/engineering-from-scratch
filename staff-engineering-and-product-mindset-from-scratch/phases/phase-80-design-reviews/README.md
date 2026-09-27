# Lesson 80: Design Review Facilitation

> **Motto**: "A great design review is a collaborative discovery, not an interrogation."

**Type:** Staff Engineering Leadership & Product Mindset  
**Prerequisites:** Phase 79  
**Estimated Time:** 60 minutes  

---

## Motto
"A great design review is a collaborative discovery, not an interrogation."

## Situation
At a fast-growing technology company, engineering teams are facing acute friction:
Facilitate architectural reviews that stress-test systems without ego.
Three separate teams (Feature Product, Infrastructure Platform, and Operations) have divergent perspectives on priorities, ownership boundaries, and technical direction. Leadership expects clarity, a concrete decision, and an actionable execution plan.

## Problem as presented
The initial complaint arrives as an emotional escalation:
*"The current setup is completely unworkable. Teams are blocked, deployments are taking forever, and we need an immediate architectural overhaul."*

## Prediction
Before analyzing the telemetry or proposing a solution:
1. What will happen if leadership accepts this complaint at face value and approves an immediate rewrite?
   - *Prediction:* The rewrite will consume six months of engineering capacity without addressing the underlying workflow bottleneck or user outcome.
2. What hidden organizational dependencies or misaligned incentives are driving this friction?
3. What is the probability that the requested technical change fails to move customer metrics?

## Reframe the problem
Peel back the surface complaint to expose the root systemic problem:
* **Naive Framing:** *"We need to adopt a new platform/framework immediately."*
* **Staff-Level Reframed Problem:** *"Cross-team interface boundaries are ambiguous and manual verification steps create a 14-day deployment lag, increasing cycle time and defect rates on core user journeys."*

## User impact
* **Who is affected?** Both external customers experiencing delayed feature fixes and internal engineers suffering from high deployment friction.
* **Severity & Frequency:** Occurs daily; impacts 100% of developers deploying to this subsystem.
* **User Behavior:** Frustration leads to batching changes into massive, high-risk bi-weekly releases.

## Product/business impact
* **Business Metric:** Lead time for changes exceeds 14 days; change failure rate sits at 18%; customer ticket escalations have increased by 25%.
* **Opportunity Cost:** Diverting three teams to an unguided rewrite would delay the Q3 customer checkout expansion.

## Evidence
Empirical telemetry gathered to validate the reframed problem:
1. CI/CD telemetry logs showing build queues waiting an average of 42 minutes for shared test environments.
2. Error budgets from production monitoring indicating 80% of outages stem from uncoordinated schema migrations.
3. Developer survey data highlighting deployment anxiety as the primary driver of team burnout.

## Stakeholders
* **Product Manager (PM):** Wants predictable feature delivery; fears multi-month platform freezes.
* **Engineering Manager (EM):** Worries about team burnout, sprint rollover, and on-call paging frequency.
* **Platform Lead:** Demands fleet-wide standardization and adherence to infrastructure policies.
* **Security & Compliance:** Requires automated audit trails for all data access changes.

## Constraints
* Zero planned customer downtime permitted during any transition.
* No net increase in cloud infrastructure budget.
* Existing team headcount remains fixed for the next two quarters.

## Unknowns
* What is the true p99 latency under peak holiday traffic?
* How many legacy internal clients depend on undocumented API behaviors?
* What is the effort required to build an automated paved road migration tool?

## Options
* **Option 1 (Minimal Sufficient Intervention):** Introduce automated contract testing in CI and add read replicas to alleviate immediate database load. (Effort: 2 weeks).
* **Option 2 (Architectural Refactoring & Paved Road):** Extract domain interfaces, provide self-service CI templates, and implement a strangler pattern for incremental migration. (Effort: 6 weeks).
* **Option 3 (Complete System Rewrite):** Halt feature work and rewrite the entire subsystem from scratch using a new language and platform. (Effort: 6 months).

## Tradeoffs
| Criterion | Option 1 (Minimal) | Option 2 (Paved Road) | Option 3 (Rewrite) |
| :--- | :--- | :--- | :--- |
| Time to First Value | **2 Weeks** | 4 Weeks | 6 Months |
| Operational Disruption | Low | Low/Med | Extremely High |
| Risk of Scope Creep | None | Controlled | Massive |
| Systemic Durability | Temporary Patch | **High (Paved Road)** | High (if completed) |

## Decision
* **Selected Decision:** **Option 2 (Architectural Refactoring & Paved Road)**.
* **Rationale:** It addresses the root socio-technical bottleneck by automating paved roads while allowing feature teams to continue shipping value incrementally.
* **Non-Goals (What we are choosing NOT to do):**
  * We will NOT rewrite the underlying database engine this quarter.
  * We will NOT build custom framework tooling where standard open-source tools suffice.
* **Revisit Condition:** If traffic increases by more than 5x before Q4, we will evaluate sharding strategies.

## Communication
* **Executive Summary (for VP / Director):**
  > *"To resolve deployment bottlenecks without freezing product delivery, we are introducing a self-service paved road and automated contract validation over the next 6 weeks. This will reduce change lead times from 14 days to under 4 hours, protect Q3 roadmap commitments, and require zero additional headcount or budget."*
* **Team Brief (for Engineers):** Walk through the RFC, interface contracts, automated CI checks, and migration runbooks.

## Execution
* **Milestone 1 (Week 2): Risk Retirement Spike.** Prototype contract validator in CI; verify zero false positives on 100 historical PRs.
* **Milestone 2 (Week 4): Pilot Team Migration.** Migrate one service using the new paved road; measure deployment lead time drop.
* **Milestone 3 (Week 6): Self-Service Rollout.** Open paved road to all teams; deprecate legacy manual verification checklists.

## Outcome
* **Target Metric:** Median lead time to production drops from 14 days to 3.5 hours.
* **Guardrail Metric:** Change failure rate drops below 2%; zero customer-facing availability regressions.

## Reflection
* The team initially resisted automated contract checks, fearing they would slow down PR merges. Once demonstrated that checks run in 90 seconds, resistance evaporated.
* Establishing the paved road created more goodwill between Platform and Product teams than two quarters of alignment meetings.

## Leverage
* **How this raised the system:**
  * Replaced manual gatekeeping with automated CI guardrails.
  * Eliminated an entire class of recurring deployment incidents across 12 teams.
  * Mentored two senior engineers who independently led the pilot rollout.

## Questions for mastery
1. How would you handle an Engineering Manager who demands a complete rewrite because their team is tired of working in legacy code?
2. If the Product Manager refuses to allocate 20% capacity for the 6-week paved road, how would you frame the business cost of delay to align them?
3. What is the difference between a staff engineer resolving this problem and a senior engineer resolving it?

## What comes next
In the next phase, we deepen these principles to build durable technical strategies and organizational momentum.
