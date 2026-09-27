# Evidence Log: Phase 61 - Buffered I/O & Syscall Overhead

- **Lesson**: Phase 61 - Buffered I/O & Syscall Overhead
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase61/Phase61Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-61-buffered-io/src/main/java/io/github/javafromscratch/phase61/Phase61Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase61.Phase61Demo`
- **Expected Output**: `Executed Buffered I/O & Syscall Overhead: Issuing a kernel syscall for every byte is a 1000x performance penalty.`
- **Actual Output**: `Executed Buffered I/O & Syscall Overhead: Issuing a kernel syscall for every byte is a 1000x performance penalty.`
- **Bytecode Inspected**: `javap -c -p Phase61Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase61DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
