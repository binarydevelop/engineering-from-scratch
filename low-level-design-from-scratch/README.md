# Low-Level Design from Scratch

> **Understand it. Model it. Build it. Break it. Refactor it. Test it. Extend it. Ship it.**

---

## What This Repository Is (and Is NOT)

> ⚠️ **This is NOT a design-pattern memorization repository.**  
> ⚠️ **This is NOT a collection of static UML diagrams to glance at before an interview.**  
> ⚠️ **This is a rigorous course in translating ambiguous requirements into maintainable, testable, invariant-protecting software designs.**

When faced with a prompt such as:
```text
"Design a Parking Lot System"
```

Most software engineers immediately shout:
> *"I'll use the Factory Pattern to create spots, the Strategy Pattern for pricing, and the Observer Pattern for the display board!"*

And then they write empty classes with public fields, anemic models, missing invariants, tight coupling, and un-testable monolithic methods.

In this repository, you will learn the true mental discipline of Low-Level Design:

```text
Requirements
     ↓
Use Cases
     ↓
Entities & Value Objects
     ↓
Responsibilities (GRASP Information Expert)
     ↓
Relationships & Invariants
     ↓
Interfaces & Explicit Contracts
     ↓
State Transitions
     ↓
Business Rules & Errors
     ↓
Extensibility Points
     ↓
Implementation
     ↓
Automated Behavioral Tests
     ↓
Requirement Evolution (Design Pressure)
     ↓
Pain-Driven Refactoring
```

**Patterns are never introduced as solutions looking for problems.** Patterns appear only after you have experienced the concrete pain of code resisting change.

---

## Pedagogical Structure

The curriculum spans **147 distinct phases (Phase 00 – Phase 146)**, accompanied by **150+ exercises**, **20+ broken-design refactoring labs**, **20+ complete LLD problem projects**, and **5 capstones**.

```text
low-level-design-from-scratch/
├── README.md               # Repository manifesto and complete guide
├── ROADMAP.md              # 147-phase sequential roadmap
├── LEARNING.md             # How to study, practice, and retain LLD
├── LESSON_TEMPLATE.md      # Canonical template for every lesson
├── VERSIONS.md             # Tooling, Java 21 LTS, and JUnit specs
├── CONTRIBUTING.md         # Guidelines for contributing
├── pom.xml                 # Maven build configuration
│
├── phases/                 # 147 deep-dive phases (Phase 00 to 146)
├── exercises/              # 150+ categorized design drills (solutions separated)
├── katas/                  # Repeatable refactoring & design katas
├── projects/               # 20+ production-grade canonical LLD systems
├── refactoring-labs/       # 20+ hands-on broken designs to fix
├── broken-designs/         # Antipattern case studies & code smells
├── diagrams/               # Class, sequence, and state diagrams (Mermaid & ASCII)
├── docs/                   # Essential theoretical reference guides
│   ├── glossary.md         # Precise terminology definitions
│   ├── mental-models.md    # Cognitive frameworks for object modeling
│   ├── java-for-lld.md     # Minimalist Java reference (no frameworks)
│   ├── design-smells.md    # Catalog of OOP code smells with examples
│   ├── pattern-map.md      # Problem-driven pattern selection matrix
│   └── interview-framework.md # 13-step interview & review framework
└── outputs/                # Student evidence reports & artifacts
```

---

## The 17 Curriculum Tiers

1. **Tier 1: The LLD Lab & First Principles (Phases 00 – 05)**  
   Environment setup, `HelloDomain`, HLD vs LLD, requirements decomposition, use case flows, entities vs behaviors, and responsibility assignment.
2. **Tier 2: Object-Oriented Fundamentals & Domain Modeling (Phases 06 – 11)**  
   Encapsulation, invariant fortresses, Value Objects vs Entities, composition over inheritance, and substitutability.
3. **Tier 3: Behavioral Contracts, Decoupling & Heuristics (Phases 12 – 18)**  
   Interfaces, manual Dependency Injection, cohesion, coupling, information hiding, Tell Don't Ask, and Law of Demeter.
4. **Tier 4: The SOLID Heuristics & Simplicity (Phases 19 – 28)**  
   Pain-driven SRP, OCP, LSP, ISP, and DIP. DRY, KISS, YAGNI, and the complete design smells catalog.
5. **Tier 5: Safe Refactoring Mechanics (Phases 29 – 32)**  
   Extract Method/Class, Replace Conditional with Polymorphism, and Replace Primitive with Value Object.
6. **Tier 6: State, Errors, Collections & Lifecycles (Phases 33 – 41)**  
   FSMs, State Pattern, domain exception hierarchies, null banishment with `Optional`, semantic collection choices, and immutability.
