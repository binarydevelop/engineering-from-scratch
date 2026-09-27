# Project: Splitwise Expense Sharing

> **Production Low-Level Design Implementation**  
> Focus: Translating requirements into collaborating, test-covered object-oriented components.

---

## 1. Problem Overview
Users, groups, expense creation, split strategies (Equal, Exact, Percentage), and debt balance graph simplification.

---

## 2. Requirements & Use Cases
### Primary Use Cases
1. **Initiation & Preconditions:** Validate input constraints and establish invariant fortress.
2. **Core Operation Execution:** Delegate responsibilities to Information Experts.
3. **State Transition & Invariants:** Advance domain lifecycle and guard against illegal operations.
4. **Completion & Querying:** Return unmodifiable snapshots of domain state.

### Domain Invariants Checklist
- [x] Sum of individual split amounts must exactly equal total expense; total group debt balance must sum to net zero.
- [x] Immutability enforced for all Value Objects and identifiers.
- [x] All collection getters return unmodifiable defensive views.

---

## 3. Responsibility Assignment (GRASP)
| Responsibility | Assigned Class | Architectural Justification |
|:---|:---|:---|
| Guard internal state invariants | Entity / Aggregate Root | Information Expert holding core mutable state. |
| Execute varying domain calculation | Strategy / Policy | Honors Open/Closed Principle; isolates variation vector. |
| Orchestrate use case workflow | Service / Coordinator | Coordinates collaborator calls without polluting domain rules. |

---

## 4. Class Collaboration Diagram
```mermaid
classDiagram
    class SplitwiseExpenseSharingContext {
        -State state
        +executeOperation()
        +getState()
    }
    class CollaboratingPolicy {
        <<interface>>
        +applyRule()
    }
    SplitwiseExpenseSharingContext --> CollaboratingPolicy : uses
```

---

## 5. Architectural Directory Layout
```text
projects/09-splitwise/
├── README.md               (This specification and architecture guide)
src/main/java/lld/problems/09_splitwise/
└── (Production-grade domain entities, value objects, and policies)
src/test/java/lld/problems/09_splitwise/
└── (Automated JUnit 5 test suite verifying invariants and behaviors)
```

---

## 6. How to Run the Test Suite
```bash
# Run all unit tests for this project
mvn test -Dtest=SplitwiseExpenseSharingTest
```
