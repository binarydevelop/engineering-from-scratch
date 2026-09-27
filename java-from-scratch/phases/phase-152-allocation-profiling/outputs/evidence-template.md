# Evidence Log: Phase 152 - Allocation Profiling & GC Pressure

- **Lesson**: Phase 152 - Allocation Profiling & GC Pressure
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase152/Phase152Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-152-allocation-profiling/src/main/java/io/github/javafromscratch/phase152/Phase152Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase152.Phase152Demo`
- **Expected Output**: `Executed Allocation Profiling & GC Pressure: The fastest garbage collection is the one that never has to run.`
- **Actual Output**: `Executed Allocation Profiling & GC Pressure: The fastest garbage collection is the one that never has to run.`
- **Bytecode Inspected**: `javap -c -p Phase152Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase152DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
