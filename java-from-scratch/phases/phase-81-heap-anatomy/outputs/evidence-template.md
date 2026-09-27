# Evidence Log: Phase 81 - The Heap & Compressed OOPs

- **Lesson**: Phase 81 - The Heap & Compressed OOPs
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase81/Phase81Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-81-heap-anatomy/src/main/java/io/github/javafromscratch/phase81/Phase81Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase81.Phase81Demo`
- **Expected Output**: `Executed The Heap & Compressed OOPs: Heap memory is managed globally; compressed OOPs save 40% memory below 32GB.`
- **Actual Output**: `Executed The Heap & Compressed OOPs: Heap memory is managed globally; compressed OOPs save 40% memory below 32GB.`
- **Bytecode Inspected**: `javap -c -p Phase81Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase81DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
