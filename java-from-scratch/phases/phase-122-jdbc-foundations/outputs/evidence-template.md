# Evidence Log: Phase 122 - JDBC from First Principles

- **Lesson**: Phase 122 - JDBC from First Principles
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase122/Phase122Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-122-jdbc-foundations/src/main/java/io/github/javafromscratch/phase122/Phase122Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase122.Phase122Demo`
- **Expected Output**: `Executed JDBC from First Principles: All Java database persistence reduces to raw JDBC drivers and sockets.`
- **Actual Output**: `Executed JDBC from First Principles: All Java database persistence reduces to raw JDBC drivers and sockets.`
- **Bytecode Inspected**: `javap -c -p Phase122Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase122DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
