# Evidence Log: Phase 42 - TreeMap & TreeSet

- **Lesson**: Phase 42 - TreeMap & TreeSet
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase42/Phase42Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-42-tree-map/src/main/java/io/github/javafromscratch/phase42/Phase42Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase42.Phase42Demo`
- **Expected Output**: `Executed TreeMap & TreeSet: Self-balancing binary search trees provide guaranteed O(log N) sorted operations.`
- **Actual Output**: `Executed TreeMap & TreeSet: Self-balancing binary search trees provide guaranteed O(log N) sorted operations.`
- **Bytecode Inspected**: `javap -c -p Phase42Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase42DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
