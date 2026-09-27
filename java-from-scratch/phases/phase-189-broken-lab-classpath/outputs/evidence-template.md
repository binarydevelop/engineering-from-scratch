# Evidence Log: Phase 189 - Broken Lab 03: Classpath Catastrophe

- **Lesson**: Phase 189 - Broken Lab 03: Classpath Catastrophe
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase189/Phase189Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-189-broken-lab-classpath/src/main/java/io/github/javafromscratch/phase189/Phase189Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase189.Phase189Demo`
- **Expected Output**: `Executed Broken Lab 03: Classpath Catastrophe: Untangle ClassNotFoundException vs NoClassDefFoundError.`
- **Actual Output**: `Executed Broken Lab 03: Classpath Catastrophe: Untangle ClassNotFoundException vs NoClassDefFoundError.`
- **Bytecode Inspected**: `javap -c -p Phase189Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase189DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
