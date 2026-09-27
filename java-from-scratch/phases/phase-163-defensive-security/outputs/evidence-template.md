# Evidence Log: Phase 163 - Defensive Security in Java

- **Lesson**: Phase 163 - Defensive Security in Java
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase163/Phase163Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-163-defensive-security/src/main/java/io/github/javafromscratch/phase163/Phase163Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase163.Phase163Demo`
- **Expected Output**: `Executed Defensive Security in Java: Never trust input; validate boundaries; avoid unsafe reflection and deserialization.`
- **Actual Output**: `Executed Defensive Security in Java: Never trust input; validate boundaries; avoid unsafe reflection and deserialization.`
- **Bytecode Inspected**: `javap -c -p Phase163Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase163DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
