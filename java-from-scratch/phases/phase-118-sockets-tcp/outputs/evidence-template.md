# Evidence Log: Phase 118 - TCP Sockets from Scratch

- **Lesson**: Phase 118 - TCP Sockets from Scratch
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase118/Phase118Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-118-sockets-tcp/src/main/java/io/github/javafromscratch/phase118/Phase118Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase118.Phase118Demo`
- **Expected Output**: `Executed TCP Sockets from Scratch: Network programming is reading and writing byte streams over OS sockets.`
- **Actual Output**: `Executed TCP Sockets from Scratch: Network programming is reading and writing byte streams over OS sockets.`
- **Bytecode Inspected**: `javap -c -p Phase118Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase118DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
