# Evidence Log: Phase 37 - ArrayList from Scratch

- **Lesson**: Phase 37 - ArrayList from Scratch
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase37/Phase37Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-37-array-list/src/main/java/io/github/javafromscratch/phase37/Phase37Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase37.Phase37Demo`
- **Expected Output**: `Executed ArrayList from Scratch: Contiguous memory guarantees O(1) random access and cache line locality.`
- **Actual Output**: `Executed ArrayList from Scratch: Contiguous memory guarantees O(1) random access and cache line locality.`
- **Bytecode Inspected**: `javap -c -p Phase37Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase37DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
