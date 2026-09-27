# staff-engineering-and-product-mindset-from-scratch

> **Understand the problem. Create clarity. Align people. Make tradeoffs. Drive outcomes. Raise the system.**

A complete, first-principles curriculum designed to transition senior software engineers into transformative technical leaders, product-minded architects, and high-leverage Staff Engineers.

---

## What This Repository Is

**This is NOT a collection of inspirational leadership quotes.**  
**This is NOT vague management advice or MBA theory.**  
**This is NOT an interview cheat sheet for Staff Engineer titles.**

This is a rigorous, practical, scenario-driven apprenticeship in the craft of staff-level engineering leadership. It teaches how to navigate extreme organizational ambiguity, make high-stakes technical tradeoffs, align autonomous teams without formal reporting authority, connect engineering investments directly to user and business outcomes, and build systems—both software and organizational—that continue thriving without depending on you personally.

```text
 ┌─────────────────────────────────────────────────────────────────────────────┐
 │                         THE STAFF LEADERSHIP JOURNEY                        │
 └─────────────────────────────────────────────────────────────────────────────┘
                                       │
                                Strong Engineer
                                       │
                                       ▼
                                Problem Framing
                                       │
                                       ▼
                                Product Thinking
                                       │
                                       ▼
                                Decision Making
                                       │
                                       ▼
                               Technical Strategy
                                       │
                                       ▼
                             Architecture Leadership
                                       │
                                       ▼
                              Cross-Team Influence
                                       │
                                       ▼
                              Execution Leadership
                                       │
                                       ▼
                             Mentoring & Leverage
                                       │
                                       ▼
                              Incident Leadership
                                       │
                                       ▼
                            Organizational Leverage
                                       │
                                       ▼
                               Staff-Level Impact
```

---

## The Target Mental Model

The central thesis of this curriculum is:

> **A staff-level engineer creates leverage across people, systems, decisions, and organizations by bringing clarity to ambiguous problems and driving durable outcomes.**

A staff engineer is **not** simply "the smartest programmer in the room" or "the person who writes the most code." When presented with an ambiguous crisis such as:

> *"Checkout latency has increased, conversion has dropped, three teams own pieces of the path, nobody agrees on the root cause, and leadership wants a plan by Friday."*

a staff engineer does not jump immediately into rewriting the database layer. Instead, they methodically reason through:

```text
What is actually happening?
     │
     ▼
What evidence do we have?
     │
     ▼
What is the user and business impact?
     │
     ▼
What is uncertain or unverified?
     │
     ▼
Who owns which part of the system?
     │
     ▼
What decisions are currently blocked?
     │
     ▼
What must happen now (mitigation)?
     │
     ▼
What can wait (non-goals)?
     │
     ▼
What are the technical options?
     │
     ▼
What are the product tradeoffs?
     │
     ▼
How do we align stakeholders without authority?
     │
     ▼
How do we slice the execution plan into thin, risk-retiring milestones?
     │
     ▼
How will we know it actually worked?
```

---

## Repository Structure

```text
staff-engineering-and-product-mindset-from-scratch/
├── README.md                           # Manifesto, mental models, and quickstart
├── ROADMAP.md                          # Exhaustive curriculum across all 201 phases
├── LEARNING.md                         # The 10-step learning cycle and 15 rules of operation
├── LESSON_TEMPLATE.md                  # Canonical lesson format (Situation to Leverage)
├── CASE_STUDY_TEMPLATE.md              # Template for ambiguous, realistic case studies
├── DECISION_TEMPLATE.md                # Architectural Decision Record / Decision Journal
├── RFC_TEMPLATE.md                     # High-impact Request for Comments proposal template
├── STRATEGY_TEMPLATE.md                # 12-24 month Technical Strategy blueprint
├── PROJECT_BRIEF_TEMPLATE.md           # Pre-sprint project shaping and boundary document
├── POSTMORTEM_TEMPLATE.md              # Blameless, systems-oriented postmortem format
├── STAKEHOLDER_MAP_TEMPLATE.md         # Influence, incentive, and RACI mapping template
├── CONTRIBUTING.md                     # Standards for contributing scenarios and drills
│
├── docs/                               # Authoritative technical leadership guides
│   ├── glossary.md                     # Precise glossary of engineering and product terms
│   ├── staff-mental-models.md          # Problem framework, leverage hierarchy, and 12 anti-patterns
│   ├── product-thinking.md             # Product thinking framework, funnels, and DevEx as product
│   ├── decision-making.md              # Two-way vs one-way doors, decision quality, and escalation
│   ├── communication.md                # Executive summaries, audience adaptation, and RFC authoring
│   ├── influence.md                    # Influence without authority, incentives, and trust
│   ├── execution.md                    # Thin slices, critical paths, risk retirement, and debt
│   └── career-framework.md             # The 4 staff archetypes, EM partnership, and promotion packets
│
├── phases/                             # 201 progressive phases (Phase 00 to Phase 200)
├── case-studies/                       # 60+ ambiguous, multi-team case studies with expert debriefs
├── simulations/                        # 30+ multi-stage adaptive leadership simulations
├── writing-drills/                     # 50+ professional writing exercises (RFCs, briefs, memos)
├── decision-drills/                    # 50+ rapid-fire decisions under incomplete information
├── stakeholder-scenarios/              # 30+ cross-functional conflict and alignment scenarios
├── product-exercises/                  # 50+ product discovery, funnel, and metric exercises
├── architecture-reviews/               # 30+ distributed system architecture review challenges
├── incident-exercises/                 # Incident command, real-time triage, and postmortems
├── projects/                           # 13 substantial multi-team engineering leadership programs
├── capstones/                          # 5 deep organizational and technical capstones
└── outputs/                            # Completed learner artifacts, logs, and evidence templates
```

