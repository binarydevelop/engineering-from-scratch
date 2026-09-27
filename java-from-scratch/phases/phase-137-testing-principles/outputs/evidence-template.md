# Evidence Log: Phase 137 - Testing from First Principles

- **Lesson**: Phase 137 - Testing from First Principles
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase137/Phase137Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-137-testing-principles/src/main/java/io/github/javafromscratch/phase137/Phase137Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase137.Phase137Demo`
- **Expected Output**: `Executed Testing from First Principles: A test is an executable assertion that verifies an invariant under controlled conditions.`
- **Actual Output**: `Executed Testing from First Principles: A test is an executable assertion that verifies an invariant under controlled conditions.`
- **Bytecode Inspected**: `javap -c -p Phase137Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase137DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
