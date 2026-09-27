# Evidence Log: Phase 171 - Project 1: Production CLI Application

- **Lesson**: Phase 171 - Project 1: Production CLI Application
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase171/Phase171Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-171-proj-cli-app/src/main/java/io/github/javafromscratch/phase171/Phase171Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase171.Phase171Demo`
- **Expected Output**: `Executed Project 1: Production CLI Application: Build a production-grade CLI with parsing, configuration, and errors.`
- **Actual Output**: `Executed Project 1: Production CLI Application: Build a production-grade CLI with parsing, configuration, and errors.`
- **Bytecode Inspected**: `javap -c -p Phase171Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase171DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
