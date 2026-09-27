# Evidence Log: Phase 07 - Control Flow & Pattern Matching

- **Lesson**: Phase 07 - Control Flow & Pattern Matching
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase07/Phase07Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-07-control-flow/src/main/java/io/github/javafromscratch/phase07/Phase07Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase07.Phase07Demo`
- **Expected Output**: `Executed Control Flow & Pattern Matching: Control flow translates to conditional jumps in the operand stack.`
- **Actual Output**: `Executed Control Flow & Pattern Matching: Control flow translates to conditional jumps in the operand stack.`
- **Bytecode Inspected**: `javap -c -p Phase07Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase07DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
