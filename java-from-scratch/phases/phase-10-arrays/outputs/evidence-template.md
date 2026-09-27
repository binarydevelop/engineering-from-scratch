# Evidence Log: Phase 10 - Arrays from First Principles

- **Lesson**: Phase 10 - Arrays from First Principles
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase10/Phase10Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-10-arrays/src/main/java/io/github/javafromscratch/phase10/Phase10Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase10.Phase10Demo`
- **Expected Output**: `Executed Arrays from First Principles: An array is a contiguous, fixed-size heap allocation with bounds checks.`
- **Actual Output**: `Executed Arrays from First Principles: An array is a contiguous, fixed-size heap allocation with bounds checks.`
- **Bytecode Inspected**: `javap -c -p Phase10Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase10DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
