# Evidence Log: Phase 12 - The String Constant Pool

- **Lesson**: Phase 12 - The String Constant Pool
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase12/Phase12Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-12-string-pool/src/main/java/io/github/javafromscratch/phase12/Phase12Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase12.Phase12Demo`
- **Expected Output**: `Executed The String Constant Pool: The string pool is a JVM intern table deduplicating literal strings.`
- **Actual Output**: `Executed The String Constant Pool: The string pool is a JVM intern table deduplicating literal strings.`
- **Bytecode Inspected**: `javap -c -p Phase12Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase12DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
