# Evidence Log: Phase 14 - Classes: State and Behavior

- **Lesson**: Phase 14 - Classes: State and Behavior
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase14/Phase14Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-14-classes/src/main/java/io/github/javafromscratch/phase14/Phase14Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase14.Phase14Demo`
- **Expected Output**: `Executed Classes: State and Behavior: A class defines a type, encapsulation boundaries, and invariant enforcement.`
- **Actual Output**: `Executed Classes: State and Behavior: A class defines a type, encapsulation boundaries, and invariant enforcement.`
- **Bytecode Inspected**: `javap -c -p Phase14Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase14DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
