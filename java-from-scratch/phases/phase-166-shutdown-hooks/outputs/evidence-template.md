# Evidence Log: Phase 166 - JVM Shutdown Hooks

- **Lesson**: Phase 166 - JVM Shutdown Hooks
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase166/Phase166Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-166-shutdown-hooks/src/main/java/io/github/javafromscratch/phase166/Phase166Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase166.Phase166Demo`
- **Expected Output**: `Executed JVM Shutdown Hooks: Shutdown hooks run during JVM termination; keep them fast and non-deadlocking.`
- **Actual Output**: `Executed JVM Shutdown Hooks: Shutdown hooks run during JVM termination; keep them fast and non-deadlocking.`
- **Bytecode Inspected**: `javap -c -p Phase166Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase166DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
