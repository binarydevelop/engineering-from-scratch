# Project: Idempotent Payment Gateway

> **Production Low-Level Design Implementation**  
> Focus: Translating requirements into collaborating, test-covered object-oriented components.

---

## 1. Problem Overview
Payment requests, idempotency key deduplication, payment processor interfaces, and refund state machines.

---

## 2. Requirements & Use Cases
### Primary Use Cases
1. **Initiation & Preconditions:** Validate input constraints and establish invariant fortress.
2. **Core Operation Execution:** Delegate responsibilities to Information Experts.
3. **State Transition & Invariants:** Advance domain lifecycle and guard against illegal operations.
4. **Completion & Querying:** Return unmodifiable snapshots of domain state.

### Domain Invariants Checklist
- [x] Identical idempotency key produces identical response without secondary debit; refunds cannot exceed original charge amount.
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
    class IdempotentPaymentGatewayContext {
        -State state
        +executeOperation()
        +getState()
    }
    class CollaboratingPolicy {
        <<interface>>
        +applyRule()
    }
    IdempotentPaymentGatewayContext --> CollaboratingPolicy : uses
```

---

## 5. Architectural Directory Layout
```text
projects/20-payment-gateway/
├── README.md               (This specification and architecture guide)
src/main/java/lld/problems/20_payment_gateway/
└── (Production-grade domain entities, value objects, and policies)
src/test/java/lld/problems/20_payment_gateway/
└── (Automated JUnit 5 test suite verifying invariants and behaviors)
```

---

## 6. How to Run the Test Suite
```bash
# Run all unit tests for this project
mvn test -Dtest=IdempotentPaymentGatewayTest
```
