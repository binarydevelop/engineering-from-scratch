# Evidence Log: Phase 111 - Concurrent Collections

- **Lesson**: Phase 111 - Concurrent Collections
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase111/Phase111Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-111-concurrent-collections/src/main/java/io/github/javafromscratch/phase111/Phase111Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase111.Phase111Demo`
- **Expected Output**: `Executed Concurrent Collections: Concurrent collections eliminate coarse synchronized bottle-necks.`
- **Actual Output**: `Executed Concurrent Collections: Concurrent collections eliminate coarse synchronized bottle-necks.`
- **Bytecode Inspected**: `javap -c -p Phase111Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase111DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
