# Evidence Log: Phase 161 - Essential JVM Tuning Flags

- **Lesson**: Phase 161 - Essential JVM Tuning Flags
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase161/Phase161Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-161-essential-jvm-flags/src/main/java/io/github/javafromscratch/phase161/Phase161Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase161.Phase161Demo`
- **Expected Output**: `Executed Essential JVM Tuning Flags: Use only flags you can justify with hard profiling data.`
- **Actual Output**: `Executed Essential JVM Tuning Flags: Use only flags you can justify with hard profiling data.`
- **Bytecode Inspected**: `javap -c -p Phase161Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase161DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
