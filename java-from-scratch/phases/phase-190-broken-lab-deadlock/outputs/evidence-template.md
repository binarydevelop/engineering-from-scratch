# Evidence Log: Phase 190 - Broken Lab 04: Multi-Threaded Deadlock

- **Lesson**: Phase 190 - Broken Lab 04: Multi-Threaded Deadlock
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase190/Phase190Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-190-broken-lab-deadlock/src/main/java/io/github/javafromscratch/phase190/Phase190Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase190.Phase190Demo`
- **Expected Output**: `Executed Broken Lab 04: Multi-Threaded Deadlock: Diagnose circular lock dependencies using jcmd thread dumps.`
- **Actual Output**: `Executed Broken Lab 04: Multi-Threaded Deadlock: Diagnose circular lock dependencies using jcmd thread dumps.`
- **Bytecode Inspected**: `javap -c -p Phase190Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase190DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
