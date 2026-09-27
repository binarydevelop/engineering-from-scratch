# Case Study 37: Managing Up: Communicating a 6-Week Launch Slip to Executive Leadership

> **Theme:** Cross-Team Leadership & Alignment  
> **Target Role:** Staff / Principal Engineer & Technical Lead  
> **Prerequisites:** Core Staff Mental Models & Product Mindset  

---

## 1. The Scenario & Setting
You are a Staff Engineer at a mid-stage technology company experiencing rapid scaling and cross-team growing pains.
The organization is grappling with:
* **The System Landscape:** A mix of legacy systems, newly extracted microservices, shared databases, and divergent operational stacks.
* **The Human Dynamics:** Autonomous feature teams under intense quarterly delivery pressure from Product Managers, while Platform and SRE teams struggle with mounting operational drag, on-call fatigue, and technical debt.
* **The Crisis Trigger:** An escalation has reached executive leadership regarding managing up: communicating a 6-week launch slip to executive leadership. Multiple teams have conflicting proposals, nobody agrees on the root cause or prioritization, and an architectural direction is required before the end of the sprint.

## 2. The Problem as Presented
The request arrives with high emotion and fragmented context:
> *"The current situation with managing up: communicating a 6-week launch slip to executive leadership has become completely unmanageable. We are wasting hundreds of engineering hours, missing roadmap dates, and risking customer outages. Team A wants to rewrite, Team B wants to patch, and leadership wants a clear plan and decision immediately."*

## 3. The Ambiguity & Incomplete Evidence
You do not have perfect data. The telemetry provided is contradictory and messy:
* **Dashboard Signals:** APM traces show intermittent latency spikes, but CPU and memory utilization remain within normal operational bounds.
* **Conflicting Perspectives:** Product insists user drop-off is driven by system latency; engineering leads suspect client-side rendering bottlenecks; operations reports uncoordinated database schema locking.
* **Unknowns:** What is the true p99 customer impact? What are the hidden upstream dependencies? What is the cost of doing nothing for the next two quarters?

## 4. Stakeholder Map & Competing Incentives
* **Product Manager:** Measured on feature velocity, conversion funnels, and quarterly roadmap delivery. Fears any multi-month platform freeze.
* **Engineering Manager:** Worried about team cognitive load, on-call alert fatigue, and sprint spillover.
* **Platform / SRE Architect:** Incentivized by fleet-wide standardization, system availability, and low incident MTTR.
* **Finance / Leadership:** Demanding predictable capital allocation, lower AWS infrastructure burn, and adherence to business timelines.

## 5. Staff-Level Framing & Strategic Options
A staff engineer does not jump immediately into technical implementation. You must reframe the problem around user outcomes and evaluate at least three distinct paths forward:

### Option 1: The Minimal Sufficient Intervention (Tactical De-risking)
* **Approach:** Implement targeted circuit breakers, add read replicas, and introduce basic rate limiting.
* **Pros:** Fast time-to-value (1-2 weeks); minimal organizational disruption; zero new technology introduced.
* **Cons:** Leaves underlying architectural coupling unresolved; will breach limits if traffic doubles.

### Option 2: The Architectural Refactoring & Paved Road (Recommended)
* **Approach:** Decouple interfaces, establish an asynchronous event contract, and provide self-service migration templates for feature teams.
* **Pros:** Directly addresses systemic friction; maintains product feature momentum; creates durable leverage.
* **Cons:** Requires cross-team coordination over 6-8 weeks; demands disciplined execution.

### Option 3: The Complete Strategic Rewrite / Platform Migration
* **Approach:** Freeze non-critical feature work and rewrite the subsystem using a greenfield architecture.
* **Pros:** Clean slate; eliminates all legacy debt in theory.
* **Cons:** High probability of delayed delivery (6+ months); massive opportunity cost; extreme risk of building for imagined future requirements.

## 6. Tradeoff Matrix
| Dimension | Option 1 (Minimal) | Option 2 (Paved Road) | Option 3 (Rewrite) |
| :--- | :--- | :--- | :--- |
| Time to First Value | **2 Weeks** | 4 Weeks | 6 Months |
| Engineering Effort | Low | Medium | Very High |
| Risk of Scope Creep | Low | Managed | Extreme |
| Systemic Durability | Low | **High** | High (if successful) |
| Impact on Product Delivery | Zero | Minor (20% capacity) | Total Freeze |

## 7. Required Learner Deliverables
To resolve this case study, author the following three artifacts using the standard repository templates:
1. **Executive Summary (1 Page):** Briefing for the VP of Engineering framing the problem, verified evidence, recommended path, and non-goals.
2. **Architectural Decision Record (ADR):** High-stakes decision document capturing context, options, tradeoffs, and revisit triggers.
3. **Execution & Risk Retirement Plan:** Thin vertical slices, critical path analysis, and milestone definitions.

## 8. Case Debrief & Expert Analysis
* **What a Senior Engineer Would Do:** Senior engineers often jump to Option 1 (quick code patch) or passionately advocate for Option 3 (rewrite the system because the legacy code is ugly).
* **What Makes the Staff-Level Response Distinct:** The staff engineer reframes the problem around user value and cross-team incentives, selects Option 2 (the paved road), defines explicit non-goals, and aligns stakeholders without formal reporting authority.
