# Evidence Log: Phase 172 - Project 2: Banking Domain Engine

- **Lesson**: Phase 172 - Project 2: Banking Domain Engine
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase172/Phase172Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-172-proj-banking-domain/src/main/java/io/github/javafromscratch/phase172/Phase172Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase172.Phase172Demo`
- **Expected Output**: `Executed Project 2: Banking Domain Engine: Implement strict invariant validation, Money, and concurrent transfers.`
- **Actual Output**: `Executed Project 2: Banking Domain Engine: Implement strict invariant validation, Money, and concurrent transfers.`
- **Bytecode Inspected**: `javap -c -p Phase172Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase172DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
