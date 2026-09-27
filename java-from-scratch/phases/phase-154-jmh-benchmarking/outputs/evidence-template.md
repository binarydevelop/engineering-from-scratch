# Evidence Log: Phase 154 - Rigorous Microbenchmarking with JMH

- **Lesson**: Phase 154 - Rigorous Microbenchmarking with JMH
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase154/Phase154Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-154-jmh-benchmarking/src/main/java/io/github/javafromscratch/phase154/Phase154Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase154.Phase154Demo`
- **Expected Output**: `Executed Rigorous Microbenchmarking with JMH: Never trust a naive timer loop; use JMH to defeat JIT optimizations.`
- **Actual Output**: `Executed Rigorous Microbenchmarking with JMH: Never trust a naive timer loop; use JMH to defeat JIT optimizations.`
- **Bytecode Inspected**: `javap -c -p Phase154Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase154DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
