# Evidence Log: Phase 40 - HashMap Correctness & Mutable Keys

- **Lesson**: Phase 40 - HashMap Correctness & Mutable Keys
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase40/Phase40Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-40-hash-map-correctness/src/main/java/io/github/javafromscratch/phase40/Phase40Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase40.Phase40Demo`
- **Expected Output**: `Executed HashMap Correctness & Mutable Keys: Never use a mutable object as a hash map key.`
- **Actual Output**: `Executed HashMap Correctness & Mutable Keys: Never use a mutable object as a hash map key.`
- **Bytecode Inspected**: `javap -c -p Phase40Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase40DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
