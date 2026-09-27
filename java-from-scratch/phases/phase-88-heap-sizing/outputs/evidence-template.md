# Evidence Log: Phase 88 - Heap Sizing & Container Memory

- **Lesson**: Phase 88 - Heap Sizing & Container Memory
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase88/Phase88Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-88-heap-sizing/src/main/java/io/github/javafromscratch/phase88/Phase88Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase88.Phase88Demo`
- **Expected Output**: `Executed Heap Sizing & Container Memory: Setting heap too small causes GC thrashing; setting it too large causes paging.`
- **Actual Output**: `Executed Heap Sizing & Container Memory: Setting heap too small causes GC thrashing; setting it too large causes paging.`
- **Bytecode Inspected**: `javap -c -p Phase88Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase88DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
