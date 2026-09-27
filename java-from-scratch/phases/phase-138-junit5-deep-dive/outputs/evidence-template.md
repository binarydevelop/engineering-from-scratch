# Evidence Log: Phase 138 - Modern JUnit 5 Deep Dive

- **Lesson**: Phase 138 - Modern JUnit 5 Deep Dive
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase138/Phase138Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-138-junit5-deep-dive/src/main/java/io/github/javafromscratch/phase138/Phase138Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase138.Phase138Demo`
- **Expected Output**: `Executed Modern JUnit 5 Deep Dive: JUnit 5 structures assertions, lifecycles, and parameterized test executions.`
- **Actual Output**: `Executed Modern JUnit 5 Deep Dive: JUnit 5 structures assertions, lifecycles, and parameterized test executions.`
- **Bytecode Inspected**: `javap -c -p Phase138Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase138DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
