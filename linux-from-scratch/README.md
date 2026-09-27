# linux-from-scratch

> **Understand it. Use it. Inspect it. Break it. Debug it. Automate it. Secure it. Operate it.**

An experimental, first-principles curriculum that transforms Linux from a collection of "magic incantations" into a transparent set of coherent system abstractions.

---

## What This Repository Is

This is **NOT** a Linux command cheat sheet.  
This is **NOT** a collection of copy-paste snippets.  
This is a rigorous course in **understanding, debugging, and operating Linux systems**.

When most engineers encounter a problem on a Linux server, their instincts look like this:

```text
               THE CARGO-CULT INSTINCT (Guessing)
   ┌────────────────────────────────────────────────────────┐
   │  "Permission denied"       ──> sudo chmod -R 777       │
   │  "Port already in use"     ──> reboot the server       │
   │  "Disk is full"            ──> rm -rf random directories│
   │  "Service failed"          ──> restart it in a loop    │
   │  "Can't connect to host"   ──> disable the firewall    │
   └────────────────────────────────────────────────────────┘
```

This repository replaces blind guessing with an accurate, mechanical mental model:

```text
               THE FIRST-PRINCIPLES REALITY
   ┌────────────────────────────────────────────────────────┐
   │                       HARDWARE                         │
   │           (CPU, RAM, Disks, NICs, Timers)              │
   ├────────────────────────────────────────────────────────┤
   │                     LINUX KERNEL                       │
   │  Processes  |  Virtual Memory  |  VFS  |  TCP/IP Stack │
   │  Syscalls   |  cgroups         |  Namespaces | Drivers │
   ├────────────────────────────────────────────────────────┤
   │                  VIRTUAL FILESYSTEMS                   │
   │   /proc (processes & kernel)  |  /sys (devices & buses)│
   ├────────────────────────────────────────────────────────┤
   │                     USER SPACE                         │
   │  systemd (PID 1)  |  daemons  |  libraries (glibc)     │
   │  bash / shells    |  coreutils (ls, ps, grep, ip)      │
   └────────────────────────────────────────────────────────┘
```

**Linux is a collection of coherent abstractions—files, processes, users, permissions, sockets, devices, mounts, services, logs, and kernel interfaces—that can be inspected and composed using small tools.**

---

## The 14 Core Competencies

1. **Linux Fundamentals**: Kernel vs. user space, distributions, system architecture.
2. **Shell Fluency**: Bash execution model, tokens, quoting, expansion, subshells.
3. **Filesystem Navigation & Manipulation**: Single-rooted hierarchy, paths, inodes, links.
4. **Processes & Services**: PIDs, process states, signals, job control, systemd units.
5. **Users & Permissions**: UIDs, GIDs, DAC, symbolic vs. numeric modes, umask, sudo.
6. **Networking**: Interfaces, IP routing, ARP, DNS resolution, sockets, packet inspection.
7. **Package Management**: Repositories, metadata, dependency trees, dpkg/apt mechanics.
8. **Storage**: Block devices, partitions, filesystems, loop mounts, VFS, df vs. du.
9. **Logging**: Systemd journal, `/var/log`, logrotate, syslog formatting and streaming.
10. **Security**: Least privilege, secure service users, SSH hardening, capabilities, firewalls.
11. **Performance**: USE method, CPU profiling, memory allocation, I/O wait, load averages.
12. **Automation**: Defensive Bash scripting (`set -euo pipefail`), traps, functions, health checks.
13. **Troubleshooting**: Systematic root-cause isolation without guessing or breaking state.
14. **Production Operations**: Real application servers, reverse proxies, multi-user systems.

---

## Curriculum Progression

