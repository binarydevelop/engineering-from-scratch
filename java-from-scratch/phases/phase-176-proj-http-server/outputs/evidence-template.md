# Evidence Log: Phase 176 - Project 6: Lightweight HTTP Server

- **Lesson**: Phase 176 - Project 6: Lightweight HTTP Server
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase176/Phase176Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-176-proj-http-server/src/main/java/io/github/javafromscratch/phase176/Phase176Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase176.Phase176Demo`
- **Expected Output**: `Executed Project 6: Lightweight HTTP Server: Build an HTTP/1.1 server from raw TCP sockets with virtual threads.`
- **Actual Output**: `Executed Project 6: Lightweight HTTP Server: Build an HTTP/1.1 server from raw TCP sockets with virtual threads.`
- **Bytecode Inspected**: `javap -c -p Phase176Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase176DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
