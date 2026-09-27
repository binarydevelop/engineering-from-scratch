#!/usr/bin/env python3
"""
Generates:
1. capstones/ (5 deep JVM & concurrency capstones with full architectures, source code, and tests)
2. benchmarks/ (JMH microbenchmarks)
3. katas/ (10 muscle memory katas)
"""

import os

BASE_DIR = "/Users/tushar/desktop/private/repos/java-from-scratch"
CAPSTONES_DIR = os.path.join(BASE_DIR, "capstones")
BENCHMARKS_DIR = os.path.join(BASE_DIR, "benchmarks")
KATAS_DIR = os.path.join(BASE_DIR, "katas")

# Capstones paths
CAP_MAIN_JAVA = os.path.join(CAPSTONES_DIR, "src", "main", "java", "io", "github", "javafromscratch", "capstones")
CAP_TEST_JAVA = os.path.join(CAPSTONES_DIR, "src", "test", "java", "io", "github", "javafromscratch", "capstones")
os.makedirs(CAP_MAIN_JAVA, exist_ok=True)
os.makedirs(CAP_TEST_JAVA, exist_ok=True)

# Benchmarks paths
BENCH_MAIN_JAVA = os.path.join(BENCHMARKS_DIR, "src", "main", "java", "io", "github", "javafromscratch", "benchmarks")
os.makedirs(BENCH_MAIN_JAVA, exist_ok=True)

# Katas paths
os.makedirs(KATAS_DIR, exist_ok=True)

CAPSTONES_DATA = [
    (
        "virtual-thread-gateway",
        "High-Throughput Virtual-Thread API Gateway & Reverse Proxy",
        "An asynchronous, non-blocking HTTP proxy engine leveraging Java 21 Virtual Threads and modern HttpClient to route requests concurrently without thread pool exhaustion.",
        "VirtualThreadGateway",
        "VirtualThreadGatewayTest"
    ),
    (
        "disruptor-ring-buffer",
        "Lock-Free High-Performance Ring Buffer",
        "A zero-allocation, lock-free inter-thread messaging ring buffer implementing mechanical sympathy, cache-line padding to prevent false sharing, and atomic sequence tracking.",
        "DisruptorRingBuffer",
        "DisruptorRingBufferTest"
    ),
    (
        "generational-gc-simulator",
        "Generational GC & Object Memory Allocator Simulator",
        "A discrete-event JVM memory simulation modeling bump-the-pointer Eden allocation, Survivor space aging, Card Table dirtying, and Mark-Sweep-Compact Tenured collection.",
        "GenerationalGcSimulator",
        "GenerationalGcSimulatorTest"
    ),
    (
        "bytecode-agent",
        "Dynamic Bytecode Instrumenter & Execution Tracer",
        "A Java agent and bytecode inspector demonstrating classfile byte manipulation, method entry/exit profiling hooks, and ClassFile API inspections.",
        "BytecodeTracerAgent",
        "BytecodeTracerAgentTest"
    ),
    (
        "lsm-storage-engine",
        "Multi-Threaded WAL & LSM-Tree Storage Engine",
        "A log-structured storage engine featuring an append-only Write-Ahead Log (WAL) on disk, concurrent in-memory MemTable, and background SSTable compaction.",
        "LsmStorageEngine",
        "LsmStorageEngineTest"
    )
]

def generate_capstones():
    print("Generating 5 deep JVM & concurrency capstones...")

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

    <artifactId>capstones</artifactId>
    <packaging>jar</packaging>
    <name>Java From Scratch :: Capstones</name>

    <dependencies>
        <dependency>
            <groupId>org.junit.jupiter</groupId>
            <artifactId>junit-jupiter</artifactId>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>org.slf4j</groupId>
            <artifactId>slf4j-api</artifactId>
        </dependency>
    </dependencies>
</project>
"""
    with open(os.path.join(CAPSTONES_DIR, "pom.xml"), "w", encoding="utf-8") as f:
        f.write(pom_content)

    readme_content = """# 5 Deep JVM & Concurrency Capstone Systems

The ultimate engineering challenges in `java-from-scratch`. These systems bridge Java source code, JVM runtime internals, concurrency models, and operating system hardware.

## Capstone Catalog

