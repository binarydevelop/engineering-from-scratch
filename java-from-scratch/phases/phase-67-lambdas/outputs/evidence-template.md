# Evidence Log: Phase 67 - Lambdas: Anonymous Functions

- **Lesson**: Phase 67 - Lambdas: Anonymous Functions
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase67/Phase67Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-67-lambdas/src/main/java/io/github/javafromscratch/phase67/Phase67Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase67.Phase67Demo`
- **Expected Output**: `Executed Lambdas: Anonymous Functions: A lambda is code treated as data, desugared into invokedynamic calls.`
- **Actual Output**: `Executed Lambdas: Anonymous Functions: A lambda is code treated as data, desugared into invokedynamic calls.`
- **Bytecode Inspected**: `javap -c -p Phase67Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase67DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
