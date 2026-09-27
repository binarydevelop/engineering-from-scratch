# Evidence Log: Phase 56 - Custom Domain Exceptions

- **Lesson**: Phase 56 - Custom Domain Exceptions
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase56/Phase56Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-56-custom-exceptions/src/main/java/io/github/javafromscratch/phase56/Phase56Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase56.Phase56Demo`
- **Expected Output**: `Executed Custom Domain Exceptions: Exceptions should carry structured domain context, not plain error strings.`
- **Actual Output**: `Executed Custom Domain Exceptions: Exceptions should carry structured domain context, not plain error strings.`
- **Bytecode Inspected**: `javap -c -p Phase56Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase56DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
