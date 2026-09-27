# Evidence Log: Phase 53 - Exceptions from First Principles

- **Lesson**: Phase 53 - Exceptions from First Principles
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase53/Phase53Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-53-exceptions-principles/src/main/java/io/github/javafromscratch/phase53/Phase53Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase53.Phase53Demo`
- **Expected Output**: `Executed Exceptions from First Principles: Exceptions provide out-of-band communication of invariant violations.`
- **Actual Output**: `Executed Exceptions from First Principles: Exceptions provide out-of-band communication of invariant violations.`
- **Bytecode Inspected**: `javap -c -p Phase53Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase53DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
