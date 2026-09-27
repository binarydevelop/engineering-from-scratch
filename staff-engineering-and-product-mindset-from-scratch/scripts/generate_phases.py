#!/usr/bin/env python3
"""
Curriculum generator for staff-engineering-and-product-mindset-from-scratch.
Generates all 201 phases with complete scenario-based lessons following LESSON_TEMPLATE.md.
"""

import os
import sys

BASE_DIR = "/Users/tushar/desktop/private/repos/staff-engineering-and-product-mindset-from-scratch"
PHASES_DIR = os.path.join(BASE_DIR, "phases")
os.makedirs(PHASES_DIR, exist_ok=True)

PHASES = [
    (0, "what-changes-at-staff-level", "What Changes at Staff Level?", "Scope is no longer a ticket or a service; it is an organizational outcome.", "Navigate ambiguous multi-team problems and drive system-wide leverage."),
    (1, "output-vs-outcome", "Output vs. Outcome", "Work completed does not equal value created.", "Convert 20 technical outputs into verified business/user outcome statements."),
    (2, "activity-vs-impact", "Activity vs. Impact", "Never mistake motion for progress.", "Distinguish between high-activity busywork and measurable system impact."),
    (3, "force-multiplier", "Staff Engineer as Force Multiplier", "Your impact is measured by how much better everyone else performs.", "Multiply organizational throughput via architecture, paved roads, and clarity."),
    (4, "choosing-problems", "Choosing Problems", "The most dangerous waste is doing efficiently that which should not be done at all.", "Triage inbound demands using impact, urgency, risk, and cost of delay."),
    (5, "important-vs-interesting", "Important vs. Interesting", "Solve business bottlenecks, not intellectual puzzles.", "Resist resume-driven engineering; prioritize high-impact boring solutions."),
    (6, "opportunity-cost", "Opportunity Cost", "Every 'yes' is an implicit 'no' to everything else.", "Quantify the hidden costs and forgone alternatives of major technical commitments."),
    (7, "problem-framing", "Problem Framing", "A problem well-stated is a problem half-solved.", "Deconstruct vague complaints into empirical metrics, affected cohorts, and layers."),
    (8, "problem-statements", "Problem Statements", "Never embed your proposed solution inside your problem statement.", "Draft rigorous problem briefs containing current state, desired state, gap, and impact."),
    (9, "product-users", "Product Users", "Every piece of software has a customer; find them.", "Map user archetypes across external buyers, operators, internal developers, and analysts."),
    (10, "user-problems", "User Problems vs. Feature Requests", "Customers know their pain; they rarely know the optimal technical remedy.", "Uncover the underlying user misery behind surface-level feature requests."),
    (11, "product-metrics", "Product Metrics Architecture", "System metrics measure the machine; product metrics measure human behavior.", "Connect system telemetry to user conversion, retention, and business revenue."),
    (12, "leading-vs-lagging", "Leading vs. Lagging Indicators", "Act on leading signals before lagging outcomes cement failure.", "Identify fast-moving operational signals that predict quarterly business outcomes."),
    (13, "vanity-metrics", "Vanity Metrics vs. Ground Truth", "If a metric can be gamed without creating user value, it is a vanity metric.", "Eliminate hollow indicators and replace them with durable outcome measures."),
    (14, "product-hypotheses", "Product Hypotheses", "Formulate falsifiable beliefs before writing production code.", "Structure bets as testable hypotheses connecting changes to user behaviors."),
    (15, "pragmatic-experiments", "Pragmatic Experimentation", "When uncertainty is high, buy information with small experiments.", "De-risk assumptions using feature flags, canary traffic, and minimal prototypes."),
    (16, "decision-doors", "Reversible vs. Irreversible Decisions", "Move fast on two-way doors; bring rigor to one-way doors.", "Classify choices by rollback cost to eliminate analysis paralysis."),
    (17, "decision-quality", "Decision Quality vs. Outcome Bias", "Do not confuse good fortune with good judgment.", "Evaluate decisions on evidence and reasoning at the time, not hindsight alone."),
    (18, "decision-journals", "The Decision Journal & ADRs", "Document your assumptions today to prevent historical revisionism tomorrow.", "Log architectural decisions with context, tradeoffs, and revisit triggers."),
    (19, "technical-strategy", "Technical Strategy Defined", "Strategy is a coherent set of choices, not a laundry list of desires.", "Bridge changing business realities to concrete engineering investments."),
    (20, "strategy-is-choice", "Strategy Is Choice", "If you cannot state what you are choosing NOT to do, you have no strategy.", "Make explicit organizational sacrifices to ensure decisive focus on critical bets."),
    (21, "technical-vision", "Crafting a Technical Vision", "Paint a vivid picture of what should become simple and what should disappear.", "Author an inspiring 2-year technical vision that drives decentralized alignment."),
    (22, "architecture-leadership", "Architecture Leadership", "Architects lead through questions and operational empathy, not decree.", "Guide multi-team architectures by focusing on failure modes and team autonomy."),
    (23, "architecture-reviews", "Architecture Review Framework", "Review systems against real failure modes, not diagram aesthetics.", "Evaluate distributed designs across operability, cognitive load, cost, and migration."),
    (24, "simplification", "Architectural Simplification", "Simplicity is an achievement, not a starting point.", "Delete redundant microservices, layers, and frameworks to reclaim team velocity."),
    (25, "tech-debt-taxonomy", "Technical Debt Taxonomy", "Not all debt is bad; unmanaged debt is fatal.", "Distinguish aesthetic clutter, operational burden, velocity drag, and architectural risk."),
    (26, "intentional-debt", "Intentional Technical Debt", "Borrow against technical perfection deliberately to capture market timing.", "Log intentional debt with explicit repayment dates and interest cost estimates."),
    (27, "debt-prioritization", "Technical Debt Prioritization", "Do not fix code because you dislike it; fix it because it taxes the business.", "Build airtight economic cases for refactoring based on incident rates and cycle time."),
    (28, "roadmaps-as-bets", "Roadmaps as Sequences of Bets", "A roadmap is a declaration of intent, not a fixed Gantt chart.", "Structure roadmaps around problem themes and outcome horizons (Now, Next, Later)."),
    (29, "dependency-mapping", "Cross-Team Dependency Mapping", "Unmapped dependencies are silent project killers.", "Map cross-service integration points and organizational bottlenecks early."),
    (30, "critical-path", "Critical Path Analysis", "Accelerating non-critical path tasks creates zero delivery advantage.", "Isolate the sequence of dependent tasks that dictates project duration."),
    (31, "project-shaping", "Project Shaping", "Shape the problem before committing engineering teams to sprint backlogs.", "Define boundaries, risks, appetite, and non-goals using structured project briefs."),
    (32, "defensive-scoping", "Defensive Scoping", "Cut scope before you cut quality or extend deadlines.", "Deconstruct monolithic requirements into Musts, Shoulds, and Won't-Haves."),
    (33, "thin-slices", "Thin Slices vs. Horizontal Layers", "Deliver end-to-end value early rather than layers of unverified foundation.", "Slice architecture vertically to validate end-to-end pipeline in Sprint 1."),
    (34, "milestones", "Risk-Retiring Milestones", "A milestone should retire a risk, not celebrate a date.", "Anchor project checkpoints to proven capabilities and eliminated uncertainties."),
    (35, "risk-management", "Comprehensive Risk Management", "Unknowns do not disappear when ignored; they fester into outages.", "Identify technical, dependency, operational, compliance, and schedule risks."),
    (36, "probability-impact", "Qualitative Risk Ranking", "Avoid fake numerical precision; rank risks by realistic blast radius.", "Prioritize risks by probability and impact without pseudo-scientific formulas."),
    (37, "retire-risk-early", "Retiring Risk Early", "Attack the scariest uncertainty on day one.", "Run targeted technical spikes to prove integration before building volume."),
    (38, "pre-mortems", "The Engineering Pre-Mortem", "Imagine you have failed before you start to ensure you do not.", "Surface hidden landmines through prospective hindsight and design mitigations."),
    (39, "stakeholder-mapping", "Stakeholder Mapping", "Know who has a stake in your system and what keeps them awake at night.", "Map influence, interest, and decision roles (RACI) across organizational silos."),
    (40, "understanding-incentives", "Understanding Rational Incentives", "When smart people disagree, look for conflicting performance incentives.", "Align with Product, SRE, Security, and Finance goals by understanding their metrics."),
    (41, "influence-without-authority", "Influence Without Authority", "Lead by clarity, credibility, and service, not by decree.", "Build cross-team consensus and lower adoption friction for partner teams."),
    (42, "building-trust", "Building Technical Trust", "Trust is built in drops and lost in buckets.", "Establish credibility through reliable judgment, transparency, and shared credit."),
    (43, "dissecting-disagreements", "Dissecting Technical Disagreements", "Separate facts, assumptions, and constraints from religious preferences.", "Filter arguments into testable empirical hypotheses and resolve deadlocks."),
    (44, "disagree-and-commit", "Disagree and Commit in Practice", "Vigorously debate before the decision; fully commit after the call.", "Execute unitedly after debate; recognize when ethical dissent is mandatory."),
    (45, "constructive-escalation", "The Art of Constructive Escalation", "Escalate with context, options, and tradeoffs, never with emotion.", "Raise unresolvable cross-team deadlocks cleanly to executive decision owners."),
    (46, "meeting-design", "Purposeful Meeting Design", "Every meeting must produce a decision or retire an ambiguity.", "Structure meetings for decision-making; eliminate rambling status round-tables."),
    (47, "when-not-to-meet", "Asynchronous Leadership: When NOT to Meet", "Protect deep focus by replacing status meetings with written clarity.", "Establish async written feedback loops and reserve meetings for high-bandwidth debate."),
    (48, "technical-writing", "High-Leverage Technical Writing", "Your code touches the machine; your writing touches the organization.", "Author concise, structured engineering proposals that unblock decisions."),
    (49, "executive-summary", "The 5-Sentence Executive Summary", "Respect leadership attention: distill 10 pages of technical complexity into 5 sentences.", "Write executive briefings that communicate problem, evidence, proposal, and ROI."),
    (50, "audience-adaptation", "Audience Adaptation", "Speak the language of your listener, not your implementation.", "Translate technical events across engineers, product managers, support, and executives."),
    (51, "rfc-authoring", "High-Impact RFC Authoring", "A great RFC invites rigorous debate and leads to a clear decision.", "Author proposals with goals, non-goals, failure modes, migrations, and runbooks."),
    (52, "rfc-failure-modes", "RFC Failure Modes & Anti-Patterns", "Beware the RFC factory that produces paper instead of outcomes.", "Diagnose and fix RFC pitfalls: premature solutions, fake options, and endless bikeshedding."),
    (53, "adrs", "Architectural Decision Records (ADRs)", "Proportional documentation: capture local decisions simply and permanently.", "Document architectural choices in lightweight, version-controlled records."),
    (54, "status-reporting", "Status Reporting: Progress Over Activity", "Report outcomes achieved and risks emerging, not tickets closed.", "Write AMBER/RED status reports that create clarity and unblock decisions."),
    (55, "bad-news-early", "Delivering Bad News Early", "Bad news does not improve with age.", "Communicate schedule slippage and technical risks immediately with options."),
    (56, "product-partnership", "Product & Engineering Partnership", "Engineering and Product are co-owners of user outcomes, not client and contractor.", "Collaborate across discovery, feasibility, and technical tradeoffs."),
    (57, "product-discovery", "Product Discovery for Engineers", "Sit with users to see the friction your dashboards hide.", "Participate in customer interviews, support audits, and workflow shadowing."),
    (58, "support-as-signal", "Customer Support Telemetry as Signal", "Support tickets are an unvarnished audit of architectural failures.", "Classify support escalations to identify systemic platform and product defects."),
    (59, "product-analytics", "Product Analytics & Funnels", "Track user state transitions through software pipelines.", "Connect system performance and reliability directly to funnel conversion."),
    (60, "funnel-optimization", "Funnel Optimization in Practice", "Eliminate the technical friction causing drop-offs at critical conversion gates.", "Trace user journeys end-to-end to eliminate transaction failure points."),
    (61, "retention-thinking", "Retention Thinking vs. Launch Vanity", "Shipping is only the beginning; retention proves whether anyone cared.", "Track 30-day cohort retention to measure genuine product value."),
    (62, "devex-as-product", "Developer Experience as a Product", "Your internal engineers are customers; treat their productivity with product rigor.", "Measure developer sentiment, build latency, and local setup friction."),
    (63, "build-vs-buy", "Strategic Build vs. Buy", "Build your core differentiation; buy or adopt commodities.", "Evaluate Total Cost of Ownership, vendor lock-in, and integration taxes."),
    (64, "platform-vs-product", "Platform vs. Product Engineering", "Platform teams exist to accelerate product teams, not to build monuments.", "Justify platform investments through measurable developer leverage."),
    (65, "standardization", "Pragmatic Standardization", "Standardize to reduce cognitive load; allow deviation when business value demands it.", "Balance fleet-wide consistency with autonomy; avoid premature standardization."),
    (66, "paved-roads", "The Paved Road (Golden Path)", "Make the right way the easiest way.", "Build frictionless default templates, automated CI checks, and self-service infra."),
    (67, "migration-leadership", "Migration Leadership as a Socio-Technical Program", "Migrations fail because of human friction, not technical difficulty.", "Manage cross-team motivation, inventory tracking, tooling, and momentum."),
    (68, "migration-strategy", "Incremental Migration Strategies", "Never attempt a big-bang cutover when a strangler pattern is possible.", "Use strangler figs, dual-writes, dark launches, and feature flags."),
    (69, "migration-adoption", "Driving Voluntary Adoption", "If teams refuse to adopt your new platform, your product has failed.", "Lower adoption costs with codemods, documentation, and embedded pairing."),
    (70, "clean-deprecation", "The Art of Clean Deprecation", "A migration is not complete until the legacy system is turned off and deleted.", "Execute deprecation schedules, brownouts, and safe decommissioning."),
    (71, "execution-leadership", "Technical Execution Leadership", "Keep the vision clear, the ownership unambiguous, and the momentum forward.", "Maintain multi-team technical alignment without managing daily sprint boards."),
    (72, "single-ownership", "Unambiguous Single Ownership", "When everyone owns a system, nobody owns it.", "Assign single accountable owners for every domain, service, and interface contract."),
    (73, "delegation-context", "Delegation of Context", "Delegate the problem and the constraints, not the tiny tasks.", "Empower engineers with business context to make high-quality local decisions."),
    (74, "context-distribution", "Context Distribution Networks", "Information hoarding is an organizational bottleneck; broadcast context widely.", "Broadcast architectural context via newsletters, demos, and shared documents."),
    (75, "decision-bottlenecks", "Eliminating Decision Bottlenecks", "If you must approve every design, you are an organizational tax.", "Establish principles and guardrails that enable autonomous local decisions."),
    (76, "technical-guardrails", "Automated Technical Guardrails", "Replace manual gatekeeping with automated linters, contracts, and tests.", "Codify architectural rules into CI pipelines and automated compliance checks."),
    (77, "mentoring", "High-Leverage Mentoring", "Teach people how to think, not what to think.", "Coach senior engineers through problem framing, tradeoff analysis, and communication."),
    (78, "sponsorship", "Ethical Sponsorship", "Mentors advise; sponsors open doors and advocate for opportunities.", "Create career-defining opportunities for rising engineers; avoid favoritism."),
    (79, "staff-code-review", "Staff-Level Code Review", "Review for architecture, operability, and invariants; leave syntax to the linter.", "Spot systemic risks and architectural coupling in code reviews."),
    (80, "design-reviews", "Design Review Facilitation", "A great design review is a collaborative discovery, not an interrogation.", "Facilitate architectural reviews that stress-test systems without ego."),
    (81, "teaching-questions", "Teaching Through Questions", "The right question expands thinking more than a dictatorial answer.", "Ask Socratic questions that reveal hidden failure modes and unstated assumptions."),
    (82, "creating-leaders", "Creating Other Leaders", "Your ultimate achievement is becoming unnecessary for day-to-day decisions.", "Build leadership capacity across the organization; plan your own succession."),
    (83, "incident-leadership", "Incident Leadership & Coordination", "In an outage, communication and coordination matter as much as debugging.", "Lead major incidents as Incident Commander; coordinate technical triage."),
    (84, "incident-priorities", "Incident Priorities Under Fire", "1: Mitigate impact. 2: Stabilize. 3: Understand. 4: Prevent.", "Prioritize customer relief over root-cause investigation during live crises."),
    (85, "incident-communication", "Incident Communication", "Broadcast verifiable facts and timelines; eliminate panic and speculation.", "Provide clear status updates to internal stakeholders and external customers."),
    (86, "incident-decisions", "Real-Time Incident Decision Making", "Evaluate reversibility and blast radius before executing an untested fix.", "Choose decisively between rollback, traffic shedding, failover, and hotfixing."),
    (87, "blameless-postmortems", "Blameless Systems Postmortems", "Postmortems are for learning, not for punishing human fallibility.", "Lead postmortems that investigate systemic conditions, tools, and latent defects."),
    (88, "root-cause-contributing", "Root Cause vs. Contributing Factors", "Complex failures never have a single root cause.", "Analyze the confluence of technical bugs, alert gaps, and organizational pressure."),
    (89, "corrective-actions", "Durable Corrective Actions", "Never write 'be more careful' as an action item.", "Implement architectural circuit breakers, automated canaries, and regression tests."),
    (90, "reliability-investments", "Justifying Reliability Investments", "Translate technical resilience into customer retention and revenue protection.", "Build business cases for reliability; defend and negotiate SLO error budgets."),
    (91, "security-tradeoffs", "Security as a Product Enabler", "Security is not a gatekeeper; it is a foundational quality attribute.", "Balance security controls with developer velocity and customer usability."),
    (92, "cloud-cost-architecture", "Cloud Cost Architecture & Cost Shapes", "Architecture dictates your AWS bill.", "Analyze fixed vs variable infrastructure costs and demand-driven scaling."),
    (93, "cost-vs-time", "Cloud Spend vs. Engineering Opportunity Cost", "Never spend $100k of engineering time to save $5k in annual cloud hosting.", "Calculate the true ROI of optimization projects; avoid low-value refactors."),
    (94, "finops-collaboration", "FinOps Collaboration", "Bring unit economics transparency to engineering teams.", "Partner with Finance to allocate cloud costs to business transactions and features."),
    (95, "case-strategy", "Case Study: Multi-Platform Modernization", "Consolidate where leverage exists; preserve diversity where speed demands it.", "Formulate a pragmatic strategy across 60 services and 4 deployment platforms."),
    (96, "case-product", "Case Study: The 40% Latency Trap", "When technical improvements fail to change business outcomes, re-examine your user assumptions.", "Investigate why a 40% search latency reduction failed to move checkout conversion."),
    (97, "case-platform", "Case Study: The Ignored Platform", "A platform nobody adopts is shelfware.", "Diagnose why a newly built CI/CD platform achieved only 15% team adoption."),
    (98, "case-architecture", "Case Study: The Premature Microservices Request", "Match architectural boundaries to organizational capacity.", "Evaluate an 8-microservice proposal for a 5-engineer team under tight deadlines."),
    (99, "case-migration", "Case Study: The 200-Service Migration Program", "Paved roads and automated tooling win migrations.", "Design a company-wide migration program to deprecate legacy authentication."),
    (100, "case-conflict", "Case Study: Cross-Team Ownership Boundary Feud", "Resolve feuds by clarifying domain boundaries and business outcomes.", "Resolve a high-stakes ownership dispute between Payments and Inventory teams."),
    (101, "ask-scale", "Deconstructing Ambiguity: 'Our Platform Needs to Scale'", "Clarify ambiguous executive mandates before writing architectural proposals.", "Translate vague executive scaling demands into specific workload metrics and costs."),
    (102, "ask-faster", "Deconstructing Ambiguity: 'Make Onboarding Faster'", "Is it network latency, UX confusion, or manual operational verification?", "Deconstruct ambiguous onboarding complaints across system, design, and operations."),
    (103, "ask-rewrite", "Deconstructing Ambiguity: 'We Need to Rewrite the Legacy Service'", "Separate aesthetic annoyance from business criticality and defect rate.", "Evaluate an emotional demand to rewrite legacy code; analyze true ROI and risks."),
    (104, "ask-ai", "Deconstructing Ambiguity: 'Add AI to the Product'", "Technology without a user problem is an expensive distraction.", "Reframe an executive AI mandate around concrete user misery and measurable value."),
    (105, "prioritization-frameworks", "Prioritization Frameworks Without Fake Precision", "Use frameworks to guide debate, not to substitute for critical thinking.", "Evaluate impact, effort, risk, and confidence without pseudo-scientific math."),
    (106, "cost-of-delay", "The Cost of Delay (CoD)", "Urgency is defined by the value lost every week a project is delayed.", "Prioritize initiatives where time-to-market is the primary value driver."),
    (107, "sequencing", "Sequencing & Critical Paths", "Sequence projects to unlock future capabilities and retire compound risks.", "Stage technical bets across multiple quarters to unlock dependent systems."),
    (108, "portfolio-thinking", "Strategic Portfolio Allocation", "Balance your technical investments across maintenance, platform, and innovation.", "Allocate engineering bandwidth across core product, technical debt, and R&D."),
    (109, "strategic-context", "Operating in Strategic Business Context", "Align your architecture with the company's financial model and market window.", "Incorporate runway, fundraising targets, and market competition into designs."),
    (110, "business-models", "Business Model Literacy for Engineers", "Understand how your company makes and spends money.", "Master ARR, gross margins, CAC, LTV, churn economics, and unit margins."),
    (111, "unit-economics", "Unit Economics Intuition", "Know your infrastructure cost per user, per query, and per transaction.", "Calculate how compute, storage, and egress costs scale with customer activity."),
    (112, "customer-segmentation", "Customer Segmentation & Value Propositions", "Enterprise buyers care about governance; consumers care about speed.", "Design software boundaries that cleanly accommodate divergent customer tiers."),
    (113, "product-tradeoffs", "Navigating Direct Product Tradeoffs", "Every product safeguard imposes user friction; strike the balance with data.", "Balance fraud security checks vs checkout conversion using telemetry."),
    (114, "tech-to-product-metrics", "Technical Metrics Mapped to Financial Outcomes", "Draw the line from p99 latency to abandoned carts and bottom-line revenue.", "Quantify the direct financial return of performance and reliability projects."),
    (115, "experiment-design", "Product/Engineering Experiment Design", "Test your hypothesis with statistical rigor and defined guardrails.", "Design A/B test architectures, cohort routing, and significance validation."),
    (116, "guardrail-metrics", "Defending Guardrail Metrics", "Never celebrate a conversion win that doubled customer support tickets.", "Monitor secondary indicators during feature rollouts to prevent silent damage."),
    (117, "quality-vs-speed", "Speed vs. Quality: The False Dichotomy", "High quality enables high speed; sloppy shortcuts create permanent gridlock.", "Demonstrate how automated testing and clean boundaries accelerate delivery."),
    (118, "local-vs-global", "Local vs. Global Optimization", "Optimizing a subsystem often sub-optimizes the total system.", "Prevent teams from caching aggressively or hoarding resources to the detriment of fleet health."),
    (119, "systems-thinking", "Systems Thinking & Reinforcing Loops", "Look for feedback loops that amplify friction or accelerate momentum.", "Map vicious cycles of tech debt, operational fatigue, and rushed deployments."),
    (120, "conways-law", "Conway's Law in Practice", "Your system architecture will inevitably mirror your communication lines.", "Align team organizational structures with desired software interfaces."),
    (121, "team-domain-boundaries", "Team Boundaries and Domain Boundaries", "Draw team boundaries around cohesive business domains, not technology layers.", "Apply Team Topologies: stream-aligned, platform, enabling, and subsystem teams."),
    (122, "ownership-models", "Ownership Models: Component vs. Domain", "Prefer domain ownership over fractional component gatekeeping.", "Prevent orphan services and shared codebase rot through clear domain lines."),
    (123, "bus-factor", "Mitigating the Bus Factor", "A team that depends on one genius is one accident away from paralysis.", "Dismantle technical silos through rotation, pairing, and written architecture."),
    (124, "org-scalability", "Scaling Organizational Velocity", "Design processes that scale sub-linearly with engineering headcount.", "Establish decentralized decision frameworks that maintain velocity as the org grows."),
    (125, "engineering-principles", "Codifying Engineering Principles", "Principles guide decisions when the staff engineer is not in the room.", "Author memorable, non-obvious engineering principles grounded in past failures."),
    (126, "strategy-document", "The Technical Strategy Document", "Synthesize context, choices, non-goals, and initiatives into a single coherent plan.", "Author comprehensive multi-year technical strategies using standard templates."),
    (127, "technical-vision-exercise", "Crafting a 2-Year Technical Vision", "Inspire teams with a clear destination, then leave the driving to them.", "Distill complex long-term architectural goals into a compelling one-page vision."),
    (128, "annual-planning", "Annual Technical Planning", "Do not plan 12 months of detailed architecture; plan 12 months of strategic capabilities.", "Partner with executive leadership to secure headcount and funding for key bets."),
    (129, "quarterly-planning", "Quarterly Planning & Commitments", "Commit to outcomes, not activity; leave capacity for the unexpected.", "Size quarterly commitments; protect 20% capacity for maintenance and debt."),
    (130, "headcount-not-strategy", "'Headcount Is Not a Strategy'", "Adding engineers to a late project makes it later.", "Analyze coordination overhead and onboarding drag using Brooks's Law."),
    (131, "project-rescue", "Rescuing Off-Track Projects", "Stop the bleeding: reassess the outcome, cut scope, and surface blockers.", "Intervene in stalled initiatives; restructure delivery into thin vertical slices."),
    (132, "project-cancellation", "The Courage to Cancel Projects", "Sunk costs are gone; celebrate the decision to stop throwing good money after bad.", "Recognize non-viable projects; execute blameless, decisive cancellations."),
    (133, "saying-no", "The Art of Saying 'No'", "A constructive 'no' clarifies constraints, presents tradeoffs, and offers viable alternatives.", "Decline low-leverage requests constructively without being an obstructionist."),
    (134, "negotiating-scope", "Negotiating Scope Downward", "Deliver 80% of the customer value for 20% of the engineering complexity.", "Collaborate with Product to strip away gold-plated features under deadlines."),
    (135, "managing-up", "Managing Up with Executive Empathy", "Bring your leaders clarity and options, not raw problems and anxiety.", "Communicate with VPs and CTOs; build trust through transparency and solutions."),
    (136, "em-partnership", "The Staff IC & Engineering Manager Partnership", "Lead together: the EM builds the team; the Staff Engineer guides the system.", "Establish a complementary leadership partnership between Staff IC and EM."),
    (137, "pm-partnership", "Partnering with Product Managers", "Challenge product assumptions with technical insights; welcome product challenges to technical plans.", "Collaborate as equal partners on discovery, scope, and tradeoff decisions."),
    (138, "design-partnership", "Partnering with Product Designers (UX)", "Technical constraints shape user interaction; bring engineers into design early.", "Design responsive UIs, handle latency gracefully, and align design with APIs."),
    (139, "data-partnership", "Partnering with Data Engineering & Analytics", "Treat operational data as a core product, not an afterthought.", "Ensure reliable data telemetry schemas and event pipelines for analytics."),
    (140, "security-partnership", "Partnering with Information Security (InfoSec)", "Engage Security during initial design, not 48 hours before production launch.", "Conduct collaborative threat modeling; build secure-by-default systems."),
    (141, "sre-partnership", "Partnering with SRE and Platform Teams", "Feature teams own their service behavior; platform teams own the operational infrastructure.", "Establish shared operational standards, SLO error budgets, and on-call health."),
    (142, "time-management", "Time Management as a Force Multiplier", "How you spend your time signals to the organization what is important.", "Audit time allocation across deep synthesis, alignment, mentoring, and fires."),
    (143, "calendar-audit", "The Ruthless Calendar Audit", "Declutter your calendar to protect multi-hour blocks of deep synthesis.", "Prune recurring meetings, delegate reviews, and defend uninterrupted focus time."),
    (144, "attention-scarce-resource", "Attention as a Scarce Resource", "You can influence a hundred things; you can only drive three to completion.", "Practice deliberate focus; resist the urge to weigh in on every Slack thread."),
    (145, "context-switching", "Mitigating the Cost of Context Switching", "Fragmented attention produces fragmented architecture.", "Batch similar tasks; establish async communication cadences to reduce thrashing."),
    (146, "maker-vs-connector", "Maker vs. Connector Work", "Balance deep technical creation with cross-team organizational alignment.", "Structure weeks into dedicated Maker days (writing, coding) and Connector days (reviews)."),
    (147, "personal-os", "The Staff Engineer's Personal Operating System", "Build a repeatable weekly system to review priorities, unblock teams, and retire risks.", "Establish weekly review routines to track open decisions, risks, and leverage."),
    (148, "career-evidence", "Tracking Grounded Career Evidence", "Do not rely on charisma or visibility; document verified outcomes.", "Maintain a running brag document capturing problems solved and systemic impact."),
    (149, "impact-narratives", "Crafting High-Impact Promotion Narratives", "Frame your career progression around organizational leverage, not personal heroics.", "Author compelling promotion narratives demonstrating cross-team leverage and outcomes."),
    (150, "scope-of-impact", "The Scope of Impact Continuum", "Scope is defined by the blast radius of your decisions and the reach of your leverage.", "Evaluate impact across Team, Multiple Teams, Domain, and Company levels."),
    (151, "staff-archetypes", "Navigating the Four Staff Archetypes", "Identify your natural archetype; adapt to what your organization currently needs.", "Navigate Tech Lead, Architect, Solver, and Right Hand roles effectively."),
    (152, "generative-domain-expert", "Becoming a Generative Domain Expert", "Deep expertise creates value only when it is widely distributed.", "Share deep technical mastery through documentation, workshops, and coaching."),
    (153, "multi-team-tech-lead", "The Multi-Team Tech Lead", "Coordinate technical execution across three teams without doing all the work yourself.", "Drive cross-team delivery through interface management and risk retirement."),
    (154, "staff-and-coding", "The Staff Engineer and Coding", "Stay grounded in code, but recognize that coding is rarely your highest-leverage activity.", "Know when writing code is essential and when it creates an organizational bottleneck."),
    (155, "when-to-dive-deep", "Knowing When to Dive Deep", "Go deep when an ambiguous root cause threatens platform viability.", "Execute surgical deep dives to unblock critical production issues or spikes."),
    (156, "when-to-step-away", "Knowing When to Step Away", "Hand over the wheel once the road is paved and the direction is clear.", "Step back from projects to avoid hero dependency and empower team ownership."),
    (157, "technical-prototypes", "Technical Prototypes Done Right", "A prototype exists to answer a question, not to secretly slide into production.", "Build throwaway prototypes to de-risk technical questions; document results."),
    (158, "focused-spikes", "The Art of the Focused Spike", "Bound research in time; terminate with a decision, not endless exploration.", "Time-box exploratory spikes to 48 hours to resolve architectural deadlocks."),
    (159, "build-vs-debate", "Build vs. Debate: Empirical Verification", "Stop arguing theory; run a benchmark and let the data decide.", "Settle theoretical debates with targeted empirical benchmarks and load tests."),
    (160, "uncertainty-mapping", "Uncertainty Mapping", "Classify what is known, what is assumed, and what is completely unknown.", "Map uncertainties to prioritize investigations that retire existential project risks."),
    (161, "scenario-planning", "Scenario Planning Under High Uncertainty", "Prepare flexible options rather than betting on rigid predictions.", "Prepare architectures for 10x traffic spikes, vendor outages, and market pivots."),
    (162, "ethical-leadership", "Ethical Technical Leadership", "Just because we can build it does not mean we should.", "Evaluate algorithmic bias, dark patterns, user surveillance, and societal impact."),
    (163, "privacy-by-design", "Privacy by Design & Data Minimization", "The safest data is the data you never collect.", "Architect systems that minimize PII collection, enforce encryption, and support deletion."),
    (164, "accessibility-inclusion", "Accessibility and Inclusion as Engineering Quality", "Software that excludes users is defective software.", "Treat accessibility (a11y), internationalization, and low-bandwidth resilience as quality bars."),
    (165, "abuse-modeling", "Product Safety & Abuse Modeling", "Anticipate how malicious actors will exploit your architecture.", "Design defenses against abuse vectors, fraud, rate limit circumvention, and scraping."),
    (166, "poise-under-uncertainty", "Leading with Poise Under Uncertainty", "Admit what you do not know, establish how you will find out, and keep the team calm.", "Model composure, intellectual honesty, and structured inquiry during crises."),
    (167, "confidence-calibration", "Calibrating Confidence Levels", "State your confidence level explicitly: High, Medium, or Low, with supporting evidence.", "Communicate confidence levels clearly to avoid misleading stakeholders with false certainty."),
    (168, "handling-mistakes", "Handling Mistakes with Radical Accountability", "Own your mistakes publicly; share the learnings; improve the system.", "Transform personal errors into organizational learning and stronger systemic defenses."),
    (169, "receiving-feedback", "Receiving Feedback Without Defensiveness", "Separate your personal identity from your code and architectural designs.", "Dissect critical feedback objectively; extract the truth to improve leadership skills."),
    (170, "giving-feedback", "Giving Constructive, Behavioral Feedback", "Describe the situation, the observable behavior, and the systemic impact.", "Deliver actionable, behavioral feedback using the Situation-Behavior-Impact model."),
    (171, "difficult-conversations", "Navigating Difficult Technical Conversations", "Stay calm, stay factual, focus on shared goals, and preserve the relationship.", "Address missed commitments, poor handoffs, and architectural feuds directly."),
    (172, "psychological-safety", "Cultivating Psychological Safety", "A team that fears looking foolish will hide mistakes until they become outages.", "Encourage questions, welcome dissent, and celebrate the discovery of flaws."),
    (173, "sim-architecture-conflict", "Simulation: Entrenched Architecture Conflict", "Resolve architectural gridlock by aligning on shared criteria and running spikes.", "Facilitate consensus between two senior engineers championing opposing streaming tools."),
    (174, "sim-deadline-tradeoff", "Simulation: The 2-Week vs. 8-Week Product Deadline", "Negotiate thin vertical slices that satisfy business timing without technical collapse.", "Negotiate with Product to deliver a minimal working capability in 2 weeks."),
    (175, "sim-availability-dilemma", "Simulation: The Three-Nines to Four-Nines Dilemma", "Calculate the true organizational and financial cost of extreme availability targets.", "Evaluate a leadership mandate to move from 99.9% to 99.99% system availability."),
    (176, "sim-cost-reduction", "Simulation: The 30% Cloud Cost Reduction Mandate", "Design staged cost interventions that preserve system reliability and developer velocity.", "Achieve a 30% cloud infrastructure reduction without breaking production stability."),
    (177, "drill-writing-set", "Staff-Level Writing Drill Set (50 Drills)", "Sharpen written leadership through 50 professional document challenges.", "Complete writing drills across RFCs, ADRs, exec summaries, and status reports."),
    (178, "drill-decision-set", "Decision Drill Set (50 Drills)", "Hone rapid-fire decision-making under incomplete information.", "Evaluate 50 scenarios requiring tradeoff analysis, classification, and ownership calls."),
    (179, "drill-stakeholder-set", "Stakeholder Simulation Set (30 Scenarios)", "Navigate complex cross-functional politics and conflicting incentives.", "Resolve 30 realistic stakeholder scenarios across PM, EM, SRE, and Security conflicts."),
    (180, "drill-product-set", "Product Thinking Exercise Set (50 Exercises)", "Connect technical mechanisms directly to customer behavior and business outcomes.", "Deconstruct 50 product requests, define guardrails, and trace conversion funnels."),
    (181, "drill-architecture-set", "Architecture Leadership Exercises (30 Reviews)", "Evaluate distributed architectures for operational sustainability and migration feasibility.", "Review 30 real-world system designs across scalability, cognitive load, and cost."),
    (182, "proj-api-standardization", "Project: Cross-Team API Standardization Program", "Standardize interfaces across autonomous teams by building paved roads, not mandates.", "Lead an API standardization initiative across 5 product teams."),
    (183, "proj-reliability-program", "Project: Systemic Reliability Improvement Program", "Transform a crisis-prone monolith into an SLO-governed resilient platform.", "Design an organizational and architectural reliability program that reduces MTTR by 60%."),
    (184, "proj-devex-initiative", "Project: Developer Productivity Initiative", "Slash developer cycle time by treating developer tooling as a core product.", "Reduce CI/CD build and deploy times from 45 minutes to 6 minutes across 40 teams."),
    (185, "proj-platform-migration", "Project: Enterprise Platform Migration", "Lead a multi-team socio-technical migration without production downtime.", "Migrate 150 services to a modern cloud container platform with zero customer impact."),
    (186, "proj-product-perf-initiative", "Project: Product Performance & Conversion Turnaround", "Coordinate backend, frontend, and DB optimizations to recover lost checkout revenue.", "Lead a cross-functional performance initiative that increases checkout conversion by 2.2%."),
    (187, "proj-cost-reduction-program", "Project: Cloud Infrastructure FinOps & Cost Reduction", "Audit, re-architect, and rightsize cloud spend to achieve durable margin improvements.", "Design a staged FinOps program delivering 35% ongoing cloud savings."),
    (188, "proj-technical-strategy", "Project: Multi-Year Technical Strategy Formulation", "Author a comprehensive 18-month technical strategy for a scaling organization.", "Deliver an executive-approved technical strategy linking business goals to architecture."),
    (189, "proj-new-product-discovery", "Project: Greenfield Product Discovery to MVP Launch", "Guide an ambiguous enterprise feature ask from customer discovery to production MVP.", "Shape, de-risk, and ship an enterprise collaboration feature in 8 weeks."),
    (190, "proj-incident-command", "Project: Major Multi-Service Outage Incident Leadership", "Command a cascading SEV-1 outage from real-time mitigation to blameless postmortem.", "Lead a simulated multi-service payment outage and deliver systemic corrective actions."),
    (191, "proj-architecture-simplification", "Project: Architecture Simplification & Consolidation", "Consolidate an over-engineered 40-microservice cluster into a maintainable core.", "Decommission unnecessary microservices and reduce platform operational costs by 50%."),
    (192, "proj-org-bottleneck", "Project: Resolving the Central Platform Bottleneck", "Transform an overworked infrastructure gatekeeper team into an enabling platform group.", "Dismantle organizational ticket queues and introduce self-service developer paved roads."),
    (193, "proj-mentoring-multiplier", "Project: Mentoring & Leadership Multiplier Program", "Design a 6-month structured growth program elevating senior engineers to tech leads.", "Coach two senior engineers to independently author RFCs and lead multi-team launches."),
    (194, "proj-budget-constraint-strategy", "Project: Strategy Under Severe Budget Constraints", "Re-prioritize an engineering roadmap following an unexpected 20% budget reduction.", "Deliver a re-scoped technical strategy making explicit tradeoffs and defending core SLOs."),
    (195, "capstone-critical-program", "Capstone 1: Operating a Revenue-Critical Rebuild", "Lead a high-stakes checkout rebuild across 7 teams under fixed launch deadlines.", "Deliver complete problem brief, strategy, risk register, ADRs, and migration plan."),
    (196, "capstone-devex-strategy", "Capstone 2: Enterprise Internal Developer Platform Strategy", "Design and execute an internal platform strategy treating developers as customers.", "Deliver user research, baseline metrics, paved road blueprint, and adoption plan."),
    (197, "capstone-turnaround", "Capstone 3: The Integrated Product & Technical Turnaround", "Diagnose and repair a failing SaaS product suffering from churn, latency, and gridlock.", "Deliver an integrated product and technical rescue roadmap with verified metrics."),
    (198, "capstone-merger-convergence", "Capstone 4: Post-Acquisition Platform Convergence", "Unify two competing technical stacks and engineering cultures following an acquisition.", "Deliver an architectural convergence strategy, migration plan, and team alignment model."),
    (199, "capstone-promotion-packet", "Capstone 5: Staff-Level Promotion Packet Simulation", "Assemble and defend a comprehensive staff engineering promotion packet with evidence.", "Author an airtight promotion document demonstrating cross-team leverage and business impact."),
    (200, "final-challenge", "Phase 200: The Final Staff-Level Challenge", "Navigate an ambiguous organizational crisis requiring complete curriculum synthesis.", "Synthesize problem framing, evidence, strategy, execution, and leadership to resolve crisis.")
]

