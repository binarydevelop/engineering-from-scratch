# Evidence Log: Phase 05 - Numeric Behavior and Overflow

- **Lesson**: Phase 05 - Numeric Behavior and Overflow
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase05/Phase05Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-05-numeric-behavior/src/main/java/io/github/javafromscratch/phase05/Phase05Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase05.Phase05Demo`
- **Expected Output**: `Executed Numeric Behavior and Overflow: Computers do not do ideal arithmetic; they do bounded binary arithmetic.`
- **Actual Output**: `Executed Numeric Behavior and Overflow: Computers do not do ideal arithmetic; they do bounded binary arithmetic.`
- **Bytecode Inspected**: `javap -c -p Phase05Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase05DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
