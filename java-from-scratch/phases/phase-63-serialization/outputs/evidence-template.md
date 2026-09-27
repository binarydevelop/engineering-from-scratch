# Evidence Log: Phase 63 - Serialization Boundaries & JSON

- **Lesson**: Phase 63 - Serialization Boundaries & JSON
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase63/Phase63Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-63-serialization/src/main/java/io/github/javafromscratch/phase63/Phase63Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase63.Phase63Demo`
- **Expected Output**: `Executed Serialization Boundaries & JSON: Java native serialization is a security minefield; prefer explicit text/binary protocols.`
- **Actual Output**: `Executed Serialization Boundaries & JSON: Java native serialization is a security minefield; prefer explicit text/binary protocols.`
- **Bytecode Inspected**: `javap -c -p Phase63Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase63DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
