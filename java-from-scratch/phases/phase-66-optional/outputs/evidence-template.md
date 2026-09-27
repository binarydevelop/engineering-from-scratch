# Evidence Log: Phase 66 - Optional Done Right

- **Lesson**: Phase 66 - Optional Done Right
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase66/Phase66Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-66-optional/src/main/java/io/github/javafromscratch/phase66/Phase66Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase66.Phase66Demo`
- **Expected Output**: `Executed Optional Done Right: Optional is a return-type signal for absent values, not a field replacement.`
- **Actual Output**: `Executed Optional Done Right: Optional is a return-type signal for absent values, not a field replacement.`
- **Bytecode Inspected**: `javap -c -p Phase66Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase66DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
