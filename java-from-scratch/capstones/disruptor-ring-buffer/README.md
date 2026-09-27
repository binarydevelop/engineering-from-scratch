# Capstone: Lock-Free High-Performance Ring Buffer

> **Overview:** A zero-allocation, lock-free inter-thread messaging ring buffer implementing mechanical sympathy, cache-line padding to prevent false sharing, and atomic sequence tracking.

---

## 1. Architectural Blueprint
This capstone implements an enterprise-grade system designed to operate under heavy concurrency while respecting JVM memory boundaries and hardware constraints.

## 2. Invariants & Design Principles
* **Non-Blocking Execution**: Maximizes CPU cache locality and non-blocking algorithms where appropriate.
* **Predictable Latency**: Bounds allocation churn to prevent garbage collection pauses.
* **Comprehensive Testing**: Validated with multi-threaded stress tests.

## 3. How to Run Tests
```bash
mvn test -pl capstones -Dtest=DisruptorRingBufferTest
```
