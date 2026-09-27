# LEARNING GUIDE & PEDAGOGICAL METHOD

> **Understand it. Use it. Inspect it. Break it. Debug it. Automate it. Secure it. Operate it.**

Operating Linux is not a collection of arbitrary commands to memorize. It is a systematic discipline of inspecting state, forming hypotheses, testing system behavior, and automating solutions.

---

## The 10-Step Mastery Loop

For every lesson in this repository, follow this execution loop:

```text
       ┌───────────────┐
       │  1. PROBLEM   │  A concrete operational or diagnostic dilemma
       └───────┬───────┘
               ▼
       ┌───────────────┐
       │  2. PREDICT   │  Write down what you expect the kernel/shell to do
       └───────┬───────┘
               ▼
       ┌───────────────┐
       │3. MENTAL MODEL│  Understand the underlying abstraction (VFS, socket, FD)
       └───────┬───────┘
               ▼
       ┌───────────────┐
       │4. USE THE TOOL│  Execute the command with precision
       └───────┬───────┘
               ▼
       ┌───────────────┐
       │5. INSPECT SYS │  Verify state in /proc, /sys, iproute2, or journal
       └───────┬───────┘
               ▼
       ┌───────────────┐
       │6. BREAK SAFELY│  Deliberately introduce the failure mode
       └───────┬───────┘
               ▼
       ┌───────────────┐
       │ 7. DIAGNOSE   │  Collect empirical proof (strace, lsof, ss, logs)
       └───────┬───────┘
               ▼
       ┌───────────────┐
       │   8. FIX IT   │  Remediate root cause without blunt force
       └───────┬───────┘
               ▼
       ┌───────────────┐
       │9. AUTOMATE IT │  Codify the diagnosis or fix into a robust script
       └───────┬───────┘
               ▼
       ┌───────────────┐
       │ 10. EVIDENCE  │  Record before/after artifacts into your log
       └───────────────┘
```

---

## Deadly Anti-Patterns to Eliminate

### 1. The Blind `sudo` Trap
- **Anti-pattern**: Command fails with `Permission denied` -> immediately prefix with `sudo`.
- **First-principles response**: Ask *why* the process is denied. What UID is running? What are the inode mode bits? Does the user belong to the owning group? Does the directory have execute (`+x`) traversal permissions?

### 2. The `chmod 777` Nuclear Option
- **Anti-pattern**: Application cannot write to `/var/www` -> `chmod -R 777 /var/www`.
- **First-principles response**: Determine which user runs the web server (`www-data`). Assign proper group ownership (`chown :www-data`) and minimal group write permissions (`chmod 775` or `chmod 2775` with SGID).

### 3. The Reboot Guess
- **Anti-pattern**: Network or service misbehaves -> reboot the host.
- **First-principles response**: Inspect the system journal (`journalctl -xeu`), check socket listening states (`ss -lntp`), trace system calls (`strace`), and evaluate resource exhaustion (`free`, `df`, `vmstat`).

### 4. Parsing `ls` Output in Scripts
- **Anti-pattern**: `for file in $(ls *.txt); do ...`
- **First-principles response**: File names in Linux can contain spaces, newlines, and special characters. Always use shell globbing (`for file in *.txt; do`), `find -print0 | xargs -0`, or `while IFS= read -r -d '' file; do`.

---

## How to Record Evidence

Learning Linux requires empirical verification. You will record your work using the template provided in [outputs/evidence-template.md](file:///Users/tushar/Desktop/private/repos/linux-from-scratch/outputs/evidence-template.md).

Never consider an exercise complete until you have:
1. Demonstrated the failure with concrete command output.
2. Identified the exact Linux object involved (e.g. Inode #2841, Socket `0.0.0.0:8080`, File Descriptor 3).
3. Restored the system and verified healthy metrics.
