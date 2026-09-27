# Evidence Log: Phase 49 - Bounded Type Parameters

- **Lesson**: Phase 49 - Bounded Type Parameters
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase49/Phase49Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-49-bounded-generics/src/main/java/io/github/javafromscratch/phase49/Phase49Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase49.Phase49Demo`
- **Expected Output**: `Executed Bounded Type Parameters: Bounds restrict type parameters to types that support required capabilities.`
- **Actual Output**: `Executed Bounded Type Parameters: Bounds restrict type parameters to types that support required capabilities.`
- **Bytecode Inspected**: `javap -c -p Phase49Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase49DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
