# java-from-scratch

> **Understand it. Compile it. Run it. Inspect it. Break it. Debug it. Measure it. Ship it.**

An uncompromising, first-principles curriculum designed to teach the Java programming language and the Java Virtual Machine (JVM) from source code to machine execution.

---

## What This Repository Is

**This is NOT a Java syntax tutorial.**  
**This is NOT a LeetCode problem catalog.**  
**This is NOT a Spring Boot quickstart.**

This is a comprehensive, hands-on engineering course designed to build an unshakable mental model of Java as both a **statically typed programming language** and a **high-performance runtime platform** with advanced memory management, concurrency, dynamic JIT compilation, and OS-level interactions.

By the end of this curriculum, you will look at any Java source file and trace its journey from syntax down to hardware:

```text
Main.java
   │
   ▼ (javac compiler)
.class Bytecode
   │
   ▼ (ClassLoader hierarchy)
JVM Class Loading & Verification
   │
   ▼ (Interpreter / C1 / C2 JIT Compilers)
Native Machine Code (x86 / ARM)
   │
   ▼ (Runtime Memory Areas)
Heap / Stacks / Metaspace / Threads
   │
   ▼ (Automatic Memory Management)
Garbage Collection (G1GC / Generational ZGC)
   │
   ▼ (Kernel Syscalls)
Native OS & Hardware Interaction
```

---

## Core Progression

```text
Source Code
   │
   ▼
Types & Memory Stacks
   │
   ▼
Methods & Frame Execution
   │
   ▼
Objects & Heap Layout
   │
   ▼
Object-Oriented Design & Invariants
   │
   ▼
Collections from Scratch (Dynamic Arrays & Hash Tables)
   │
   ▼
Generics, Wildcards, & Type Erasure
   │
   ▼
Exceptions & Stack Unwinding
   │
   ▼
I/O Streams, Bytes, Encodings, & NIO
   │
   ▼
Functional Java, Lambdas, & Stream Pipelines
   │
   ▼
Reflection, Annotations, & Dynamic Class Loading
   │
   ▼
JVM Memory Anatomy & Escape Analysis
   │
   ▼
Garbage Collection & Memory Leak Forensics
   │
   ▼
Threads, Race Conditions, & Monitors
   │
   ▼
The Java Memory Model (Happens-Before & Visibility)
   │
   ▼
Executors, CompletableFuture, & Modern Virtual Threads (Loom)
   │
   ▼
TCP Sockets, HTTP/1.1 Servers, & JSON Serialization
   │
   ▼
Raw JDBC, Transactions, & Connection Pools
   │
   ▼
Build Tooling (Maven), Packaging, & Classpaths
   │
   ▼
Testing Disciplines, Fakes, & Mocking
   │
   ▼
Benchmarking (JMH) & Production Profiling (JFR / JMC)
   │
   ▼
Production Java & Framework Demystification
```

---

## Target Mental Model

The central thesis of this curriculum is:

> **Java is a statically typed programming language executed by the JVM, with strong runtime services for memory management, concurrency, dynamic optimization, and portability.**

You will never view Java as "just syntax and classes." You will understand:
* Why Java is **strictly pass-by-value**, and why passing an object reference copies the address bits.
* Why `volatile` guarantees memory visibility and instruction ordering, but **fails** to make compound operations like `count++` atomic.
* Why two threads mutating a shared counter produce incorrect totals without synchronization.
* How dynamic method dispatch (`invokevirtual`) resolves methods at runtime using class **vtables**.
* Why mutating an object after adding it to a `HashSet` or `HashMap` causes it to vanish from searches.
* How **Generics Type Erasure** strips type parameters at compile-time and inserts synthetic cast bytecodes.
* Why **Generational Garbage Collection** relies on the Weak Generational Hypothesis, and why memory leaks can still occur in garbage-collected languages.
* Why creating 10,000 platform threads exhausts OS memory, while 1,000,000 **Virtual Threads** run smoothly on the JVM heap.
* How frameworks like Spring, Hibernate, and JUnit operate underneath by combining **reflection, annotations, dynamic bytecode generation, and socket loops**.

---

## Repository Structure

```text
java-from-scratch/
├── README.md               # Curriculum manifesto and quickstart
├── ROADMAP.md              # Exhaustive guide across all 201 phases
├── LEARNING.md             # The 14-step learning loop and study rules
├── LESSON_TEMPLATE.md      # Standard lesson format
├── VERSIONS.md             # Version discipline (Java 21 LTS, HotSpot)
├── CONTRIBUTING.md         # Contribution standards
├── pom.xml                 # Root multi-module Maven configuration
│
├── scripts/                # Verification, build, and test automation
│   ├── check-environment.sh
│   ├── build-all.sh
│   ├── run-tests.sh
│   ├── run-broken-labs.sh
│   ├── run-capstones.sh
│   └── inspect-bytecode.sh
│
├── docs/                   # Authoritative reference guides
│   ├── glossary.md         # Precise technical terms
│   ├── mental-models.md    # Core architecture diagrams
│   ├── jvm-guide.md        # Class loading, JIT, object layout, and GC
│   ├── concurrency-guide.md# JMM, happens-before, atomics, and virtual threads
│   ├── debugging.md        # jcmd, thread dumps, stack traces, and leaks
│   └── performance.md      # JMH, JFR profiling, and allocation tuning
│
├── phases/                 # Phases 00 to 200 (Foundations to Mastery)
├── exercises/              # 200+ practical exercises with separate solutions
├── broken-programs/        # 35+ realistic broken-Java debugging labs
├── projects/               # 16 complete production-grade applications
├── capstones/              # 5 deep JVM & Concurrency Capstone systems
├── benchmarks/             # JMH microbenchmarks defeating JIT optimizations
├── katas/                  # Repetition katas for muscle memory
└── outputs/                # Structured evidence logs from actual runs
```

---

## Quickstart: Your First Commands

### 1. Verify Your Environment
Before starting, ensure your system has JDK 21+ and Maven installed:

```bash
./scripts/check-environment.sh
```

### 2. Begin Phase 00 & Phase 01: From Source to Bytecode
Compile and disassemble your first Java program manually without an IDE:

```bash
# Compile with strict release flags
javac --release 21 -d target/classes phases/phase-01-source-to-bytecode/src/Hello.java

# Run on the JVM
java -cp target/classes Hello

# Inspect the compiled bytecode
javap -c -v -p target/classes/Hello.class
```

### 3. Build All Modules & Run Automated Tests
```bash
./scripts/build-all.sh
./scripts/run-tests.sh
```

---

## The 14-Step Lesson Methodology

Every lesson in `phases/` follows this rigorous structure:

```text
MOTTO ──► PROBLEM ──► PREDICT ──► FIRST PRINCIPLES ──► MENTAL MODEL
  ──► IMPLEMENT ──► COMPILE ──► RUN ──► INSPECT (javap) ──► TEST (JUnit 5)
  ──► BREAK IT ──► DEBUG IT ──► MEASURE IT ──► EVIDENCE
```

A lesson is **never complete** simply because the code compiles. You must predict its behavior, inspect its bytecode, intentionally break it, debug the failure with runtime tools, measure its performance, and record concrete empirical evidence.

---

## License

This educational repository is open source under the [MIT License](LICENSE).
