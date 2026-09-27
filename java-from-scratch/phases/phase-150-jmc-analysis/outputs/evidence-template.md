# Evidence Log: Phase 150 - JDK Mission Control (JMC)

- **Lesson**: Phase 150 - JDK Mission Control (JMC)
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase150/Phase150Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-150-jmc-analysis/src/main/java/io/github/javafromscratch/phase150/Phase150Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase150.Phase150Demo`
- **Expected Output**: `Executed JDK Mission Control (JMC): Visualize JFR recordings to isolate latency spikes and memory hotspots.`
- **Actual Output**: `Executed JDK Mission Control (JMC): Visualize JFR recordings to isolate latency spikes and memory hotspots.`
- **Bytecode Inspected**: `javap -c -p Phase150Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase150DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
