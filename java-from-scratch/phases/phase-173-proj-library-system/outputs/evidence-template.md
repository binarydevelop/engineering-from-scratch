# Evidence Log: Phase 173 - Project 3: Library Management System

- **Lesson**: Phase 173 - Project 3: Library Management System
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase173/Phase173Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-173-proj-library-system/src/main/java/io/github/javafromscratch/phase173/Phase173Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase173.Phase173Demo`
- **Expected Output**: `Executed Project 3: Library Management System: Model domain rules with collections, interfaces, and custom exceptions.`
- **Actual Output**: `Executed Project 3: Library Management System: Model domain rules with collections, interfaces, and custom exceptions.`
- **Bytecode Inspected**: `javap -c -p Phase173Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase173DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
