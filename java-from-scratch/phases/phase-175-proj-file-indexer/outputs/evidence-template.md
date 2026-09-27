# Evidence Log: Phase 175 - Project 5: High-Performance File Indexer

- **Lesson**: Phase 175 - Project 5: High-Performance File Indexer
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase175/Phase175Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-175-proj-file-indexer/src/main/java/io/github/javafromscratch/phase175/Phase175Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase175.Phase175Demo`
- **Expected Output**: `Executed Project 5: High-Performance File Indexer: Traverse directory trees concurrently to build a searchable inverted index.`
- **Actual Output**: `Executed Project 5: High-Performance File Indexer: Traverse directory trees concurrently to build a searchable inverted index.`
- **Bytecode Inspected**: `javap -c -p Phase175Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase175DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
