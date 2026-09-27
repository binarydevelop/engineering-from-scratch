# Evidence Log: Phase 170 - The Native Boundary & JNI/FFM

- **Lesson**: Phase 170 - The Native Boundary & JNI/FFM
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase170/Phase170Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-170-native-boundary/src/main/java/io/github/javafromscratch/phase170/Phase170Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase170.Phase170Demo`
- **Expected Output**: `Executed The Native Boundary & JNI/FFM: The JVM interacts with the operating system kernel and hardware via native code.`
- **Actual Output**: `Executed The Native Boundary & JNI/FFM: The JVM interacts with the operating system kernel and hardware via native code.`
- **Bytecode Inspected**: `javap -c -p Phase170Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase170DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
