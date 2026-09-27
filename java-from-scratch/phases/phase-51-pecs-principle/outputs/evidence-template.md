# Evidence Log: Phase 51 - The PECS Principle

- **Lesson**: Phase 51 - The PECS Principle
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase51/Phase51Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-51-pecs-principle/src/main/java/io/github/javafromscratch/phase51/Phase51Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase51.Phase51Demo`
- **Expected Output**: `Executed The PECS Principle: Use ? extends T when reading data out; use ? super T when putting data in.`
- **Actual Output**: `Executed The PECS Principle: Use ? extends T when reading data out; use ? super T when putting data in.`
- **Bytecode Inspected**: `javap -c -p Phase51Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase51DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
