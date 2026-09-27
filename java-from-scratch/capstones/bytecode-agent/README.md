# Capstone: Dynamic Bytecode Instrumenter & Execution Tracer

> **Overview:** A Java agent and bytecode inspector demonstrating classfile byte manipulation, method entry/exit profiling hooks, and ClassFile API inspections.

---

## 1. Architectural Blueprint
This capstone implements an enterprise-grade system designed to operate under heavy concurrency while respecting JVM memory boundaries and hardware constraints.

## 2. Invariants & Design Principles
* **Non-Blocking Execution**: Maximizes CPU cache locality and non-blocking algorithms where appropriate.
* **Predictable Latency**: Bounds allocation churn to prevent garbage collection pauses.
* **Comprehensive Testing**: Validated with multi-threaded stress tests.

## 3. How to Run Tests
```bash
mvn test -pl capstones -Dtest=BytecodeTracerAgentTest
```
