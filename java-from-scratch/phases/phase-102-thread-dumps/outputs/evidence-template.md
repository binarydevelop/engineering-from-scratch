# Evidence Log: Phase 102 - Thread Dumps & Deadlock Analysis

- **Lesson**: Phase 102 - Thread Dumps & Deadlock Analysis
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase102/Phase102Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-102-thread-dumps/src/main/java/io/github/javafromscratch/phase102/Phase102Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase102.Phase102Demo`
- **Expected Output**: `Executed Thread Dumps & Deadlock Analysis: A thread dump cuts through deadlocks and stuck threads instantly.`
- **Actual Output**: `Executed Thread Dumps & Deadlock Analysis: A thread dump cuts through deadlocks and stuck threads instantly.`
- **Bytecode Inspected**: `javap -c -p Phase102Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase102DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