7. **Tier 7: Design Patterns from First Principles (Phases 42 – 55)**  
   Factory Method, Abstract Factory, Builder, Singleton caution, Strategy, Observer, Command, Template Method, Adapter, Facade, Decorator, Proxy, Chain of Responsibility, and Mediator.
8. **Tier 8: Architectural Boundaries & Layering (Phases 56 – 63)**  
   Repositories, Domain Services vs Application Services, 4-layer architecture, Aggregate Roots, Persistence Boundaries, and DTO mapping.
9. **Tier 9: Test-Driven Design & Testability (Phases 64 – 70)**  
   Testing observable behavior, hand-rolled Test Doubles (Fakes, Stubs, Mocks), and writing testable decoupled code.
10. **Tier 10: Real-World Forces: Concurrency, Time & Boundaries (Phases 71 – 80)**  
    Thread safety in domain objects, atomic boundaries, idempotency, time injection (`Clock`), external service adapters, retry policies, and typed configuration.
11. **Tier 11: API Design, Granularity & UML (Phases 81 – 89)**  
    Hard-to-misuse method contracts, eliminating boolean flag parameters, expressive naming, and pragmatic UML (class, sequence, state).
12. **Tier 12: Canonical LLD Interview Problems (Phases 90 – 120)**  
    Full implementations and test suites for 30+ classic systems: Tic-Tac-Toe, Snake and Ladder, Vending Machine, Parking Lot, Elevator, Library, Chess, ATM, Splitwise, Movie Ticket Booking, Hotel, Car Rental, Food Delivery, Ride Sharing, Logger, Cache (LRU/LFU), Rate Limiter, Task Scheduler, Notification Platform, Payment System, Inventory, Shopping Cart, Order Domain, File Storage, In-Memory DB, Message Queue, Pub/Sub, Metrics Library, Feature Flags, and RBAC Access Control.
13. **Tier 13: Refactoring Labs & Advanced Design Skills (Phases 121 – 132)**  
    Hands-on refactoring challenges, characterization testing, concurrency races, database decoupling, pattern restraint, and anti-patterns.
14. **Tier 14: LLD in the Real World & System Design (Phases 133 – 136)**  
    Connecting LLD to relational schemas, HTTP APIs, Domain Events, and High-Level microservice design.
15. **Tier 15: Interview Simulations (Phases 137 – 139)**  
    Simulated 45-minute interviews: handling unseen problems, mid-flight requirement shifts, and late-stage concurrency constraints.
16. **Tier 16: Capstone Projects (Phases 140 – 144)**  
    Multi-stage production projects: Enterprise Parking Platform, Generic Booking Engine, Resilient Notification Platform, E-Commerce Order Domain, and Building a Mini IoC/Event Framework from scratch.
17. **Tier 17: Mastery & Final Challenges (Phases 145 – 146)**  
    25 unseen challenges across beginner, intermediate, and advanced levels, culminating in the autonomous First-Principles Mental Model.

---

## Quickstart: Running Your First Lab

### Prerequisites
- **Java 21 LTS** (`openjdk@21`)
- **Apache Maven 3.9+** (`mvn`)

```bash
# Clone the repository
git clone https://github.com/rohitg00/low-level-design-from-scratch.git
cd low-level-design-from-scratch

# Verify compiler and build
mvn clean test
```

### Running Phase 00 (LLD Lab)
```bash
# Run tests for Phase 00
mvn test -Dtest=HelloDomainTest
```

---

## How to Work Through a Lesson

1. Navigate to the phase: `cd phases/phase-XX-<name>`
2. Read `docs/en.md` to understand the domain problem, use cases, and first principles.
3. Trace the responsibilities table.
4. Inspect the initial design in `src/` and run the tests in `tests/`.
5. Read the **New Requirement** section in `docs/en.md`. Observe how the code resists change.
6. Apply the refactoring to introduce the principle or pattern.
7. Run `mvn test` to verify zero regression.
8. Copy `outputs/evidence-template.md` to `outputs/evidence-<your-initials>.md` and record your reflections.

---

## The Final Standard of Mastery

When you finish this repository, an interviewer or tech lead can hand you an ambiguous prompt like:
```text
"Design an automated locker delivery hub."
```

And you will **never** freeze or wonder:
> *"Which design pattern does the interviewer want me to recite?"*

Instead, you will deliberately reason:
```text
Who are the actors?
  ↓
What are the use case workflows?
  ↓
What invariants must never be violated?
  ↓
What entities and value objects exist?
  ↓
Who should own each responsibility?
  ↓
Where are the boundaries and contracts?
  ↓
What dependencies must be injected?
  ↓
What can vary, and what should stay simple?
  ↓
How do we test every transition?
  ↓
What happens when the next requirement arrives?
```

You will move deliberately from behavior to responsibilities to collaborating objects—and defend why every single line lives where it does.
