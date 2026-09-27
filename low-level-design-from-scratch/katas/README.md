# Repeatable Low-Level Design Katas

A kata is a targeted exercise practiced repeatedly until the design reflexes become second nature.

| Kata | Title | Core Reflex Developed |
|:---|:---|:---|
| `kata-01-primitive-to-value-object` | **Primitive to Value Object** | Refactor double amount and String currency fields in an account transfer method into an immutable Money value object. |
| `kata-02-replace-conditional-polymorphism` | **Replace Conditional with Polymorphism** | Replace an ugly switch statement over shipping types (Standard, Express, Overnight) with polymorphic Strategy objects. |
| `kata-03-tell-dont-ask` | **Tell, Don't Ask** | Refactor a procedural service that queries wallet balance, computes tax, and updates balance into a single behavioral wallet method. |
| `kata-04-clock-injection` | **Clock Dependency Injection** | Refactor a Subscription service calling Instant.now() to accept java.time.Clock, writing deterministic expiry tests. |
| `kata-05-invariant-guarding` | **Constructor Invariant Guarding** | Refactor a UserRegistration class with public mutable fields into an immutable, self-validating domain entity. |
| `kata-06-null-elimination-optional` | **Null Elimination via Optional** | Replace scattered defensive if (obj != null) checks with Optional<T> and guaranteed non-null domain collections. |
| `kata-07-builder-assembly` | **Builder Aggregate Assembly** | Refactor a class with telescoping constructors (6 overloaded constructors) into a fluent, invariant-validating Builder. |
| `kata-08-strategy-dispatch` | **Dynamic Strategy Dispatch** | Refactor a hardcoded pricing algorithm into an interchangeable Strategy pattern allowing runtime tariff swapping. |
| `kata-09-observer-decoupling` | **Observer Event Decoupling** | Decouple a monolithic checkout function by publishing OrderPlaced domain events to email, audit, and inventory listeners. |
| `kata-10-fsm-transition-table` | **FSM Transition Table** | Implement a deterministic Finite State Machine using a state transition table that rejects invalid lifecycle leaps. |