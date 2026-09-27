# Evidence Log: Phase 199 - Java in Modern Backend Engineering

- **Lesson**: Phase 199 - Java in Modern Backend Engineering
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase199/Phase199Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-199-java-backend-eng/src/main/java/io/github/javafromscratch/phase199/Phase199Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase199.Phase199Demo`
- **Expected Output**: `Executed Java in Modern Backend Engineering: Connect Java to Linux OS primitives, epoll, and cloud clusters.`
- **Actual Output**: `Executed Java in Modern Backend Engineering: Connect Java to Linux OS primitives, epoll, and cloud clusters.`
- **Bytecode Inspected**: `javap -c -p Phase199Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase199DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
