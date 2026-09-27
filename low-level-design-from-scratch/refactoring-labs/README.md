# Refactoring Labs Catalog

This directory contains **22 hands-on refactoring labs**. Each lab provides real-world code suffering from acute architectural smells, complete with automated test harnesses, diagnosis guides, and reference clean solutions.

| Lab | Title | Smells Addressed | Target Principle / Pattern |
|:---|:---|:---|:---|
| `lab-01-parking-lot-god-class` | **Deconstructing the Parking Lot God Class** | `God Object, Low Cohesion, High Coupling` | Single Responsibility Principle & Information Expert |
| `lab-02-notification-shotgun-surgery` | **Curing Shotgun Surgery in Notifications** | `Shotgun Surgery, Divergent Change` | Open/Closed Principle & Adapter Pattern |
| `lab-03-order-state-invariants` | **Enforcing Invariants in Order Lifecycle** | `Anemic Domain Model, Leaky State` | Encapsulation & State Invariant Fortress |
| `lab-04-primitive-obsession-money` | **Eliminating Primitive Obsession with Money** | `Primitive Obsession, Data Clumps` | Value Objects & Type-Driven Design |
| `lab-05-boolean-flag-arguments` | **Refactoring Mystery Boolean Flag Arguments** | `Flag Arguments, Cryptic Call Sites` | Explicit Behavioral APIs |
| `lab-06-divergent-change-report` | **Splitting Divergent Change in Report Generator** | `Divergent Change, Mixed Concerns` | Single Responsibility Principle |
| `lab-07-feature-envy-shipping` | **Curing Feature Envy in Shipping Calculator** | `Feature Envy, Inappropriate Intimacy` | Tell, Don't Ask & Information Expert |
| `lab-08-inappropriate-intimacy-wallet` | **Breaking Inappropriate Intimacy in Digital Wallet** | `Inappropriate Intimacy, Encapsulation Leak` | Information Hiding & Loose Coupling |
| `lab-09-rigid-inheritance-birds` | **Refactoring Rigid Inheritance (Fragile Base Class)** | `LSP Violation, Fragile Base Class` | Liskov Substitution Principle & Composition |
| `lab-10-giant-switch-tax-engine` | **Replacing Giant Switch with Polymorphism** | `Giant Switch, Type Code Conditional` | Replace Conditional with Polymorphism (Strategy) |
| `lab-11-tight-coupling-mailer` | **Decoupling Hardcoded Email Dependencies** | `Hardcoded Dependency, Un-testable Code` | Dependency Inversion Principle & Constructor Injection |
| `lab-12-anemic-domain-model-account` | **Re-hydrating an Anemic Domain Model** | `Anemic Domain Model, Procedural OOP` | Rich Domain Modeling & Encapsulation |
| `lab-13-temporal-coupling-parser` | **Eliminating Dangerous Temporal Coupling** | `Temporal Coupling, Hidden Preconditions` | Constructor Completeness & Safe State Machines |
| `lab-14-hidden-clock-dependency` | **Injecting Time as an Explicit Dependency** | `Hidden State, Non-Deterministic Tests` | Explicit Dependencies & Deterministic Testing |
| `lab-15-leaky-abstraction-cart` | **Defending Collections Against Encapsulation Leaks** | `Leaky Encapsulation, State Corruption` | Defensive Copying & Unmodifiable Views |
| `lab-16-singleton-testing-bottleneck` | **Dismantling the Global Singleton Bottleneck** | `Global Mutable State, Flaky Tests` | Dependency Injection over Static Singletons |
| `lab-17-race-condition-inventory` | **Fixing a Critical Multi-Threaded Inventory Race** | `Race Condition, Lost Updates` | Thread Safety & Atomic Invariant Guards |
| `lab-18-violated-demeter-invoice` | **Refactoring Deep Demeter Navigation Violations** | `Law of Demeter Violation, Deep Coupling` | Principle of Least Knowledge |
| `lab-19-unvalidated-constructor-user` | **Securing Constructors Against Invalid Domain Birth** | `Unvalidated Birth, NullPointer Landmines` | Fail-Fast Invariants at Construction |
| `lab-20-speculative-generality-cache` | **Stripping Speculative Generality from Simple Cache** | `Speculative Generality, Pattern Soup` | KISS, YAGNI & Simplicity |
| `lab-21-interface-pollution-worker` | **Segregating Polluted Worker Interfaces** | `Interface Pollution, Fat Interface` | Interface Segregation Principle |
| `lab-22-swallowed-exceptions-payment` | **Eliminating Swallowed Exceptions in Payment Gateway** | `Exception Swallowing, Silent Failures` | Explicit Domain Error Modeling |