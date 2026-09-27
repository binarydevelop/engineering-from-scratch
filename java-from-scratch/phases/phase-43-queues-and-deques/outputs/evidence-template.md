# Evidence Log: Phase 43 - Queues and Deques

- **Lesson**: Phase 43 - Queues and Deques
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase43/Phase43Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-43-queues-and-deques/src/main/java/io/github/javafromscratch/phase43/Phase43Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase43.Phase43Demo`
- **Expected Output**: `Executed Queues and Deques: Queues enforce temporal ordering: First-In, First-Out.`
- **Actual Output**: `Executed Queues and Deques: Queues enforce temporal ordering: First-In, First-Out.`
- **Bytecode Inspected**: `javap -c -p Phase43Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase43DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
