# Evidence Log: Phase 71 - Stream vs Collection Architecture

- **Lesson**: Phase 71 - Stream vs Collection Architecture
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase71/Phase71Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-71-stream-vs-collection/src/main/java/io/github/javafromscratch/phase71/Phase71Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase71.Phase71Demo`
- **Expected Output**: `Executed Stream vs Collection Architecture: A collection is space-bound; a stream is time-bound and single-use.`
- **Actual Output**: `Executed Stream vs Collection Architecture: A collection is space-bound; a stream is time-bound and single-use.`
- **Bytecode Inspected**: `javap -c -p Phase71Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase71DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
