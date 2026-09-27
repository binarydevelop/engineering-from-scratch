# Evidence Log: Phase 142 - Property-Based Invariant Testing

- **Lesson**: Phase 142 - Property-Based Invariant Testing
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase142/Phase142Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-142-property-based-testing/src/main/java/io/github/javafromscratch/phase142/Phase142Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase142.Phase142Demo`
- **Expected Output**: `Executed Property-Based Invariant Testing: Generate thousands of random inputs to discover corner cases you never imagined.`
- **Actual Output**: `Executed Property-Based Invariant Testing: Generate thousands of random inputs to discover corner cases you never imagined.`
- **Bytecode Inspected**: `javap -c -p Phase142Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase142DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