```text
Terminal & Shell (00-13)
        │
        ▼
Text Tools & Pipes (14-20)
        │
        ▼
Users, Groups & Permissions (21-27)
        │
        ▼
Processes & Virtual Filesystems (28-34)
        │
        ▼
Packages & Libraries (35-38)
        │
        ▼
Services, systemd & Boot (39-46)
        │
        ▼
Networking & Sockets (47-62)
        │
        ▼
Storage, Filesystems & Inodes (63-71)
        │
        ▼
Logs, Time & Backups (72-76)
        │
        ▼
Defensive Shell Scripting (77-86)
        │
        ▼
Resource Limits & Performance (87-95)
        │
        ▼
Security & Kernel Interfaces (96-107)
        │
        ▼
Debugging & Failure Injection Labs (108-120)
        │
        ▼
Practical Projects (121-129)
        │
        ▼
Modern Linux in Docker, K8s & Systems (130-135)
```

---

## Diagnostic Questions You Will Answer

When sitting in front of an unfamiliar Linux machine, you will be able to answer:

| Question | Diagnostic Inspection Object | Primary Tools |
| :--- | :--- | :--- |
| **What distribution & kernel is this?** | `/etc/os-release`, `/proc/version` | `uname -r`, `cat /etc/os-release` |
| **What processes are running?** | Kernel process table (`/proc`) | `ps aux`, `pstree`, `top` |
| **What is consuming CPU / memory?** | `/proc/stat`, `/proc/meminfo` | `top`, `pidstat`, `free -m` |
| **What filesystems are mounted?** | `/proc/mounts`, superblock | `findmnt`, `df -hT`, `lsblk` |
| **What services are running/failing?** | systemd unit states & journal | `systemctl --failed`, `journalctl -xeu` |
| **What ports are listening?** | Kernel socket table (`/proc/net/tcp`) | `ss -lntp`, `lsof -i` |
| **Why is access denied?** | Inode permissions, parent paths, UID | `ls -ld`, `namei -l`, `id` |
| **Why did a service fail?** | Service journal stream & exit code | `journalctl -u <unit> -b`, `strace` |
| **Why can't this host reach another?** | Interfaces, routes, ARP, firewalls | `ip addr`, `ip route`, `ping`, `curl -v` |
| **Why is DNS failing?** | Resolver config, systemd-resolved | `resolvectl status`, `dig`, `/etc/resolv.conf` |
| **Why is disk full if du shows space?** | Deleted unlinked open file descriptors | `lsof +L1`, `df -h`, `du -sh` |
| **Why are there "Too many open files"?** | Process FD table vs ulimit | `ls -l /proc/<pid>/fd`, `ulimit -n` |

---

## The Learning Methodology

Every single lesson follows a strict, scientific learning loop:

```text
MOTTO
  ↓
PROBLEM           (Concrete real-world challenge)
  ↓
PREDICT           (State expected system behavior before executing)
  ↓
MENTAL MODEL      (The kernel/userspace abstraction involved)
  ↓
USE THE TOOL      (Targeted commands with flag explanations)
  ↓
INSPECT SYSTEM    (Verify the underlying Linux state)
  ↓
CHANGE SOMETHING  (Modify configuration or state)
  ↓
BREAK IT SAFELY   (Inject a realistic failure mode)
  ↓
DEBUG IT          (Collect evidence without guessing)
  ↓
FIX IT            (Restore desired system state)
  ↓
AUTOMATE IT       (Turn diagnosis into a repeatable script)
  ↓
EVIDENCE          (Record measurable before/after metrics)
```

---

## Repository Structure

