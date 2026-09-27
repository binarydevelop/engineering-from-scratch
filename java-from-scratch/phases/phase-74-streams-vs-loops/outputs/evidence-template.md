# Evidence Log: Phase 74 - Streams vs Loops Performance

- **Lesson**: Phase 74 - Streams vs Loops Performance
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase74/Phase74Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-74-streams-vs-loops/src/main/java/io/github/javafromscratch/phase74/Phase74Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase74.Phase74Demo`
- **Expected Output**: `Executed Streams vs Loops Performance: Write for humans first; optimize with loops only when profiling proves necessary.`
- **Actual Output**: `Executed Streams vs Loops Performance: Write for humans first; optimize with loops only when profiling proves necessary.`
- **Bytecode Inspected**: `javap -c -p Phase74Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase74DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
