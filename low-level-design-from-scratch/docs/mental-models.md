# Mental Models for Low-Level Design

Mastering Low-Level Design is not about memorizing 23 Gang of Four patterns or drawing complex UML boxes. It is about acquiring **first-principles mental models** that allow you to decompose ambiguous real-world problems into clean, testable, and adaptable software systems.

---

## 1. The Core Mental Model: Behavior Before Classes

The most common failure mode in object-oriented design is **immediate noun extraction**:

```text
[Ambiguous Prompt: "Design a Parking Lot"]
  ↓ Beginner's knee-jerk reaction
Classes: ParkingLot, Floor, Spot, Vehicle, Ticket, Gate, Payment
  ↓ (Now staring at blank classes wondering what fields to put in them)
```

### The Professional Flow:
Start with **dynamics and observable behavior**:

```text
1. A Vehicle arrives at an entry gate.
2. The gate senses the vehicle dimensions/type (e.g., Electric, Oversized, Compact).
3. We must query available inventory for a compatible spot.
4. We reserve/occupy that spot atomically to prevent race conditions.
5. We issue a Ticket containing entry timestamp, spot coordinates, and secure hash.
6. The barrier opens.
7. ... later ...
8. The Vehicle arrives at an exit gate.
9. We compute the tariff based on elapsed time, vehicle type, and active pricing rules.
10. Payment is completed.
11. The spot is released back into available inventory.
```

Only after tracing the flow do we ask:
> **"Who should own each responsibility?"**

```text
Who knows spot dimensions?             → The Spot.
Who determines spot compatibility?     → The Spot (or SpotCompatibilityRule).
Who calculates the parking duration?   → The Ticket / TimeRange value object.
Who calculates the fee?                → The PricingStrategy (NOT the ParkingLot).
Who orchestrates entry and exit?       → The ParkingService (Use Case coordinator).
```

Classes are derived **from responsibilities**, not by guessing nouns from English sentences.

---

## 2. The Responsibility Assignment Heuristic (GRASP)

When deciding which class should perform an operation, use the **Information Expert** heuristic:

> **Assign a responsibility to the information expert—the class that has the information necessary to fulfill the responsibility.**

### Example:
Should `ParkingLot` calculate the total bill for an exiting car?
- `ParkingLot` holds floors and spots.
- But `Ticket` holds the `entryTime`, `exitTime`, and `spotType`.
- And `PricingTariff` holds the hourly rates.
- Therefore, having `ParkingLot` do math on tickets creates a **bloated God Object** with low cohesion and high coupling. Pass the `Ticket` to a `PricingPolicy`.

---

## 3. The Invariant Fortress Model

An object is not a passive container of data. An object is a **fortress that protects its invariants**:

```text
                ┌────────────────────────────────┐
                │        Public Contract         │
                │  deposit(Money)                │
                │  withdraw(Money)               │
                └───────────────┬────────────────┘
                                │
                      [Guards Invariants]
                      - Balance >= 0
                      - Currency matches
                      - Transaction limit <= $10,000
                                │
                ┌───────────────▼────────────────┐
                │         Private State          │
                │  balance: Money                │
                │  transactions: List<Txn>       │
                └────────────────────────────────┘
```

If any caller can bypass the rules and put the object into an illegal state (e.g. via public fields or unvalidated setters), **encapsulation has failed**.
- Invariants must be established at construction (`new`).
- Invariants must be preserved across every public method invocation.
- Make invalid states **unrepresentable in the type system** wherever practical.

---

## 4. The Pain-Driven Design Loop

Never introduce an abstraction or pattern speculatively ("just in case"). Introduce abstractions only when **concrete requirements apply design pressure**:

```text
1. Naive Implementation
   - Start with the simplest code that works (even a single class or switch statement).
   - Write automated tests verifying all behavior.

2. A New Requirement Arrives
   - Product manager asks for a new pricing rule, a new channel, or a second payment provider.

3. Feel the Design Pain
   - Notice the code resisting change:
     * Shotgun surgery: modifying 5 files for 1 feature.
     * Giant conditionals: an if/else chain that grows every week.
     * Fragile tests: changing one method breaks 10 unrelated tests.

4. Diagnose the Design Smell
   - Identify the exact smell (e.g., Divergent Change, Feature Envy, Primitive Obsession).

5. Refactor to a Principle / Pattern
   - Introduce Strategy, State, Value Object, or Dependency Injection.
   - Run tests to prove external behavior remained unchanged.
```

---

## 5. The Seams and Boundaries Model

A well-designed low-level system separates **core domain decisions** from **infrastructure and transport mechanisms**:

```text
                  ┌───────────────────────────────┐
                  │      Delivery / Transport     │
                  │   CLI / HTTP Controller       │
                  └───────────────┬───────────────┘
                                  │ (DTOs)
                  ┌───────────────▼───────────────┐
                  │      Application Service      │
                  │  (Use Case Orchestration)     │
                  └───────┬───────────────┬───────┘
                          │               │
             ┌────────────▼──────┐ ┌──────▼────────────┐
             │   Domain Model    │ │  Output Port      │
             │ (Entities, Rules, │ │ (Repository /     │
             │   Value Objects)  │ │  Gateway contract)│
             └───────────────────┘ └──────┬────────────┘
                                          │ implements
                                   ┌──────▼────────────┐
                                   │  Infrastructure   │
                                   │ (Postgres, Stripe)│
                                   └───────────────────┘
```

- The **Domain Model** has zero dependencies on databases, HTTP libraries, or frameworks.
- The **Infrastructure** depends inwards on domain interfaces (Dependency Inversion).
- You can test 100% of domain business logic in memory in milliseconds without touching Docker or a network socket.

---

## 6. The Testability as a Design Diagnostic Model

If an object is painful or awkward to test:
1. **It creates its own dependencies with `new`** → Refactor to Constructor Injection.
2. **It relies on hidden static state** → Refactor to an explicit instance collaborator.
3. **It does too many unrelated things** → Refactor using Single Responsibility Principle.
4. **It calls `Instant.now()` or `UUID.randomUUID()` internally** → Inject a `Clock` or ID generator.

**Test difficulty is an architecture smell, not a test writing problem.**
