# Phases 01 – 10: Production Foundations & Systems Physics

> **Motto**: Understand it. Instrument it. Measure it. Break it. Detect it. Debug it. Recover it. Automate it. Improve it. Operate it.

---

## Phase 01: What Does Production Mean?

### Motto
"Production = Real Users + Real State + Real Consequences."

### Problem
Engineers often view production as simply "development with a domain name attached." This creates a mindset where untested changes are pushed, state is treated as easily replaceable, and outages are viewed as unfortunate accidents rather than engineering defects.

### First Principles
In development, an unhandled exception prints a traceback to stdout, you restart the process in your IDE, and nobody is harmed.  
In production:
1. **Real Users**: Thousands of concurrent humans depend on the service for their livelihood, payments, medical records, or daily workflow.
2. **Real State**: The database contains millions of financial records and customer invariants. A corrupted column or lost transaction cannot be fixed by deleting `db.sqlite3`.
3. **Real Consequences**: Every minute of downtime translates directly to financial loss, legal liability, SLA penalties, and customer churn.

### Mental Model
```text
Development Environment               Production Environment
├── 1 User (You)                      ├── 100,000 Concurrent Customers
├── Synthetic InMemory State          ├── Distributed ACID PostgreSQL Cluster
├── Can pause with breakpoint         ├── Cannot halt execution for 100ms
└── Zero financial consequence        └── $50,000 / minute revenue impact
```

### Questions for Mastery
1. Why is an untested database rollback script in production a SEV-1 risk event?
2. If your service has 99.9% uptime, how many minutes of downtime are permissible in a 30-day month? (Answer: 43.2 minutes).

---

## Phase 02: Development vs Production

### Motto
"Concurrency is not 1 request repeated 10,000 times; it is 10,000 requests contending for the exact same resource."

### Problem
Code works flawlessly in local tests (`pytest`) where single requests execute sequentially. When deployed to production, the service crashes under concurrent load due to race conditions, thread starvation, and connection pool exhaustion.

### First Principles & Mental Model
In development, sequential execution means contention is zero. In production:
* 100 threads attempt to write to the same database row simultaneously.
* The Linux kernel CFS scheduler rapidly context-switches between threads.
* In-flight requests consume memory buffers concurrently.

### Empirical Experiment
Run the comparison between sequential and concurrent load:
```bash
# 1. Sequential: 100 requests in series
python3 load-tests/load_generator.py --rps 10 --duration 10 --concurrency 1

# 2. Concurrent: 100 requests with 50 concurrency
python3 load-tests/load_generator.py --rps 100 --duration 10 --concurrency 50
```
Observe how p99 latency increases from 12ms to 45ms purely due to resource contention.

---

## Phase 03: Production Failure Model

### Motto
"Systems fail in 10 fundamental ways; if you do not design for them, production will find them for you."

### The 10 Production Failure Domains
```text
1. Code Bugs: Unhandled NoneType, integer overflow, infinite loop.
2. Configuration Drift: Staging and production settings diverge; wrong port or URL.
3. Dependency Outage: Payment provider returns HTTP 500 or hangs.
4. Network Partitions: Packet loss, DNS resolution failure, SSL cert expiry.
5. CPU Saturation: Cryptographic hashing, JSON deserialization burning cores.
6. Memory Exhaustion: Memory leaks, unbounded cache growth, Linux OOM killer.
7. Disk Pressure: WAL logs fill scratch partition; disk I/O saturated (100% iowait).
8. Traffic Spikes: Marketing campaign triggers sudden 10x arrival surge.
9. Deployment Changes: Schema migration incompatible with running code.
10. Human Action: Running manual DROP TABLE or misconfiguring security group.
```

---

## Phase 04: Users Experience Symptoms

### Motto
"Alert on symptoms; diagnose through causes."

### Problem
Engineers configure alarms on CPU utilization, disk reads, and memory percentages. When CPU hits 88%, the on-call engineer is paged at 3 AM. However, checkout requests are succeeding at 100% with 20ms latency. The page was completely unnecessary.

### Mental Model: The Causal Ladder
```text
CAUSE (Internal Mechanism)          SYMPTOM (Customer Reality)
├── CPU at 95%             ──────►   Checkout latency is 25ms (HEALTHY)
├── Database lock wait     ──────►   Cart POST returns 504 (OUTAGE)
└── Memory at 90%          ──────►   Zero failed requests (HEALTHY)
```
* **Paging Rules**: Wake a human engineer ONLY when the user symptom violates an SLO or threatens immediate business failure.

