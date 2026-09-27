# Refactoring Lab: Eliminating Swallowed Exceptions in Payment Gateway

> **Core Focus:** Transforming smelly, fragile code into robust, testable, invariant-protecting OOP design.

---

## 1. The Design Smell
**Identified Smells:** `Exception Swallowing, Silent Failures`  
**Guiding Principle:** `Explicit Domain Error Modeling`  

### What's Broken?
PaymentService catches Exception e and does nothing, returning false and concealing network connection failures.

---

## 2. Why This Hurts in Production
- **Fragility:** Modifying one behavior introduces regressions in unrelated features.
- **Un-testability:** Tight coupling prevents fast, isolated unit testing without external services.
- **Invariant Violations:** Callers can manipulate internal state into corrupt, unrecoverable configurations.

---

## 3. The Target Architecture
Catch specific IOException, log context, and rethrow PaymentProcessingException preserving root cause.

```text
[Smelly Monolith / Leaky State]
              ↓ Refactoring
[Cohesive Domain Entity] ──> [Explicit Contract] ──> [Polymorphic Strategy / Port]
```

---

## 4. Step-by-Step Refactoring Plan
1. **Pin Behavior with Tests:** Run existing tests in `tests/` to verify current baseline behavior.
2. **Identify Boundary Seams:** Identify which fields and methods belong to separate change vectors.
3. **Extract Collaborators:** Create new focused classes or Value Objects.
4. **Invert Dependencies:** Inject the new collaborators into the main class via constructor.
5. **Verify Zero Regressions:** Ensure all unit tests pass with green status.

---

## 5. Lab Directory Structure
- `src/` — The original broken, smelly code before refactoring.
- `solution/` — The clean, refactored production-grade solution.
- `tests/` — Automated unit tests validating both happy path and invariant guards.
