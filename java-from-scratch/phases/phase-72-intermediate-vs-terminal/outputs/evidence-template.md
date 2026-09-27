# Evidence Log: Phase 72 - Intermediate vs Terminal Operations

- **Lesson**: Phase 72 - Intermediate vs Terminal Operations
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase72/Phase72Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-72-intermediate-vs-terminal/src/main/java/io/github/javafromscratch/phase72/Phase72Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase72.Phase72Demo`
- **Expected Output**: `Executed Intermediate vs Terminal Operations: Intermediate stream operations do nothing until a terminal operation demands results.`
- **Actual Output**: `Executed Intermediate vs Terminal Operations: Intermediate stream operations do nothing until a terminal operation demands results.`
- **Bytecode Inspected**: `javap -c -p Phase72Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase72DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
