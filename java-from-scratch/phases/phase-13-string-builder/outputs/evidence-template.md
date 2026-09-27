# Evidence Log: Phase 13 - StringBuilder and Mutation

- **Lesson**: Phase 13 - StringBuilder and Mutation
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase13/Phase13Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-13-string-builder/src/main/java/io/github/javafromscratch/phase13/Phase13Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase13.Phase13Demo`
- **Expected Output**: `Executed StringBuilder and Mutation: Repeated string concatenation in loops is an O(N^2) allocation disaster.`
- **Actual Output**: `Executed StringBuilder and Mutation: Repeated string concatenation in loops is an O(N^2) allocation disaster.`
- **Bytecode Inspected**: `javap -c -p Phase13Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase13DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
