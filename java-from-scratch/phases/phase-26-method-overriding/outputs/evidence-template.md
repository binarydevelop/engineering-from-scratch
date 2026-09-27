# Evidence Log: Phase 26 - Method Overriding vs Overloading

- **Lesson**: Phase 26 - Method Overriding vs Overloading
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase26/Phase26Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-26-method-overriding/src/main/java/io/github/javafromscratch/phase26/Phase26Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase26.Phase26Demo`
- **Expected Output**: `Executed Method Overriding vs Overloading: Overloading is resolved statically at compile time; overriding dynamically at runtime.`
- **Actual Output**: `Executed Method Overriding vs Overloading: Overloading is resolved statically at compile time; overriding dynamically at runtime.`
- **Bytecode Inspected**: `javap -c -p Phase26Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase26DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
