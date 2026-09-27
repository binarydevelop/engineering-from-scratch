# Lesson Template

Use this canonical template when authoring, reviewing, or completing any lesson in `java-from-scratch`. Every lesson must honor the repository motto:

> **Understand it. Compile it. Run it. Inspect it. Break it. Debug it. Measure it. Ship it.**

---

# Lesson [XX]: [Lesson Title]

> **Motto**: "[A memorable, punchy one-sentence principle that captures the technical reality.]"

**Type:** Implementation / Inspection / Concurrency Lab / Performance Lab  
**Prerequisites:** [List prior phase numbers]  
**Target Java Release:** Java 21 LTS  
**Estimated Time:** [e.g., 45 minutes]

---

## Motto
State the motto clearly with conceptual emphasis.

## Problem
Explain the concrete, practical problem that makes this language or runtime mechanism necessary.
* What happens if this mechanism does not exist?
* Show the pain point using minimal, intuitive code before the feature is introduced.
* Do not start with syntax; start with the engineering failure.

## Prediction
Before compiling or running any code:
1. What will the compiler do? (Succeed, produce warning, or emit specific compiler error?)
2. What will the JVM do at runtime?
3. What will memory (Heap, Stack, Metaspace) look like?
4. What output is printed to standard output or standard error?

Write down your hypothesis explicitly before touching the shell.

## Why this matters
Explain the real-world operational consequence:
* What production outages, silent data corruption, thread deadlocks, memory leaks, or latency degradation happen when an engineer misunderstands this mechanism?
* Connect language syntax to JVM runtime behavior.

## First principles
Derive the concept from fundamental computer science truths:
* OS processes, threads, virtual address spaces, and hardware caches.
* Bytecode execution on an abstract operand stack machine.
* Reference resolution, pointer mechanics, and garbage collection roots.
* Happens-before relations and memory barrier instructions.
* Avoid hand-waving or reciting slogans.

## Mental model
Provide a precise ASCII diagram illustrating the state transition, memory layout, class hierarchy, or execution pipeline:

```text
[Input / Source]
       │
       ▼
 [Transformation]  ───► [JVM / Memory Consequence]
       │
       ▼
 [Final State / Output]
```

## Implement it
Provide the complete, self-contained Java source code. No ellipsis (`...`), no hidden imports, no missing declarations.

```java
package io.github.javafromscratch.phaseXX;

public class Demonstration {
    public static void main(String[] args) {
        // Implementation
    }
}
```

## Compile it
Specify the exact terminal command used to compile:

```bash
javac --release 21 -d target/classes src/main/java/io/github/javafromscratch/phaseXX/Demonstration.java
```

## Run it
Specify the exact command to execute the compiled bytecode:

```bash
java -cp target/classes io.github.javafromscratch.phaseXX.Demonstration
```

Show the exact standard output.

## Inspect it
Use JDK diagnostic tools to see underneath the syntax:
* Disassemble bytecode: `javap -c -v -p target/classes/...`
* Inspect runtime flags: `java -XX:+PrintFlagsFinal -version`
* Inspect threads: `jcmd <pid> Thread.print` or `jstack <pid>`
* Inspect heap/classes: `jcmd <pid> GC.class_histogram`

Explain key bytecode instructions (e.g., `invokevirtual`, `invokestatic`, `monitorenter`, `aload`, `ireturn`).

## Test it
Provide automated JUnit 5 tests asserting correct behavior, invariants, and edge cases:

```java
@Test
void shouldDemonstrateExpectedBehavior() {
    // Assertions asserting runtime invariants
}
```

## Break it
Intentionally break the code to trigger the failure mode:
* Break an invariant.
* Mutate an object inside a hash-based collection.
* Omit synchronization or `volatile`.
* Force an `OutOfMemoryError`, `StackOverflowError`, or `ConcurrentModificationException`.

Show the broken code snippet.

## Debug it
Walk through the diagnostic workflow:
1. What was the exact exception or corrupted output?
2. How do you read the stack trace or thread dump?
3. Which tool revealed the root cause (`jstack`, `javap`, heap dump, or debugger)?
4. What language or JVM specification rule explains the failure?
5. Show the fixed code.

## Measure it
Measure execution time, allocation rate, memory footprint, or lock contention:
* Naive measurement pitfall vs proper warmup.
* JMH microbenchmark where applicable.
* Log output or memory metrics.

## Modify it
Exercises for the learner to alter the code:
1. **Challenge 1**: [Specific modification and predicted outcome]
2. **Challenge 2**: [Stress test with high concurrency or large data volume]
3. **Challenge 3**: [Refactor to alternate idiomatic pattern]

## Production connection
How does this manifest in real high-scale backend systems:
* Connection pools, database queries, thread pool exhaustion, latency percentiles.
* How frameworks (Spring, Micronaut, Quarkus, Netty) rely on this mechanism underneath.

## Evidence
Fill out the structured evidence template verifying execution:

```text
Lesson: Phase XX
Date: YYYY-MM-DD
Java version: 21 (build 27)
JDK vendor: Homebrew OpenJDK
Prediction: [Hypothesis]
Compilation: PASSED
Runtime: PASSED
Actual output matches prediction: YES/NO
Bytecode inspected: [Key opcode observed]
Breakage verified: [Observed exception/failure]
Root cause identified: [Technical explanation]
Fix confirmed: [Test pass status]
```

## Questions for mastery
High-caliber reasoning questions (no trivia):
1. [Scenario-based question testing JVM mechanics]
2. [Question testing concurrency, memory visibility, or type erasure]
3. [Question evaluating production tradeoffs]

## What comes next
Preview the next logical concept in the roadmap and explain why this lesson is a prerequisite for it.
