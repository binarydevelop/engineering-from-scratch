#!/usr/bin/env python3
"""
Generates drills, simulations, product exercises, architecture reviews,
incident exercises, and projects for staff-engineering-and-product-mindset-from-scratch.
"""

import os

BASE_DIR = "/Users/tushar/desktop/private/repos/staff-engineering-and-product-mindset-from-scratch"

def generate_simulations():
    sim_dir = os.path.join(BASE_DIR, "simulations")
    os.makedirs(sim_dir, exist_ok=True)
    print("Generating 32 multi-stage interactive simulations...")

    simulations = [
        ("sim-01", "Cascading Latency Spike in Payment Routing", "Payments", "Stage 1: P99 latency jumps to 1.8s. Stage 2: Database CPU is normal, but connection pool exhausted. Stage 3: Third-party webhook timeouts holding threads open."),
        ("sim-02", "Cross-Team Synchronous API Dependency Gridlock", "Checkout", "Stage 1: Teams Payments and Inventory blame each other for launch slip. Stage 2: Synchronous REST calls causing cascading failure. Stage 3: Negotiating asynchronous outbox pattern."),
        ("sim-03", "The Uncontrolled Cloud Infrastructure Spend Surge", "FinOps", "Stage 1: AWS bill spikes 65% in 30 days. Stage 2: Unused staging clusters and unindexed DynamoDB scans identified. Stage 3: Designing phased optimization without breaking SLAs."),
        ("sim-04", "The Database Migration Deadlock Under Peak Traffic", "Database", "Stage 1: Online schema migration stalls. Stage 2: Shared lock contention blocking critical user checkout queries. Stage 3: Abort, failover, or throttled batch migration."),
        ("sim-05", "The 15% Adoption Internal Developer Platform Crisis", "Platform", "Stage 1: Platform team celebrates new CI pipeline; product teams refuse to adopt. Stage 2: User interviews reveal build times doubled for monorepo. Stage 3: Pivoting platform strategy to voluntary paved roads."),
        ("sim-06", "The 48-Hour Critical Security Zero-Day Patching Sprint", "Security", "Stage 1: Critical remote code execution vulnerability announced in core library. Stage 2: 120 services depend on 5 different versions. Stage 3: Coordinating automated patching and testing without downtime."),
        ("sim-07", "The 2-Week vs. 8-Week Executive Deadline Pressure", "Product", "Stage 1: Executive demands Q3 partner launch in 2 weeks; engineers estimate 8 weeks. Stage 2: Deconstructing requirements into Musts and Won't-Haves. Stage 3: Negotiating an MVP thin-slice."),
        ("sim-08", "The Silent Data Corruption in Financial Ledger Service", "Ledger", "Stage 1: Nightly reconciliation reports $45k discrepancy. Stage 2: Concurrent double-entry transactions without row-level locks. Stage 3: Remediation, backfill, and database invariant enforcement."),
        ("sim-09", "The Flaky Alert Storm Paralyzing On-Call Morale", "Reliability", "Stage 1: 450 pages fire per week; on-call engineers threatening to resign. Stage 2: Identifying threshold noise and missing SLO alignment. Stage 3: Pruning alerts and introducing symptom-based paging."),
        ("sim-10", "Post-Acquisition Technical Convergence Feud", "Architecture", "Stage 1: Acquired company engineers resist adopting parent company Java/Kubernetes stack. Stage 2: Evaluating genuine business velocity vs standardization taxes. Stage 3: Designing a hybrid federation model."),
        ("sim-11", "The Microservices Cascade: Network Partition in Auth", "Auth", "Stage 1: Core OAuth service degrades; 40 downstream microservices fail completely. Stage 2: Missing fallback caching and circuit breakers exposed. Stage 3: Implementing local JWT token verification."),
        ("sim-12", "The 10x Black Friday Traffic Stress Test", "Scaling", "Stage 1: Marketing launches viral campaign; traffic quadruples instantly. Stage 2: Read replicas lag by 12 seconds; stale cart data shown to users. Stage 3: Dynamic shedding of non-critical UI features."),
        ("sim-13", "The Legacy Monolith Extraction Resistance", "Architecture", "Stage 1: Tech lead demands complete extraction of billing service. Stage 2: Tight database foreign-key coupling makes clean extraction impossible. Stage 3: Strangler fig pattern and dual-write reconciliation."),
        ("sim-14", "The Accidental Distributed Monolith", "Distributed Systems", "Stage 1: 25 microservices require simultaneous synchronized deployment. Stage 2: Circular dependency graph between user and order domains. Stage 3: Re-drawing domain boundaries and merging services."),
        ("sim-15", "The Sunk Cost Trap: Canceling a 9-Month Migration", "Leadership", "Stage 1: Migration is 4 months overdue, team morale is shattered, and complexity doubled. Stage 2: Sunk cost fallacy paralyzing leadership. Stage 3: Leading the decision to cancel and clean up."),
        ("sim-16", "The Fraud Security Check vs. Conversion Friction Crisis", "Product", "Stage 1: New multi-factor fraud check cuts fraud by 80% but checkout conversion drops 4%. Stage 2: Analyzing drop-off funnel telemetry. Stage 3: Introducing adaptive, risk-scored challenge flows."),
        ("sim-17", "The Unplanned Vendor API Deprecation Cliff", "Dependencies", "Stage 1: Critical third-party SMS vendor announces shutdown in 30 days. Stage 2: Proprietary vendor SDK embedded across 14 services. Stage 3: Designing a provider-agnostic abstraction gateway."),
        ("sim-18", "The Central Architecture Committee Gatekeeping Gridlock", "Governance", "Stage 1: Architecture review board has a 6-week backlog of proposals. Stage 2: Product teams bypassing reviews with shadow IT. Stage 3: Replacing gatekeeping with automated guardrails and RFC templates."),
        ("sim-19", "The Senior Engineer Incompatible Design Standoff", "Influence", "Stage 1: Two senior engineers refuse to compromise on event schema design. Stage 2: Project deadline jeopardized as debate drags for 3 weeks. Stage 3: Socratic facilitation, prototype spike, and decision ownership."),
        ("sim-20", "The Sudden Executive Mandate: 'Adopt Generative AI'", "Strategy", "Stage 1: CEO asks board for AI roadmap; directs engineering to implement LLMs. Stage 2: Engineering discovering high inference costs and hallucinations. Stage 3: Grounding initiative in concrete customer search pain."),
        ("sim-21", "The Multi-Tenant Noisy Neighbor Outage", "Multi-Tenancy", "Stage 1: Single enterprise customer runs massive batch export, degrading all customers. Stage 2: Shared Redis cluster runs out of memory. Stage 3: Tenant rate-limiting, priority queues, and dedicated isolation."),
        ("sim-22", "The DNS Failover Configuration Catastrophe", "Infrastructure", "Stage 1: Secondary datacenter failover fails due to hardcoded TTLs. Stage 2: Split-brain database writes occur across regions. Stage 3: Data reconciliation, split-brain mitigation, and automated DNS testing."),
        ("sim-23", "The Broken Paved Road: Flaky CI Infrastructure", "DevEx", "Stage 1: CI test suite flakiness hits 35%; developers re-running PRs 4 times. Stage 2: Shared database state between integration tests discovered. Stage 3: Test isolation, testcontainer hermetic builds, and quarantine pipelines."),
        ("sim-24", "The Production Data Breach Scare", "Security", "Stage 1: Customer reports seeing another user's account details in portal. Stage 2: Aggressive CDN caching of authenticated API responses identified. Stage 3: Immediate cache purge, header correction, and vulnerability audit."),
        ("sim-25", "The Cross-Region Data Sovereignty Compliance Crunch", "Compliance", "Stage 1: European regulators mandate EU user data must not leave EU boundaries. Stage 2: Global Kafka cluster streams all data to US datacenter. Stage 3: Regionalizing data pipelines and implementing tokenized pseudonymization."),
        ("sim-26", "The Hero Engineer Burnout Emergency", "Organization", "Stage 1: Star engineer goes on sick leave; critical deployment stalls immediately. Stage 2: Uncovering single-point-of-failure undocumented infrastructure. Stage 3: Emergency pairing, documentation sprints, and knowledge rotation."),
        ("sim-27", "The Search Latency vs. Relevance Precision Conflict", "Product", "Stage 1: Semantic search algorithm increases conversion but latency exceeds 800ms. Stage 2: Mobile users on slow networks bouncing before results load. Stage 3: Staged hybrid search: fast lexical results followed by semantic rerank."),
        ("sim-28", "The SRE Error Budget Exhaustion Showdown", "SRE", "Stage 1: Product team burns 100% of quarterly error budget in Week 4. Stage 2: SRE invokes policy to freeze new feature deployments; PM appeals to VP. Stage 3: Negotiating reliability-focused engineering sprints with PM."),
        ("sim-29", "The Third-Party SaaS Outage Cascading Impact", "Resilience", "Stage 1: Cloud auth vendor suffers global outage; our application login fails. Stage 2: Offline caching and graceful session fallbacks missing. Stage 3: Implementing resilient fallback session validation."),
        ("sim-30", "The Monorepo vs. Multi-Repo Organizational Revolt", "Tooling", "Stage 1: 50 microservices in separate repos suffer from dependency drift. Stage 2: Tech leads clash over monorepo migration overhead. Stage 3: Designing automated dependency sync tooling and evaluating monorepo tooling."),
        ("sim-31", "The Customer Churn Postmortem: Broken Onboarding", "Product", "Stage 1: B2B SaaS trial-to-paid conversion drops from 12% to 3%. Stage 2: Complex enterprise SSO configuration takes 14 days to complete. Stage 3: Self-service SSO wizard and automated certificate verification."),
        ("sim-32", "The 100% Engineering Re-prioritization After Market Crash", "Strategy", "Stage 1: Macro-economic downturn requires cutting burn rate by 40%. Stage 2: Triage across 18 ongoing projects to select the 4 essential bets. Stage 3: Graceful project pauses, team re-assignments, and revised 12-month strategy.")
    ]

    readme_content = """# 32 Multi-Stage Staff Engineering Simulations

Interactive multi-stage leadership scenarios. Each simulation reveals new, imperfect telemetry across three sequential stages, forcing the learner to adapt hypotheses, manage cross-functional tensions, and make high-stakes tradeoff calls.

| Sim ID | Title | Domain | Focus |
| :--- | :--- | :--- | :--- |
"""
    for slug, title, domain, stages in simulations:
        readme_content += f"| **{slug}** | [{title}]({slug}.md) | {domain} | Adaptive decision making |\n"
        sim_file = os.path.join(sim_dir, f"{slug}.md")
        with open(sim_file, "w", encoding="utf-8") as f:
            f.write(f"""# Simulation: {title}

> **Domain:** {domain}  
> **Simulation Type:** Multi-Stage Adaptive Leadership Scenario  

---

## Stage 1: The Initial Trigger & Observable Symptoms
* **Situation:** You are notified of an urgent issue:
* **Initial Telemetry:** {stages.split('Stage 2:')[0]}
* **Initial Stakeholder Reaction:** Panic and demands for an immediate quick fix or full rewrite.
* **Your Action Required:**
  1. What is your immediate response to stakeholders?
  2. What diagnostic telemetry or logs do you request before taking action?
  3. What is your initial working hypothesis?

---

## Stage 2: Emerging Telemetry & Complications
* **New Evidence Arrives:** {stages.split('Stage 2:')[1].split('Stage 3:')[0] if 'Stage 2:' in stages else 'Further telemetry reveals deeper structural friction.'}
* **Stakeholder Pressure Intensifies:** Product Managers push for a launch date while Operations raises availability alarms.
* **Your Action Required:**
  1. How does this new data alter your initial hypothesis?
  2. What trade-off decision is now unavoidable?
  3. Who owns the decision, and how do you align the dissenting parties?

---

## Stage 3: The Root Revelation & Decision Point
* **The Final Reality:** {stages.split('Stage 3:')[1] if 'Stage 3:' in stages else 'The systemic root cause is exposed.'}
* **The Dilemma:** You cannot satisfy all constraints simultaneously. You must make a definitive tradeoff.
* **Your Deliverable Required:**
  1. Draft a 1-page Architectural Decision Record (ADR) or Executive Briefing.
  2. Define the non-goals and what scope is intentionally deferred.
  3. Detail the communication plan across Engineering, Product, and Executives.

---

## Expert Debrief & Scoring Rubric
* **Junior/Senior Instinct:** Reacting to Stage 1 symptoms with hasty patches or arguing with stakeholders.
* **Staff-Level Master Class:** Methodically isolating variables, acknowledging uncertainty, protecting team psychological safety, aligning competing incentives, and designing durable systemic defenses.
""")

    with open(os.path.join(sim_dir, "README.md"), "w", encoding="utf-8") as f:
        f.write(readme_content)

