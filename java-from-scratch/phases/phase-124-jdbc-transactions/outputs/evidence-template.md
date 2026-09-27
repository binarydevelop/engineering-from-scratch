# Evidence Log: Phase 124 - Database Transactions: ACID in Java

- **Lesson**: Phase 124 - Database Transactions: ACID in Java
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase124/Phase124Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-124-jdbc-transactions/src/main/java/io/github/javafromscratch/phase124/Phase124Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase124.Phase124Demo`
- **Expected Output**: `Executed Database Transactions: ACID in Java: Transactions group operations into indivisible units of atomic durability.`
- **Actual Output**: `Executed Database Transactions: ACID in Java: Transactions group operations into indivisible units of atomic durability.`
- **Bytecode Inspected**: `javap -c -p Phase124Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase124DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
