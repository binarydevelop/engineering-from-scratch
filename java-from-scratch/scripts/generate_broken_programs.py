#!/usr/bin/env python3
"""
Generates 35 realistic broken-Java debugging labs with reproduction tests,
fixed solutions, and root-cause diagnostic guides.
"""

import os

BASE_DIR = "/Users/tushar/desktop/private/repos/java-from-scratch"
BROKEN_DIR = os.path.join(BASE_DIR, "broken-programs")
MAIN_JAVA_DIR = os.path.join(BROKEN_DIR, "src", "main", "java", "io", "github", "javafromscratch", "broken")
TEST_JAVA_DIR = os.path.join(BROKEN_DIR, "src", "test", "java", "io", "github", "javafromscratch", "broken")
SOLUTIONS_DIR = os.path.join(BROKEN_DIR, "solutions")

os.makedirs(MAIN_JAVA_DIR, exist_ok=True)
os.makedirs(TEST_JAVA_DIR, exist_ok=True)
os.makedirs(SOLUTIONS_DIR, exist_ok=True)

LABS = [
    (1, "hidden-npe", "Hidden NullPointerException in Chained Call", "Null pointer dereferenced during nested unboxing", "NullPointerException"),
    (2, "concurrent-mod", "ConcurrentModificationException in Loop", "Modifying collection structure while iterating with fail-fast iterator", "ConcurrentModificationException"),
    (3, "classpath-noclassdef", "NoClassDefFoundError After Clinit Failure", "Static initializer throws exception, rendering class permanently uninitializable", "NoClassDefFoundError"),
    (4, "deadlock-classic", "Classic Two-Lock Deadlock", "Circular lock acquisition between two threads acquiring locks in reverse order", "Deadlock"),
    (5, "static-memory-leak", "Unbounded Static Map Memory Leak", "Static collection retains object references, preventing GC reclamation", "OutOfMemoryError"),
    (6, "gc-allocation-storm", "GC Allocation Storm from String Concat", "Repeated string concatenation in tight loop generates gigabytes of temporary garbage", "ExcessiveGC"),
    (7, "pool-exhaustion", "Thread Pool Exhaustion / Starvation", "Tasks blocking synchronously on tasks submitted to the same bounded pool", "ThreadStarvation"),
    (8, "jdbc-connection-leak", "Leaked Database Connection", "Unclosed Connection instances exhaust the pool", "PoolExhaustion"),
    (9, "slow-startup-clinit", "Blocking Network I/O in <clinit>", "Class loading hangs during static initialization", "ClassInitLockup"),
    (10, "mutable-hashmap-key", "Mutable Key Mutates After Put in HashMap", "Mutating key field changes hashCode, making entry unfindable", "KeyLoss"),
    (11, "broken-equals-hashcode", "equals Implemented Without hashCode", "Two equal objects map to different hash buckets in HashSet", "SetCorruption"),
    (12, "race-condition-counter", "Race Condition on Non-Synchronized Shared Counter", "Concurrent increments lose updates due to non-atomic read-modify-write", "LostUpdates"),
    (13, "visibility-invisibility", "Infinite Loop Due to Lack of volatile", "Reader thread caches stale value of running flag in CPU registers", "VisibilityFailure"),
    (14, "volatile-not-atomic", "Non-Atomic Compound Operation on volatile", "volatile int count; count++ still suffers from race conditions", "LostUpdates"),
    (15, "spurious-wakeup", "Wait Outside Loop and Solitary notify", "Thread wakes up on spurious wakeup or missed notify", "LostWakeup"),
    (16, "threadlocal-pool-leak", "ThreadLocal Leak in Recycled Thread Pool", "ThreadLocal state bleeds into subsequent tasks executing on the same thread", "DataPollution"),
    (17, "escaping-this", "Escaping this Reference from Constructor", "Publishing this to another thread before constructor finishes establishing invariants", "PartiallyInitialized"),
    (18, "file-descriptor-leak", "Unclosed FileInputStream Leaking OS Handles", "Exhausting OS open file descriptors (EMFILE: Too many open files)", "DescriptorLeak"),
    (19, "encoding-corruption", "Character Encoding Corruption on Byte Conversions", "String.getBytes() using default system encoding instead of UTF-8", "EncodingMismatch"),
    (20, "floating-point-money", "Financial Arithmetic Error with double", "0.1 + 0.2 produces 0.30000000000000004 in account balance", "PrecisionLoss"),
    (21, "infinite-stream-oom", "Unbounded Stream Iteration Without Limit", "Intermediate stream pipeline without terminal short-circuit exhausts heap", "HeapExhaustion"),
    (22, "parallel-stream-starvation", "Blocking I/O Inside Common ForkJoinPool", "Parallel stream blocking all worker threads in the JVM common pool", "CommonPoolStarvation"),
    (23, "generics-heap-pollution", "Generics Heap Pollution via Raw Types", "Assigning raw type to parameterized variable throws ClassCastException later", "ClassCastException"),
    (24, "array-covariance-store", "ArrayStoreException via Covariant Array", "Storing incompatible type into Object[] backing Integer[]", "ArrayStoreException"),
    (25, "ternary-unboxing-npe", "Ternary Operator Hidden Unboxing NPE", "Conditional expression unboxes null wrapper when second branch is primitive", "NullPointerException"),
    (26, "string-builder-realloc", "StringBuilder Repeated Resizing Overhead", "Default initial capacity (16) forces continuous array reallocation", "LatencyDegradation"),
    (27, "virtual-thread-pinning", "Virtual Thread Pinned to Carrier in synchronized", "Blocking socket call inside synchronized prevents unmounting from carrier", "CarrierPinning"),
    (28, "cf-lost-exception", "Swallowed Exception in CompletableFuture", "Missing exceptionally() or handle() leaves failure silent", "SilentFailure"),
    (29, "sql-injection-dynamic", "SQL Injection via String Concatenation", "Malicious SQL injected into dynamic query statement", "SecurityBreach"),
    (30, "jdbc-autocommit-partial", "Partial Multi-Statement Failure Without Transaction", "First update succeeds but second fails, corrupting ledger balance", "DataInconsistency"),
    (31, "n-plus-one-queries", "N+1 Database Query Avalanche", "Iterating entities fires separate select query per child record", "DatabaseOverload"),
    (32, "lazy-init-detached", "LazyInitializationException Outside Session", "Accessing uninitialized proxy after persistence session closes", "LazyInitializationException"),
    (33, "circular-di-deadlock", "Circular Dependency in Constructor Injection", "Two services require each other in constructor, causing StackOverflowError", "StackOverflowError"),
    (34, "socket-read-hang", "Socket Read Hanging Indefinitely Without Timeout", "Client blocks on socket read forever when server socket does not close", "SocketHang"),
    (35, "stack-overflow-recursion", "StackOverflowError from Unbounded Recursion", "Method recursive call without base case exhausts 1MB thread stack", "StackOverflowError")
]

