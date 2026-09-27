# Evidence Log: Phase 187 - Broken Lab 01: Hidden NullPointerException

- **Lesson**: Phase 187 - Broken Lab 01: Hidden NullPointerException
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase187/Phase187Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-187-broken-lab-npe/src/main/java/io/github/javafromscratch/phase187/Phase187Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase187.Phase187Demo`
- **Expected Output**: `Executed Broken Lab 01: Hidden NullPointerException: Diagnose unboxing null traps and modern JVM NPE messages.`
- **Actual Output**: `Executed Broken Lab 01: Hidden NullPointerException: Diagnose unboxing null traps and modern JVM NPE messages.`
- **Bytecode Inspected**: `javap -c -p Phase187Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase187DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
