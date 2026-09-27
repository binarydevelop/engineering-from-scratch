# Evidence Log: Phase 128 - The N+1 Query Problem

- **Lesson**: Phase 128 - The N+1 Query Problem
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase128/Phase128Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-128-n-plus-one-problem/src/main/java/io/github/javafromscratch/phase128/Phase128Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase128.Phase128Demo`
- **Expected Output**: `Executed The N+1 Query Problem: Naively traversing lazy relations executes N+1 database queries; fix with JOIN FETCH.`
- **Actual Output**: `Executed The N+1 Query Problem: Naively traversing lazy relations executes N+1 database queries; fix with JOIN FETCH.`
- **Bytecode Inspected**: `javap -c -p Phase128Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase128DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
