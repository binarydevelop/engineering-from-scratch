# How to Learn Java from First Principles

> **Motto**: Understand it. Compile it. Run it. Inspect it. Break it. Debug it. Measure it. Ship it.

This curriculum is not a collection of syntax summaries or LeetCode recipes. It is an engineering apprenticeship in understanding Java as both a statically typed programming language and a high-performance runtime platform (the Java Virtual Machine).

---

## 1. The Core Learning Loop

For every concept, phase, and exercise in this repository, follow this systematic fourteen-step cycle:

```text
    ┌──────────────┐
    │   Problem    │  Why does this mechanism exist? What breaks without it?
    └──────┬───────┘
           │
           ▼
    ┌──────────────┐
    │   Predict    │  State what compiler/JVM will do BEFORE touching the keyboard.
    └──────┬───────┘
           │
           ▼
    ┌──────────────┐
    │    Write     │  Author complete, self-contained Java source code.
    └──────┬───────┘
           │
           ▼
    ┌──────────────┐
    │   Compile    │  Run javac manually. Observe compilation errors and classfiles.
    └──────┬───────┘
           │
           ▼
    ┌──────────────┐
    │     Run      │  Execute on the JVM. Observe output, exit codes, and crashes.
    └──────┬───────┘
           │
           ▼
    ┌──────────────┐
    │   Inspect    │  Use javap, jcmd, jstack, and JFR. Look underneath the source.
    └──────┬───────┘
           │
           ▼
    ┌──────────────┐
    │    Break     │  Intentionally corrupt invariants, cause races, trigger leaks.
    └──────┬───────┘
           │
           ▼
    ┌──────────────┐
    │    Debug     │  Read stack traces, analyze thread dumps, trace references.
    └──────┬───────┘
           │
           ▼
    ┌──────────────┐
    │   Measure    │  Benchmark using JMH, monitor GC pauses, track allocation rate.
    └──────┬───────┘
           │
           ▼
    ┌──────────────┐
    │   Explain    │  Articulate the exact JLS rule or HotSpot behavior in your own words.
    └──────────────┘
```

---

## 2. Non-Negotiable Rules for the Learner

### Rule 1: Compile Manually Early
Do not hide behind an IDE's "Play" button in early phases. You must manually invoke `javac` and `java` on the command line. You must understand classpath (`-cp`), sourcepath, package directory structures, and classfile formats before allowing Maven to automate them.

### Rule 2: Predict Before Executing
Never run code blindly. If you cannot predict the exact output, compiler diagnostic, or exception before hitting enter, you do not yet understand the code. Stop, re-read the code, draw the memory graph, and make a written prediction.

### Rule 3: Inspect Bytecode (`javap`)
Java source code is an abstraction. The JVM only sees bytecode. Disassemble compiled classes with:
```bash
javap -c -v -p MyClass.class
```
Observe how the operand stack works, what `invokevirtual` does, how string concatenation compiles, and how generics disappear under type erasure.

### Rule 4: Draw Memory Graphs (Stack vs. Heap)
Whenever you work with references, primitives, or objects:
* Draw the thread stack with local variable frames.
* Draw the heap with object instances, mark words, and field references.
* Trace reference copies to internalize that **Java is strictly pass-by-value**.

### Rule 5: Deliberately Trigger and Study Failures
A mechanism is only understood when you know how it fails:
* Trigger `NullPointerException` and trace the chained access.
* Trigger `ConcurrentModificationException` during collection iteration.
* Trigger `OutOfMemoryError: Java heap space` and analyze a heap dump.
* Induce deadlocks and extract thread dumps with `jcmd` or `jstack`.

### Rule 6: Master Low-Level Primitives Before Higher Abstractions
We follow a strict bottom-up order:
* Sockets **before** HTTP servers.
* Raw threads and monitors (`synchronized`) **before** `ExecutorService` and `CompletableFuture`.
* Raw `wait()`/`notify()` **before** `BlockingQueue`.
* Raw JDBC with manual `PreparedStatement` and transactions **before** ORMs (Hibernate/JPA).
* Plain Java interfaces and reflection **before** Dependency Injection frameworks (Spring).

### Rule 7: Profile Before Optimizing
Never declare "Java is slow" or "this code needs optimization" based on intuition. Measure using JMH (Java Microbenchmark Harness). Inspect JIT compilation tiers, escape analysis, and GC pause times before changing a single line for performance.

### Rule 8: Rebuild Implementations from Scratch Without Notes
To confirm mastery:
1. Close the browser and editor tabs.
2. Open an empty file.
3. Re-implement `ArrayList` (dynamic array resizing), `HashMap` (bucket hash collisions), an LRU Cache, or a Bounded Blocking Queue using low-level primitives.
4. If you get stuck, study the principles, delete your code, and rebuild again tomorrow.

### Rule 9: Never Proceed While JVM Behavior Feels Magical
If something runs and you do not know *why* it behaved that way, do not advance to the next phase. Is it a language rule? A JVM specification constraint? Or a HotSpot JIT optimization? Find out, record the evidence, and only then proceed.
