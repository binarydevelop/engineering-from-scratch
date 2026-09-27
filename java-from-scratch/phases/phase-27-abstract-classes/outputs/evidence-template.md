# Evidence Log: Phase 27 - Abstract Classes

- **Lesson**: Phase 27 - Abstract Classes
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase27/Phase27Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-27-abstract-classes/src/main/java/io/github/javafromscratch/phase27/Phase27Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase27.Phase27Demo`
- **Expected Output**: `Executed Abstract Classes: An abstract class provides partial implementation and enforces template workflows.`
- **Actual Output**: `Executed Abstract Classes: An abstract class provides partial implementation and enforces template workflows.`
- **Bytecode Inspected**: `javap -c -p Phase27Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase27DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
