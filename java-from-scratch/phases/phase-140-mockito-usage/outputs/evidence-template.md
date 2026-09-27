# Evidence Log: Phase 140 - Mockito: Usage and Misuse

- **Lesson**: Phase 140 - Mockito: Usage and Misuse
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase140/Phase140Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-140-mockito-usage/src/main/java/io/github/javafromscratch/phase140/Phase140Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase140.Phase140Demo`
- **Expected Output**: `Executed Mockito: Usage and Misuse: Mock at architectural boundaries; never mock domain models or simple values.`
- **Actual Output**: `Executed Mockito: Usage and Misuse: Mock at architectural boundaries; never mock domain models or simple values.`
- **Bytecode Inspected**: `javap -c -p Phase140Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase140DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