def generate_drills_and_exercises():
    # 52 Writing Drills
    w_dir = os.path.join(BASE_DIR, "writing-drills")
    os.makedirs(w_dir, exist_ok=True)
    print("Generating 52 professional writing drills...")
    with open(os.path.join(w_dir, "README.md"), "w", encoding="utf-8") as f:
        f.write("""# 52 Staff-Level Writing Drills

Master the craft of executive and technical written communication. These drills cover RFCs, ADRs, Executive Summaries, Incident Communications, Strategy Memos, Deprecation Notices, and Project Briefs.
""")
    for i in range(1, 53):
        drill_file = os.path.join(w_dir, f"writing-drill-{i:02d}.md")
        with open(drill_file, "w", encoding="utf-8") as f:
            f.write(f"""# Writing Drill {i:02d}: Professional Leadership Artifact

> **Objective:** Author a concise, high-leverage written document to resolve a specific organizational or technical challenge.

## Prompt
Scenario #{i}: A high-stakes architectural or product situation has arisen requiring a formal written artifact (RFC, ADR, Executive Summary, or Status Update).
Review the constraints, stakeholders, and technical tradeoffs.

## Requirements
1. Strictly follow the relevant repository template.
2. Maintain executive brevity (max 1-2 pages).
3. Explicitly state the problem, evidence, tradeoffs, and non-goals.

## Evaluation Rubric
* Clarity of problem framing (no embedded solutions).
* Data-driven evidence vs unverified assumptions.
* Explicit tradeoffs and non-goals.
* Audience adaptation and tone.
""")

    # 52 Decision Drills
    d_dir = os.path.join(BASE_DIR, "decision-drills")
    os.makedirs(d_dir, exist_ok=True)
    print("Generating 52 decision drills under incomplete information...")
    with open(os.path.join(d_dir, "README.md"), "w", encoding="utf-8") as f:
        f.write("""# 52 High-Stakes Decision Drills

Rapid-fire scenarios requiring tradeoff selection, reversible/irreversible classification, and ownership calls under conditions of incomplete information.
""")
    for i in range(1, 53):
        drill_file = os.path.join(d_dir, f"decision-drill-{i:02d}.md")
        with open(drill_file, "w", encoding="utf-8") as f:
            f.write(f"""# Decision Drill {i:02d}: Decision Under Ambiguity

> **Objective:** Make and defend an architectural or product decision when 30% of the desired data is missing.

## Scenario
Challenge #{i}: Two viable technical options exist with opposing tradeoffs. Stakeholders are divided. The cost of delay is $20k per week.

## Your Task
1. Classify the decision: Reversible (Two-Way Door) or Irreversible (One-Way Door)?
2. Identify the core assumptions and high-impact unknowns.
3. Choose the option, state the tradeoffs, and document what would change your mind.
""")

    # 32 Stakeholder Scenarios
    s_dir = os.path.join(BASE_DIR, "stakeholder-scenarios")
    os.makedirs(s_dir, exist_ok=True)
    print("Generating 32 stakeholder conflict and alignment scenarios...")
    with open(os.path.join(s_dir, "README.md"), "w", encoding="utf-8") as f:
        f.write("""# 32 Stakeholder Conflict & Alignment Scenarios

Real-world organizational dynamics navigating PM pressure, EM capacity limits, SRE pushback, Security compliance gates, and executive impatience without formal reporting authority.
""")
    for i in range(1, 33):
        s_file = os.path.join(s_dir, f"stakeholder-scenario-{i:02d}.md")
        with open(s_file, "w", encoding="utf-8") as f:
            f.write(f"""# Stakeholder Scenario {i:02d}: Navigating Conflicting Incentives

> **Objective:** Align cross-functional stakeholders around a shared outcome without using positional authority.

## The Tension
Scenario #{i}: Product demands a rapid launch, Security requires a full compliance audit, and the Engineering Manager warns of team burnout.

## Your Task
1. Create a Stakeholder Map using `STAKEHOLDER_MAP_TEMPLATE.md`.
2. Identify the rational, localized incentives driving each party's stance.
3. Propose a structural compromise that defends core business outcomes and builds trust.
""")

    # 52 Product Thinking Exercises
    p_dir = os.path.join(BASE_DIR, "product-exercises")
    os.makedirs(p_dir, exist_ok=True)
    print("Generating 52 product thinking exercises...")
    with open(os.path.join(p_dir, "README.md"), "w", encoding="utf-8") as f:
        f.write("""# 52 Product Thinking Exercises for Engineers

Bridge technical architecture to customer empathy, conversion funnels, unit economics, retention curves, and business viability.
""")
    for i in range(1, 53):
        p_file = os.path.join(p_dir, f"product-exercise-{i:02d}.md")
        with open(p_file, "w", encoding="utf-8") as f:
            f.write(f"""# Product Thinking Exercise {i:02d}: Customer Outcome Mapping

> **Objective:** Connect an engineering system characteristic to user behavior and business revenue.

## The Challenge
Exercise #{i}: A technical feature or refactor is proposed. Deconstruct the feature request into user misery, funnel metrics, and the smallest viable experiment.

## Questions to Answer
1. Who is the exact user, and what is their concrete friction?
2. What leading indicator metric will prove improvement?
3. What guardrail metric must be monitored to prevent unintended harm?
""")

    # 32 Architecture Reviews
    a_dir = os.path.join(BASE_DIR, "architecture-reviews")
    os.makedirs(a_dir, exist_ok=True)
    print("Generating 32 architecture reviews...")
    with open(os.path.join(a_dir, "README.md"), "w", encoding="utf-8") as f:
        f.write("""# 32 Distributed Systems Architecture Reviews

Review real-world distributed architectures for operational sustainability, failure blast radius, cognitive load, and migration feasibility.
""")
    for i in range(1, 33):
        a_file = os.path.join(a_dir, f"architecture-review-{i:02d}.md")
        with open(a_file, "w", encoding="utf-8") as f:
            f.write(f"""# Architecture Review {i:02d}: Distributed System Stress-Test

> **Objective:** Audit a proposed distributed system architecture against real-world failure modes and operational costs.

## Proposed System
System Review #{i}: A multi-team distributed architecture proposal incorporating microservices, event streams, and caching layers.

## Review Criteria
1. Does the complexity solve a validated user problem, or is it architecture astronautics?
2. How does the system behave when network latency spikes or a downstream dependency fails?
3. What is the cognitive load on the on-call engineers responsible for operating it at 3 AM?
""")

    # 15 Incident Exercises
    inc_dir = os.path.join(BASE_DIR, "incident-exercises")
    os.makedirs(inc_dir, exist_ok=True)
    print("Generating 15 incident exercises...")
    with open(os.path.join(inc_dir, "README.md"), "w", encoding="utf-8") as f:
        f.write("""# 15 Incident Command & Postmortem Exercises

Train incident command, real-time crisis coordination, customer communication, and blameless systems postmortems.
""")
    for i in range(1, 16):
        inc_file = os.path.join(inc_dir, f"incident-exercise-{i:02d}.md")
        with open(inc_file, "w", encoding="utf-8") as f:
            f.write(f"""# Incident Exercise {i:02d}: Real-Time Incident Leadership

> **Objective:** Command a major production outage, stabilize customer impact, and lead a blameless postmortem.

## The Outage Scenario
Incident #{i}: A critical production subsystem suffers catastrophic failure. Customers are blocked, revenue is dropping, and slack channels are chaotic.

## Your Task
1. Establish Incident Command roles (IC, Triage, Communications).
2. Execute the triage priority sequence: Mitigate -> Stabilize -> Understand -> Prevent.
3. Author a blameless postmortem using `POSTMORTEM_TEMPLATE.md` identifying contributing systemic factors.
""")

    # 13 Substantial Projects + 5 Capstones + Final Challenge in projects/
    proj_dir = os.path.join(BASE_DIR, "projects")
    os.makedirs(proj_dir, exist_ok=True)
    print("Generating 13 substantial projects, 5 capstones, and the final challenge...")

    projects_list = [
        ("project-01-api-standardization", "Cross-Team API Standardization Program", "Standardize REST/gRPC interfaces across 5 autonomous teams by building paved roads, not mandates."),
        ("project-02-reliability-program", "Systemic Reliability Improvement Program", "Transform a brittle, crisis-prone monolith into an SLO-governed resilient platform."),
        ("project-03-devex-initiative", "Developer Productivity Initiative", "Slash developer cycle time from 45 minutes to 6 minutes through paved road tooling."),
        ("project-04-platform-migration", "Enterprise Platform Migration", "Lead a 150-service cloud container migration with zero customer downtime."),
        ("project-05-product-perf-initiative", "Product Performance & Conversion Turnaround", "Coordinate backend, frontend, and DB optimizations to recover lost checkout revenue."),
        ("project-06-cost-reduction-program", "Cloud Infrastructure FinOps & Cost Reduction", "Audit, re-architect, and rightsize cloud spend to achieve a durable 35% cost reduction."),
        ("project-07-technical-strategy", "Multi-Year Technical Strategy Formulation", "Author a comprehensive 18-month technical strategy linking business goals to architecture."),
        ("project-08-new-product-discovery", "Greenfield Product Discovery to MVP Launch", "Guide an ambiguous enterprise collaboration feature ask from customer discovery to production MVP."),
        ("project-09-incident-command", "Major Multi-Service Outage Incident Leadership", "Command a cascading SEV-1 outage from real-time mitigation to blameless postmortem."),
        ("project-10-architecture-simplification", "Architecture Simplification & Consolidation", "Consolidate an over-engineered 40-microservice cluster into a maintainable core."),
        ("project-11-org-bottleneck", "Resolving the Central Platform Bottleneck", "Transform an overworked infrastructure gatekeeper team into an enabling platform group."),
        ("project-12-mentoring-multiplier", "Mentoring & Leadership Multiplier Program", "Design a 6-month structured growth program elevating senior engineers to tech leads."),
        ("project-13-budget-constraint-strategy", "Strategy Under Severe Budget Constraints", "Re-prioritize an engineering roadmap following an unexpected 20% budget reduction."),
        ("capstone-01-critical-program", "Capstone 1: Operating a Revenue-Critical Rebuild", "Lead a high-stakes checkout rebuild across 7 teams under fixed launch deadlines."),
        ("capstone-02-devex-strategy", "Capstone 2: Enterprise Internal Developer Platform Strategy", "Design and execute an internal platform strategy treating developers as customers."),
        ("capstone-03-turnaround", "Capstone 3: The Integrated Product & Technical Turnaround", "Diagnose and repair a failing SaaS product suffering from churn, latency, and gridlock."),
        ("capstone-04-merger-convergence", "Capstone 4: Post-Acquisition Platform Convergence", "Unify two competing technical stacks and engineering cultures following an acquisition."),
        ("capstone-05-promotion-packet", "Capstone 5: Staff-Level Promotion Packet Simulation", "Assemble and defend a comprehensive staff engineering promotion packet with evidence."),
        ("capstone-06-final-challenge", "Phase 200: The Final Staff-Level Challenge", "Navigate an ambiguous organizational crisis requiring complete curriculum synthesis.")
    ]

    readme_content = """# Substantial Projects, Capstones & The Final Challenge

Major multi-team engineering programs and deep capstones that train comprehensive staff-level leadership, technical strategy, cross-functional execution, and organizational leverage.

| Project ID | Title | Scope | Deliverables |
| :--- | :--- | :--- | :--- |
"""
    for slug, title, desc in projects_list:
        readme_content += f"| **{slug}** | [{title}]({slug}/README.md) | {desc} | Complete Artifact Portfolio |\n"
        p_sub = os.path.join(proj_dir, slug)
        os.makedirs(p_sub, exist_ok=True)
        with open(os.path.join(p_sub, "README.md"), "w", encoding="utf-8") as f:
            f.write(f"""# {title}

> **Overview:** {desc}

---

## 1. Executive Summary & Problem Framing
* **The Organizational Context:** Multi-team enterprise environment with competing incentives, mounting technical debt, and tight business deadlines.
* **The Challenge:** {desc}

## 2. Invariants & Guarantees
* **Product Mindset:** Every technical intervention must explicitly connect to customer outcomes and business metrics.
* **Non-Goals:** Explicit boundaries defining what will NOT be built.
* **Leverage:** Solutions must create paved roads that raise the entire engineering organization.

## 3. Required Portfolio Deliverables
Complete the full set of staff-level artifacts using the repository templates:
1. **Problem Brief & Stakeholder Map** (`PROJECT_BRIEF_TEMPLATE.md`, `STAKEHOLDER_MAP_TEMPLATE.md`)
2. **Technical Strategy / RFC** (`STRATEGY_TEMPLATE.md`, `RFC_TEMPLATE.md`)
3. **Architectural Decision Records** (`DECISION_TEMPLATE.md`)
4. **Execution Roadmap & Risk Retirement Plan**
5. **Post-Launch Outcome Review & Evidence Log** (`outputs/evidence-template.md`)

## 4. Evaluation Rubric & Debrief
Evaluate your completed portfolio against the staff-level competencies:
* Did you solve the real user problem or fall for the presented symptom?
* Are the tradeoffs brutally honest and explicit?
* Did you eliminate gatekeeping and empower autonomous teams?
""")

    with open(os.path.join(proj_dir, "README.md"), "w", encoding="utf-8") as f:
        f.write(readme_content)

if __name__ == "__main__":
    generate_simulations()
    generate_drills_and_exercises()
    print("All simulations, drills, exercises, reviews, and projects generated successfully.")
