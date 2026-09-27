# Exercise TEST-11: Verifying Immutability via Reflection

**Category:** 05-testing-and-testability  
**Focus:** Write test asserting all fields of Money record are private, final, and lack setters.  

---

## 1. Problem Description
Write test asserting all fields of Money record are private, final, and lack setters. You are tasked with analyzing the domain requirements, establishing invariants, defining behavioral contracts, and creating a robust design from first principles.

---

## 2. Requirements & Constraints
### Functional Requirements
- **FR-1:** Identify all actors, triggers, and expected outcomes.
- **FR-2:** Model the core domain entities, value objects, and behavioral boundaries.
- **FR-3:** Enforce all domain invariants (e.g. non-negativity, capacity limits, valid transitions).

### Non-Functional Constraints
- **NFR-1:** Decouple domain decisions from transport and storage mechanisms.
- **NFR-2:** Design explicit interfaces allowing 100% testability with in-memory test doubles.
- **NFR-3:** Make invalid states impossible to represent in the type system.

---

## 3. Ambiguities to Clarify
Before writing any classes or interfaces, identify at least 3 ambiguous questions you must resolve:
1. What happens during unexpected failure or timeout?
2. What are the boundary limits on volume, duration, or capacity?
3. Which operations must be idempotent or thread-safe?

---

## 4. Expected Deliverables
1. **Responsibility Assignment Table:** Map every requirement to a specific class with GRASP Information Expert rationale.
2. **Contract Signatures:** Provide explicit Java interface signatures with typed parameters and return values.
3. **Invariant Checklist:** Document the pre-conditions, post-conditions, and invariant guards.
4. **Extension Scenario:** Explain how your design adapts when a new variation is introduced.

---

> 💡 **Self-Check:** Compare your design against the reference solution in `exercises/solutions/05-testing-and-testability/test-11-solution.md`.
