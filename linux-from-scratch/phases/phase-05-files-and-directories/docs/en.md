# Phase 05 — Files and Directories

## Motto
*Understand it. Use it. Inspect it. Break it. Debug it. Automate it. Secure it. Operate it.*

---

## Problem
Creating, copying, moving, and safely deleting filesystem nodes.

---

## Prediction
Before running any commands:
- **Expected System Behavior**: cp creates a new inode with new metadata; mv within same filesystem updates directory entries without copying data.
- **Exit Status**: Successful execution returns exit code `0`; configuration or permission failures produce non-zero status (`1`, `2`, `126`, or `127`).
- **Kernel State**: Observable state changes will manifest in the kernel process table, file descriptor arrays, network socket buffers, or virtual filesystems (`/proc`, `/sys`).

---

## Why This Matters
In production environments, systems engineers and SREs cannot afford to treat the operating system as an opaque black box. When an alert fires in the middle of the night, copy-pasting random commands or rebooting the server destroys critical diagnostic evidence and risks catastrophic data loss. Understanding `Files and Directories` from first principles allows you to isolate root causes from observable facts.

---

## Mental Model
Directory entry (dentry) maps string filename -> Inode number. Data blocks hold contents.

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
- **Primary Inspection Sources**: `/tmp/lfs-lab, stat`
- **Diagnostic Utilities**: `touch, mkdir -p, cp -a, mv, rm -i, rmdir`

---

## Use the Linux Tools
Execute the foundational commands step-by-step:
```bash
# Execute primary inspection and usage commands
touch, mkdir -p, cp -a, mv, rm -i, rmdir
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
Create nested directories and files, test atomic renames.
```
Observe the immediate reflection of this change in system metrics, directory listings, or kernel virtual files.

---

## Break It Safely
Deliberately inject the failure mode within an isolated sandbox:
- **Risk Assessment**: Confine all failure testing strictly to test sandboxes, loopback mounts, or network namespaces.
- **Failure Command**:
```bash
# Deliberate failure injection
Attempt to remove a non-empty directory with rmdir to observe error ENOTEMPTY.
```
- **Observed Impact**: The system reports an error, rejects the syscall, or halts execution.

---

## Diagnose It
Do not guess or apply blunt-force workarounds. Use empirical inspection to prove what broke:
```bash
# Decisive diagnostic inspection command
Use ls -ld to inspect directory contents before removal.
```
- What file, socket, inode, or process descriptor proves the root cause?
- Trace system calls using `strace` or inspect kernel messages with `dmesg -T` if needed.

---

## Fix It
Apply the targeted, minimal remediation that resolves the root cause without side-effects:
```bash
# Permanent targeted remediation
Use rm -r or clean directory contents first.
```
Verify that the error condition disappears and the system returns to a clean, healthy state.

---

## Automate It
Codify the verification or diagnosis into a reusable, defensive Bash one-liner or script:
```bash
#!/usr/bin/env bash
set -euo pipefail

# Automated diagnostic or remediation check
mkdir -p /tmp/lfs-lab/{src,dest} && cp -a /tmp/lfs-lab/src/. /tmp/lfs-lab/dest/
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
1. **Why is 'mv' across different filesystems fundamentally slower than 'mv' within the same filesystem?**
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
Proceed to **[Phase 06: Wildcards and Globbing](../phase-06-wildcards-and-globbing/docs/en.md)** to continue building your first-principles mastery of Linux systems.
