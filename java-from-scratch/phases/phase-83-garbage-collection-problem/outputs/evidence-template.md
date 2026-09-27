# Evidence Log: Phase 83 - The Garbage Collection Problem

- **Lesson**: Phase 83 - The Garbage Collection Problem
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase83/Phase83Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-83-garbage-collection-problem/src/main/java/io/github/javafromscratch/phase83/Phase83Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase83.Phase83Demo`
- **Expected Output**: `Executed The Garbage Collection Problem: Manual memory management leads to leaks and dangling pointers; GC guarantees safety.`
- **Actual Output**: `Executed The Garbage Collection Problem: Manual memory management leads to leaks and dangling pointers; GC guarantees safety.`
- **Bytecode Inspected**: `javap -c -p Phase83Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase83DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
