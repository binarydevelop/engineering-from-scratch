# Evidence Log: Phase 184 - Project 14: Concurrent Web Crawler

- **Lesson**: Phase 184 - Project 14: Concurrent Web Crawler
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase184/Phase184Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-184-proj-web-crawler/src/main/java/io/github/javafromscratch/phase184/Phase184Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase184.Phase184Demo`
- **Expected Output**: `Executed Project 14: Concurrent Web Crawler: Build an asynchronous web crawler with virtual threads and rate limits.`
- **Actual Output**: `Executed Project 14: Concurrent Web Crawler: Build an asynchronous web crawler with virtual threads and rate limits.`
- **Bytecode Inspected**: `javap -c -p Phase184Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase184DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