```text
linux-from-scratch/
├── README.md               # Curriculum overview and philosophy
├── ROADMAP.md              # Detailed syllabus for all 136 phases
├── LEARNING.md             # Pedagogical method, study loops, anti-patterns
├── LESSON_TEMPLATE.md      # Standard 16-section lesson framework
├── VERSIONS.md             # Target OS releases, tool versions, distribution notes
├── SAFETY.md               # Safety guidelines for failure injection and recovery
├── CONTRIBUTING.md         # Contribution guidelines and validation rules
├── Makefile                # Verification, environment checks, and lab targets
│
├── scripts/                # Environment validation and lab recovery scripts
│   ├── check-environment.sh
│   ├── reset-lab.sh
│   └── cleanup.sh
│
├── docs/                   # Conceptual references & diagnostic workflows
│   ├── platform-setup.md   # VM, WSL2, cloud VM, and container trade-offs
│   ├── mental-models.md    # Kernel, VFS, processes, networking, storage diagrams
│   ├── command-map.md      # Diagnostic command reference organized by question
│   ├── troubleshooting.md  # 10-step systematic root-cause methodology
│   └── glossary.md         # 100+ Linux concepts defined from first principles
│
├── phases/                 # All 136 Phases (phase-00 through phase-135)
│   └── phase-XX-<slug>/
│       └── docs/en.md      # Comprehensive 16-section lesson guide
│
├── exercises/              # 100+ hands-on challenges across 10 problem sets
│   ├── 01-navigation-and-files/
│   ├── ...
│   └── solutions/          # Step-by-step solutions for every exercise
│
├── broken-systems/         # 32 hands-on realistic troubleshooting scenarios
│   ├── scenario-XX-<slug>/ # Symptom, safe setup script, verification test
│   └── solutions/          # Systematic triage and root-cause analysis guide
│
├── projects/               # 9 production-grade practical projects
│   ├── project-01-build-linux-service/
│   ├── project-02-reverse-proxy-server/
│   ├── ...
│   └── project-09-linux-application-host/
│
├── scripts-examples/       # Production-style automation and audit tools
└── outputs/
    └── evidence-template.md# Markdown template for student evidence logs
```

---

## Safe Platform Strategy

Linux commands interact directly with hardware and system state. You should never practice destructive failure injection on your personal primary workstation.

| Platform | Recommended For | Systemd? | Loop Devices? | Raw Sockets? | Notes |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **Native Linux PC / Laptop** | Full curriculum | Yes | Yes | Yes | Recommended on secondary/dedicated partition |
| **Linux VM (Multipass / UTM / VirtualBox)** | Full curriculum (**Recommended**) | Yes | Yes | Yes | Safest, instantaneous snapshot/revert |
| **Disposable Cloud VM (Hetzner / AWS / DO)** | Full curriculum | Yes | Yes | Yes | Cheap, isolated, pristine Ubuntu LTS |
| **WSL2 (Windows Subsystem for Linux)** | Phases 00-42, 47-86 | Partial | Requires setup | Mostly | Default init is init/systemd (configurable) |
| **Docker Container** | Fast CLI syntax practice only | No | No | No | **Cannot** teach real systemd, mounts, kernel |

Read [docs/platform-setup.md](file:///Users/tushar/Desktop/private/repos/linux-from-scratch/docs/platform-setup.md) for step-by-step setup guides.

---

## Quick Start

1. **Verify your environment**:
   ```bash
   bash scripts/check-environment.sh
   ```

2. **Read the Safety Guidelines**:
   Read [SAFETY.md](file:///Users/tushar/Desktop/private/repos/linux-from-scratch/SAFETY.md) before executing commands.

3. **Begin Lesson 00**:
   Open [phases/phase-00-linux-orientation/docs/en.md](file:///Users/tushar/Desktop/private/repos/linux-from-scratch/phases/phase-00-linux-orientation/docs/en.md) and start building your mental model.

---

## The Ultimate Standard

You will know you have completed this curriculum when your first response to a server failure is never:
- "Let's reboot it"
- "Let's run it with sudo"
- "Let's chmod 777"
- "Let's copy-paste an error into a search engine without inspecting state"

Instead, your mind will immediately ask:
> **What Linux object is involved?**  
> *Is it a process, file descriptor, inode, socket, route, netfilter rule, cgroup, or mount point?*  
> **What observable evidence in `/proc`, `/sys`, or the system journal proves what is happening?**
