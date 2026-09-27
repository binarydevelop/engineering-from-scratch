# Evidence Log: Phase 101 - Deadlocks: Creation & Prevention

- **Lesson**: Phase 101 - Deadlocks: Creation & Prevention
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase101/Phase101Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-101-deadlocks/src/main/java/io/github/javafromscratch/phase101/Phase101Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase101.Phase101Demo`
- **Expected Output**: `Executed Deadlocks: Creation & Prevention: Deadlock occurs when circular lock acquisition dependencies form.`
- **Actual Output**: `Executed Deadlocks: Creation & Prevention: Deadlock occurs when circular lock acquisition dependencies form.`
- **Bytecode Inspected**: `javap -c -p Phase101Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase101DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
