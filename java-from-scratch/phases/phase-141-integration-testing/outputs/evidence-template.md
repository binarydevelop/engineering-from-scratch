# Evidence Log: Phase 141 - Integration Testing & Real DBs

- **Lesson**: Phase 141 - Integration Testing & Real DBs
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase141/Phase141Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-141-integration-testing/src/main/java/io/github/javafromscratch/phase141/Phase141Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase141.Phase141Demo`
- **Expected Output**: `Executed Integration Testing & Real DBs: Unit tests verify logic; integration tests verify communication with real dependencies.`
- **Actual Output**: `Executed Integration Testing & Real DBs: Unit tests verify logic; integration tests verify communication with real dependencies.`
- **Bytecode Inspected**: `javap -c -p Phase141Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase141DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
