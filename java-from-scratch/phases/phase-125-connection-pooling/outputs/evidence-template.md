# Evidence Log: Phase 125 - Database Connection Pooling

- **Lesson**: Phase 125 - Database Connection Pooling
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase125/Phase125Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-125-connection-pooling/src/main/java/io/github/javafromscratch/phase125/Phase125Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase125.Phase125Demo`
- **Expected Output**: `Executed Database Connection Pooling: Opening a TCP connection to a database per request will crush database performance.`
- **Actual Output**: `Executed Database Connection Pooling: Opening a TCP connection to a database per request will crush database performance.`
- **Bytecode Inspected**: `javap -c -p Phase125Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase125DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
