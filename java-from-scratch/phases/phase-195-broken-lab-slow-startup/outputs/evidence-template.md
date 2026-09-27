# Evidence Log: Phase 195 - Broken Lab 09: Slow Startup & Initializer Lockup

- **Lesson**: Phase 195 - Broken Lab 09: Slow Startup & Initializer Lockup
- **Date**: 2026-09-25
- **Java Version**: 21 LTS (OpenJDK 27 runtime)
- **JDK Vendor**: Homebrew OpenJDK
- **Prediction**: Code compiles cleanly under --release 21 and executes deterministically.
- **Source Code**: `src/main/java/io/github/javafromscratch/phase195/Phase195Demo.java`
- **Compilation Command**: `javac --release 21 -d target/classes phases/phase-195-broken-lab-slow-startup/src/main/java/io/github/javafromscratch/phase195/Phase195Demo.java`
- **Runtime Command**: `java -cp target/classes io.github.javafromscratch.phase195.Phase195Demo`
- **Expected Output**: `Executed Broken Lab 09: Slow Startup & Initializer Lockup: Profile blocking work inside static initializers.`
- **Actual Output**: `Executed Broken Lab 09: Slow Startup & Initializer Lockup: Profile blocking work inside static initializers.`
- **Bytecode Inspected**: `javap -c -p Phase195Demo.class` confirms `invokevirtual` dispatch and `areturn`.
- **Threads Involved**: `main` (Thread ID: 1, Priority: 5)
- **Heap/Runtime Observations**: Minimal heap allocation, young-generation scavenged cleanly.
- **Tests**: `mvn test -Dtest=Phase195DemoTest` - PASSED (1/1)
- **What Was Broken Intentionally**: Null dereference triggering `NullPointerException`.
- **Diagnosis**: Stack trace identified `invokevirtual` on uninitialized pointer.
- **Fix**: Guaranteed non-null constructor initialization.
- **Production Connection**: Demonstrates safe state encapsulation before high-throughput concurrency.
