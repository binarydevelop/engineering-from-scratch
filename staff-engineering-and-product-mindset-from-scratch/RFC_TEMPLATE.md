# Request for Comments (RFC) Template

An RFC is a proposal for a major architectural change, cross-team interface contract, or technical initiative. It builds consensus through asynchronous written debate and structured review.

---

# RFC-[NNN]: [Title of Proposal]

* **Author(s):** [Name / Handle]
* **Status:** Draft | In Review | Approved | Rejected | Superseded
* **Target Review Date:** YYYY-MM-DD
* **Approvers / Key Stakeholders:** [Lead Engineers, EMs, PMs, Security, SRE]
* **Target Milestone / Launch:** [Quarter / Date]

---

## 1. Summary
A concise, 3-4 sentence overview of the proposal: what is being proposed, why it matters to users or the business, and the core technical approach.

## 2. Context
What background information does a reader need to evaluate this proposal?
* Current system architecture and historical trajectory.
* Recent changes in business scale, product requirements, or team organization.
* Previous attempts or related initiatives.

## 3. Problem Statement
What concrete problem does this RFC address?
* Quantify the pain with metrics, incidents, or developer hours wasted.
* Avoid jumping directly into the solution.

## 4. Goals and Non-Goals
* **Goals:**
  * Specific, measurable technical or product capabilities delivered.
  * Problems that will be completely resolved.
* **Non-Goals:**
  * Adjacent problems we are explicitly choosing NOT to solve in this initiative.
  * Scope boundaries to prevent project creep.

## 5. Requirements
* **Functional Requirements:** What capabilities must the system provide?
* **Non-Functional Requirements:**
  * Throughput, latency percentiles (p50, p99), and concurrency targets.
  * Availability and reliability targets (e.g., 99.95% uptime).
  * Data durability and consistency models.

## 6. Options Considered
Describe each viable alternative explored, including the "do nothing" or minimal refactor option.
* **Option A (Alternative):** Overview, pros, cons, and why it was rejected.
* **Option B (Alternative):** Overview, pros, cons, and why it was rejected.

## 7. Proposed Technical Approach
Detailed architecture of the recommended solution:
* **System Architecture Diagram:** (ASCII flow or component interaction).
* **Data Models & Storage:** Schemas, access patterns, partitioning, indexing.
* **API Contracts & Interfaces:** Request/response schemas, event payloads, synchronous vs asynchronous communication.
* **Key Algorithms / Workflows:** Sequence of operations for critical user paths.

## 8. Tradeoffs & Inherent Disadvantages
What are we intentionally sacrificing by choosing this approach?
* What complexity is added?
* What operational burden or cognitive load is introduced?

## 9. Failure Modes & Blast Radius
* What happens when downstream services fail, latency spikes, or networks partition?
* How does the system degrade gracefully?
* Circuit breakers, fallbacks, retry policies with jitter, and dead-letter queues.

## 10. Migration & Rollout Strategy
How do we get from current state to the proposed state safely without downtime?
* Phased rollout plan (e.g., dark launches, canary deployments, feature flags).
* Strangler pattern or dual-write / dual-read verification steps.
* Backwards compatibility guarantees and deprecation timelines.
* Rollback plan if critical metrics degrade during migration.

## 11. Observability & Operability
* **Metrics:** SLIs and SLOs defined for this component.
* **Logging & Tracing:** Distributed trace propagation, log levels, sensitive data masking.
* **Alerting:** Symptoms-based alert definitions (paging alerts vs ticketing).
* **Runbooks:** Standard operational procedures for common incidents.

## 12. Security, Privacy, and Compliance
* Data classifications handled (PII, PCI, HIPAA).
* Authentication, authorization, and network isolation models.
* Threat modeling: potential abuse vectors and defenses.

## 13. Financial Cost Analysis
* Estimated compute, storage, and egress costs at current scale and 5x scale.
* Third-party vendor licensing fees vs self-hosted infrastructure expenses.

## 14. Open Questions & Unresolved Issues
List specific questions where feedback from reviewers is requested:
1. [Question regarding database indexing or partition keys]
2. [Question regarding API backwards compatibility]

## 15. Decision & Next Steps
* Final status and resolution of the RFC.
* Immediate implementation milestones and workstream assignments.
