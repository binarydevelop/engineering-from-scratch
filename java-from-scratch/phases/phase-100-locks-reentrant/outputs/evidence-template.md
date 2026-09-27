# Evidence Log: Phase 100 - Explicit Locks: ReentrantLock

- **Lesson**: Phase 100 - Explicit Locks: ReentrantLock
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase100/Phase100Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-100-locks-reentrant/src/main/java/io/github/javafromscratch/phase100/Phase100Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase100.Phase100Demo`
- **Expected Output**: `Executed Explicit Locks: ReentrantLock: ReentrantLock provides timed, interruptible, and fair lock acquisition.`
- **Actual Output**: `Executed Explicit Locks: ReentrantLock: ReentrantLock provides timed, interruptible, and fair lock acquisition.`
- **Bytecode Inspected**: `javap -c -p Phase100Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase100DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
