# Evidence Log: Phase 39 - HashMap from First Principles

- **Lesson**: Phase 39 - HashMap from First Principles
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase39/Phase39Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-39-hash-map-scratch/src/main/java/io/github/javafromscratch/phase39/Phase39Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase39.Phase39Demo`
- **Expected Output**: `Executed HashMap from First Principles: Hash functions project infinite key spaces into finite bucket arrays.`
- **Actual Output**: `Executed HashMap from First Principles: Hash functions project infinite key spaces into finite bucket arrays.`
- **Bytecode Inspected**: `javap -c -p Phase39Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase39DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
