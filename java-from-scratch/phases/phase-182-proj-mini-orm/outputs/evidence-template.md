# Evidence Log: Phase 182 - Project 12: Mini Object-Relational Mapper

- **Lesson**: Phase 182 - Project 12: Mini Object-Relational Mapper
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase182/Phase182Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-182-proj-mini-orm/src/main/java/io/github/javafromscratch/phase182/Phase182Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase182.Phase182Demo`
- **Expected Output**: `Executed Project 12: Mini Object-Relational Mapper: Map SQL rows to Java domain objects via reflection and metadata.`
- **Actual Output**: `Executed Project 12: Mini Object-Relational Mapper: Map SQL rows to Java domain objects via reflection and metadata.`
- **Bytecode Inspected**: `javap -c -p Phase182Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase182DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
