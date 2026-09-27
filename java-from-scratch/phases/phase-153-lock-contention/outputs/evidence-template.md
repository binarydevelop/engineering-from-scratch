# Evidence Log: Phase 153 - Lock Contention & Amdahl's Law

- **Lesson**: Phase 153 - Lock Contention & Amdahl's Law
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase153/Phase153Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-153-lock-contention/src/main/java/io/github/javafromscratch/phase153/Phase153Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase153.Phase153Demo`
- **Expected Output**: `Executed Lock Contention & Amdahl's Law: Amdahl's Law: The speedup of a program is limited by its serial fraction.`
- **Actual Output**: `Executed Lock Contention & Amdahl's Law: Amdahl's Law: The speedup of a program is limited by its serial fraction.`
- **Bytecode Inspected**: `javap -c -p Phase153Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase153DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
