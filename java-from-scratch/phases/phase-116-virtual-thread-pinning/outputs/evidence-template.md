# Evidence Log: Phase 116 - Virtual Thread Pinning Caveats

- **Lesson**: Phase 116 - Virtual Thread Pinning Caveats
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase116/Phase116Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-116-virtual-thread-pinning/src/main/java/io/github/javafromscratch/phase116/Phase116Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase116.Phase116Demo`
- **Expected Output**: `Executed Virtual Thread Pinning Caveats: synchronized blocks pin virtual threads to carrier threads; use ReentrantLock.`
- **Actual Output**: `Executed Virtual Thread Pinning Caveats: synchronized blocks pin virtual threads to carrier threads; use ReentrantLock.`
- **Bytecode Inspected**: `javap -c -p Phase116Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase116DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
