# Evidence Log: Phase 54 - Checked vs Unchecked Exceptions

- **Lesson**: Phase 54 - Checked vs Unchecked Exceptions
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase54/Phase54Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-54-checked-vs-unchecked/src/main/java/io/github/javafromscratch/phase54/Phase54Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase54.Phase54Demo`
- **Expected Output**: `Executed Checked vs Unchecked Exceptions: Recoverable environmental faults are checked; programmer defects are unchecked.`
- **Actual Output**: `Executed Checked vs Unchecked Exceptions: Recoverable environmental faults are checked; programmer defects are unchecked.`
- **Bytecode Inspected**: `javap -c -p Phase54Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase54DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
