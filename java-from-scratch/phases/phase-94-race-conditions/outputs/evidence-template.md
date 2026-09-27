# Evidence Log: Phase 94 - Race Conditions & Data Races

- **Lesson**: Phase 94 - Race Conditions & Data Races
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase94/Phase94Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-94-race-conditions/src/main/java/io/github/javafromscratch/phase94/Phase94Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase94.Phase94Demo`
- **Expected Output**: `Executed Race Conditions & Data Races: When concurrent threads mutate shared state without synchronization, chaos ensues.`
- **Actual Output**: `Executed Race Conditions & Data Races: When concurrent threads mutate shared state without synchronization, chaos ensues.`
- **Bytecode Inspected**: `javap -c -p Phase94Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase94DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
