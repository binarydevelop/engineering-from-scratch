# Phase 147: Domain-Driven Design (DDD) Tactical Patterns in Low-Level Design

## 1. Why This Matters for MAANG & Senior/Staff Roles
At Senior and Staff levels, interviewers do not want to see naive anemic domain models where classes are just data containers with getters/setters controlled by massive service classes. Domain-Driven Design (DDD) tactical patterns provide the architectural blueprint for modeling complex business logic, establishing consistency boundaries, and preventing state corruption.

---

## 2. Core Concepts & Architecture Deep-Dive
### Core Tactical DDD Primitives
1. **Entities**: Domain objects defined by an explicit thread of identity that endures across state mutations (e.g., `Order` with `OrderId`). Two orders with identical items are distinct if IDs differ.
2. **Value Objects**: Immutable objects defined strictly by their attributes, with no conceptual identity (e.g., `Money`, `Address`, `DateRange`). If two `Money` objects have amount=100 and currency=USD, they are interchangeable. Always self-validating in constructors.
3. **Aggregates & Aggregate Roots**: A cluster of associated domain objects treated as a unit for data changes. External objects may ONLY hold a reference to the Aggregate Root (e.g., `Order` is the root; `OrderItem` can only be altered through methods on `Order`).
   - Rule 1: The Aggregate Root enforces all business invariants.
   - Rule 2: Transactions modify one Aggregate at a time.
4. **Repositories**: Provide the illusion of an in-memory collection of Aggregate Roots (`OrderRepository.save(order)`). Repositories exist ONLY for Aggregate Roots, never for internal entities or value objects.
5. **Domain Events**: Significant domain occurrences published when aggregate state changes (`OrderPlacedEvent`, `PaymentFailedEvent`).

---

## 3. High-Value Interview Angle & Failure Modes
### Interview Questions & Design Drills
- **"How do you prevent race conditions when two concurrent requests update the same entity?"**:
  Inside the Aggregate Root, protect state transitions with invariant validation. In the repository layer, implement Optimistic Concurrency Control using `@Version` or conditional updates (`WHERE version = expected_version`).
- **"Where does business logic belong vs orchestration logic?"**:
  - *Domain Model (Entities/Aggregates)*: Pure business rules and invariant enforcement (e.g., `order.applyDiscount(coupon)`).
  - *Application Service*: Orchestration only (fetches aggregate from repo, calls domain method, persists aggregate, dispatches events).

---

## 4. Hands-On Practice & Implementation Drills
### Code Drill: Aggregate Root Pattern
```java
// Invariant-enforcing Aggregate Root
public class Order {
    private final OrderId id;
    private final List<OrderItem> items = new ArrayList<>();
    private OrderStatus status;
    private Money totalAmount;

    public void addItem(Product product, int quantity) {
        if (this.status != OrderStatus.DRAFT) {
            throw new DomainRuleViolationException("Cannot modify items in a submitted order");
        }
        if (items.size() >= 50) {
            throw new DomainRuleViolationException("Maximum item count exceeded");
        }
        this.items.add(new OrderItem(product.getId(), quantity, product.getPrice()));
        recalculateTotal();
    }
    
    // External code cannot mutate items directly
    public List<OrderItem> getItems() {
        return Collections.unmodifiableList(items);
    }
}
```

---

## 5. Key Takeaways & Cheat Sheet
- Entities have identity; Value Objects are immutable and defined by attributes.
- Aggregate Roots protect internal state and enforce all business invariants.
- Transactions must only span a single Aggregate boundary.
- Separates pure domain logic from framework and infrastructure concerns.
