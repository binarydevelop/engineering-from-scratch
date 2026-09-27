# Evidence Log: Phase 21 - Static Members & Class State

- **Lesson**: Phase 21 - Static Members & Class State
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase21/Phase21Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-21-static-members/src/main/java/io/github/javafromscratch/phase21/Phase21Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase21.Phase21Demo`
- **Expected Output**: `Executed Static Members & Class State: Static state is shared across all instances and lives for the classloader lifetime.`
- **Actual Output**: `Executed Static Members & Class State: Static state is shared across all instances and lives for the classloader lifetime.`
- **Bytecode Inspected**: `javap -c -p Phase21Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase21DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
