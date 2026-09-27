# Evidence Log: Phase 156 - Warmup Phenomena & Cold Starts

- **Lesson**: Phase 156 - Warmup Phenomena & Cold Starts
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase156/Phase156Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-156-jit-warmup/src/main/java/io/github/javafromscratch/phase156/Phase156Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase156.Phase156Demo`
- **Expected Output**: `Executed Warmup Phenomena & Cold Starts: A freshly started JVM runs in interpreted mode; give it time to optimize.`
- **Actual Output**: `Executed Warmup Phenomena & Cold Starts: A freshly started JVM runs in interpreted mode; give it time to optimize.`
- **Bytecode Inspected**: `javap -c -p Phase156Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase156DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
