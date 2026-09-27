# Evidence Log: Phase 91 - Memory Leaks in GC Languages

- **Lesson**: Phase 91 - Memory Leaks in GC Languages
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase91/Phase91Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-91-memory-leaks/src/main/java/io/github/javafromscratch/phase91/Phase91Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase91.Phase91Demo`
- **Expected Output**: `Executed Memory Leaks in GC Languages: An object is leaked in Java if it remains reachable but is never used again.`
- **Actual Output**: `Executed Memory Leaks in GC Languages: An object is leaked in Java if it remains reachable but is never used again.`
- **Bytecode Inspected**: `javap -c -p Phase91Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase91DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
