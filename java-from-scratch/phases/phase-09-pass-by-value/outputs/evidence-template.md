# Evidence Log: Phase 09 - Pass-by-Value Mechanics

- **Lesson**: Phase 09 - Pass-by-Value Mechanics
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase09/Phase09Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-09-pass-by-value/src/main/java/io/github/javafromscratch/phase09/Phase09Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase09.Phase09Demo`
- **Expected Output**: `Executed Pass-by-Value Mechanics: Java is strictly pass-by-value: references are passed by value.`
- **Actual Output**: `Executed Pass-by-Value Mechanics: Java is strictly pass-by-value: references are passed by value.`
- **Bytecode Inspected**: `javap -c -p Phase09Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase09DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