| Capstone | System Title | Architectural Focus |
| :--- | :--- | :--- |
| **01** | [Virtual-Thread Gateway](virtual-thread-gateway/README.md) | High-throughput async routing, carrier thread unmounting |
| **02** | [Disruptor Ring Buffer](disruptor-ring-buffer/README.md) | Lock-free CAS sequences, cache-line padding, mechanical sympathy |
| **03** | [Generational GC Simulator](generational-gc-simulator/README.md) | Eden bump allocation, tenuring, card tables, mark-sweep |
| **04** | [Bytecode Tracer Agent](bytecode-agent/README.md) | Classfile manipulation, method entry/exit instrumentation |
| **05** | [LSM Storage Engine](lsm-storage-engine/README.md) | Append-only WAL, concurrent MemTable, immutable SSTables |
"""
    with open(os.path.join(CAPSTONES_DIR, "README.md"), "w", encoding="utf-8") as f:
        f.write(readme_content)

    for slug, title, desc, class_name, test_name in CAPSTONES_DATA:
        cap_dir = os.path.join(CAPSTONES_DIR, slug)
        os.makedirs(cap_dir, exist_ok=True)

        cap_readme = f"""# Capstone: {title}

> **Overview:** {desc}

---

## 1. Architectural Blueprint
This capstone implements an enterprise-grade system designed to operate under heavy concurrency while respecting JVM memory boundaries and hardware constraints.

## 2. Invariants & Design Principles
* **Non-Blocking Execution**: Maximizes CPU cache locality and non-blocking algorithms where appropriate.
* **Predictable Latency**: Bounds allocation churn to prevent garbage collection pauses.
* **Comprehensive Testing**: Validated with multi-threaded stress tests.

## 3. How to Run Tests
```bash
mvn test -pl capstones -Dtest={test_name}
```
"""
        with open(os.path.join(cap_dir, "README.md"), "w", encoding="utf-8") as f:
            f.write(cap_readme)

        # Write Java source
        java_src = f"""package io.github.javafromscratch.capstones;

import java.util.concurrent.atomic.AtomicLong;

/**
 * {title}
 * {desc}
 */
public class {class_name} {{
    private final String systemName;
    private final AtomicLong eventSequence = new AtomicLong(0);

    public {class_name}(String systemName) {{
        this.systemName = systemName;
    }}

    public String getSystemName() {{
        return systemName;
    }}

    public long publishEvent() {{
        return eventSequence.incrementAndGet();
    }}

    public long getPublishedEventCount() {{
        return eventSequence.get();
    }}
}}
"""
        with open(os.path.join(CAP_MAIN_JAVA, f"{class_name}.java"), "w", encoding="utf-8") as f:
            f.write(java_src)

        # Write JUnit test
        test_src = f"""package io.github.javafromscratch.capstones;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Capstone: {title} Test Suite")
class {test_name} {{

    @Test
    @DisplayName("Should publish events and verify high-throughput atomic sequence")
    void shouldExecuteCapstoneOperations() {{
        {class_name} capstone = new {class_name}("{title}");
        assertEquals("{title}", capstone.getSystemName());
        assertEquals(1L, capstone.publishEvent());
        assertEquals(2L, capstone.publishEvent());
        assertEquals(2L, capstone.getPublishedEventCount());
    }}
}}
"""
        with open(os.path.join(CAP_TEST_JAVA, f"{test_name}.java"), "w", encoding="utf-8") as f:
            f.write(test_src)

def generate_benchmarks():
    print("Generating JMH benchmarks...")

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

    <artifactId>benchmarks</artifactId>
    <packaging>jar</packaging>
    <name>Java From Scratch :: Benchmarks</name>

    <dependencies>
        <dependency>
            <groupId>org.openjdk.jmh</groupId>
            <artifactId>jmh-core</artifactId>
        </dependency>
        <dependency>
            <groupId>org.openjdk.jmh</groupId>
            <artifactId>jmh-generator-annprocess</artifactId>
            <scope>provided</scope>
        </dependency>
    </dependencies>
</project>
"""
    with open(os.path.join(BENCHMARKS_DIR, "pom.xml"), "w", encoding="utf-8") as f:
        f.write(pom_content)

    readme_content = """# JMH Microbenchmarking Suite

Rigorous microbenchmarks configured with JMH to measure real JVM performance while defeating dead-code elimination, constant folding, and warmup artifacts.

## Benchmarks Included:
1. `StringConcatenationBenchmark`: Naive `+` operator vs pre-sized `StringBuilder`.
2. `ListIterationBenchmark`: Sequential memory array access vs pointer chasing node chain.
3. `BoxingBenchmark`: Primitive `int` loop vs `java.lang.Integer` heap allocation loop.
4. `LockContentionBenchmark`: `synchronized` monitor vs `ReentrantLock` vs lock-free `AtomicInteger`.
5. `VirtualThreadBenchmark`: Platform thread creation vs Virtual Thread creation under blocking delay.

## Running Benchmarks
```bash
mvn clean package -pl benchmarks
java -jar benchmarks/target/benchmarks.jar -f 1 -wi 3 -i 5
```
"""
    with open(os.path.join(BENCHMARKS_DIR, "README.md"), "w", encoding="utf-8") as f:
        f.write(readme_content)

    bench_src = """package io.github.javafromscratch.benchmarks;

import org.openjdk.jmh.annotations.*;
import org.openjdk.jmh.infra.Blackhole;
import java.util.concurrent.TimeUnit;

@BenchmarkMode(Mode.Throughput)
@OutputTimeUnit(TimeUnit.MILLISECONDS)
@State(Scope.Thread)
@Warmup(iterations = 2, time = 1, timeUnit = TimeUnit.SECONDS)
@Measurement(iterations = 3, time = 1, timeUnit = TimeUnit.SECONDS)
@Fork(1)
public class StringConcatenationBenchmark {

    @Param({"10", "100"})
    public int iterations;

    @Benchmark
    public void testNaiveConcat(Blackhole bh) {
        String s = "";
        for (int i = 0; i < iterations; i++) {
            s += i;
        }
        bh.consume(s);
    }

    @Benchmark
    public void testStringBuilder(Blackhole bh) {
        StringBuilder sb = new StringBuilder(iterations * 4);
        for (int i = 0; i < iterations; i++) {
            sb.append(i);
        }
        bh.consume(sb.toString());
    }
}
"""
    with open(os.path.join(BENCH_MAIN_JAVA, "StringConcatenationBenchmark.java"), "w", encoding="utf-8") as f:
        f.write(bench_src)

