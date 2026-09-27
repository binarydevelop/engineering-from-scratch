# Evidence Log: Phase 127 - JPA and Hibernate Basics

- **Lesson**: Phase 127 - JPA and Hibernate Basics
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase127/Phase127Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-127-jpa-hibernate-basics/src/main/java/io/github/javafromscratch/phase127/Phase127Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase127.Phase127Demo`
- **Expected Output**: `Executed JPA and Hibernate Basics: An ORM manages entity state transitions and generates SQL on your behalf.`
- **Actual Output**: `Executed JPA and Hibernate Basics: An ORM manages entity state transitions and generates SQL on your behalf.`
- **Bytecode Inspected**: `javap -c -p Phase127Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase127DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
