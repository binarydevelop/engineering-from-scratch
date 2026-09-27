# Evidence Log: Phase 119 - Modern HTTP Client (java.net.http)

- **Lesson**: Phase 119 - Modern HTTP Client (java.net.http)
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase119/Phase119Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-119-http-client/src/main/java/io/github/javafromscratch/phase119/Phase119Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase119.Phase119Demo`
- **Expected Output**: `Executed Modern HTTP Client (java.net.http): Issue resilient HTTP requests with modern asynchronous HTTP clients.`
- **Actual Output**: `Executed Modern HTTP Client (java.net.http): Issue resilient HTTP requests with modern asynchronous HTTP clients.`
- **Bytecode Inspected**: `javap -c -p Phase119Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase119DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
