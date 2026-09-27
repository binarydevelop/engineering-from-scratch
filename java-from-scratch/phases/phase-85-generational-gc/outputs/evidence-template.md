# Evidence Log: Phase 85 - Generational Garbage Collection

- **Lesson**: Phase 85 - Generational Garbage Collection
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase85/Phase85Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-85-generational-gc/src/main/java/io/github/javafromscratch/phase85/Phase85Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase85.Phase85Demo`
- **Expected Output**: `Executed Generational Garbage Collection: The Weak Generational Hypothesis: Most allocated objects die young.`
- **Actual Output**: `Executed Generational Garbage Collection: The Weak Generational Hypothesis: Most allocated objects die young.`
- **Bytecode Inspected**: `javap -c -p Phase85Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase85DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