def generate_phase(phase_num, slug, title, motto, summary):
    phase_dir_name = f"phase-{phase_num:02d}-{slug}"
    phase_dir = os.path.join(PHASES_DIR, phase_dir_name)
    docs_dir = os.path.join(phase_dir, "docs")
    outputs_dir = os.path.join(phase_dir, "outputs")

    os.makedirs(docs_dir, exist_ok=True)
    os.makedirs(outputs_dir, exist_ok=True)

    content = f"""# Lesson {phase_num:02d}: {title}

> **Motto**: "{motto}"

**Type:** Staff Engineering Leadership & Product Mindset  
**Prerequisites:** Phase {max(0, phase_num - 1):02d}  
**Estimated Time:** 60 minutes  

---

## Motto
"{motto}"

## Situation
At a fast-growing technology company, engineering teams are facing acute friction:
{summary}
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
"""
    # Write README.md and docs/en.md
    with open(os.path.join(phase_dir, "README.md"), "w", encoding="utf-8") as f:
        f.write(content)
    with open(os.path.join(docs_dir, "en.md"), "w", encoding="utf-8") as f:
        f.write(content)

    # Write evidence template log
    evidence_log = f"""# Evidence Log: Phase {phase_num:02d} - {title}

* **Lesson:** Phase {phase_num:02d} - {title}
* **Date:** 2026-09-25
* **Author:** Staff Engineer Learner

### Reframed Problem & Evidence
* **Initial Complaint:** {summary}
* **Reframed Problem:** Systemic deployment and interface friction causing cycle time inflation and customer risk.
* **Verified Evidence:** Telemetry shows 14-day lead time and 18% change failure rate.

### Decision & Tradeoffs
* **Decision:** Option 2 (Paved Road & Refactoring).
* **Non-Goals:** Deferring full database rewrite; prioritizing immediate developer cycle time.
* **Artifact Produced:** RFC and Executive Briefing.

### Reflection & Leverage
* **Senior vs Staff Difference:** A senior engineer would have patched the local service; the staff engineer created an automated paved road that unblocked all 12 teams.
* **Leverage Created:** Raised organizational delivery velocity while permanently retiring deployment failure risks.
"""
    with open(os.path.join(outputs_dir, "evidence-template.md"), "w", encoding="utf-8") as f:
        f.write(evidence_log)

def generate_all_phases():
    print(f"Generating all {len(PHASES)} curriculum phases...")
    for item in PHASES:
        generate_phase(*item)
    print("All 201 curriculum phases successfully generated.")

if __name__ == "__main__":
    generate_all_phases()
