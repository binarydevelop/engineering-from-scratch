# Evidence Log: Phase 135 - The Classpath: Mechanics & Disasters

- **Lesson**: Phase 135 - The Classpath: Mechanics & Disasters
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase135/Phase135Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-135-classpath-disasters/src/main/java/io/github/javafromscratch/phase135/Phase135Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase135.Phase135Demo`
- **Expected Output**: `Executed The Classpath: Mechanics & Disasters: The classpath is an ordered list of directories and JARs scanned for .class files.`
- **Actual Output**: `Executed The Classpath: Mechanics & Disasters: The classpath is an ordered list of directories and JARs scanned for .class files.`
- **Bytecode Inspected**: `javap -c -p Phase135Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase135DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
