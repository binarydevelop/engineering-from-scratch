# Java Concurrency and Memory Model Guide

A rigorous guide to multithreading, memory ordering, synchronization, and modern concurrency architectures in Java.

---

## 1. The Concurrency Engineering Discipline

Whenever reasoning about concurrent Java code, answer these six questions before writing or debugging a single line:

1. **What state is shared across threads?** (Heap objects, static variables, cached entries)
2. **Who mutates that state?** (Single writer vs. concurrent writers)
3. **What class invariant must hold?** (e.g., `balance >= 0`, `size == items.length`)
4. **What synchronization mechanism establishes a happens-before relationship?** (`volatile`, `synchronized`, `ReentrantLock`, atomic CAS)
5. **Can state sharing be completely eliminated?** (Local stack variables, thread-confined structures, immutable records)
6. **Can immutable data structures guarantee thread safety by design?**

---

## 2. The Four Pillars of the Java Memory Model (JMM)

The JMM defines valid interactions between threads and physical computer memory:

```text
┌─────────────────┬────────────────────────────────────────────────────────┐
│ Pillar          │ Definition & Java Mechanism                            │
├─────────────────┼────────────────────────────────────────────────────────┤
│ 1. Atomicity    │ Operations happen indivisibly.                         │
│                 │ - 32-bit/64-bit primitive assignments (JLS 17.7)       │
│                 │ - Atomic CAS: AtomicInteger, AtomicReference           │
│                 │ - Critical sections: synchronized, ReentrantLock       │
├─────────────────┼────────────────────────────────────────────────────────┤
│ 2. Visibility   │ When thread A modifies state, thread B observes it.    │
│                 │ - volatile: forces CPU store buffers/cache flush.      │
│                 │ - Monitor exit releases lock and flushes caches.       │
│                 │ - Thread.start() and Thread.join() boundaries.         │
├─────────────────┼────────────────────────────────────────────────────────┤
│ 3. Ordering     │ The sequence in which operations appear to execute.    │
│                 │ - Prevents compiler/CPU instruction reordering.        │
│                 │ - Enforced via hardware memory barriers (MFENCE/DMB).  │
├─────────────────┼────────────────────────────────────────────────────────┤
│ 4. Happens-     │ A formal partial order. If A happens-before B,         │
│    Before       │ all memory writes by A are guaranteed visible to B.    │
└─────────────────┴────────────────────────────────────────────────────────┘
```

### The Canonical Happens-Before Rules (JLS §17.4.5)
1. **Program Order Rule**: Each action in a single thread happens-before every action in that thread that comes later in program order.
2. **Monitor Lock Rule**: An unlock on a monitor lock happens-before every subsequent lock on that same monitor.
3. **Volatile Variable Rule**: A write to a `volatile` field happens-before every subsequent read of that same field.
4. **Thread Start Rule**: A call to `Thread.start()` on a thread happens-before any action in the started thread.
5. **Thread Join Rule**: Any action in a thread happens-before any other thread successfully returns from `join()` on that thread.
6. **Transitivity**: If $A \to B$ and $B \to C$, then $A \to C$.

---

## 3. Synchronization Spectrum

Choose the lightest mechanism that safely guarantees correctness:

```text
Lightweight, Lock-Free                                Heavyweight, Blocking
──────────────────────────────────────────────────────────────────────────►
Immutable Record  ►  volatile Field  ►  Atomic CAS  ►  ReentrantLock  ►  synchronized
(No sharing)       (Visibility only)   (Single var)     (Fair/tryLock)    (Intrinsic)
```

### Common Trap: `volatile` Does Not Provide Compound Atomicity
```java
// BUG: Non-atomic compound check-and-act / read-modify-write!
private volatile int counter = 0;

public void increment() {
    counter++; // Bytecode: getfield, iadd, putfield (3 distinct ops!)
               // Two concurrent threads can read the same value and overwrite each other.
}

// FIX: Use AtomicInteger or synchronized
private final AtomicInteger counter = new AtomicInteger();
public void increment() {
    counter.incrementAndGet(); // Single CAS hardware loop
}
```

---

## 4. Thread Pools & Sizing Architecture

Never create raw platform threads per incoming request. A platform thread allocates ~1MB native stack space; spawning thousands exhausts OS virtual memory.

### Sizing Heuristics
* **CPU-Bound Tasks** (JSON parsing, cryptography, image encoding):
  $$N_{\text{threads}} = N_{\text{CPU cores}}$$
  Adding threads beyond CPU core count introduces wasteful context switching overhead.
* **I/O-Bound Tasks on Platform Threads** (Traditional JDBC, blocking HTTP calls):
  $$N_{\text{threads}} = N_{\text{CPU cores}} \times \left(1 + \frac{\text{Wait Time}}{\text{Service Time}}\right)$$
* **I/O-Bound Tasks on Modern Java 21+**:
  Use **Virtual Threads** (`Executors.newVirtualThreadPerTaskExecutor()`). Do not pool virtual threads; spawn a new virtual thread per task!

---

## 5. Virtual Threads (Project Loom) in Java 21+

Virtual threads decouple Java threads from OS kernel threads.

### Platform Threads vs. Virtual Threads:
```text
Dimension              Platform Thread                     Virtual Thread
---------------------------------------------------------------------------------
OS Mapping             1 : 1 (Kernel Thread)               M : N (Carrier Thread Pool)
Memory Footprint       ~1 MB native stack reserved         ~few KB on heap (dynamic)
Creation Cost          High (OS syscall, native memory)    Low (plain Java object allocation)
Context Switch Cost    High (Kernel transition, CPU cache) Low (User-mode continuation jump)
Maximum Safe Count     ~2,000 - 5,000 per JVM              1,000,000+
Pooling Recommended?   YES (via ThreadPoolExecutor)        NO! (Spawning is practically free)
```

### The Pinning Caveat in Java 21:
A virtual thread is **pinned** to its carrier platform thread when it performs a blocking operation inside:
1. A `synchronized` block or method.
2. A native JNI method.

When pinned, the carrier thread cannot unmount the virtual thread to execute other work.
* **Remedy**: Replace `synchronized` blocks that guard blocking I/O with `java.util.concurrent.locks.ReentrantLock`.
