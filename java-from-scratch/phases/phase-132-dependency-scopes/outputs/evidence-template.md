# Evidence Log: Phase 132 - Maven Dependency Scopes

- **Lesson**: Phase 132 - Maven Dependency Scopes
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase132/Phase132Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-132-dependency-scopes/src/main/java/io/github/javafromscratch/phase132/Phase132Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase132.Phase132Demo`
- **Expected Output**: `Executed Maven Dependency Scopes: Scopes restrict library visibility across compilation, testing, and runtime.`
- **Actual Output**: `Executed Maven Dependency Scopes: Scopes restrict library visibility across compilation, testing, and runtime.`
- **Bytecode Inspected**: `javap -c -p Phase132Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase132DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
