# Evidence Log: Phase 16 - Constructors & Invariants

- **Lesson**: Phase 16 - Constructors & Invariants
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase16/Phase16Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-16-constructors/src/main/java/io/github/javafromscratch/phase16/Phase16Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase16.Phase16Demo`
- **Expected Output**: `Executed Constructors & Invariants: An object must never exist in an invalid state; invariants begin in the constructor.`
- **Actual Output**: `Executed Constructors & Invariants: An object must never exist in an invalid state; invariants begin in the constructor.`
- **Bytecode Inspected**: `javap -c -p Phase16Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase16DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
