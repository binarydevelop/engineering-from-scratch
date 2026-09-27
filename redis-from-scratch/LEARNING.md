# How to Learn From This Repository

> **Motto:** Understand it. Build it. Measure it. Break it. Fix it. Scale it. Ship it.

This curriculum is not a collection of syntax tutorials or Redis command cheat sheets. It is a systems-engineering apprenticeship.

If you simply copy-paste commands and watch them print `OK`, you will learn almost nothing. Redis will remain a mysterious black box that "just runs fast" until it crashes in production under 100k requests/second.

---

## The Learning Loop

Every phase in this repository demands that you engage in the following twelve-step cycle:

```text
       ┌──────────┐
       │   Read   │ (Understand the engineering problem)
       └────┬─────┘
            ▼
       ┌──────────┐
       │ Predict  │ (Write down your expectation BEFORE running commands)
       └────┬─────┘
            ▼
       ┌──────────┐
       │ Build It │ (Implement a toy version from scratch in Python)
       └────┬─────┘
            ▼
       ┌──────────┐
       │ Run Real │ (Execute real Redis commands against the engine)
       └────┬─────┘
            ▼
       ┌──────────┐
       │ Inspect  │ (Check internal encodings, memory headers, and raw bytes)
       └────┬─────┘
            ▼
       ┌──────────┐
       │ Measure  │ (Measure p50, p99 latency, ops/sec, memory fragmentation)
       └────┬─────┘
            ▼
       ┌──────────┐
       │ Explain  │ (Articulate the mechanics in your own words)
       └────┬─────┘
            ▼
       ┌──────────┐
       │ Modify   │ (Tweak thresholds, algorithms, or payload sizes)
       └────┬─────┘
            ▼
       ┌──────────┐
       │ Break It │ (Inject failures: fill memory, drop sockets, corrupt logs)
       └────┬─────┘
            ▼
       ┌──────────┐
       │ Debug It │ (Use SLOWLOG, INFO, and error outputs to diagnose)
       └────┬─────┘
            ▼
       ┌──────────┐
       │ Rebuild  │ (Re-implement from blank memory to achieve true mastery)
       └──────────┘
```

---

## The Golden Rules

### 1. Predict First
Never type a command without formulating a concrete hypothesis.
* *Example:* Before running `INCR mykey` on a non-existent key, predict: Does it throw an error? Does it return 1? What data type does `TYPE mykey` report?

### 2. Inspect Underneath the Abstraction
When you run `SET name Alice`, you have not finished.
Run `OBJECT ENCODING name`. Run `MEMORY USAGE name`. Connect via raw `nc` or Python sockets to inspect the RESP wire protocol `*3\r\n$3\r\nSET...`. Never stop at the CLI's formatted string.

### 3. Measure Claims with Quantitative Rigor
Do not accept statements like *"Redis is blindingly fast"* or *"Pipelining improves throughput."*
Measure them. Record numbers:
* Single command round-trips over TCP: `~8,000 ops/sec` at `0.12 ms/op`.
* Pipelined batch (100 commands): `~320,000 ops/sec` at `0.003 ms/op`.
* Write down the hardware, OS, and client conditions under which your measurements were gathered.

### 4. Break It Intentionally
A system is not truly understood until you know exactly how it fails:
* What happens when you store a 50MB string in Redis?
* What happens when memory hits `maxmemory` under `noeviction`?
* What happens to a Redis replica when the replication backlog overflows?
* What happens to an application when a hot cached key expires during high traffic?

### 5. Document Evidence
Each lesson directory contains an `outputs/evidence-template.md`.
Fill it out. Keep a personal learning log of your predictions, command outputs, latency benchmarks, and intentional bugs.

---

## The Completion Standard

You have **NOT** completed a lesson merely because the script exited with code 0.

You are finished with a lesson when you can:
1. Explain the underlying systems problem without using buzzwords.
2. Predict the exact return value and side-effects of the commands.
3. Draw the mental model ASCII diagram from memory on a blank whiteboard.
4. Intentionally induce the failure mode and diagnose it using Redis diagnostic tooling.
5. Explain clearly when an architect should choose Redis for this problem—and when they should **refuse** to use Redis.
