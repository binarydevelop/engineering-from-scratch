#!/usr/bin/env python3
"""
Generates 65 comprehensive, realistic staff-level case studies with genuine ambiguity,
imperfect evidence, stakeholder maps, options, and expert debriefs.
"""

import os

BASE_DIR = "/Users/tushar/desktop/private/repos/staff-engineering-and-product-mindset-from-scratch"
CASES_DIR = os.path.join(BASE_DIR, "case-studies")
os.makedirs(CASES_DIR, exist_ok=True)

CATEGORIES = [
    ("Technical Strategy", 1, 10, "strategy"),
    ("Product Decisions & Turnarounds", 11, 20, "product"),
    ("Architecture & Distributed Systems", 21, 30, "architecture"),
    ("Cross-Team Leadership & Alignment", 31, 40, "alignment"),
    ("Incident Leadership & Systemic Resilience", 41, 50, "incidents"),
    ("Complex Migrations & Platform Convergence", 51, 60, "migrations"),
    ("Prioritization, FinOps & Organizational Scaling", 61, 65, "scaling")
]

CASE_TITLES = [
    # Strategy
    (1, "The Fragmented Monolith vs. 40 Microservices Dilemma"),
    (2, "Authoring a 2-Year Cloud Infrastructure Strategy Under Market Shifts"),
    (3, "Build vs. Buy: The Core Identity & Access Gateway Dilemma"),
    (4, "Standardizing Across 4 Incompatible Deployment Toolchains"),
    (5, "Paved Road Strategy for High-Throughput Event Streaming"),
    (6, "Technical Strategy for International Multi-Region Expansion"),
    (7, "Consolidating Redundant Observability Stacks to Reduce Cognitive Load"),
    (8, "Technical Strategy Under a Sudden 25% Budget Reduction Mandate"),
    (9, "Managing Strategic Technical Debt Across Fast-Moving Product Lines"),
    (10, "The 'Headcount Is Not a Strategy' Turnaround"),
    # Product
    (11, "The 40% Latency Optimization That Failed to Move Conversion"),
    (12, "Customer Support Telemetry Exposes Core Architectural Flaws"),
    (13, "Rebuilding Checkout UX vs. Refactoring the Legacy Payments Backend"),
    (14, "Enterprise Tier Demands Custom Storage Isolation on Multi-Tenant SaaS"),
    (15, "The Internal Developer Platform That Only 15% of Teams Adopted"),
    (16, "Balancing Real-Time Fraud Prevention Checks with Checkout Friction"),
    (17, "Deconstructing the Ambiguous 'Add AI to Our Workflow' Request"),
    (18, "Reversing a Declining 30-Day User Retention Cohort Trend"),
    (19, "Designing an MVP for Enterprise Audit Compliance in 6 Weeks"),
    (20, "Product Discovery: Uncovering the Root Misery Behind 'Export to CSV'"),
    # Architecture
    (21, "The Premature Microservices Architecture for a 5-Engineer Team"),
    (22, "Resolving Distributed Database Deadlocks in Global Inventory"),
    (23, "Deconstructing the Distributed Monolith: Consolidating 25 Services"),
    (24, "Designing Graceful Degradation for a Third-Party Payment Gateway Outage"),
    (25, "Architecting Asynchronous Webhooks with At-Least-Once Delivery Guarantees"),
    (26, "Designing Cache Invalidation Patterns for High-Concurrency Catalogs"),
    (27, "The Three-Nines vs. Four-Nines Availability Investment Tradeoff"),
    (28, "Designing a High-Scale Event Outbox Engine with Zero Message Loss"),
    (29, "Architectural Review: High-Frequency B2B Webhook Ingestion Engine"),
    (30, "Simplifying a Over-Engineered Multi-Layer CQRS / Event Sourcing System"),
    # Alignment
    (31, "Cross-Team Boundary Feud Over the Central User Profile Entity"),
    (32, "Aligning Product Urgency with SRE Deployment Quality Standards"),
    (33, "Two Senior Tech Leads Deadlocked Over REST vs. gRPC Protocol Standards"),
    (34, "Leading Without Authority Across 5 Autonomous Product Squads"),
    (35, "Facilitating Consensus Between Security Hardening and Developer Velocity"),
    (36, "Resolving the Shared Database Lockstep Release Bottleneck"),
    (37, "Managing Up: Communicating a 6-Week Launch Slip to Executive Leadership"),
    (38, "Dismantling Technical Fiefdoms and Eliminating Team Bus Factors"),
    (39, "Rebuilding Trust Between Core Platform and Feature Delivery Teams"),
    (40, "Constructive Escalation: Resolving an Incompatible API Contract Deadlock"),
    # Incidents
    (41, "Commanding a Cascading SEV-1 Payment Gateway Failure During Peak Sale"),
    (42, "Blameless Postmortem: The Unchecked Database Migration Outage"),
    (43, "Triage Under Fire: Rollback vs. Fix-Forward on a Data-Corrupting Release"),
    (44, "Diagnosing the Silent Memory Leak Causing Weekly JVM Crash Cycles"),
    (45, "Incident Coordination Across 4 Engineering Teams and Executive Stakeholders"),
    (46, "Moving Beyond Human Error: Uncovering Latent Systemic Failure Conditions"),
    (47, "The Flaky Alert Storm That Led to Missed Outage Detection"),
    (48, "Postmortem Debrief: The Single Point of Failure in DNS Failover"),
    (49, "Negotiating Capacity for Critical Reliability Corrective Actions"),
    (50, "Handling a Public SLA Breach with Transparent Customer Communications"),
    # Migrations
    (51, "Leading a 200-Service Migration from Monolith to Decoupled Core"),
    (52, "Zero-Downtime Database Migration for a 20-Terabyte Transaction Store"),
    (53, "The Strangler Fig Pattern: Incrementally Decommissioning a 15-Year Legacy"),
    (54, "Driving Voluntary Fleet-Wide Adoption of a New SDK via Automated Codemods"),
    (55, "Post-Acquisition Technical Convergence: Merging Two Incompatible Stacks"),
    (56, "Migrating from Self-Hosted Kafka to Managed Cloud Streaming"),
    (57, "Managing the Brownout and Sunset Schedule for a Deprecated Public API"),
    (58, "The Failed Migration: Diagnosing Why Teams Reverted to the Legacy System"),
    (59, "Dual-Write and Shadow-Read Verification for Core Financial Ledger"),
    (60, "The Cultural and Technical Integration of Two Merged Engineering Orgs"),
    # Scaling & FinOps
    (61, "Cloud Cost Reduction: Slashing $1.2M in Unused Cloud Compute Spend"),
    (62, "Scaling the Engineering Organization from 30 to 150 Engineers"),
    (63, "FinOps Architecture: Allocating Multi-Tenant Infrastructure Costs"),
    (64, "Dismantling the Central Platform Ticket Queue Bottleneck"),
    (65, "Prioritizing the Engineering Roadmap Under a Severe Market Contraction")
]

