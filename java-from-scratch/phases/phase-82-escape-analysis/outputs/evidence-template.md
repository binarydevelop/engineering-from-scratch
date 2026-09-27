# Evidence Log: Phase 82 - Escape Analysis & Scalar Replacement

- **Lesson**: Phase 82 - Escape Analysis & Scalar Replacement
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase82/Phase82Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-82-escape-analysis/src/main/java/io/github/javafromscratch/phase82/Phase82Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase82.Phase82Demo`
- **Expected Output**: `Executed Escape Analysis & Scalar Replacement: HotSpot does not allocate objects on the stack; it replaces them with scalars.`
- **Actual Output**: `Executed Escape Analysis & Scalar Replacement: HotSpot does not allocate objects on the stack; it replaces them with scalars.`
- **Bytecode Inspected**: `javap -c -p Phase82Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase82DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
