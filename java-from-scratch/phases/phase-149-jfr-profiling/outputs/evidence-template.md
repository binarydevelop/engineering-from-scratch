# Evidence Log: Phase 149 - Java Flight Recorder (JFR)

- **Lesson**: Phase 149 - Java Flight Recorder (JFR)
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase149/Phase149Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-149-jfr-profiling/src/main/java/io/github/javafromscratch/phase149/Phase149Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase149.Phase149Demo`
- **Expected Output**: `Executed Java Flight Recorder (JFR): Record continuous, low-overhead event telemetry directly from the HotSpot kernel.`
- **Actual Output**: `Executed Java Flight Recorder (JFR): Record continuous, low-overhead event telemetry directly from the HotSpot kernel.`
- **Bytecode Inspected**: `javap -c -p Phase149Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase149DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
