# Evidence Log: Phase 147 - Stack Trace Forensics

- **Lesson**: Phase 147 - Stack Trace Forensics
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase147/Phase147Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-147-stack-trace-forensics/src/main/java/io/github/javafromscratch/phase147/Phase147Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase147.Phase147Demo`
- **Expected Output**: `Executed Stack Trace Forensics: Read stack traces backwards from the ultimate root cause.`
- **Actual Output**: `Executed Stack Trace Forensics: Read stack traces backwards from the ultimate root cause.`
- **Bytecode Inspected**: `javap -c -p Phase147Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase147DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
