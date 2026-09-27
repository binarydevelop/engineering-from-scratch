# Evidence Log: Phase 123 - SQL Injection & PreparedStatement

- **Lesson**: Phase 123 - SQL Injection & PreparedStatement
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase123/Phase123Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-123-prepared-statements/src/main/java/io/github/javafromscratch/phase123/Phase123Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase123.Phase123Demo`
- **Expected Output**: `Executed SQL Injection & PreparedStatement: Never concatenate user input into SQL; parameterize with PreparedStatement.`
- **Actual Output**: `Executed SQL Injection & PreparedStatement: Never concatenate user input into SQL; parameterize with PreparedStatement.`
- **Bytecode Inspected**: `javap -c -p Phase123Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase123DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
