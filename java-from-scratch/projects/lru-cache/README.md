# Project: Generic Thread-Safe LRU Cache

> **Core Focus:** HashMap + DoublyLinkedList, generic <K,V>, ReentrantLock mutual exclusion

---

## 1. Architectural Overview
This system is designed from first principles using modern Java 21 LTS constructs.
It avoids opaque framework abstractions to expose raw threading, data structures, and memory behaviors.

## 2. Invariants & Guarantees
* **Correctness**: Enforces class invariants via defensive constructors.
* **Thread Safety**: Uses proper memory barriers (`volatile`, `ReentrantLock`, or lock-free atomics).
* **Resource Cleanup**: Conforms to `AutoCloseable` for clean resource reclamation.

## 3. Running and Testing
Run automated unit and integration tests:
```bash
mvn test -pl projects -Dtest=LruCacheTest
```
