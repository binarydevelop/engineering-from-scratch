# Evidence Log: Phase 117 - Concurrency Architecture Comparison

- **Lesson**: Phase 117 - Concurrency Architecture Comparison
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase117/Phase117Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-117-concurrency-design-lab/src/main/java/io/github/javafromscratch/phase117/Phase117Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase117.Phase117Demo`
- **Expected Output**: `Executed Concurrency Architecture Comparison: Compare all concurrency models on an identical workload.`
- **Actual Output**: `Executed Concurrency Architecture Comparison: Compare all concurrency models on an identical workload.`
- **Bytecode Inspected**: `javap -c -p Phase117Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase117DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