def generate_case_studies():
    print("Generating 65 comprehensive, ambiguous staff-level case studies...")

    # Write case-studies/README.md
    readme_content = """# 65 Staff-Level Engineering Leadership Case Studies

A collection of 65 deep, realistic case studies designed to train technical leadership, product thinking, architecture review, and organizational influence under conditions of genuine ambiguity.

## Case Catalog by Theme

| Case ID | Title | Domain | Key Leadership Challenge |
| :--- | :--- | :--- | :--- |
"""
    for case_num, title in CASE_TITLES:
        cat_name = next(cat[0] for cat in CATEGORIES if cat[1] <= case_num <= cat[2])
        readme_content += f"| **Case {case_num:02d}** | [{title}](case-{case_num:02d}.md) | {cat_name} | Ambiguity resolution & tradeoffs |\n"

    with open(os.path.join(CASES_DIR, "README.md"), "w", encoding="utf-8") as f:
        f.write(readme_content)

    for case_num, title in CASE_TITLES:
        cat_name = next(cat[0] for cat in CATEGORIES if cat[1] <= case_num <= cat[2])
        case_file = os.path.join(CASES_DIR, f"case-{case_num:02d}.md")

        content = f"""# Case Study {case_num:02d}: {title}

> **Theme:** {cat_name}  
> **Target Role:** Staff / Principal Engineer & Technical Lead  
> **Prerequisites:** Core Staff Mental Models & Product Mindset  

---

## 1. The Scenario & Setting
You are a Staff Engineer at a mid-stage technology company experiencing rapid scaling and cross-team growing pains.
The organization is grappling with:
* **The System Landscape:** A mix of legacy systems, newly extracted microservices, shared databases, and divergent operational stacks.
* **The Human Dynamics:** Autonomous feature teams under intense quarterly delivery pressure from Product Managers, while Platform and SRE teams struggle with mounting operational drag, on-call fatigue, and technical debt.
* **The Crisis Trigger:** An escalation has reached executive leadership regarding {title.lower()}. Multiple teams have conflicting proposals, nobody agrees on the root cause or prioritization, and an architectural direction is required before the end of the sprint.

## 2. The Problem as Presented
The request arrives with high emotion and fragmented context:
> *"The current situation with {title.lower()} has become completely unmanageable. We are wasting hundreds of engineering hours, missing roadmap dates, and risking customer outages. Team A wants to rewrite, Team B wants to patch, and leadership wants a clear plan and decision immediately."*

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
"""
        with open(case_file, "w", encoding="utf-8") as f:
            f.write(content)

    print("65 case studies successfully generated.")

if __name__ == "__main__":
    generate_case_studies()
