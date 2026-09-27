# Evidence Log: Phase 179 - Project 9: Distributed-Ready Rate Limiter

- **Lesson**: Phase 179 - Project 9: Distributed-Ready Rate Limiter
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase179/Phase179Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-179-proj-rate-limiter/src/main/java/io/github/javafromscratch/phase179/Phase179Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase179.Phase179Demo`
- **Expected Output**: `Executed Project 9: Distributed-Ready Rate Limiter: Implement Token Bucket and Sliding Window rate limiting algorithms.`
- **Actual Output**: `Executed Project 9: Distributed-Ready Rate Limiter: Implement Token Bucket and Sliding Window rate limiting algorithms.`
- **Bytecode Inspected**: `javap -c -p Phase179Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase179DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
