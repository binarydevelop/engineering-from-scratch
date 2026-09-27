# Phase 67 — The df vs du Discrepancy

## Motto
*Understand it. Use it. Inspect it. Break it. Debug it. Automate it. Secure it. Operate it.*

---

## Problem
Why disk allocation tools report wildly conflicting numbers for the same filesystem.

---

## Prediction
Before running any commands:
- **Expected System Behavior**: df reads allocated block counters from the filesystem superblock; du walks directory entries summing file sizes.
- **Exit Status**: Successful execution returns exit code `0`; configuration or permission failures produce non-zero status (`1`, `2`, `126`, or `127`).
- **Kernel State**: Observable state changes will manifest in the kernel process table, file descriptor arrays, network socket buffers, or virtual filesystems (`/proc`, `/sys`).

---

## Why This Matters
In production environments, systems engineers and SREs cannot afford to treat the operating system as an opaque black box. When an alert fires in the middle of the night, copy-pasting random commands or rebooting the server destroys critical diagnostic evidence and risks catastrophic data loss. Understanding `The df vs du Discrepancy` from first principles allows you to isolate root causes from observable facts.

---

## Mental Model
df: Superblock -> Total allocated blocks. du: VFS Directory Walk -> Sum(stat.st_size).

```text
               THE FIRST-PRINCIPLES ABSTRACTION
   ┌────────────────────────────────────────────────────────┐
   │                     USER APPLICATION                   │
   │               (Shell / Command / Daemon)               │
   ├──────────────────────────┬─────────────────────────────┤
   │                          │ System Call (syscall)       │
   │                          ▼                             │
   │                  THE LINUX KERNEL                      │
   │       Virtual Filesystem  |  Scheduler  |  Networking  │
   │       Inodes & Dentries   |  task_struct|  Socket Buffer│
   ├──────────────────────────┼─────────────────────────────┤
   │                          ▼ Hardware Interfaces         │
   │                       HARDWARE                         │
   │            (CPU, Physical RAM, Storage, NIC)           │
   └────────────────────────────────────────────────────────┘
```

---

## Inspect
To inspect the ground truth of this object on a live Linux system:
- **Primary Inspection Sources**: `df, du, lsof`
- **Diagnostic Utilities**: `df -h, du -sh /path/*, lsof +L1`

---

## Use the Linux Tools
Execute the foundational commands step-by-step:
```bash
# Execute primary inspection and usage commands
df -h, du -sh /path/*, lsof +L1
```

Every flag and argument has an intentional purpose:
- Verify command syntax and options using `man` or `--help`.
- Observe standard output (`stdout`) and standard error (`stderr`).
- Verify the return status immediately: `echo $?`.

---

## Change Something
Safely alter the system state to observe how Linux responds:
```bash
# State transition exercise
Create a scenario where df reports 100MB used while du reports 0MB used.
```
Observe the immediate reflection of this change in system metrics, directory listings, or kernel virtual files.

---

## Break It Safely
Deliberately inject the failure mode within an isolated sandbox:
- **Risk Assessment**: Confine all failure testing strictly to test sandboxes, loopback mounts, or network namespaces.
- **Failure Command**:
```bash
# Deliberate failure injection
Delete a large active log file while a process holds it open; observe du drops to 0 while df remains full.
```
- **Observed Impact**: The system reports an error, rejects the syscall, or halts execution.

---

## Diagnose It
Do not guess or apply blunt-force workarounds. Use empirical inspection to prove what broke:
```bash
# Decisive diagnostic inspection command
Inspect open deleted file descriptors with lsof +L1.
```
- What file, socket, inode, or process descriptor proves the root cause?
- Trace system calls using `strace` or inspect kernel messages with `dmesg -T` if needed.

---

## Fix It
Apply the targeted, minimal remediation that resolves the root cause without side-effects:
```bash
# Permanent targeted remediation
Terminate process holding file or truncate via /proc/<pid>/fd/<fd>.
```
Verify that the error condition disappears and the system returns to a clean, healthy state.

---

## Automate It
Codify the verification or diagnosis into a reusable, defensive Bash one-liner or script:
```bash
#!/usr/bin/env bash
set -euo pipefail

# Automated diagnostic or remediation check
lsof +L1
```

---

## Evidence
Record your experimental findings using the standard evidence template:
1. **Initial State**: Recorded baseline metrics before execution.
2. **Commands Executed**: Exact shell commands and positional parameters.
3. **Failure Output**: Raw error messages and exit codes generated during the break step.
4. **Diagnostic Proof**: The specific command output that conclusively proved the root cause.
5. **Post-Fix State**: Verified healthy system state after remediation.

Refer to [outputs/evidence-template.md](file:///Users/tushar/Desktop/private/repos/linux-from-scratch/outputs/evidence-template.md) to log your work.

---

## Questions for Mastery
1. **Why does deleting an active log file with 'rm' fail to reclaim disk space immediately?**
2. *How does this mechanism behave differently under high concurrency or low memory conditions?*
3. *What specific alert or metric would you monitor in production to detect failures in this subsystem before users are affected?*

---

## Production Connection
In real-world cloud infrastructure (Kubernetes worker nodes, database clusters, high-traffic API gateways), failures in this subsystem manifest as:
- Latency spikes and elevated queue depths.
- Unexpected service crashes or restarts by the supervisor.
- Cascading connection timeouts or connection refused errors.
- Unplanned disk saturation or filesystem remounts.

---

## What Comes Next
Proceed to **[Phase 68: Inodes and Inode Exhaustion](../phase-68-inodes/docs/en.md)** to continue building your first-principles mastery of Linux systems.
