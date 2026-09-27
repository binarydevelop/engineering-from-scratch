# Evidence Log: Phase 168 - Pluggable Architecture: ServiceLoader

- **Lesson**: Phase 168 - Pluggable Architecture: ServiceLoader
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase168/Phase168Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-168-service-loader/src/main/java/io/github/javafromscratch/phase168/Phase168Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase168.Phase168Demo`
- **Expected Output**: `Executed Pluggable Architecture: ServiceLoader: ServiceLoader discovers interface implementations dynamically at runtime.`
- **Actual Output**: `Executed Pluggable Architecture: ServiceLoader: ServiceLoader discovers interface implementations dynamically at runtime.`
- **Bytecode Inspected**: `javap -c -p Phase168Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase168DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
