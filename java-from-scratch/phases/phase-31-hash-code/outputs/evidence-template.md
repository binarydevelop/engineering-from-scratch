# Evidence Log: Phase 31 - The hashCode and equals Contract

- **Lesson**: Phase 31 - The hashCode and equals Contract
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase31/Phase31Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-31-hash-code/src/main/java/io/github/javafromscratch/phase31/Phase31Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase31.Phase31Demo`
- **Expected Output**: `Executed The hashCode and equals Contract: Equal objects MUST produce equal hash codes; violate this and hash sets break.`
- **Actual Output**: `Executed The hashCode and equals Contract: Equal objects MUST produce equal hash codes; violate this and hash sets break.`
- **Bytecode Inspected**: `javap -c -p Phase31Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase31DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