---

## Phase 05: Availability

### Motto
"Ping uptime is a vanity metric; request-based availability is the truth."

### Problem
Infrastructure teams report "99.99% server uptime" because the container process never died and ping succeeded. However, the database connection was broken, and 40% of user checkout requests failed with HTTP 500.

### The Mathematical Definition
$$\text{Availability} = \frac{\text{Successful Valid Requests}}{\text{Total Valid Requests}}$$

If your service processes 1,000,000 requests in an hour, and 5,000 return HTTP 500:
$$\text{Availability} = \frac{995,000}{1,000,000} = 99.5\%$$
Under a 99.9% SLO, this single hour depleted the entire monthly error budget!

---

## Phase 06: Latency (Quantiles & Skew)

### Motto
"The average latency is a lie told by happy path requests."

### Problem
An API reports an average latency of 25ms. The product manager is thrilled. However, 1 in 100 users experiences an 8-second hang and abandons their cart. The average completely masks this failure.

### Quantiles Breakdown
* **p50 (Median)**: 50% of users experience latency $\le$ this value.
* **p90**: 90% of requests are faster than this value.
* **p95**: Standard SLA benchmark.
* **p99 (Tail)**: 1 out of every 100 requests. In an e-commerce app with 20 backend requests per page view, **1 in 5 page loads experiences the p99 latency!**
* **p99.9 (Extreme Tail)**: The worst 1 in 1,000 requests, representing lock waits, GC pauses, or connection timeouts.

---

## Phase 07: Throughput

### Motto
"Throughput is what the system completes; arrival rate is what the client demands."

### Mental Model
* **Arrival Rate ($\lambda$)**: The volume of requests per second arriving at your edge gateway.
* **Effective Throughput**: The volume of requests per second your workers successfully process and return.
* When Arrival Rate > Throughput: Queues grow, latency climbs, and requests eventually timeout.

---

## Phase 08: Saturation

### Motto
"Every system has exactly one bottleneck at any given moment."

### First Principles
As load increases, systems do not run out of all resources simultaneously. One resource always saturates first:
1. **CPU Bound**: Serialization, cryptographic hashing.
2. **Memory Bound**: Large in-memory caches, uncollected objects.
3. **I/O Bound**: Disk write IOPS, PostgreSQL WAL sync.
4. **Network Socket / Pool Bound**: Database connections, worker thread pool.

### How to Identify the First Bottleneck
Run `load-tests/load_generator.py` while monitoring `dashboards/use-resources-dashboard.json`. Watch whether CPU, connection pool, or worker lag crosses 80% first.

---

## Phase 09: Queueing Dynamics (Kingman's Formula)

### Motto
"Queues precede cliffs; utilization above 80% is operational Russian roulette."

### The Mathematical Formula (Kingman's Approximation)
$$W_q \approx \left(\frac{U}{1-U}\right) \cdot \left(\frac{c_a^2 + c_s^2}{2}\right) \cdot t_s$$
Notice the term $\frac{U}{1-U}$:
* At $U = 50\%$: $\frac{0.50}{1 - 0.50} = 1$
* At $U = 80\%$: $\frac{0.80}{1 - 0.80} = 4$
* At $U = 95\%$: $\frac{0.95}{1 - 0.95} = 19$
* At $U = 99\%$: $\frac{0.99}{1 - 0.99} = 99$

Latency does not double as utilization doubles; it explodes by **99x**!

---

## Phase 10: Little's Law

### Motto
"Concurrency = Throughput × Latency. If downstream latency doubles, required worker concurrency doubles."

### Mathematical Proof
$$L = \lambda W$$
Where:
* $L$ = Number of concurrent in-flight requests in the system.
* $\lambda$ = Arrival rate (Requests per second).
* $W$ = Average time each request takes (Latency in seconds).

### The Production Domino Disaster
If your API processes 1,000 RPS with 50ms latency:
$$L = 1000 \times 0.050 = 50\text{ concurrent worker slots}$$

If `payment-service` slows down to 500ms:
$$L = 1000 \times 0.500 = 500\text{ concurrent worker slots}$$

If your web server is configured with 100 worker threads, all 100 threads become saturated immediately, 400 requests are rejected, and the API collapses.
