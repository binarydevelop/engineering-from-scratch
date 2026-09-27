# Evidence Log: Phase 162 - Startup Latency vs Throughput

- **Lesson**: Phase 162 - Startup Latency vs Throughput
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase162/Phase162Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-162-startup-vs-throughput/src/main/java/io/github/javafromscratch/phase162/Phase162Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase162.Phase162Demo`
- **Expected Output**: `Executed Startup Latency vs Throughput: CLI tools require fast startup; server backends require high peak throughput.`
- **Actual Output**: `Executed Startup Latency vs Throughput: CLI tools require fast startup; server backends require high peak throughput.`
- **Bytecode Inspected**: `javap -c -p Phase162Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase162DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
