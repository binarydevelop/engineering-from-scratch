# Engineering From Scratch: The Master Monorepo

> **Understand it. Build it. Measure it. Break it. Debug it. Scale it. Secure it. Operate it. Ship it.**

A comprehensive, first-principles engineering academy covering systems, networking, language internals, low-level design, backend architecture, distributed consensus, databases, streaming, cloud infrastructure, SRE, platform engineering, and production AI systems.

---

## 🏛️ Monorepo Architecture & Directory Index

### 1. Systems & Networking Foundations
- **[`operating-systems-from-scratch/`](operating-systems-from-scratch/)** — Processes, threads, virtual memory, syscalls, page tables, and file systems in pure C.
- **[`linux-from-scratch/`](linux-from-scratch/)** — Kernel inspection, cgroups, namespaces, signals, procfs, sysfs, and troubleshooting.
- **[`computer-networking-from-scratch/`](computer-networking-from-scratch/)** — Raw sockets, packet parsing, TCP handshake, sliding windows, congestion control, and epoll.

### 2. Core Craftsmanship, LLD & Backend Engineering
- **[`java-from-scratch/`](java-from-scratch/)** — Modern Java 21+, JVM bytecode execution, garbage collection, memory model, and concurrency.
- **[`low-level-design-from-scratch/`](low-level-design-from-scratch/)** — Object-oriented modeling, Gang of Four design patterns, SOLID principles, and refactoring katas.
- **[`backend-engineering-from-scratch/`](backend-engineering-from-scratch/)** — 206 phases, 905 tests: HTTP/wire protocols, connection pools, outbox pattern, **Raft consensus, Protobuf/gRPC, LSM-Trees, and Zero-Trust mTLS**.

### 3. The Persistence, Cache & Analytical Data Tier
- **[`database-and-sql-from-scratch/`](database-and-sql-from-scratch/)** — Relational storage engines, ACID transactions, WAL, indexing, and query execution.
- **[`redis-from-scratch/`](redis-from-scratch/)** — In-memory data structures, RESP protocol, event loops, replication, and distributed locks.
- **[`kafka-from-scratch/`](kafka-from-scratch/)** — Append-only logs, partition routers, consumer group rebalancing, and KRaft metadata consensus.
- **[`elasticsearch-from-scratch/`](elasticsearch-from-scratch/)** — Lucene inverted indexes, BM25 scoring, term vectors, and sharded search coordination.
- **[`nosql-databases-and-query-languages-from-scratch/`](nosql-databases-and-query-languages-from-scratch/)** — Document, key-value, column-family, and graph databases.
- **[`olap-databases-and-analytical-querying-from-scratch/`](olap-databases-and-analytical-querying-from-scratch/)** — Columnar layouts, vectorized execution, ClickHouse/DuckDB internals, and star schema analytics.
- **[`data-engineering-from-scratch/`](data-engineering-from-scratch/)** — Batch and streaming pipelines, Spark transformations, dbt modeling, and Airflow orchestration.

### 4. Distributed Systems, Cloud & Infrastructure
- **[`docker-from-scratch/`](docker-from-scratch/)** — Containerization via Linux namespaces, cgroups, overlayfs, and runtime engines.
- **[`kubernetes-from-scratch/`](kubernetes-from-scratch/)** — Control plane architecture, custom controllers, reconciliation loops, and ingress scheduling.
- **[`aws-from-scratch/`](aws-from-scratch/)** — Cloud design patterns, IAM security perimeters, VPC networking, and serverless architectures.
- **[`system-design-from-scratch/`](system-design-from-scratch/)** — 201 phases, 899 tests: Back-of-envelope estimation, consensus, consistent hashing, and high-scale architectures.

### 5. Production Reliability & SRE
- **[`production-sre-observability-platform-engineering-from-scratch/`](production-sre-observability-platform-engineering-from-scratch/)** — 109 tests: OpenTelemetry tracing, Prometheus metrics, multi-window SLO burn rates, chaos engineering, and 42 broken labs.

### 6. Modern AI & Machine Learning Systems
- **[`ai-engineering-from-scratch/`](ai-engineering-from-scratch/)** — Machine learning fundamentals, transformers, prompt engineering, RAG, and autonomous agent swarms.
- **[`ai-systems-from-scratch/`](ai-systems-from-scratch/)** — AI compilers, Triton GPU kernels, continuous batching, KV caching, and low-latency inference serving.

### 7. Technical Leadership & Impact
- **[`staff-engineering-and-product-mindset-from-scratch/`](staff-engineering-and-product-mindset-from-scratch/)** — Architectural RFCs, technical strategy, ADRs, engineering culture, and stakeholder alignment.

---

## 🚀 Getting Started

Ensure you have Python 3.12, OpenJDK 27, and Docker installed:
```bash
# Verify environment
python3.12 --version
mvn -v
docker --version
```
