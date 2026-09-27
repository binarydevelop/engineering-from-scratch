# Evidence Log: Phase 151 - CPU Profiling: Hot Path Optimization

- **Lesson**: Phase 151 - CPU Profiling: Hot Path Optimization
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase151/Phase151Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-151-cpu-profiling/src/main/java/io/github/javafromscratch/phase151/Phase151Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase151.Phase151Demo`
- **Expected Output**: `Executed CPU Profiling: Hot Path Optimization: Optimize the 5% of code where the CPU spends 90% of its cycles.`
- **Actual Output**: `Executed CPU Profiling: Hot Path Optimization: Optimize the 5% of code where the CPU spends 90% of its cycles.`
- **Bytecode Inspected**: `javap -c -p Phase151Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase151DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
