# Evidence Log: Phase 134 - Anatomy of a JAR File

- **Lesson**: Phase 134 - Anatomy of a JAR File
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase134/Phase134Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-134-jar-packaging/src/main/java/io/github/javafromscratch/phase134/Phase134Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase134.Phase134Demo`
- **Expected Output**: `Executed Anatomy of a JAR File: A JAR is a ZIP archive with a META-INF/MANIFEST.MF contract.`
- **Actual Output**: `Executed Anatomy of a JAR File: A JAR is a ZIP archive with a META-INF/MANIFEST.MF contract.`
- **Bytecode Inspected**: `javap -c -p Phase134Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase134DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
