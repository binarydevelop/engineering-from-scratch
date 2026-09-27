# Java and JVM Performance Engineering Guide

A practical guide to benchmarking, profiling, JIT optimization, allocation analysis, and memory tuning in modern Java systems.

---

## 1. The Performance Engineering Discipline

> "Never tune JVM flags or rewrite code based on intuition. Measure. Profile. Form a hypothesis. Change one variable. Measure again."

```text
  ┌─────────────────┐
  │ Identify Metric │  Throughput (req/sec), Latency (p99/p99.9), Allocation Rate (MB/s)
  └────────┬────────┘
           │
           ▼
  ┌─────────────────┐
  │ Establish Base  │  Execute repeatable, controlled baseline measurement.
  └────────┬────────┘
           │
           ▼
  ┌─────────────────┐
  │ Profile Runtime │  Use JFR (Java Flight Recorder) or async-profiler to locate hotspots.
  └────────┬────────┘
           │
           ▼
  ┌─────────────────┐
  │ Form Hypothesis │  Identify root cause (e.g., lock contention, cache misses, boxing allocations).
  └────────┬────────┘
           │
           ▼
  ┌─────────────────┐
  │ Implement Fix   │  Refactor code or adjust resource allocation.
  └────────┬────────┘
           │
           ▼
  ┌─────────────────┐
  │ Compare Delta   │  Measure under identical load; verify improvement is statistically significant.
  └─────────────────┘
```

---

## 2. Why Naive Microbenchmarks Lie

A common beginner mistake is measuring code execution with `System.currentTimeMillis()` or `System.nanoTime()` in a basic loop:

```java
// DO NOT DO THIS FOR PERFORMANCE MEASUREMENT
long start = System.nanoTime();
for (int i = 0; i < 1_000_000; i++) {
    compute(i);
}
long elapsed = System.nanoTime() - start;
```

### Why This Benchmark Fails:
1. **Tiered Warmup Artifacts**: The first 10,000 iterations execute in the slow interpreter and C1 compiler. You measure compiler latency rather than compiled code performance.
2. **Dead-Code Elimination (DCE)**: If the return value of `compute(i)` is never consumed, the C2 optimizer will completely remove the loop body, measuring zero nanoseconds.
3. **Constant Folding**: If input arguments are compile-time constants, C2 precomputes the result and replaces the method call with a constant literal.
4. **Safepoint Bias & OSR**: On-Stack Replacement during long loops causes transient pauses and skewed sampling.

---

## 3. Microbenchmarking with JMH (Java Microbenchmark Harness)

JMH is the official OpenJDK benchmarking tool built to defeat JIT optimizations:

```java
package io.github.javafromscratch.benchmarks;

import org.openjdk.jmh.annotations.*;
import org.openjdk.jmh.infra.Blackhole;
import java.util.concurrent.TimeUnit;

@BenchmarkMode(Mode.Throughput)
@OutputTimeUnit(TimeUnit.MILLISECONDS)
@State(Scope.Thread)
@Warmup(iterations = 3, time = 1, timeUnit = TimeUnit.SECONDS)
@Measurement(iterations = 5, time = 1, timeUnit = TimeUnit.SECONDS)
@Fork(2)
public class StringConcatenationBenchmark {

    @Param({"10", "100", "1000"})
    public int iterations;

    @Benchmark
    public void testNaiveConcat(Blackhole bh) {
        String result = "";
        for (int i = 0; i < iterations; i++) {
            result += i;
        }
        bh.consume(result); // Defeats Dead-Code Elimination
    }

    @Benchmark
    public void testStringBuilder(Blackhole bh) {
        StringBuilder sb = new StringBuilder(iterations * 4);
        for (int i = 0; i < iterations; i++) {
            sb.append(i);
        }
        bh.consume(sb.toString()); // Defeats Dead-Code Elimination
    }
}
```

---

## 4. Production Profiling with Java Flight Recorder (JFR)

Java Flight Recorder is built directly into HotSpot, providing low-overhead (< 1% CPU impact) telemetry suitable for production workloads:

```bash
# Start an application with continuous JFR recording
java -XX:+FlightRecorder \
     -XX:StartFlightRecording=duration=60s,filename=production-profile.jfr,settings=profile \
     -jar app.jar

# Dump a JFR recording from a running process dynamically
jcmd <PID> JFR.start name=OnDemand duration=30s filename=/tmp/dump.jfr
```

### JFR Telemetry Events to Inspect:
* `jdk.ExecutionSample`: CPU profiling samples showing where threads spend CPU cycles.
* `jdk.ObjectAllocationInNewTLAB`: Tracks which classes cause high young-generation allocation rates.
* `jdk.JavaMonitorEnter`: Identifies severe lock contention and threads blocked on monitors.
* `jdk.GarbageCollection`: Detailed GC pause durations, scavenged bytes, and memory phases.

---

## 5. Memory Tuning Hierarchy

When facing GC pauses or high memory pressure, follow this order of intervention:

1. **Step 1: Reduce Application Allocation Rate**
   * Eliminate unnecessary autoboxing (`Integer` vs `int`).
   * Reuse byte buffers and streams instead of generating huge temporary byte arrays.
   * Size collections properly (`new ArrayList<>(expectedSize)`) to avoid repeated internal array copying.
2. **Step 2: Correct Heap Sizing (`-Xms`, `-Xmx`)**
   * Set initial heap (`-Xms`) equal to maximum heap (`-Xmx`) on dedicated production servers to eliminate runtime dynamic heap resizing pauses.
3. **Step 3: Select Appropriate Garbage Collector**
   * For batch throughput workloads: `-XX:+UseParallelGC`.
   * For standard balanced server APIs: `-XX:+UseG1GC`.
   * For strict sub-millisecond SLA requirements: `-XX:+UseZGC`.
4. **Step 4: Avoid "Flag Magic"**
   * Do not copy archaic flag strings (`-XX:+UseCMSInitiatingOccupancyFraction`, etc.). Modern HotSpot self-tunes ergonomics dynamically.
