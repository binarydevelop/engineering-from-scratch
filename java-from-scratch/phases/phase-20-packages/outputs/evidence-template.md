# Evidence Log: Phase 20 - Packages and Namespaces

- **Lesson**: Phase 20 - Packages and Namespaces
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase20/Phase20Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-20-packages/src/main/java/io/github/javafromscratch/phase20/Phase20Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase20.Phase20Demo`
- **Expected Output**: `Executed Packages and Namespaces: Packages partition the global type space and enforce directory structures.`
- **Actual Output**: `Executed Packages and Namespaces: Packages partition the global type space and enforce directory structures.`
- **Bytecode Inspected**: `javap -c -p Phase20Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase20DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