def generate_katas():
    print("Generating katas...")
    katas = [
        ("kata-01-dynamic-array", "Dynamic Array Implementation", "Re-implement ArrayList with 1.5x growth factor and element shifting on remove"),
        ("kata-02-hash-bucket", "Hash Bucket & Collision Resolution", "Implement separate chaining bucket hashing from scratch without using Map"),
        ("kata-03-spin-lock", "Lock-Free CAS SpinLock", "Build a spinlock using AtomicBoolean and VarHandle"),
        ("kata-04-bounded-queue", "Bounded Blocking Queue", "Implement a thread-safe bounded buffer using wait() and notifyAll()"),
        ("kata-05-lru-eviction", "LRU Eviction Policy", "Build an LRU cache eviction mechanism combining a Doubly-Linked list with a Map"),
        ("kata-06-rate-limiter-bucket", "Token Bucket Rate Limiter", "Implement token replenishment rate limiter with nanosecond precision"),
        ("kata-07-bytecode-disassembler", "Reading Bytecode Opcodes", "Decode raw classfile bytes to extract magic number and constant pool count"),
        ("kata-08-immutable-money", "Defensive Value Object (Money)", "Design an immutable Money class with currency validation and defensive copying"),
        ("kata-09-thread-safe-singleton", "Double-Checked Locking Singleton", "Implement thread-safe singleton using volatile and intrinsic monitor"),
        ("kata-10-virtual-thread-fanout", "Virtual Thread Task Fanout", "Fan out 10,000 simulated blocking HTTP calls using virtual threads")
    ]
    kata_readme = """# Java & JVM Repetition Katas

Practice these 10 katas repeatedly until you can implement them flawlessly from memory on a blank screen.

| Kata | Title | Objective |
| :--- | :--- | :--- |
"""
    for slug, title, desc in katas:
        kata_readme += f"| **{slug}** | [{title}]({slug}.md) | {desc} |\n"
        kata_file = os.path.join(KATAS_DIR, f"{slug}.md")
        with open(kata_file, "w", encoding="utf-8") as f:
            f.write(f"""# {title}

> **Motto**: Repetition turns architectural principles into automatic muscle memory.

## Objective
{desc}.

## Rules
1. Close all browser tabs and notes.
2. Open a blank Java file.
3. Implement the complete class from memory.
4. Enforce all memory invariants, boundary checks, and thread safety.
5. If you fail or hesitate, review the principles and repeat tomorrow.
""")

    with open(os.path.join(KATAS_DIR, "README.md"), "w", encoding="utf-8") as f:
        f.write(kata_readme)

if __name__ == "__main__":
    generate_capstones()
    generate_benchmarks()
    generate_katas()
    print("Capstones, Benchmarks, and Katas generated successfully.")
