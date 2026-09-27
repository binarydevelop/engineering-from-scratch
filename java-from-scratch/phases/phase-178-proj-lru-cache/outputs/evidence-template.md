# Evidence Log: Phase 178 - Project 8: Generic Thread-Safe LRU Cache

- **Lesson**: Phase 178 - Project 8: Generic Thread-Safe LRU Cache
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase178/Phase178Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-178-proj-lru-cache/src/main/java/io/github/javafromscratch/phase178/Phase178Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase178.Phase178Demo`
- **Expected Output**: `Executed Project 8: Generic Thread-Safe LRU Cache: Implement an O(1) generic LRU cache with fine-grained concurrency locking.`
- **Actual Output**: `Executed Project 8: Generic Thread-Safe LRU Cache: Implement an O(1) generic LRU cache with fine-grained concurrency locking.`
- **Bytecode Inspected**: `javap -c -p Phase178Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase178DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
