# Evidence Log: Phase 34 - Primitive Wrapper Types

- **Lesson**: Phase 34 - Primitive Wrapper Types
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase34/Phase34Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-34-wrapper-types/src/main/java/io/github/javafromscratch/phase34/Phase34Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase34.Phase34Demo`
- **Expected Output**: `Executed Primitive Wrapper Types: Wrappers bridge primitives to object-oriented generics at the cost of heap allocation.`
- **Actual Output**: `Executed Primitive Wrapper Types: Wrappers bridge primitives to object-oriented generics at the cost of heap allocation.`
- **Bytecode Inspected**: `javap -c -p Phase34Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase34DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
