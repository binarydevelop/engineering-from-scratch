# Evidence Log: Phase 50 - Generics Subtyping and Wildcards

- **Lesson**: Phase 50 - Generics Subtyping and Wildcards
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase50/Phase50Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-50-wildcards/src/main/java/io/github/javafromscratch/phase50/Phase50Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase50.Phase50Demo`
- **Expected Output**: `Executed Generics Subtyping and Wildcards: List<Integer> is NOT a subtype of List<Number>.`
- **Actual Output**: `Executed Generics Subtyping and Wildcards: List<Integer> is NOT a subtype of List<Number>.`
- **Bytecode Inspected**: `javap -c -p Phase50Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase50DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