---

## The Core Curriculum Arcs

* **Arc 0: The Shift to Staff Level & Leverage Mindset** (Phases 00–06)
* **Arc 1: Problem Selection, Framing & User Discovery** (Phases 07–10)
* **Arc 2: Product Mindset, Metrics & Empirical Hypotheses** (Phases 11–15)
* **Arc 3: High-Stakes Decision Making & Decision Journals** (Phases 16–18)
* **Arc 4: Technical Strategy & Architecture Leadership** (Phases 19–24)
* **Arc 5: Technical Debt Prioritization & Roadmapping** (Phases 25–30)
* **Arc 6: Project Shaping, Thin Slicing & Milestones** (Phases 31–34)
* **Arc 7: Risk Management, Retiring Risk Early & Pre-Mortems** (Phases 35–38)
* **Arc 8: Stakeholder Mapping, Incentives & Technical Trust** (Phases 39–42)
* **Arc 9: Navigating Conflict, Disagree & Commit, and Escalation** (Phases 43–47)
* **Arc 10: Executive Writing, RFCs & Delivering Bad News** (Phases 48–55)
* **Arc 11: Cross-Functional Partnership & Funnel Thinking** (Phases 56–61)
* **Arc 12: Developer Experience (DevEx) as Product & Paved Roads** (Phases 62–66)
* **Arc 13: Migration Leadership, Adoption & Deprecation** (Phases 67–70)
* **Arc 14: Execution Leadership, Ownership & Automated Guardrails** (Phases 71–76)
* **Arc 15: Mentoring, Sponsorship & Socratic Design Reviews** (Phases 77–82)
* **Arc 16: Incident Leadership & Blameless Systems Postmortems** (Phases 83–89)
* **Arc 17: Reliability Investment, Security Tradeoffs & FinOps** (Phases 90–94)
* **Arc 18: Foundational Case Studies & Ambiguous Executive Asks** (Phases 95–104)
* **Arc 19: Prioritization Frameworks, Cost of Delay & Sequencing** (Phases 105–109)
* **Arc 20: Business Models, Unit Economics & Product Tradeoffs** (Phases 110–116)
* **Arc 21: Systems Thinking, Conway's Law & Org Scalability** (Phases 117–124)
* **Arc 22: Engineering Strategy Artifacts & Annual Planning** (Phases 125–130)
* **Arc 23: Project Rescues, Saying No & Managing Up** (Phases 131–135)
* **Arc 24: Cross-Functional Partnerships (EM, PM, Design, Data, Sec)** (Phases 136–141)
* **Arc 25: Time Management, Attention Allocation & Personal OS** (Phases 142–147)
* **Arc 26: Career Growth, Impact Narratives & Staff Archetypes** (Phases 148–156)
* **Arc 27: Spikes, Prototypes & Uncertainty Mapping** (Phases 157–161)
* **Arc 28: Ethics, Privacy by Design & Leading Under Uncertainty** (Phases 162–167)
* **Arc 29: Constructive Feedback, Difficult Conversations & Safety** (Phases 168–172)
* **Arc 30: Multi-Dimensional Tradeoff Simulations** (Phases 173–176)
* **Arc 31: Professional Writing Drills & Decision Sets** (Phases 177–181)
* **Arc 32: 13 Substantial Staff-Level Programs & Projects** (Phases 182–194)
* **Arc 33: 5 Deep Capstones & The Final Staff-Level Challenge** (Phases 195–200)

---

## How to Begin Lesson 01

Start with [Phase 00: What Changes at Staff Level?](phases/phase-00-what-changes-at-staff-level/README.md) and [Phase 01: Output vs. Outcome](phases/phase-01-output-vs-outcome/README.md).

```bash
# 1. Review the first lesson situation and prompt
cat phases/phase-01-output-vs-outcome/README.md

# 2. Complete the Output vs. Outcome Conversion Exercise
# Transform 20 common technical tasks into verifiable user/business outcome statements

# 3. Fill out your first Evidence Log
cp outputs/evidence-template.md outputs/evidence-phase-01.md
```

---

## License

This repository is open source under the [MIT License](LICENSE).
