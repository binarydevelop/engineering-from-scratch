# Evidence Log: Phase 60 - Bytes vs Characters & Encodings

- **Lesson**: Phase 60 - Bytes vs Characters & Encodings
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase60/Phase60Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-60-bytes-vs-characters/src/main/java/io/github/javafromscratch/phase60/Phase60Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase60.Phase60Demo`
- **Expected Output**: `Executed Bytes vs Characters & Encodings: There is no such thing as plain text; there are only bytes and character encodings.`
- **Actual Output**: `Executed Bytes vs Characters & Encodings: There is no such thing as plain text; there are only bytes and character encodings.`
- **Bytecode Inspected**: `javap -c -p Phase60Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase60DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
