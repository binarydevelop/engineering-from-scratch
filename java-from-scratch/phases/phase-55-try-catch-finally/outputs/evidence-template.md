# Evidence Log: Phase 55 - try, catch, and finally Mechanics

- **Lesson**: Phase 55 - try, catch, and finally Mechanics
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase55/Phase55Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-55-try-catch-finally/src/main/java/io/github/javafromscratch/phase55/Phase55Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase55.Phase55Demo`
- **Expected Output**: `Executed try, catch, and finally Mechanics: finally blocks execute unconditionally, even in the presence of returns.`
- **Actual Output**: `Executed try, catch, and finally Mechanics: finally blocks execute unconditionally, even in the presence of returns.`
- **Bytecode Inspected**: `javap -c -p Phase55Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase55DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
