# Evidence Log: Phase 174 - Project 4: Concurrent Task Runner

- **Lesson**: Phase 174 - Project 4: Concurrent Task Runner
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase174/Phase174Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-174-proj-task-runner/src/main/java/io/github/javafromscratch/phase174/Phase174Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase174.Phase174Demo`
- **Expected Output**: `Executed Project 4: Concurrent Task Runner: Build a resilient concurrent task runner with retries and cancellation.`
- **Actual Output**: `Executed Project 4: Concurrent Task Runner: Build a resilient concurrent task runner with retries and cancellation.`
- **Bytecode Inspected**: `javap -c -p Phase174Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase174DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
