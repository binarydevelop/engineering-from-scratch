# Java and JVM Glossary

A precise, disambiguated technical glossary of core terms across the Java language, Java Virtual Machine (JVM), and HotSpot execution engine.

---

### A
* **Abstract Syntax Tree (AST)**: An intermediate hierarchical tree representation of Java source code produced by the compiler (`javac`) during syntactic analysis prior to semantic attribution and bytecode generation.
* **Access Flags**: Bitmasks in a compiled `.class` file specifying access permissions and properties for classes, fields, and methods (e.g., `ACC_PUBLIC`, `ACC_FINAL`, `ACC_SYNCHRONIZED`).
* **Atomic Operation**: An operation that completes in a single discrete step relative to other threads; it cannot be observed in an intermediate or partially completed state.
* **Autoboxing / Unboxing**: The compiler-driven automatic conversion between primitive types (e.g., `int`) and their corresponding object wrapper types (e.g., `Integer`), utilizing `Integer.valueOf(int)` and `Integer.intValue()`.

### B
* **Biased Locking**: A historical HotSpot lock optimization where a monitor was biased towards the first thread that acquired it, avoiding atomic compare-and-swap operations until contention occurred. Deprecated in Java 15 and obsolete in modern HotSpot runtimes.
* **Boot ClassLoader**: The foundational JVM class loader responsible for loading core platform classes (`java.base`). In modern modular Java, it is implemented directly within the VM kernel in C/C++.
* **Bytecode**: The platform-independent instruction set of the Java Virtual Machine. Bytecodes are 1-byte opcodes followed by zero or more operands, executed on an abstract stack machine.

### C
* **C1 Compiler (Client Compiler)**: A high-speed, lightweight JIT compiler that quickly compiles hot bytecode into native code with basic optimizations (inlining, simple devirtualization) to reduce application startup latency.
* **C2 Compiler (Server Compiler)**: An aggressive, optimizing JIT compiler that performs deep static analysis, loop unrolling, global value numbering, escape analysis, and speculative profile-guided optimizations for maximum steady-state throughput.
* **Card Table**: A byte array maintained by the JVM garbage collector where each byte ("card") corresponds to a 512-byte region of the heap. When an old-generation object is modified to point to a young-generation object, its corresponding card is dirtied to allow generational GC without scanning the entire old generation.
* **CAS (Compare-And-Swap)**: A hardware-level atomic CPU instruction (`CMPXCHG` on x86/ARM) that updates a memory location only if it currently holds an expected value, forming the foundation of lock-free data structures in `java.util.concurrent.atomic`.
* **Class Invariant**: A condition or constraint that must always evaluate to true for every valid instance of a class throughout its entire lifetime.
* **Compressed OOPs (Ordinary Object Pointers)**: A 64-bit JVM optimization enabled when max heap is below 32GB (`-XX:+UseCompressedOops`) that represents 64-bit heap object pointers as 32-bit unsigned integers by exploiting 8-byte object alignment.
* **Constant Pool**: A per-class lookup table within the compiled `.class` file containing symbolic references to classes, interfaces, method names, field descriptors, and string/numeric literals.

### D
* **Deadlock**: A permanent failure condition where two or more threads are unable to proceed because each is waiting to acquire a lock or resource held by another thread in the set, forming a circular wait cycle.
* **Defensive Copying**: The defensive programming practice of creating copies of mutable objects passed into or returned from an object to protect internal state encapsulation and immutability.
* **Devirtualization**: A JIT compiler optimization where a dynamic method dispatch (`invokevirtual` or `invokeinterface`) is replaced with a direct native jump or static call when profiling reveals only a single concrete implementation is invoked (monomorphic call site).

### E
* **Ephemeral Port**: A temporary, short-lived transport-layer port assigned automatically by the operating system kernel for the client side of a TCP connection.
* **Escape Analysis**: A static compiler analysis performed by the C2 JIT compiler to determine if the reference to a newly allocated object escapes the executing method or the allocating thread.
* **Execution Stack**: Per-thread runtime memory region holding activation frames (stack frames) for active method invocations.

### F
* **False Sharing**: A performance degradation occurring when two independent variables accessed concurrently by different CPU cores reside on the same 64-byte hardware CPU cache line, forcing continuous cache coherency invalidations.
* **Finalizer**: The obsolete and dangerous `finalize()` mechanism in `java.lang.Object`, deprecated since Java 9 and fundamentally superseded by `java.lang.ref.Cleaner` and `AutoCloseable`.
* **ForkJoinPool**: An implementation of `ExecutorService` built upon work-stealing algorithms where idle worker threads steal tasks from the deques of busy threads, powering Parallel Streams and Virtual Threads.

### G
* **Garbage Collection (GC)**: The automated runtime process of reclaiming memory occupied by objects that are no longer reachable from any GC root.
* **GC Root**: An anchor point in JVM runtime memory that is unconditionally considered live (e.g., active thread local variable references, active JNI handles, static class fields, JVM system dictionary classes).
* **Generational ZGC**: A modern, concurrent, low-pause garbage collector in JDK 21+ that separates the heap into young and old generations while executing marking, relocation, and reference updating concurrently with application threads, bounding pause times to under 1 millisecond.

### H
* **Happens-Before Relationship**: A formal partial order defined by the Java Memory Model (JMM). If action $A$ happens-before action $B$, then the memory writes performed by $A$ are guaranteed to be visible to action $B$, and $A$ is ordered before $B$.
* **Heap**: The shared JVM runtime data area from which memory for all class instances and arrays is allocated.
* **HotSpot**: The predominant reference JVM implementation originally created by Longview Technologies and maintained by Oracle and the OpenJDK community, characterized by dynamic adaptive optimization.