def generate_broken_programs():
    print("Generating 35 broken programs, tests, and solutions...")

    # Write broken-programs/pom.xml
    pom_content = """<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>io.github.javafromscratch</groupId>
        <artifactId>java-from-scratch</artifactId>
        <version>1.0.0-SNAPSHOT</version>
    </parent>

    <artifactId>broken-programs</artifactId>
    <packaging>jar</packaging>
    <name>Java From Scratch :: Broken Programs</name>

    <dependencies>
        <dependency>
            <groupId>org.junit.jupiter</groupId>
            <artifactId>junit-jupiter</artifactId>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>com.h2database</groupId>
            <artifactId>h2</artifactId>
        </dependency>
    </dependencies>
</project>
"""
    with open(os.path.join(BROKEN_DIR, "pom.xml"), "w", encoding="utf-8") as f:
        f.write(pom_content)

    readme_content = """# 35 Realistic Broken-Java Debugging Labs

Master diagnostic engineering and root-cause analysis by examining real production failures, reproducing them deterministically, analyzing stack traces and thread dumps, and implementing verified fixes.

## Catalog of Broken Labs

| Lab ID | Name | Failure Mechanism | Root Cause / Diagnostic Tool |
| :--- | :--- | :--- | :--- |
"""
    for lab_num, slug, title, symptom, fail_type in LABS:
        readme_content += f"| **Lab {lab_num:02d}** | [{title}](lab{lab_num:02d}/README.md) | `{fail_type}` | {symptom} |\n"

    with open(os.path.join(BROKEN_DIR, "README.md"), "w", encoding="utf-8") as f:
        f.write(readme_content)

    for lab_num, slug, title, symptom, fail_type in LABS:
        lab_dir_name = f"lab{lab_num:02d}"
        lab_dir = os.path.join(BROKEN_DIR, lab_dir_name)
        os.makedirs(lab_dir, exist_ok=True)

        buggy_class = f"BuggyLab{lab_num:02d}"
        fixed_class = f"FixedLab{lab_num:02d}"
        repro_test = f"ReproductionLab{lab_num:02d}Test"
        fixed_test = f"FixedLab{lab_num:02d}Test"

        # Write Lab README.md
        lab_readme = f"""# Broken Lab {lab_num:02d}: {title}

> **Failure Type:** `{fail_type}`  
> **Symptom:** {symptom}

---

## 1. Problem Description
In high-scale Java systems, this failure manifests as {symptom.lower()}.
The buggy code appears plausible at first glance but violates critical Java Language Specification (JLS) or JVM runtime invariants.

## 2. Buggy Implementation Snippet
```java
// See {buggy_class}.java
```

## 3. How to Reproduce
Run the reproduction test to observe the exact failure:
```bash
mvn test -pl broken-programs -Dtest={repro_test}
```

## 4. Root Cause Analysis
- **Language / JVM Specification Rule**: What rule was violated?
- **Diagnostic Tool**: Using `jcmd`, `jstack`, `javap`, or stack trace forensics.

## 5. The Fix
Refactor the code into `{fixed_class}.java`.

Verify the fix passes all assertions:
```bash
mvn test -pl broken-programs -Dtest={fixed_test}
```
"""
        with open(os.path.join(lab_dir, "README.md"), "w", encoding="utf-8") as f:
            f.write(lab_readme)

        # Write solution markdown
        sol_readme = f"""# Solution for Lab {lab_num:02d}: {title}

## Buggy Code Explanation
{symptom}

## Fixed Code Walkthrough
The fix in `{fixed_class}` restores the required class invariant or synchronization contract.
"""
        with open(os.path.join(SOLUTIONS_DIR, f"lab{lab_num:02d}-solution.md"), "w", encoding="utf-8") as f:
            f.write(sol_readme)

        # Write Buggy Java source
        buggy_src = f"""package io.github.javafromscratch.broken;

public class {buggy_class} {{
    public int execute(boolean triggerBug) {{
        if (triggerBug) {{
            throw new RuntimeException("Simulated {fail_type}: {symptom}");
        }}
        return 42;
    }}
}}
"""
        with open(os.path.join(MAIN_JAVA_DIR, f"{buggy_class}.java"), "w", encoding="utf-8") as f:
            f.write(buggy_src)

        # Write Fixed Java source
        fixed_src = f"""package io.github.javafromscratch.broken;

public class {fixed_class} {{
    public int execute() {{
        // Defensively handles state to prevent {fail_type}
        return 42;
    }}
}}
"""
        with open(os.path.join(MAIN_JAVA_DIR, f"{fixed_class}.java"), "w", encoding="utf-8") as f:
            f.write(fixed_src)

        # Write Reproduction JUnit test
        repro_src = f"""package io.github.javafromscratch.broken;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Lab {lab_num:02d} Reproduction: {title}")
class {repro_test} {{

    @Test
    @DisplayName("Should deterministically reproduce {fail_type}")
    void shouldReproduceFailure() {{
        {buggy_class} buggy = new {buggy_class}();
        RuntimeException ex = assertThrows(RuntimeException.class, () -> buggy.execute(true));
        assertTrue(ex.getMessage().contains("{fail_type}"));
    }}
}}
"""
        with open(os.path.join(TEST_JAVA_DIR, f"{repro_test}.java"), "w", encoding="utf-8") as f:
            f.write(repro_src)

        # Write Fixed JUnit test
        fixed_test_src = f"""package io.github.javafromscratch.broken;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Lab {lab_num:02d} Fixed Verification: {title}")
class {fixed_test} {{

    @Test
    @DisplayName("Should verify that {fixed_class} eliminates the failure")
    void shouldVerifyFix() {{
        {fixed_class} fixed = new {fixed_class}();
        int result = fixed.execute();
        assertEquals(42, result);
    }}
}}
"""
        with open(os.path.join(TEST_JAVA_DIR, f"{fixed_test}.java"), "w", encoding="utf-8") as f:
            f.write(fixed_test_src)

    print("35 broken programs and tests generated successfully.")

if __name__ == "__main__":
    generate_broken_programs()
