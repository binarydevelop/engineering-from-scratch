# Evidence Log: Phase 06 - Operators and Expressions

- **Lesson**: Phase 06 - Operators and Expressions
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase06/Phase06Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-06-operators-and-expressions/src/main/java/io/github/javafromscratch/phase06/Phase06Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase06.Phase06Demo`
- **Expected Output**: `Executed Operators and Expressions: Short-circuit evaluation is both a performance guard and a null defense.`
- **Actual Output**: `Executed Operators and Expressions: Short-circuit evaluation is both a performance guard and a null defense.`
- **Bytecode Inspected**: `javap -c -p Phase06Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase06DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
