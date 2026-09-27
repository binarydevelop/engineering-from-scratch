# Evidence Log: Phase 181 - Project 11: Mini Dependency Injection Container

- **Lesson**: Phase 181 - Project 11: Mini Dependency Injection Container
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase181/Phase181Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-181-proj-mini-di/src/main/java/io/github/javafromscratch/phase181/Phase181Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase181.Phase181Demo`
- **Expected Output**: `Executed Project 11: Mini Dependency Injection Container: Demystify frameworks by building constructor-based dependency injection.`
- **Actual Output**: `Executed Project 11: Mini Dependency Injection Container: Demystify frameworks by building constructor-based dependency injection.`
- **Bytecode Inspected**: `javap -c -p Phase181Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase181DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
