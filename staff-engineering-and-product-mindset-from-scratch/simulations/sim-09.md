# Simulation: The Flaky Alert Storm Paralyzing On-Call Morale

> **Domain:** Reliability  
> **Simulation Type:** Multi-Stage Adaptive Leadership Scenario  

---

## Stage 1: The Initial Trigger & Observable Symptoms
* **Situation:** You are notified of an urgent issue:
* **Initial Telemetry:** Stage 1: 450 pages fire per week; on-call engineers threatening to resign. 
* **Initial Stakeholder Reaction:** Panic and demands for an immediate quick fix or full rewrite.
* **Your Action Required:**
  1. What is your immediate response to stakeholders?
  2. What diagnostic telemetry or logs do you request before taking action?
  3. What is your initial working hypothesis?

---

## Stage 2: Emerging Telemetry & Complications
* **New Evidence Arrives:**  Identifying threshold noise and missing SLO alignment. 
* **Stakeholder Pressure Intensifies:** Product Managers push for a launch date while Operations raises availability alarms.
* **Your Action Required:**
  1. How does this new data alter your initial hypothesis?
  2. What trade-off decision is now unavoidable?
  3. Who owns the decision, and how do you align the dissenting parties?

---

## Stage 3: The Root Revelation & Decision Point
* **The Final Reality:**  Pruning alerts and introducing symptom-based paging.
* **The Dilemma:** You cannot satisfy all constraints simultaneously. You must make a definitive tradeoff.
* **Your Deliverable Required:**
  1. Draft a 1-page Architectural Decision Record (ADR) or Executive Briefing.
  2. Define the non-goals and what scope is intentionally deferred.
  3. Detail the communication plan across Engineering, Product, and Executives.

---

## Expert Debrief & Scoring Rubric
* **Junior/Senior Instinct:** Reacting to Stage 1 symptoms with hasty patches or arguing with stakeholders.
* **Staff-Level Master Class:** Methodically isolating variables, acknowledging uncertainty, protecting team psychological safety, aligning competing incentives, and designing durable systemic defenses.
