# Evidence Log: Phase 73 - Collectors & Reductions

- **Lesson**: Phase 73 - Collectors & Reductions
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase73/Phase73Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-73-collectors/src/main/java/io/github/javafromscratch/phase73/Phase73Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase73.Phase73Demo`
- **Expected Output**: `Executed Collectors & Reductions: Collectors fold stream elements into complex downstream data structures.`
- **Actual Output**: `Executed Collectors & Reductions: Collectors fold stream elements into complex downstream data structures.`
- **Bytecode Inspected**: `javap -c -p Phase73Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase73DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
