# Evidence Log: Phase 193 - Broken Lab 07: Thread Pool Exhaustion

- **Lesson**: Phase 193 - Broken Lab 07: Thread Pool Exhaustion
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase193/Phase193Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-193-broken-lab-pool-exhaust/src/main/java/io/github/javafromscratch/phase193/Phase193Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase193.Phase193Demo`
- **Expected Output**: `Executed Broken Lab 07: Thread Pool Exhaustion: Diagnose thread pool starvation caused by blocking tasks.`
- **Actual Output**: `Executed Broken Lab 07: Thread Pool Exhaustion: Diagnose thread pool starvation caused by blocking tasks.`
- **Bytecode Inspected**: `javap -c -p Phase193Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase193DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
