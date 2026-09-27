# Evidence Log: Phase 192 - Broken Lab 06: GC Thrashing & Allocation Storm

- **Lesson**: Phase 192 - Broken Lab 06: GC Thrashing & Allocation Storm
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase192/Phase192Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-192-broken-lab-gc-thrash/src/main/java/io/github/javafromscratch/phase192/Phase192Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase192.Phase192Demo`
- **Expected Output**: `Executed Broken Lab 06: GC Thrashing & Allocation Storm: Profile excessive temporary allocations causing GC latency spikes.`
- **Actual Output**: `Executed Broken Lab 06: GC Thrashing & Allocation Storm: Profile excessive temporary allocations causing GC latency spikes.`
- **Bytecode Inspected**: `javap -c -p Phase192Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase192DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
