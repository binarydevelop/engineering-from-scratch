# Evidence Log: Phase 80 - Stack Frames & Operand Stack

- **Lesson**: Phase 80 - Stack Frames & Operand Stack
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase80/Phase80Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-80-stack-frames/src/main/java/io/github/javafromscratch/phase80/Phase80Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase80.Phase80Demo`
- **Expected Output**: `Executed Stack Frames & Operand Stack: JVM execution is a stack of frames containing local variables and operand stacks.`
- **Actual Output**: `Executed Stack Frames & Operand Stack: JVM execution is a stack of frames containing local variables and operand stacks.`
- **Bytecode Inspected**: `javap -c -p Phase80Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase80DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
