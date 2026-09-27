# Evidence Log: Phase 92 - Threads from First Principles

- **Lesson**: Phase 92 - Threads from First Principles
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase92/Phase92Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-92-threads-foundations/src/main/java/io/github/javafromscratch/phase92/Phase92Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase92.Phase92Demo`
- **Expected Output**: `Executed Threads from First Principles: A thread is an independent execution context sharing memory with other threads.`
- **Actual Output**: `Executed Threads from First Principles: A thread is an independent execution context sharing memory with other threads.`
- **Bytecode Inspected**: `javap -c -p Phase92Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase92DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
