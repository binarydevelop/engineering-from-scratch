# Evidence Log: Phase 136 - Dependency Conflicts & Diamond Trees

- **Lesson**: Phase 136 - Dependency Conflicts & Diamond Trees
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase136/Phase136Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-136-dependency-conflicts/src/main/java/io/github/javafromscratch/phase136/Phase136Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase136.Phase136Demo`
- **Expected Output**: `Executed Dependency Conflicts & Diamond Trees: Two versions of the same library on the classpath lead to runtime version roulette.`
- **Actual Output**: `Executed Dependency Conflicts & Diamond Trees: Two versions of the same library on the classpath lead to runtime version roulette.`
- **Bytecode Inspected**: `javap -c -p Phase136Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase136DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
