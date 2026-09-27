# Lesson Template

Use this canonical template when authoring, reviewing, or solving any lesson in `staff-engineering-and-product-mindset-from-scratch`. Every lesson must anchor in a concrete engineering leadership situation and result in tangible artifacts, decisions, and system leverage.

> **Motto**: Understand the problem. Create clarity. Align people. Make tradeoffs. Drive outcomes. Raise the system.

---

# Lesson [XX]: [Lesson Title]

> **Motto**: "[A memorable, punchy one-sentence principle that captures the technical leadership reality.]"

**Type:** Problem Selection / Product Mindset / Strategy / Architecture Review / Stakeholder Alignment / Incident Leadership  
**Prerequisites:** [List prior phase numbers]  
**Estimated Time:** [e.g., 60 minutes]

---

## Motto
State the motto clearly with conceptual and behavioral emphasis.

## Situation
Describe the messy organizational and technical context.
* Who are the teams involved?
* What are the competing incentives, historical baggage, and existing systems?
* What is the time pressure or escalation trigger?
* Avoid sanitized toy examples; include the political, architectural, and operational realities.

## Problem as presented
State the symptom, complaint, or request exactly as it arrived at your desk.
* Examples: "The monolith is too slow," "We need Kafka," "Team X is blocking our launches," or "Checkout latency is unacceptable."

## Prediction
Before analyzing the data or proposing a path forward:
1. What will happen if the organization takes the presented problem at face value and implements the requested fix?
2. What hidden dependencies, organizational conflicts, or technical landmines do you predict exist?
3. What is the likelihood that the proposed technical fix fails to move the business or user metric?

## Reframe the problem
Peel back the layers of assumptions to state the true underlying problem.
* Separate symptoms from root causes.
* Frame the problem around user value, operational constraints, and system throughput rather than technology preferences.
* Contrast the naive framing with the reframed problem.

## User impact
* Who is the user? (External customer, internal developer, operations team, customer support, data analyst).
* What concrete friction, delay, failure, or degradation are they experiencing?
* How frequent is this problem, and how severe is its impact on their workflow?

## Product/business impact
* What business metric is damaged? (Conversion rate, customer retention, churn, AWS/infrastructure costs, SLA breach penalties, engineering cycle time).
* What is the cost of doing nothing for the next two quarters?
* What is the estimated opportunity cost of diverting engineering attention to this problem?

## Evidence
List the empirical data required to validate the reframed problem:
* Metrics, logs, traces, APM flame graphs, and database queries.
* Customer support tickets, user research interview recordings, and onboarding drop-off funnels.
* Deployment failure rates, rollback logs, and cycle time telemetry.
* Explicitly distinguish verified facts from anecdotal claims.

## Stakeholders
Map the key players, their local incentives, and their concerns:
* **Product Manager (PM)**: Delivery velocity, user conversion, feature parity.
* **Engineering Manager (EM)**: Team capacity, career progression, predictable sprint delivery.
* **Staff/Principal Architects**: System consistency, cross-service cohesion, operational risk.
* **SRE / Platform**: Outage blast radius, on-call burden, infrastructure spend.
* **Finance / Legal / Security**: Compliance, data sovereignty, budget caps.

## Constraints
Document the non-negotiable boundaries:
* Hard calendar deadlines (e.g., regulatory mandate, Black Friday, contractual launch).
* Team bandwidth and skill gaps.
* Legacy system compatibility requirements.
* Budgetary and compute resource caps.

## Unknowns
Classify the information gaps:
* **Known Unknowns**: Questions we know we need to answer (e.g., p99 database query time during peak traffic).
* **Assumptions**: Beliefs we are treating as true until proven otherwise.
* **Spikes/Prototypes Needed**: Time-boxed experiments required to de-risk technical choices.

## Options
Detail at least three distinct paths forward:
* **Option 1: The Minimal Sufficient Intervention** (Smallest change that solves 80% of the pain).
* **Option 2: The Architectural Refactoring** (Medium-term investment addressing the structural cause).
* **Option 3: The Strategic Platform Rewrite / Migration** (High-effort, long-term paradigm shift).
* **Option 4: The Intentional Do-Nothing / Deferral** (Living with the constraint to focus on higher priorities).

## Tradeoffs
Compare the options across explicit criteria:
| Criterion | Option 1 (Minimal) | Option 2 (Refactor) | Option 3 (Platform) |
| :--- | :--- | :--- | :--- |
| Time to Value | | | |
| Engineering Effort | | | |
| Operational Burden | | | |
| Reversibility | | | |
| User Outcome Risk | | | |

## Decision
State the chosen path with unambiguous clarity:
* Which option is selected?
* Why this option over the alternatives?
* **What are we explicitly choosing NOT to do?** (Non-goals are mandatory).
* What condition or evidence would cause us to reverse or alter this decision?

## Communication
How is this decision communicated across audiences?
* **Executive Summary (for VP / Director)**: 3-5 sentences focusing on business impact, risk, and timeline.
* **Team / RFC Framing (for Engineers)**: Technical depth, interfaces, migration steps, and operational runbooks.
* **Cross-Functional Partner Brief (for PM / Operations)**: Roadmap changes, release stages, and user-facing benefits.

## Execution
Define the execution strategy:
* How is work sliced into thin, independently deliverable vertical milestones?
* What is the critical path?
* How are cross-team dependencies coordinated without weekly 20-person status meetings?
* Who is the single accountable owner for each workstream?

## Outcome
How do we know the intervention worked?
* **Target Metric**: Primary outcome metric and measurable goal (e.g., p99 latency < 250ms, checkout drop-off down 4%).
* **Guardrail Metric**: Metrics that must not degrade (e.g., error rate remains < 0.01%, AWS bill increases < 5%).
* When will the outcome be formally evaluated?

## Reflection
Post-decision analysis:
* What surprised us during rollout?
* Which assumptions held, and which failed?
* What organizational friction slowed down progress?

## Leverage
How did this work raise the system beyond the immediate project?
* Did we create a shared reusable component, paved road, or automated linter?
* Did we elevate the technical judgment of senior engineers through pairing or review?
* Did we eliminate a class of recurring production incidents or cross-team debates?

## Questions for mastery
Scenario-based evaluation questions:
1. [Scenario testing stakeholder conflict under deadline pressure]
2. [Scenario testing tradeoff selection when data is incomplete]
3. [Scenario evaluating the boundary between staff engineer and engineering manager]

## What comes next
Preview the next logical concept in the curriculum and explain how this lesson's mental model provides the foundation.
