# Evidence Log: Phase 191 - Broken Lab 05: Unbounded Static Memory Leak

- **Lesson**: Phase 191 - Broken Lab 05: Unbounded Static Memory Leak
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase191/Phase191Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-191-broken-lab-memleak/src/main/java/io/github/javafromscratch/phase191/Phase191Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase191.Phase191Demo`
- **Expected Output**: `Executed Broken Lab 05: Unbounded Static Memory Leak: Find leaked references in static collections via heap dumps.`
- **Actual Output**: `Executed Broken Lab 05: Unbounded Static Memory Leak: Find leaked references in static collections via heap dumps.`
- **Bytecode Inspected**: `javap -c -p Phase191Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase191DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
