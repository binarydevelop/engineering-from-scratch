# Systems Safety Protocol & Failure Containment Guide

> **Motto:** Understand it. Build it. Run it. Inspect it. Measure it. Break it. Debug it. Rebuild it.  
> **Safety Rule:** Never break your host machine to learn how an operating system fails.

Operating systems manage physical resources: CPU cores, RAM bytes, disk blocks, network packets, and process IDs. When you intentionally induce resource exhaustion, race conditions, deadlocks, or namespace isolation, you touch the very boundaries designed to prevent catastrophic computer failure.

This document outlines the strict containment protocols required while completing this curriculum.

---

## 1. Safety Principles

1. **Isolation First:** Highly privileged experiments (cgroups, network namespaces, pivot_root, raw sockets) must be run inside a disposable Linux container or virtual machine.
2. **Explicit Limits Before Execution:** Never run an allocation loop without an upper bound or an active resource limit (`ulimit -v`, `ulimit -u`).
3. **No Uncontrolled Fork Bombs:** The curriculum forbids uncontrolled recursive `fork()` bombs (`:(){ :|:& };:`). All process-spawning experiments use hard-coded execution limits (`MAX_PROCS = 16`).
4. **Graceful Signal Handling:** Every long-running server, thread worker, or consumer must install signal handlers for `SIGINT` (Ctrl+C) and `SIGTERM` to perform deterministic teardown.
5. **Deterministic Cleanup:** Every lab provides an explicit cleanup command or script to unmount temporary filesystems, kill orphaned background processes, and delete scratch disk images.

---

## 2. Resource Containment Matrix

| Threat Domain | Potential Host Impact | Mandatory Safety Guard | Emergency Kill Command |
| :--- | :--- | :--- | :--- |
| **Process Exhaustion (PID Exhaustion)** | System freeze, denial of shell execution (`bash: fork: Resource temporarily unavailable`) | `ulimit -u 64` before running fork experiments; hardcoded iteration caps in C (`int i = 0; i < 8; i++`). | `killall -9 <binary_name>` or log out from second TTY |
| **Memory Exhaustion (OOM Invocation)** | Host paging lockup, OS thrashing, unprovoked killing of user applications | Virtual memory simulation first; in real C code, allocate in strict increments with `ulimit -v 524288` (512MB max). | `Ctrl + C` or `kill -9 <PID>` |
| **Disk Exhaustion (Zeroing Space)** | Root partition fills, logs fail to write, system databases crash | Fixed-size scratch disk images (`dd if=/dev/zero of=scratch.img bs=1M count=32`); all I/O is confined to the scratch image. | `rm -f scratch.img` |
| **File Descriptor Leaks** | Shell cannot open files; sockets reject incoming connections | Restrict descriptor table using `ulimit -n 128` during leak debugging labs. | Close leaking process via `kill -9 <PID>` |
| **Unbounded CPU Loops** | 100% core saturation, battery drain, thermal throttling | Run compute loops with low priority (`nice -n 19`) or limit CPU shares in cgroups. | `kill -9 <PID>` |
| **Network Interface Manipulation** | Disconnection from host Wi-Fi or local network | Restrict `ip link` and route changes strictly inside isolated `ip netns` network namespaces. | `ip netns del <ns_name>` |

---

## 3. Four-Point Experiment Safety Checklist

Every potentially disruptive experiment in this repository adheres to this 4-point structure:

```text
1. Expected Resource Impact: Exactly how many MB of RAM, number of PIDs, or disk blocks will be touched.
2. Safe Limits: The exact ulimit, cgroup limit, or counter cap active during the experiment.
3. How to Stop It: The interactive key combination or signal to halt execution.
4. Cleanup: The precise commands to return the system to pristine condition.
```

---

## 4. Emergency Procedures

If a test process ever becomes unresponsive or locks your terminal:

### Scenario A: Process Ignores `Ctrl + C` (`SIGINT`)
Processes blocked in uninterruptible kernel sleep (`TASK_UNINTERRUPTIBLE` / `D` state waiting on raw I/O) or processes that have masked `SIGINT` will not exit with `Ctrl + C`.
* **Action:** Send non-maskable `SIGKILL`:
  ```bash
  Ctrl + Z         # Suspend to background
  kill -9 %1       # Send SIGKILL to the suspended job
  ```
  Or from another terminal:
  ```bash
  kill -9 $(pgrep <process_name>)
  ```

### Scenario B: Orphaned Background Server Owning a Port
If an experiment fails with `bind: Address already in use` (errno 98 / 48):
* **Action:** Identify the owning PID using `lsof` or `ss` and terminate it:
  ```bash
  # Linux & macOS
  lsof -i :8080
  kill -9 <PID>
  ```

### Scenario C: Scratch Loop Disk Image Stuck
If a temporary loopback mount was created during filesystem capstones:
* **Action:** Cleanly unmount before removing the backing image:
  ```bash
  sudo umount /mnt/testfs 2>/dev/null || true
  rm -f scratch_disk.img
  ```

### Scenario D: General Workspace Sanitization
Run the repository master cleanup script at any time:
```bash
make clean
# or
./scripts/cleanup.sh
```
This halts background test daemons, cleans compiled binaries, and removes temporary socket and image files.
