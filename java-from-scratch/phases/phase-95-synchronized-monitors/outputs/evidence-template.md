# Evidence Log: Phase 95 - Intrinsic Locks & synchronized

- **Lesson**: Phase 95 - Intrinsic Locks & synchronized
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase95/Phase95Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-95-synchronized-monitors/src/main/java/io/github/javafromscratch/phase95/Phase95Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase95.Phase95Demo`
- **Expected Output**: `Executed Intrinsic Locks & synchronized: synchronized establishes mutual exclusion and memory visibility across threads.`
- **Actual Output**: `Executed Intrinsic Locks & synchronized: synchronized establishes mutual exclusion and memory visibility across threads.`
- **Bytecode Inspected**: `javap -c -p Phase95Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase95DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
