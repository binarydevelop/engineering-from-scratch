# The Problem-Driven Pattern Map

> **Rule #1 of Design Patterns:**  
> **Patterns are solutions to specific design pain points. If you do not feel the pain, do NOT apply the pattern.**

Do not begin an interview or design session by announcing: *"I will use the Factory and Observer patterns here."* Begin by identifying the varying behaviors, invariants, and responsibilities.

---

## The Decision Matrix: Map the Pain to the Solution

| What Pain Are You Experiencing? | Root Cause | Candidate Pattern | When NOT to Use (Simpler Alternative) |
|:---|:---|:---|:---|
| **Multiple algorithmic variations or tariffs are cluttered in giant if/else or switch statements.** | Behavior varies independently from the object using it. | **Strategy** | If there are only 2 static variants that will never change, a simple `if` condition is clearer and requires fewer classes. |
| **Object construction requires 7+ parameters, many optional, leading to confusing telescoping constructors.** | Complex object assembly; constructor ambiguity. | **Builder** | If the object has only 2-3 fields, a standard public constructor or factory method is cleaner. |
| **Callers need to instantiate objects without coupling to concrete runtime classes.** | Concrete instantiation violates Open/Closed and DIP. | **Factory Method / Abstract Factory** | Direct `new MyClass()` is fine if there is only one concrete type and tests do not need to substitute it. |
| **An external library or legacy API has methods that don't match our domain interface.** | Interface incompatibility. | **Adapter** | If you control both codebases, refactor the method signatures directly instead of creating an adapter wrapper. |
| **An object behaves completely differently depending on its current lifecycle phase.** | State-dependent conditionals scattered across all methods. | **State** | If the state machine has only 2-3 simple states with no diverging behavior, a simple `enum` with a state field is vastly simpler. |
| **When an action occurs (e.g. Order Placed), multiple independent components must react (email, analytics, audit).** | High coupling between the subject and secondary side effects. | **Observer / Event Listener** | Direct synchronous method calls are better when there is only one dependent action that is part of the core transactional invariant. |
| **You need to add cross-cutting behaviors (logging, caching, metrics, retry) without modifying the core class.** | Open/Closed violation; rigid inheritance. | **Decorator / Wrapper** | If the behavior is intrinsic to the class and used everywhere, just put it directly in the class. |
| **A request must pass through a dynamic pipeline of filters, authorizers, and validators.** | Hardcoded monolithic processing pipeline. | **Chain of Responsibility** | A simple `List<Validator>` evaluated in a loop is usually much easier to debug than a linked chain. |
| **Many objects are tightly interconnected in an $O(N^2)$ communication web.** | Spaghetti coupling between peers. | **Mediator** | Direct dependency injection between pairs of classes when interactions are linear and small. |
| **Callers need to execute operations that need undo/redo, queuing, or deferred execution.** | Direct method execution couples invoker to receiver. | **Command** | Plain method calls or lambdas/Runnables if no undo/history/queue metadata is required. |
| **A complex subsystem of 10+ classes is overwhelming for everyday clients to interact with.** | Leaky abstractions; high cognitive load. | **Facade** | Don't create a Facade if clients actually need fine-grained control of individual subsystem components. |
| **You need to control access, delay expensive instantiation (lazy loading), or cross a boundary.** | Direct access is expensive or unsafe. | **Proxy** | Direct access is preferred if instantiation is lightweight and security checks are handled at the perimeter. |

---

## The Default Option: NO PATTERN

```text
                  ┌───────────────────────────────┐
                  │ Does the code resist change?  │
                  └───────────────┬───────────────┘
                                  │
                         No ──────┴────── Yes
                         │                 │
                         ▼                 ▼
                 ┌───────────────┐  ┌──────────────────────────────┐
                 │  NO PATTERN   │  │ What is changing?            │
                 │ Keep it simple│  │ - Behavior?   → Strategy     │
                 │ and readable  │  │ - Lifecycle?  → State        │
                 └───────────────┘  │ - Pipeline?   → Chain        │
                                    │ - Reactions?  → Observer     │
                                    └──────────────────────────────┘
```

> **Warning against "Pattern Soup":**  
> Writing 8 interfaces, 4 abstract factories, 6 builders, and a mediator for a problem that can be solved in 50 lines of clean Java is poor engineering. Every abstraction adds cognitive load, indirection, and navigation friction.
