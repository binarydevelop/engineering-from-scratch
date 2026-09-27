# Evidence Log: Phase 139 - Test Doubles: Fakes, Stubs, Mocks

- **Lesson**: Phase 139 - Test Doubles: Fakes, Stubs, Mocks
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase139/Phase139Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-139-test-doubles/src/main/java/io/github/javafromscratch/phase139/Phase139Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase139.Phase139Demo`
- **Expected Output**: `Executed Test Doubles: Fakes, Stubs, Mocks: Fakes have working implementations; stubs return canned data; mocks verify interactions.`
- **Actual Output**: `Executed Test Doubles: Fakes, Stubs, Mocks: Fakes have working implementations; stubs return canned data; mocks verify interactions.`
- **Bytecode Inspected**: `javap -c -p Phase139Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase139DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
