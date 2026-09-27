# Evidence Log: Phase 04 - Primitive vs Reference Types

- **Lesson**: Phase 04 - Primitive vs Reference Types
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase04/Phase04Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-04-primitive-vs-reference/src/main/java/io/github/javafromscratch/phase04/Phase04Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase04.Phase04Demo`
- **Expected Output**: `Executed Primitive vs Reference Types: Primitives hold values; references hold memory coordinates.`
- **Actual Output**: `Executed Primitive vs Reference Types: Primitives hold values; references hold memory coordinates.`
- **Bytecode Inspected**: `javap -c -p Phase04Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase04DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
