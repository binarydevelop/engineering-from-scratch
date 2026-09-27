# Evidence Log: Phase 105 - High-Throughput Producer-Consumer

- **Lesson**: Phase 105 - High-Throughput Producer-Consumer
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase105/Phase105Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-105-producer-consumer/src/main/java/io/github/javafromscratch/phase105/Phase105Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase105.Phase105Demo`
- **Expected Output**: `Executed High-Throughput Producer-Consumer: Decouple processing stages with bounded queues to smooth traffic bursts.`
- **Actual Output**: `Executed High-Throughput Producer-Consumer: Decouple processing stages with bounded queues to smooth traffic bursts.`
- **Bytecode Inspected**: `javap -c -p Phase105Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase105DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
