# Evidence Log: Phase 38 - LinkedList from Scratch

- **Lesson**: Phase 38 - LinkedList from Scratch
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase38/Phase38Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-38-linked-list/src/main/java/io/github/javafromscratch/phase38/Phase38Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase38.Phase38Demo`
- **Expected Output**: `Executed LinkedList from Scratch: Pointers provide O(1) insertions at known positions but destroy cache locality.`
- **Actual Output**: `Executed LinkedList from Scratch: Pointers provide O(1) insertions at known positions but destroy cache locality.`
- **Bytecode Inspected**: `javap -c -p Phase38Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase38DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
