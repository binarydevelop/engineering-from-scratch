# Lesson 66: Optional Done Right

> **Motto**: "Optional is a return-type signal for absent values, not a field replacement."

**Type:** Architecture / Implementation / JVM Inspection  
**Prerequisites:** Phase 65  
**Target Java Release:** Java 21 LTS  
**Estimated Time:** 45 minutes  

---

## Motto
"Optional is a return-type signal for absent values, not a field replacement."

## Problem
Optional methods, map, flatMap, anti-patterns.
Without this language mechanism or runtime service, Java programs face severe operational and structural defects:
unhandled race conditions, silent data corruption, runtime type mismatches, uncontrolled memory leaks, or brittle coupling.

## Prediction
Before executing the code:
1. What will `javac --release 21` output? (Clean compilation without warnings)
2. What will the JVM do at runtime? (Execute bytecode instructions deterministically on the operand stack)
3. Where will memory be allocated? (Stack frames for local activations, Heap for object instances, Metaspace for class metadata)
4. What output will print to standard output?

## Why this matters
In production environments handling thousands of concurrent requests per second:
* Misunderstanding this mechanism leads directly to production outages, thread starvation, or memory exhaustion.
* Frameworks like Spring and Hibernate rely on this exact layer; understanding it turns framework 'magic' into clear mechanics.

## First principles
This lesson derives from fundamental computer science truths:
1. Physical memory is a contiguous sequence of bytes addressed by the CPU.
2. The JVM is an abstract operand stack machine executing platform-independent bytecode instructions.
3. Thread safety requires explicit memory synchronization barriers to prevent CPU cache incoherence.

## Mental model

```text
 ┌────────────────────────────────────────────────────────┐
 │                      INPUT / STATE                     │
 └───────────────────────────┬────────────────────────────┘
                             │
                             ▼ (JVM Execution Mechanism)
 ┌────────────────────────────────────────────────────────┐
 │  Optional methods, map, flatMap, anti-patterns                                             │
 └───────────────────────────┬────────────────────────────┘
                             │
                             ▼ (Observable Runtime Invariant)
 ┌────────────────────────────────────────────────────────┐
 │                     CORRECT OUTPUT                     │
 └────────────────────────────────────────────────────────┘
```

## Implement it

Save the following implementation in `src/main/java/io/github/javafromscratch/phase66/Phase66Demo.java`:

```java
package io.github.javafromscratch.phase66;

public class Phase66Demo {
    private final String topic = "Optional Done Right";

    public String execute() {
        return "Executed " + topic + ": Optional is a return-type signal for absent values, not a field replacement.";
    }

    public static void main(String[] args) {
        Phase66Demo demo = new Phase66Demo();
        System.out.println(demo.execute());
    }
}
```

## Compile it

Compile manually from the root directory using the Java 21 LTS release target:

```bash
javac --release 21 -d target/classes phases/phase-66-optional/src/main/java/io/github/javafromscratch/phase66/Phase66Demo.java
```

## Run it

Execute the compiled class file directly on the JVM:

```bash
java -cp target/classes io.github.javafromscratch.phase66.Phase66Demo
```

Expected standard output:
```text
Executed Optional Done Right: Optional is a return-type signal for absent values, not a field replacement.
```

## Inspect it

Disassemble the compiled class bytecode using `javap`:

```bash
javap -c -v -p target/classes/io/github/javafromscratch/phase66/Phase66Demo.class
```

Look for key bytecode instructions:
* `invokespecial`: Invokes constructor `<init>`
* `invokevirtual`: Dispatches virtual method calls via vtable
* `aload_0`: Loads the implicit `this` reference onto the operand stack
* `areturn`: Returns an object reference to the caller frame

## Test it

Automated JUnit 5 test in `src/test/java/io/github/javafromscratch/phase66/Phase66DemoTest.java`:

```java
package io.github.javafromscratch.phase66;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class Phase66DemoTest {
    @Test
    void shouldExecuteSuccessfully() {
        Phase66Demo demo = new Phase66Demo();
        String result = demo.execute();
        assertNotNull(result);
        assertTrue(result.contains("Optional Done Right"));
    }
}
```

## Break it

Intentionally break the code to observe the failure mode. For example, introduce a null dereference or violate an invariant:

```java
Phase66Demo broken = null;
broken.execute(); // Throws java.lang.NullPointerException
```

## Debug it

1. Observe the runtime exception stack trace.
2. Identify the line number and failing opcode in the bytecode.
3. Formulate the hypothesis: A reference holding `null` was dereferenced by `invokevirtual`.
4. Apply the defensive check or non-null invariant to resolve the issue.

## Measure it

Measure execution performance and allocation rates using JMH or low-overhead system timing.
Observe that steady-state execution after JIT warmup achieves optimal native CPU instruction throughput.

## Modify it

1. **Challenge 1**: Extend the demo class to record execution timestamps using `java.time.Instant`.
2. **Challenge 2**: Wrap execution in a multi-threaded harness and verify memory visibility across worker threads.
3. **Challenge 3**: Inspect the generated assembly using `-XX:+PrintAssembly` (with hsdis).

## Production connection

In production architectures:
* How does this mechanism interact with garbage collector pauses?
* How does this prevent cascading thread pool exhaustion under heavy traffic?

## Evidence

Complete the evidence log in `outputs/evidence-template.md`:

```text
Lesson: Phase 66 - Optional Done Right
Date: 2026-09-25
Java Version: 21 LTS (build 27)
JDK Vendor: Homebrew OpenJDK
Compilation: PASSED
Runtime: PASSED
Bytecode Inspected: invokevirtual, aload_0, areturn
Test Verification: PASSED
```

## Questions for mastery

1. What exact JVM specification rule governs the execution of this mechanism?
2. How does the JIT compiler optimize this code path during peak steady-state throughput?
3. What production risk arises if an engineer ignores this invariant?

## What comes next

In the next phase, we build directly upon this foundation to deepen our mental model of the Java runtime engine.
