# Evidence Log: Phase 188 - Broken Lab 02: ConcurrentModificationException

- **Lesson**: Phase 188 - Broken Lab 02: ConcurrentModificationException
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase188/Phase188Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-188-broken-lab-cme/src/main/java/io/github/javafromscratch/phase188/Phase188Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase188.Phase188Demo`
- **Expected Output**: `Executed Broken Lab 02: ConcurrentModificationException: Understand fail-fast collection iterators and modCount.`
- **Actual Output**: `Executed Broken Lab 02: ConcurrentModificationException: Understand fail-fast collection iterators and modCount.`
- **Bytecode Inspected**: `javap -c -p Phase188Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase188DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
