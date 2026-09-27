# Evidence Log: Phase 11 - Strings as Immutable Values

- **Lesson**: Phase 11 - Strings as Immutable Values
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase11/Phase11Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-11-strings/src/main/java/io/github/javafromscratch/phase11/Phase11Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase11.Phase11Demo`
- **Expected Output**: `Executed Strings as Immutable Values: Immutability guarantees safe sharing across threads and hash stability.`
- **Actual Output**: `Executed Strings as Immutable Values: Immutability guarantees safe sharing across threads and hash stability.`
- **Bytecode Inspected**: `javap -c -p Phase11Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase11DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
