# System Design & Distributed Systems Glossary

An unambiguous lexicon of foundational terms used throughout this curriculum.

---

- **ACID**: Atomicity, Consistency, Isolation, Durability. Properties of traditional database transactions.
- **Amdahl's Law**: Formula finding the maximum improvement possible by improving a portion of a system.
- **At-Least-Once Delivery**: Messages are guaranteed to be delivered, but duplicates may occur due to network retries.
- **Backpressure**: Mechanism allowing a downstream receiver to signal an upstream sender to slow down ingestion.
- **Bulkhead Pattern**: Isolating system elements into pools so failure of one does not bring down the entire system.
- **Cache-Aside**: Application code queries the cache first; on a miss, reads from the database and updates the cache.
- **CAP Theorem**: In the presence of a network partition, a system must choose between consistency and availability.
- **Circuit Breaker**: A proxy that detects failures and prevents repeated calls to a broken downstream service.
- **Consistent Hashing**: A hashing technique where adding or removing a node requires remapping only $K/N$ keys.
- **Dead-Letter Queue (DLQ)**: A service queue that holds messages that cannot be processed after maximum retry attempts.
- **Fan-Out**: Distributing a single incoming message or query to multiple downstream queues, workers, or shards.
- **Fencing Token**: A monotonically increasing number issued by a lock service to reject requests from stale lock holders.
- **Idempotency**: An operation that produces the exact same outcome whether executed once or multiple times.
- **Lamport Timestamp**: A logical clock mechanism used to determine the partial ordering of events in a distributed system.
- **Little's Law**: Average number of concurrent items $L$ in a stationary queueing system equals arrival rate $\lambda \times$ latency $W$.
- **Optimistic Concurrency Control (OCC)**: Transactions execute without locks and verify at commit time that data was not modified.
- **Pessimistic Concurrency Control (PCC)**: Explicit row or table locks prevent concurrent transactions from accessing the same resource.
- **Read-Your-Writes Consistency**: Guarantees that a user always sees their own updates immediately upon subsequent reads.
- **Saga Pattern**: A sequence of local transactions where each step updates state and publishes an event or compensation.
- **Single Point of Failure (SPOF)**: A component whose failure will cause the entire system to stop functioning.
- **Split-Brain**: A condition where a cluster fragments into independent sub-clusters, each believing it is the authoritative leader.
- **Transactional Outbox**: Writing domain state and outbox event records into the same local database transaction.
- **Vector Clock**: An algorithm for generating a partial ordering of events and detecting causal conflicts in distributed systems.
