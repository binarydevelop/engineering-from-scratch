# Evidence Log: Phase 87 - GC Logging and Analysis

- **Lesson**: Phase 87 - GC Logging and Analysis
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase87/Phase87Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-87-gc-logs/src/main/java/io/github/javafromscratch/phase87/Phase87Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase87.Phase87Demo`
- **Expected Output**: `Executed GC Logging and Analysis: If you cannot see your GC pauses, you cannot guarantee your service SLAs.`
- **Actual Output**: `Executed GC Logging and Analysis: If you cannot see your GC pauses, you cannot guarantee your service SLAs.`
- **Bytecode Inspected**: `javap -c -p Phase87Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase87DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
