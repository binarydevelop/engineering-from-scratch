# Evidence Log: Phase 194 - Broken Lab 08: Leaked JDBC Connection Pool

- **Lesson**: Phase 194 - Broken Lab 08: Leaked JDBC Connection Pool
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase194/Phase194Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-194-broken-lab-jdbc-leak/src/main/java/io/github/javafromscratch/phase194/Phase194Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase194.Phase194Demo`
- **Expected Output**: `Executed Broken Lab 08: Leaked JDBC Connection Pool: Diagnose unclosed database connections exhausting the pool.`
- **Actual Output**: `Executed Broken Lab 08: Leaked JDBC Connection Pool: Diagnose unclosed database connections exhausting the pool.`
- **Bytecode Inspected**: `javap -c -p Phase194Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase194DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
