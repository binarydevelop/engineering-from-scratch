# Evidence Log: Phase 76 - Reflection from First Principles

- **Lesson**: Phase 76 - Reflection from First Principles
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase76/Phase76Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-76-reflection/src/main/java/io/github/javafromscratch/phase76/Phase76Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase76.Phase76Demo`
- **Expected Output**: `Executed Reflection from First Principles: Reflection lets code inspect and mutate its own structure at runtime.`
- **Actual Output**: `Executed Reflection from First Principles: Reflection lets code inspect and mutate its own structure at runtime.`
- **Bytecode Inspected**: `javap -c -p Phase76Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase76DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
