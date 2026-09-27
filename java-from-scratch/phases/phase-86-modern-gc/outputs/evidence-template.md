# Evidence Log: Phase 86 - Modern GC: G1GC vs Generational ZGC

- **Lesson**: Phase 86 - Modern GC: G1GC vs Generational ZGC
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase86/Phase86Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-86-modern-gc/src/main/java/io/github/javafromscratch/phase86/Phase86Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase86.Phase86Demo`
- **Expected Output**: `Executed Modern GC: G1GC vs Generational ZGC: Modern GC trades minor CPU overhead for sub-millisecond pause guarantees.`
- **Actual Output**: `Executed Modern GC: G1GC vs Generational ZGC: Modern GC trades minor CPU overhead for sub-millisecond pause guarantees.`
- **Bytecode Inspected**: `javap -c -p Phase86Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase86DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
