# Learning Methodology: The First-Principles Kafka Loop

> **Repository Motto:**
> **Understand it. Build it. Measure it. Break it. Recover it. Scale it. Ship it.**

---

## 1. The Core Learning Loop

Real distributed systems mastery does not come from memorizing CLI flags or copying configuration files from blog posts. It is forged by predicting behavior, observing raw socket and disk state, intentionally breaking systems, and diagnosing the resulting failure modes.

Every lesson in `kafka-from-scratch` demands following this 11-step execution loop:

```text
    1. READ
       Understand the architectural problem and mechanical context.
         │
         ▼
    2. PREDICT
       Write down your explicit hypothesis before touching a terminal.
         │
         ▼
    3. BUILD (From Scratch)
       Construct a minimal Python implementation to expose the mechanics.
         │
         ▼
    4. RUN (In Kafka)
       Execute the corresponding Kafka feature against the pinned engine.
         │
         ▼
    5. INSPECT
       Look underneath the abstraction: topic metadata, log segments, offsets.
         │
         ▼
    6. MEASURE
       Collect real metrics: records/sec, latency p99, consumer lag, bytes.
         │
         ▼
    7. EXPLAIN
       Articulate what occurred in your own words, validating your prediction.
         │
         ▼
    8. MODIFY
       Alter configuration knobs (linger.ms, batch.size, acks, partition keys).
         │
         ▼
    9. BREAK
       Intentionally crash a broker, inject skew, or sever connections.
         │
         ▼
   10. RECOVER
       Diagnose the failure with logs/metrics and execute the recovery steps.
         │
         ▼
   11. REBUILD
       Reconstruct the core mechanism from memory without referencing notes.
```

---

## 2. The 5 Golden Rules of Study

### Rule 1: Always Predict Before Executing
Never run a command blindly. If you are about to kill broker 1 hosting partition 0 leader:
* *What will happen to the producer currently sending records?*
* *Will the write fail immediately, or buffer in memory and retry?*
* *How many milliseconds until a new leader is elected?*
* *What will the consumer see?*
Commit your prediction to writing. When reality differs from your prediction, learning occurs.

### Rule 2: Never Proceed While Something Feels Magical
If you run `kafka-console-consumer.sh` and records appear on your screen, ask:
* *How did the consumer discover which broker holds partition 0?*
* *Where is the current offset stored?*
* *What happens if the consumer process receives SIGKILL right now?*
If you cannot answer, stop. Inspect the network packets, query `__consumer_offsets`, or examine the code.

### Rule 3: Type Commands Manually
Do not blindly copy-paste blocks of shell commands. Typing the flags (`--bootstrap-server`, `--topic`, `--partitions`, `--group`) builds muscle memory and forces you to read every parameter.

### Rule 4: Measure Every Claim
Do not take claims like "batching improves throughput" or "page cache makes Kafka fast" on faith.
Run the benchmark. Measure 1 record/request vs. 500 records/request. Plot the latency percentiles (p50, p95, p99). Inspect CPU utilization.

### Rule 5: Keep Rigorous Evidence
Maintain an evidence log in each phase under `outputs/evidence-template.md`. Document what happened, what surprised you, what broke, and what guarantees were provided.

---

## 3. The Completion Rule

A lesson is **NOT** complete merely because the scripts executed with return code 0.

You are finished with a phase only when you can:
1. Explain the underlying problem without using the word "Kafka".
2. Explain how the simplified Python mechanism solves it.
3. Contrast the simplified mechanism with Kafka's production implementation.
4. Intentionally induce the primary failure mode and restore the system.
5. Explain the concrete guarantees and non-guarantees.
6. Identify exactly when Kafka is appropriate for this problem, and when it is the wrong tool.
