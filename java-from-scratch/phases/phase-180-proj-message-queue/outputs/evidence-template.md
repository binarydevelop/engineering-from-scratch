# Evidence Log: Phase 180 - Project 10: In-Memory Message Broker

- **Lesson**: Phase 180 - Project 10: In-Memory Message Broker
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase180/Phase180Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-180-proj-message-queue/src/main/java/io/github/javafromscratch/phase180/Phase180Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase180.Phase180Demo`
- **Expected Output**: `Executed Project 10: In-Memory Message Broker: Build an educational pub/sub message broker with bounded queues.`
- **Actual Output**: `Executed Project 10: In-Memory Message Broker: Build an educational pub/sub message broker with bounded queues.`
- **Bytecode Inspected**: `javap -c -p Phase180Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase180DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