### I
* **Intrinsic Function**: A method implementation provided directly by the JVM using hand-crafted, architecture-specific machine code sequences rather than compiled bytecode (e.g., `Math.sin()`, `System.arraycopy()`, `String.compareTo()`).
* **`invokedynamic` (Indy)**: A bytecode instruction introduced in Java 7 to support dynamically typed languages and used extensively since Java 8 for lambda meta-factories, string concatenation, and record serialization.
* **`invokeinterface`**: Bytecode instruction used to invoke a method declared in a Java interface, requiring runtime interface table (itable) resolution.
* **`invokespecial`**: Bytecode instruction used for direct, non-virtual invocation of private methods, constructors (`<init>`), and `super` method calls.
* **`invokestatic`**: Bytecode instruction used to invoke a static method bound directly at compile time.
* **`invokevirtual`**: Bytecode instruction used for standard public and protected instance method calls, dispatched dynamically using a virtual method table (vtable).

### J
* **Java Memory Model (JMM)**: The formal specification (JLS Chapter 17) governing how threads interact through shared memory, establishing visibility, ordering, atomicity, and synchronization guarantees.
* **JIT (Just-In-Time) Compiler**: A runtime subsystem that compiles frequently executed ("hot") bytecode sequences into native host CPU instructions during execution.
* **JMH (Java Microbenchmark Harness)**: The standard benchmarking framework created by OpenJDK engineers to measure JVM performance while defending against dead-code elimination, constant folding, and warmup artifacts.
* **JNI (Java Native Interface)**: The foreign interface mechanism allowing Java code running in the JVM to interoperate with applications and libraries written in native languages (C/C++).

### L
* **Livelock**: A concurrency bug where two or more threads continuously change their states in response to each other without making any functional forward progress, consuming 100% CPU.
* **Lock Coarsening**: A JIT optimization that merges adjacent synchronized blocks operating on the same monitor into a single larger lock region to reduce lock acquisition overhead.
* **Lock Elision**: A JIT optimization where synchronization operations on a monitor are completely eliminated after escape analysis proves the locked object never escapes the current thread.

### M
* **Mark Word**: The first header word of every Java heap object containing runtime metadata including hash code, GC age bits, biased lock flags, and locking pointers.
* **Metaspace**: Native memory region (replacing the legacy PermGen in Java 8) used by the JVM to store class metadata, method bytecode representations, constant pools, and annotations.
* **Monomorphic Call Site**: A method call location in bytecode that historically executes against exactly one concrete class implementation, enabling direct inlining by the JIT compiler.

### O
* **Operand Stack**: A pushdown stack within a thread's stack frame used to hold intermediate values for bytecode instructions and parameters for method calls.
* **OutOfMemoryError (OOM)**: An unchecked JVM error thrown when the runtime environment cannot allocate an object because available memory is exhausted and no further memory can be reclaimed by garbage collection.

### P
* **PECS**: A mnemonic rule for Java generics wildcards: **Producer Extends, Consumer Super**. Use `? extends T` when your collection produces values (read-only); use `? super T` when your collection consumes values (write-only).
* **PhantomReference**: A reference type enqueued only after its referent has been finalized and its memory reclaimed, used for resource cleanup tracking via `ReferenceQueue`.
* **Platform Thread**: A traditional Java thread (`Thread`) that maps 1-to-1 to an underlying operating system kernel thread.

### R
* **Race Condition**: A concurrency flaw where the correctness of a program depends on the relative timing or non-deterministic interleaving of multiple concurrent threads.
* **Record**: A transparent carrier for immutable data introduced in Java 16 where the compiler automatically generates private final fields, canonical constructor, accessors, `equals()`, `hashCode()`, and `toString()`.

### S
* **Scalar Replacement**: A JIT compiler optimization based on escape analysis where an aggregate object is decomposed into its individual scalar fields, avoiding heap allocation and placing values directly in CPU registers.
* **Safepoint**: A designated location in compiled code or bytecode interpretation where an application thread can be safely paused to allow the JVM to perform global operations (e.g., stop-the-world GC phases, thread dumps, deoptimization).
* **Sequenced Collection**: An interface hierarchy introduced in Java 21 (`SequencedCollection`, `SequencedSet`, `SequencedMap`) providing defined first/last element access and reversed views.
* **Stop-The-World (STW)**: A JVM execution pause where all application mutator threads are suspended at safepoints to allow garbage collection or runtime servicing without concurrent mutation.

### T
* **Thread-Local Storage (`ThreadLocal`)**: A mechanism that provides independent, isolated copies of a variable for each thread accessing it.
* **Tiered Compilation**: HotSpot's default compilation strategy combining the fast startup of the interpreter and C1 client compiler with the high peak optimization of the C2 server compiler.
* **Type Erasure**: The compile-time process by which the Java compiler removes all generic type parameter information, replacing them with raw bounds and inserting synthetic casts for bytecode compatibility.

### V
* **Virtual Method Table (vtable)**: An internal JVM dispatch table associated with each loaded class, containing pointers to the concrete method implementations used for dynamic dispatch (`invokevirtual`).
* **Virtual Thread**: A lightweight, user-mode thread managed directly by the JVM runtime rather than the OS kernel, allowing millions of concurrent tasks to execute efficiently without thread pool exhaustion.
* **Volatile**: A Java field modifier guaranteeing that all reads and writes are performed directly against main memory (establishing visibility) and preventing instruction reordering across the access boundary via memory fences.
