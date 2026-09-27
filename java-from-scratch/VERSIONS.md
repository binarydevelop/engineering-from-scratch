# Java and Tooling Version Matrix

This repository enforces strict version discipline to ensure all code, bytecode inspections, mental models, and performance benchmarks reflect modern production Java standards rather than legacy idioms.

---

## 1. Primary Target Version

* **Primary Language Target**: **Java 21 LTS** (with forward compatibility through Java 25 LTS)
* **Bytecode Target Release**: `--release 21`
* **Current Execution & Validation Environment**:
  * **JDK Vendor**: Homebrew OpenJDK build 27 (`openjdk 27 2026-09-15`)
  * **Runtime Engine**: OpenJDK 64-Bit Server VM (build 27, mixed mode, sharing)
  * **Java Compiler**: `javac 27` (configured with `--release 21`)
  * **Build Tool**: Apache Maven `3.9.16`
  * **Host Architecture**: Apple Silicon macOS (`aarch64`, macOS `26.6.2`)

```bash
$ java -version
openjdk version "27" 2026-09-15
OpenJDK Runtime Environment Homebrew (build 27)
OpenJDK 64-Bit Server VM Homebrew (build 27, mixed mode, sharing)

$ javac -version
javac 27

$ mvn -version
Apache Maven 3.9.16 (2bdd9fddda4b155ebf8000e807eb73fd829a51d5)
Maven home: /opt/homebrew/Cellar/maven/3.9.16/libexec
Java version: 27, vendor: Homebrew
```

---

## 2. Java LTS Release Cadence & Timeline

| Release | Release Date | Support Classification | Key Modern Features Relevant to this Curriculum |
| :--- | :--- | :--- | :--- |
| **Java 8** | Mar 2014 | Legacy LTS | Lambdas, Streams, Optional, Date/Time API (`java.time`) |
| **Java 11** | Sep 2018 | Prior LTS | HTTP Client (`java.net.http`), `var` local inference, ZGC initial |
| **Java 17** | Sep 2021 | Prior LTS | Records, Sealed classes, Pattern Matching for `instanceof`, Strong Encapsulation |
| **Java 21** | Sep 2023 | **Current Core LTS** | **Virtual Threads (Project Loom)**, Sequenced Collections, Pattern Matching for `switch`, Record Patterns, Generational ZGC |
| **Java 25** | Sep 2025 | Next LTS | Flexible Constructor Bodies, Scoped Values, Structured Concurrency |

---

## 3. Scope Boundaries: Language vs. JVM vs. HotSpot

A foundational goal of `java-from-scratch` is distinguishing between three distinct layers that are often conflated:

```text
+-------------------------------------------------------------------------+
| Layer 1: Java Language Specification (JLS)                              |
| - Syntax, static type rules, definite assignment, pass-by-value semantics|
| - Definite unreachability, generics erasure rules, interface contracts  |
+-------------------------------------------------------------------------+
                                    |
                                    v (javac compiler)
+-------------------------------------------------------------------------+
| Layer 2: Java Virtual Machine Specification (JVMS)                      |
| - Bytecode instruction set (aload, invokevirtual, invokedynamic)        |
| - Classfile binary layout, constant pool structures, verification rules |
| - Abstract memory areas (Heap, Method Area, PC, Stacks)                 |
+-------------------------------------------------------------------------+
                                    |
                                    v (execution)
+-------------------------------------------------------------------------+
| Layer 3: HotSpot Virtual Machine Implementation Details                 |
| - Tiered Compilation (C1 Client / C2 Server JIT compilers)              |
| - Compressed OOPs (Ordinary Object Pointers), object header layout      |
| - Garbage collector algorithms (G1GC, ZGC, Shenandoah, Serial, Parallel)|
| - Escape analysis and scalar replacement (NOT true stack allocation)    |
| - Biased locking removal, monitor deflation, lock coarsening            |
+-------------------------------------------------------------------------+
```

### Clarified Architectural Distinctions

1. **Pass-by-Value**:
   * *Language rule*: Java is **strictly pass-by-value**. For primitive types, the actual bit value is copied. For reference types, the reference value (pointer handle) is copied. The object itself is never passed.
2. **Object Allocation & Escape Analysis**:
   * *Language rule*: Objects are conceptually created on the heap with indefinite lifetime.
   * *HotSpot detail*: When C2 escape analysis determines an object does not escape a method scope, it performs **scalar replacement**, mapping fields directly to CPU registers or stack slots. It does NOT allocate a contiguous C-struct on the stack.
3. **Generics & Type Erasure**:
   * *Language rule*: Java enforces parametric polymorphism at compile-time with covariance/contravariance rules (`? extends`, `? super`).
   * *JVM rule*: Type parameters are erased to their bounds (typically `Object`) in bytecode, with cast instructions (`checkcast`) inserted at call sites.
4. **Virtual Threads**:
   * *Language API*: `Thread.ofVirtual().start(runnable)` returns an instance of `java.lang.Thread`.
   * *JVM/HotSpot implementation*: Virtual threads are user-mode fibers mounted onto carrier platform threads pool (`ForkJoinPool`) and unmounted when parking on blocking I/O or synchronizers.

---

## 4. Modern Defaults Enforced Across All Lessons

To avoid obsolete habits, this curriculum enforces:

* **Modern Collections**: Use `List.of(...)`, `Map.of(...)`, `Set.of(...)` for unmodifiable collections; use sequenced collection APIs (`getFirst()`, `reversed()`) instead of ad-hoc indexing.
* **Modern Data Carriers**: Use `record` for transparent, immutable data aggregates.
* **Modern Date/Time**: Exclusively use `java.time.*` (`Instant`, `Duration`, `LocalDate`, `ZonedDateTime`). Never use `java.util.Date` or `java.util.Calendar`.
* **Modern Networking**: Exclusively use `java.net.http.HttpClient` with asynchronous/synchronous models. Never teach `HttpURLConnection`.
* **Modern Concurrency**:
  * Use `Executors.newVirtualThreadPerTaskExecutor()` for high-throughput I/O.
  * Use `CompletableFuture` for asynchronous composition.
  * Use `ReentrantLock` and `java.util.concurrent` synchronizers over raw `wait()`/`notify()`.
* **Modern I/O**: Exclusively use `java.nio.file.Path` and `java.nio.file.Files`.
* **Modern Serialization**: Use standard JSON (`org.json` or Jackson) or byte buffers. Do NOT treat `java.io.Serializable` as a modern default.

---

## 5. Verification Commands

Run these commands in your shell to verify your setup matches the required environment:

```bash
# Verify compiler support for target release
javac --release 21 -version

# Verify preview features availability
java --enable-preview --version

# Verify JVM vendor flags
java -XX:+PrintFlagsFinal -version | grep -E "UseG1GC|UseZGC|CompressedClassPointers"
```
