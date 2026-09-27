# Refactoring Lab: Defending Collections Against Encapsulation Leaks

> **Core Focus:** Transforming smelly, fragile code into robust, testable, invariant-protecting OOP design.

---

## 1. The Design Smell
**Identified Smells:** `Leaky Encapsulation, State Corruption`  
**Guiding Principle:** `Defensive Copying & Unmodifiable Views`  

### What's Broken?
ShoppingCart returns its internal List<CartItem> via getItems(), allowing external callers to clear() or add free items.

---

## 2. Why This Hurts in Production
- **Fragility:** Modifying one behavior introduces regressions in unrelated features.
- **Un-testability:** Tight coupling prevents fast, isolated unit testing without external services.
- **Invariant Violations:** Callers can manipulate internal state into corrupt, unrecoverable configurations.

---

## 3. The Target Architecture
Return Collections.unmodifiableList() and provide atomic cart.addItem() with invariant checks.

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
