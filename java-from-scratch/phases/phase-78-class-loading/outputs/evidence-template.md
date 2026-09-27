# Evidence Log: Phase 78 - Class Loading & Custom Loaders

- **Lesson**: Phase 78 - Class Loading & Custom Loaders
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase78/Phase78Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-78-class-loading/src/main/java/io/github/javafromscratch/phase78/Phase78Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase78.Phase78Demo`
- **Expected Output**: `Executed Class Loading & Custom Loaders: A class in the JVM is identified by its fully qualified name AND its ClassLoader.`
- **Actual Output**: `Executed Class Loading & Custom Loaders: A class in the JVM is identified by its fully qualified name AND its ClassLoader.`
- **Bytecode Inspected**: `javap -c -p Phase78Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase78DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
