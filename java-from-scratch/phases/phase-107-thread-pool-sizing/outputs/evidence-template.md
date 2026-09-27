# Evidence Log: Phase 107 - Thread Pool Sizing Dynamics

- **Lesson**: Phase 107 - Thread Pool Sizing Dynamics
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase107/Phase107Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-107-thread-pool-sizing/src/main/java/io/github/javafromscratch/phase107/Phase107Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase107.Phase107Demo`
- **Expected Output**: `Executed Thread Pool Sizing Dynamics: Size CPU pools to cores; size I/O pools to blocking latency ratios.`
- **Actual Output**: `Executed Thread Pool Sizing Dynamics: Size CPU pools to cores; size I/O pools to blocking latency ratios.`
- **Bytecode Inspected**: `javap -c -p Phase107Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase107DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
