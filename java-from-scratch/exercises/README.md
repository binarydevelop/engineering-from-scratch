# 205 Practical Java & JVM Exercises

A comprehensive suite of 205 rigorous exercises spanning language fundamentals, object-oriented engineering, collections, generics, the Java Memory Model, JVM internals, concurrency, and networking.

## Exercise Categories

| ID Range | Category | Topics Covered |
| :--- | :--- | :--- |
| **001 - 015** | Language Basics & Primitives | Bitwise operations, overflow, two's complement, casts |
| **016 - 030** | Control Flow & Methods | Switch expressions, stack frames, pass-by-value |
| **031 - 045** | Arrays & Strings | Bounds checks, string pool, compact strings, StringBuilder |
| **046 - 060** | OOP, Encapsulation & Records | Invariant enforcement, defensive copying, modern records |
| **061 - 075** | Inheritance, Polymorphism & Interfaces | Dynamic dispatch, vtables, composition, contracts |
| **076 - 090** | Object Contracts | equals, hashCode, identity vs value, hash buckets |
| **091 - 110** | Collections Framework | ArrayList, LinkedList, HashMap, ArrayDeque, PriorityQueue |
| **111 - 125** | Generics & Type Erasure | Invariance, wildcards, PECS, bytecode bridge methods |
| **126 - 140** | Exceptions & Resource Management | Exception tables, suppressed exceptions, AutoCloseable |
| **141 - 155** | I/O, NIO & Encodings | UTF-8 encodings, ByteBuffer, zero-copy FileChannel |
| **156 - 170** | Functional Programming & Streams | Functional interfaces, lambdas, lazy collectors |
| **171 - 185** | Concurrency, JMM & Atomics | Race conditions, happens-before, volatile, ReentrantLock |
| **186 - 195** | Virtual Threads & Concurrency | Carrier mounting, high-concurrency I/O, pinning |
| **196 - 200** | Networking, Sockets & JDBC | Sockets, HTTP/1.1 parsing, raw JDBC transactions |
| **201 - 205** | JVM Diagnostics, GC & Profiling | Heap dump inspection, GC logs, allocation profiling |

## How to Work on Exercises

1. Navigate to the specification: `exercises/specs/ex-XXX.md`.
2. Review the problem, requirements, and invariants.
3. Implement your solution in `exercises/src/main/java/...`.
4. Run the automated tests: `mvn test -pl exercises -Dtest=ExerciseXXXTest`.
5. Compare your implementation with the reference solution in `exercises/solutions/ex-XXX-solution.md`.
