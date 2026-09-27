# Evidence Log: Phase 146 - Interactive Debugging & JDWP

- **Lesson**: Phase 146 - Interactive Debugging & JDWP
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase146/Phase146Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-146-debugger-jdwp/src/main/java/io/github/javafromscratch/phase146/Phase146Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase146.Phase146Demo`
- **Expected Output**: `Executed Interactive Debugging & JDWP: The debugger connects to the JVM socket to inspect variables and control execution.`
- **Actual Output**: `Executed Interactive Debugging & JDWP: The debugger connects to the JVM socket to inspect variables and control execution.`
- **Bytecode Inspected**: `javap -c -p Phase146Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase146DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
