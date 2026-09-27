# Evidence Log: Phase 157 - Dead Code & Constant Folding

- **Lesson**: Phase 157 - Dead Code & Constant Folding
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase157/Phase157Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-157-dead-code-elimination/src/main/java/io/github/javafromscratch/phase157/Phase157Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase157.Phase157Demo`
- **Expected Output**: `Executed Dead Code & Constant Folding: The C2 compiler ruthlessly deletes code whose results are never observed.`
- **Actual Output**: `Executed Dead Code & Constant Folding: The C2 compiler ruthlessly deletes code whose results are never observed.`
- **Bytecode Inspected**: `javap -c -p Phase157Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase157DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
