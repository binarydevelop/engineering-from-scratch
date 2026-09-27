# Evidence Log: Phase 126 - ORM Motivation & Row Mapping

- **Lesson**: Phase 126 - ORM Motivation & Row Mapping
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase126/Phase126Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-126-orm-motivation/src/main/java/io/github/javafromscratch/phase126/Phase126Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase126.Phase126Demo`
- **Expected Output**: `Executed ORM Motivation & Row Mapping: Understand the impedance mismatch between relational tables and object graphs.`
- **Actual Output**: `Executed ORM Motivation & Row Mapping: Understand the impedance mismatch between relational tables and object graphs.`
- **Bytecode Inspected**: `javap -c -p Phase126Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase126DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
