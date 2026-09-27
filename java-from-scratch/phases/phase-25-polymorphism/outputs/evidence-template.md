# Evidence Log: Phase 25 - Polymorphism & Dispatch

- **Lesson**: Phase 25 - Polymorphism & Dispatch
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase25/Phase25Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-25-polymorphism/src/main/java/io/github/javafromscratch/phase25/Phase25Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase25.Phase25Demo`
- **Expected Output**: `Executed Polymorphism & Dispatch: Variables have static compile types; objects have dynamic runtime types.`
- **Actual Output**: `Executed Polymorphism & Dispatch: Variables have static compile types; objects have dynamic runtime types.`
- **Bytecode Inspected**: `javap -c -p Phase25Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase25DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
