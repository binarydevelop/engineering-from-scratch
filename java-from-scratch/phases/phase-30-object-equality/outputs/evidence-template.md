# Evidence Log: Phase 30 - Object Equality: == vs equals

- **Lesson**: Phase 30 - Object Equality: == vs equals
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase30/Phase30Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-30-object-equality/src/main/java/io/github/javafromscratch/phase30/Phase30Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase30.Phase30Demo`
- **Expected Output**: `Executed Object Equality: == vs equals: == tests pointer identity; equals tests semantic value equivalence.`
- **Actual Output**: `Executed Object Equality: == vs equals: == tests pointer identity; equals tests semantic value equivalence.`
- **Bytecode Inspected**: `javap -c -p Phase30Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase30DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
