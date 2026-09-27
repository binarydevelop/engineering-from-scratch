# Evidence Log: Phase 165 - Graceful Shutdown Architecture

- **Lesson**: Phase 165 - Graceful Shutdown Architecture
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase165/Phase165Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-165-graceful-shutdown/src/main/java/io/github/javafromscratch/phase165/Phase165Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase165.Phase165Demo`
- **Expected Output**: `Executed Graceful Shutdown Architecture: A production service must finish in-flight requests before exiting on SIGTERM.`
- **Actual Output**: `Executed Graceful Shutdown Architecture: A production service must finish in-flight requests before exiting on SIGTERM.`
- **Bytecode Inspected**: `javap -c -p Phase165Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase165DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
