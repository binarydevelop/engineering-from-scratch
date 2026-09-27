# Evidence Log: Phase 197 - Deconstructing the Spring Framework

- **Lesson**: Phase 197 - Deconstructing the Spring Framework
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase197/Phase197Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-197-spring-motivation/src/main/java/io/github/javafromscratch/phase197/Phase197Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase197.Phase197Demo`
- **Expected Output**: `Executed Deconstructing the Spring Framework: Map framework abstractions to core Java primitives.`
- **Actual Output**: `Executed Deconstructing the Spring Framework: Map framework abstractions to core Java primitives.`
- **Bytecode Inspected**: `javap -c -p Phase197Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase197DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
