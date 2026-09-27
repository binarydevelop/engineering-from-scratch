# Evidence Log: Phase 24 - Inheritance & Subtyping

- **Lesson**: Phase 24 - Inheritance & Subtyping
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase24/Phase24Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-24-inheritance/src/main/java/io/github/javafromscratch/phase24/Phase24Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase24.Phase24Demo`
- **Expected Output**: `Executed Inheritance & Subtyping: Inheritance is for 'is-a' substitution, not a code-reuse shortcut.`
- **Actual Output**: `Executed Inheritance & Subtyping: Inheritance is for 'is-a' substitution, not a code-reuse shortcut.`
- **Bytecode Inspected**: `javap -c -p Phase24Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase24DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
