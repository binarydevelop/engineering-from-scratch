# How to Learn in This Repository

> **Motto:**  
> **Understand it. Model it. Build it. Break it. Refactor it. Test it. Extend it. Ship it.**

Welcome to **Low-Level Design from Scratch**. This repository is not a textbook to read passively, nor is it a cheat sheet of design pattern class diagrams to memorize before an interview.

It is an active **engineering simulator** designed to rewire how you think about software structure.

---

## The Core Mental Shift

When given a problem like:
```text
"Design an Elevator Control System"
```

### ❌ The Junior Reflex:
1. Immediately write classes: `Elevator`, `Button`, `Floor`, `Motor`, `Door`.
2. Pick a design pattern to force into the design: *"I'll use the State Pattern and Strategy Pattern."*
3. Connect classes with tangled getters, setters, and bidirectional links.
4. Discover that handling edge cases (e.g., emergency stops, multiple cars, load balancing) breaks the entire structure.

### ✅ The Senior Engineering Process:
1. **Clarify Requirements & Boundaries:** What is the elevator's scope? Single elevator or multicar bank? Hall calls vs car calls? Dispatch algorithm requirements?
2. **Trace Behaviors & Use Cases:** What happens when a passenger presses 'UP' on floor 4? What state changes? What must be decided?
3. **Assign Responsibilities:** Who should decide which car moves? (The Dispatcher/Scheduler, not the individual Elevator car). Who protects car status? (The Elevator car).
4. **Define Explicit Contracts:** Interfaces with clear behavioral pre- and post-conditions.
5. **Establish Invariants:** A car cannot move with doors open. A car cannot exceed passenger weight capacity.
6. **Implement Simply:** Write clean code without premature patterns.
7. **Introduce Pressure:** Introduce a new requirement (e.g. fire mode or VIP reservation). Notice where the design resists change.
8. **Refactor Driven by Pain:** Introduce an abstraction only when the resistance to change makes it necessary.

---

## The Standard Learning Loop

Every lesson in this repository guides you through this repeatable loop:

```text
       Requirements Decomposition
                   ↓
         Use Cases & Workflows
                   ↓
      Identify Responsibilities (GRASP)
                   ↓
         Domain & State Modeling
                   ↓
       Initial Simple Implementation
                   ↓
           Automated Testing
                   ↓
    ⚡ NEW REQUIREMENT ARRIVES (Pressure)
                   ↓
       Observe Design Smell & Pain
                   ↓
       Refactor with SOLID / Pattern
                   ↓
        Verify Tests Still Pass
                   ↓
         Fill Evidence Report
```

---

## Golden Rules for Students

1. **Never write a class until you know its responsibilities.** If you cannot describe what a class does without using the word "and" or words like "Manager" and "Helper", stop and decompose it further.
2. **Never apply a design pattern without feeling the pain.** If your code does not already suffer from a giant switch statement or duplicate algorithmic variations, you do not need Strategy. Keep it simple.
3. **Make invalid states unrepresentable.** Leverage types, constructors, and immutability. If an order cannot have a negative price, `Money` must reject it at birth.
4. **Treat testability as your architectural compass.** If an object is painful to test without heavy mocking frameworks, its design is flawed. Decouple its dependencies via constructor injection.
5. **Re-implement without notes.** After finishing a lesson, close the repository, open a blank editor, and rebuild the domain model from requirements from memory. If you stumble, revisit the responsibilities.
