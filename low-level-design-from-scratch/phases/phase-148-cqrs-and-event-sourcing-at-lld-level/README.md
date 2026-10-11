# Phase 148: CQRS and Event Sourcing at the Low-Level Class & Component Level

## 1. Why This Matters for MAANG & Senior/Staff Roles
In high-throughput transactional domains (e.g., trading order books, ride-share dispatch, e-commerce checkouts), unified read-write domain models create severe locking contention and schema compromises. Command Query Responsibility Segregation (CQRS) splits the domain model into an invariant-enforcing write model (Commands) and a query-optimized read model (Queries).

---

## 2. Core Concepts & Architecture Deep-Dive
### CQRS Class Structure & Separation of Concerns
1. **Command Side**:
   - `Command`: An intention to alter state (`PlaceOrderCommand`, `CancelReservationCommand`).
   - `CommandHandler`: Executes domain operations against the Aggregate Root.
   - Writes to the append-only write store or relational primary DB.
2. **Query Side**:
   - `Query`: A request for data (`GetCustomerOrdersQuery`, `GetInventorySummaryQuery`).
   - `QueryHandler`: Bypasses domain aggregates completely; queries denormalized, read-optimized tables, Elasticsearch, or Redis caches directly.
3. **Synchronization / Event Bus**:
   - Synchronous in-memory projection (same transaction) OR asynchronous via Kafka/Transactional Outbox.

### Event Sourcing Primitive
Instead of storing current state, store the sequence of state-changing Domain Events:
- State of an aggregate is reconstructed by replaying events from genesis:
  `State = foldLeft(InitialState, Events, ApplyEvent)`
- Guaranteed audit log, time-travel debugging, and zero lost data.

---

## 3. High-Value Interview Angle & Failure Modes
### Interview Scenarios
- **"When is CQRS an anti-pattern?"**: For simple CRUD systems, CQRS introduces catastrophic complexity (eventual consistency lag, dual data stores, projection failures). Only introduce it when read and write access patterns, SLAs, and data shapes diverge significantly.
- **"How do you handle the eventual consistency window on the read model in UI?"**:
  1. Return newly generated ID and optimistic client-side UI updates.
  2. Implement read-your-own-writes session consistency using version/timestamp tokens.

---

## 4. Hands-On Practice & Implementation Drills
### Implementation Diagram & Code Pattern
```java
// Command Bus & Handler
public record CreateAccountCommand(AccountId id, CustomerId customerId, Money initialDeposit) {}

public class CreateAccountCommandHandler {
    private final AccountRepository repo;
    
    public void handle(CreateAccountCommand cmd) {
        Account account = Account.open(cmd.id(), cmd.customerId(), cmd.initialDeposit());
        repo.save(account); // Emits AccountOpenedEvent
    }
}

// Separate Query Model (Denormalized)
public record AccountSummaryView(String accountId, String customerName, BigDecimal currentBalance) {}

public class AccountQueryService {
    private final ReadOnlyJdbcTemplate jdbc;
    public AccountSummaryView getSummary(String accountId) {
        // Direct SQL read from denormalized view - zero aggregate overhead
        return jdbc.queryForObject("SELECT * FROM view_account_summary WHERE id = ?", mapper, accountId);
    }
}
```

---

## 5. Key Takeaways & Cheat Sheet
- Separate Command model (validates and mutates) from Query model (denormalized read).
- Eliminates database lock contention on hot read-heavy tables.
- Query models can be rebuilt or re-indexed without altering write data.
- Essential for senior design interviews involving financial, booking, or audit systems.
