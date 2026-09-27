# Evidence Log: Phase 112 - Resource Throttling: Semaphore

- **Lesson**: Phase 112 - Resource Throttling: Semaphore
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase112/Phase112Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-112-semaphores/src/main/java/io/github/javafromscratch/phase112/Phase112Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase112.Phase112Demo`
- **Expected Output**: `Executed Resource Throttling: Semaphore: A semaphore bounds concurrent access to physical resources.`
- **Actual Output**: `Executed Resource Throttling: Semaphore: A semaphore bounds concurrent access to physical resources.`
- **Bytecode Inspected**: `javap -c -p Phase112Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase112DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
