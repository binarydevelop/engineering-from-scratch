# Hands-On Linux Mastery Exercises

This directory contains **101 structured exercises** organized across 10 core competencies. Every exercise is designed to develop diagnostic intuition and shell fluency.

---

## Problem Set Index

| Set | Topic | Exercises | Core Abstractions |
| :---: | :--- | :---: | :--- |
| **01** | [Navigation & File System](01-navigation-and-files/README.md) | 10 | Paths, inodes, directory traversal, hidden files |
| **02** | [Pipes & Redirection](02-pipes-and-redirection/README.md) | 10 | File descriptors (0, 1, 2), streams, kernel buffers |
| **03** | [Text Processing Mastery](03-text-processing/README.md) | 15 | `grep`, `sed`, `awk`, `cut`, `sort`, `uniq`, `tr` |
| **04** | [Filesystem Traversal with Find & Xargs](04-find-and-xargs/README.md) | 10 | Search predicates, timestamps, null-delimited streams |
| **05** | [Users, Groups & Permissions](05-users-and-permissions/README.md) | 10 | DAC, UIDs, GIDs, symbolic/octal modes, umask |
| **06** | [Processes, Signals & Job Control](06-processes-and-signals/README.md) | 12 | PIDs, signals (TERM, KILL, HUP), `/proc`, foreground/background |
| **07** | [Network Inspection & Sockets](07-networking-inspection/README.md) | 12 | `ip`, `ss`, `curl`, `dig`, socket states, listening ports |
| **08** | [Storage, Mounts & Filesystems](08-storage-and-mounts/README.md) | 10 | `lsblk`, `df` vs `du`, inodes, loopback filesystems |
| **09** | [Services, systemd & Logging](09-services-and-systemd/README.md) | 10 | `systemctl`, unit files, `journalctl`, timers |
| **10** | [Defensive Bash Scripting](10-bash-scripting/README.md) | 12 | `set -euo pipefail`, loops, traps, argument parsing |

---

## Instructions

1. Attempt each exercise manually in your lab VM without looking at the solutions.
2. Formulate your prediction **before** executing commands.
3. Compare your diagnostic reasoning with the reference solutions in [exercises/solutions/README.md](solutions/README.md).
