# Evidence Log: Phase 70 - Streams: Declarative Pipelines

- **Lesson**: Phase 70 - Streams: Declarative Pipelines
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase70/Phase70Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-70-streams-foundations/src/main/java/io/github/javafromscratch/phase70/Phase70Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase70.Phase70Demo`
- **Expected Output**: `Executed Streams: Declarative Pipelines: Collections store data in memory; streams compute data through pipelines.`
- **Actual Output**: `Executed Streams: Declarative Pipelines: Collections store data in memory; streams compute data through pipelines.`
- **Bytecode Inspected**: `javap -c -p Phase70Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase70DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
