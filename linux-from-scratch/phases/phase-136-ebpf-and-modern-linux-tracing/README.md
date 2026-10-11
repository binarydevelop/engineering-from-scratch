# Phase 136: eBPF and Modern Linux Kernel Tracing

## 1. Why This Matters for MAANG & Senior/Staff Roles
At MAANG scale, running `strace` or attaching heavy debuggers in production introduces unacceptable overhead (strace stops process on every syscall, causing 50x-100x slowdowns). Extended Berkeley Packet Filter (eBPF) provides a revolutionary, sandboxed in-kernel virtual machine that executes verified bytecode safely at kernel speed without modifying kernel source or restarting running microservices.

---

## 2. Core Concepts & Architecture Deep-Dive
### What is eBPF?
eBPF allows user-space engineers to attach custom programs to kernel events:
- **Kprobes / Kretprobes**: Dynamic instrumentation of arbitrary kernel function entries and returns.
- **Uprobes / Uretprobes**: Dynamic instrumentation of user-space functions (e.g., tracing OpenSSL function calls to inspect encrypted traffic before encryption).
- **Tracepoints**: Static, stable kernel instrumentation points.
- **USDT (User Statically-Defined Tracing)**: User-space tracepoints compiled into JVM, Python, Node, MySQL.
- **XDP (eXpress Data Path)**: Programmable packet processing directly in the network driver before Linux network stack allocation.

### The Safety Verifier & BPF Maps
- **In-Kernel Verifier**: Guarantees memory safety, prevents infinite loops, dereferencing invalid pointers, or crashing the OS.
- **BPF Maps**: Key-value data structures in kernel memory allowing bidirectional data exchange between eBPF programs and user-space collectors (C, Go via Cilium, Python via BCC).

### BCC & bpftrace Tooling
- **bpftrace**: High-level tracing language for rapid one-line production forensics.
- **BCC (BPF Compiler Collection)**: Deep Python/Go frameworks for production agents (e.g., Datadog, Pixie, Cilium).

---

## 3. High-Value Interview Angle & Failure Modes
### Production Forensic Scenarios (Interview Golden Cases)
- **"How do you trace disk I/O latency distribution without restarting the database?"**:
  Run `biolatency -m` (BCC). Output produces a microsecond histogram revealing hardware latency spikes vs kernel queue delays.
- **"How do you detect short-lived processes exhausting CPU or file descriptors?"**:
  Run `execsnoop` to trace ephemeral sub-processes created by scripts that evade `top`/`htop` sampling.
- **"How does Cilium leverage eBPF to replace kube-proxy and iptables?"**:
  iptables evaluates rules sequentially O(N); eBPF uses BPF hash maps O(1) for routing and service lookup directly at the network socket layer.

---

## 4. Hands-On Practice & Implementation Drills
### 5 Production bpftrace One-Liners
```bash
# 1. Histogram of read() syscall latencies for a specific PID
bpftrace -e 'kprobe:sys_read /pid == 1234/ { @start[tid] = nsecs; } kretprobe:sys_read /@start[tid]/ { @latency_us = hist((nsecs - @start[tid]) / 1000); delete(@start[tid]); }'

# 2. Count TCP connections created by process name
bpftrace -e 'tracepoint:syscalls:sys_enter_connect { @[comm] = count(); }'

# 3. Trace slow disk I/O requests exceeding 10ms
bpftrace -e 'tracepoint:block:block_rq_complete { if (args->nr_bytes > 0 && args->duration > 10000000) { printf("Slow disk I/O: %d us\n", args->duration / 1000); } }'

# 4. Snoop all files opened in the system by command
bpftrace -e 'tracepoint:syscalls:sys_enter_openat { printf("%s opened %s\n", comm, str(args->filename)); }'

# 5. Measure CPU scheduling runqueue latency (runqlat equivalent)
bpftrace -e 'tracepoint:sched:sched_wakeup { @ts[args->pid] = nsecs; } tracepoint:sched:sched_switch { if (@ts[args->next_pid]) { @usecs = hist((nsecs - @ts[args->next_pid])/1000); delete(@ts[args->next_pid]); } }'
```

---

## 5. Key Takeaways & Cheat Sheet
- eBPF executes verified, sandboxed bytecode safely inside the Linux kernel.
- Never run `strace` on production workloads; use eBPF/bpftrace.
- Powers modern networking (Cilium), observability (Pixie), and security (Falco).
- A mandatory capability for senior production infrastructure and SRE roles.
