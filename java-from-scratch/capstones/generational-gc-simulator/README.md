# Capstone: Generational GC & Object Memory Allocator Simulator

> **Overview:** A discrete-event JVM memory simulation modeling bump-the-pointer Eden allocation, Survivor space aging, Card Table dirtying, and Mark-Sweep-Compact Tenured collection.

---

## 1. Architectural Blueprint
This capstone implements an enterprise-grade system designed to operate under heavy concurrency while respecting JVM memory boundaries and hardware constraints.

## 2. Invariants & Design Principles
* **Non-Blocking Execution**: Maximizes CPU cache locality and non-blocking algorithms where appropriate.
* **Predictable Latency**: Bounds allocation churn to prevent garbage collection pauses.
* **Comprehensive Testing**: Validated with multi-threaded stress tests.

## 3. How to Run Tests
```bash
mvn test -pl capstones -Dtest=GenerationalGcSimulatorTest
```
