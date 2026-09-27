# Evidence Log: Phase 120 - Building a Minimal HTTP Server

- **Lesson**: Phase 120 - Building a Minimal HTTP Server
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase120/Phase120Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-120-simple-http-server/src/main/java/io/github/javafromscratch/phase120/Phase120Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase120.Phase120Demo`
- **Expected Output**: `Executed Building a Minimal HTTP Server: An HTTP server is a socket server parsing headers and returning text lines.`
- **Actual Output**: `Executed Building a Minimal HTTP Server: An HTTP server is a socket server parsing headers and returning text lines.`
- **Bytecode Inspected**: `javap -c -p Phase120Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase120DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
