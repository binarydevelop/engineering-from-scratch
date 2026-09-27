# Evidence Log: Phase 115 - Platform vs Virtual Threads Benchmark

- **Lesson**: Phase 115 - Platform vs Virtual Threads Benchmark
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase115/Phase115Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-115-virtual-vs-platform/src/main/java/io/github/javafromscratch/phase115/Phase115Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase115.Phase115Demo`
- **Expected Output**: `Executed Platform vs Virtual Threads Benchmark: Virtual threads excel at high-concurrency blocking I/O, not CPU-bound math.`
- **Actual Output**: `Executed Platform vs Virtual Threads Benchmark: Virtual threads excel at high-concurrency blocking I/O, not CPU-bound math.`
- **Bytecode Inspected**: `javap -c -p Phase115Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase115DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
