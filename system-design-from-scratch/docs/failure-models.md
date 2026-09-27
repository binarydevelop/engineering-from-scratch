# Failure Models and Chaos Taxonomy

In distributed systems, failure is an invariant, not an anomaly. Designing resilient systems requires defining explicit failure models.

---

## 1. Node Failure Classifications

| Failure Model | Description | System Assumption |
| :--- | :--- | :--- |
| **Crash-Stop** | A node halts execution and remains halted indefinitely. | Standard assumption in Raft, Paxos, and fail-stop clusters. |
| **Crash-Recovery** | A node crashes, restarts, reads durable disk state, and rejoins the cluster. | Reality of production Linux servers, container restarts, and VM preemption. |
| **Fail-Slow / Gray Failure** | Node does not crash, but experiences high CPU saturation, packet loss, or disk degradation. | Most dangerous failure mode; hard to detect via binary health checks. |
| **Byzantine Faults** | Nodes exhibit arbitrary, malicious, or corrupt behavior (altered messages). | Addressed in blockchain and cryptographic consensus (PBFT); rarely needed in private VPCs. |

---

## 2. Common Distributed Failure Scenarios

### 1. Network Partitions (Split-Brain)
- **Mechanism**: Routers fail or security groups misconfigure, isolating Node A and Node B while both remain alive.
- **Danger**: Both nodes elect themselves leader and accept conflicting writes.
- **Defense**: Odd-numbered quorums ($2f + 1$) and fencing tokens.

### 2. The Thundering Herd / Cache Stampede
- **Mechanism**: A popular cache key expires. 5,000 concurrent requests miss the cache simultaneously and hit the primary database.
- **Danger**: Database CPU hits 100%, connection pool exhausts, database crashes.
- **Defense**: Mutex locking (single-flight), probabilistic early expiration (XFetch), or background refresh.

### 3. Retry Amplification & Cascading Failures
- **Mechanism**: Service B experiences transient latency. Service A times out and retries 3 times. Service C retries Service A 3 times.
- **Math**: $1 \times 3 \times 3 = 9\times$ inbound request volume slamming an already failing service.
- **Defense**: Exponential backoff with full jitter, circuit breakers, and bounded retry budgets (e.g., max 10% retries).

### 4. Clock Skew and Drift
- **Mechanism**: Physical NTP clocks drift by milliseconds or seconds across datacenters.
- **Danger**: "Last-Write-Wins" (LWW) timestamp comparisons overwrite newer data with older data.
- **Defense**: Monotonic clocks, Lamport logical timestamps, Vector Clocks, or TrueTime (GPS + Atomic clocks).

### 5. Poison Pill Messages
- **Mechanism**: A malformed message enters a queue. The consumer parses it, crashes, and restarts without acknowledging.
- **Danger**: Infinite crash-loop halts queue processing for all valid messages.
- **Defense**: Dead-Letter Queues (DLQ) with max delivery attempt thresholds.
