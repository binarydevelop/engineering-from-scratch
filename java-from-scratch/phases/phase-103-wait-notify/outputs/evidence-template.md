# Evidence Log: Phase 103 - Low-Level Coordination: wait/notify

- **Lesson**: Phase 103 - Low-Level Coordination: wait/notify
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase103/Phase103Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-103-wait-notify/src/main/java/io/github/javafromscratch/phase103/Phase103Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase103.Phase103Demo`
- **Expected Output**: `Executed Low-Level Coordination: wait/notify: Always wait in a loop; never rely on solitary notify.`
- **Actual Output**: `Executed Low-Level Coordination: wait/notify: Always wait in a loop; never rely on solitary notify.`
- **Bytecode Inspected**: `javap -c -p Phase103Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase103DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
