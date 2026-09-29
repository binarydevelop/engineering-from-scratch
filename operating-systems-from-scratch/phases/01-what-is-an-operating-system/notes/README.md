# Phase 01: Core Notes & Conceptual Deconstructions

> **"Understand it. Build it. Measure it. Break it. Debug it. Scale it. Secure it. Operate it. Ship it."**

This folder contains deep, first-principles engineering notes built collaboratively for **Phase 01: What is an Operating System**:

| Note | Title | Description | Link |
|---|---|---|---|
| **01** | **What is an Operating System?** | Bare-metal execution vs OS, The 3 Great Illusions (Processes, Virtual Memory, VFS), CPU Privilege Modes (Ring 0/3, EL0/1), and Syscall transitions. | [01-what-is-an-operating-system.md](file:///Users/tushar/desktop/private/repos/operating-systems-from-scratch/phases/01-what-is-an-operating-system/notes/01-what-is-an-operating-system.md) |
| **02** | **CPU Architectures: ARM64 vs x86_64** | ISAs as hardware-software contracts, CISC vs RISC, 32-bit vs 64-bit address limits, Register allocations, Weak vs Strong memory ordering, and Docker multi-arch caveats. | [02-cpu-architectures-arm64-vs-x86_64.md](file:///Users/tushar/desktop/private/repos/operating-systems-from-scratch/phases/01-what-is-an-operating-system/notes/02-cpu-architectures-arm64-vs-x86_64.md) |
| **03** | **What is the Kernel Actually?** | The binary on disk, boot sequence to Ring 0/EL1, higher-half virtual memory split, the 5 core subsystems, monolithic vs microkernel, and the idle thread (`hlt`/`wfi`). | [03-what-is-the-kernel-actually.md](file:///Users/tushar/desktop/private/repos/operating-systems-from-scratch/phases/01-what-is-an-operating-system/notes/03-what-is-the-kernel-actually.md) |
| **04** | **Virtual Memory & Page Tables** | Pages vs Frames, PTE flags (Present, Writable, User, NX), 4-level page table trees, MMU translation, TLB caching, Demand Paging, and Page Fault handlers. | [04-virtual-memory-and-page-tables.md](file:///Users/tushar/desktop/private/repos/operating-systems-from-scratch/phases/01-what-is-an-operating-system/notes/04-virtual-memory-and-page-tables.md) |

### 🧪 Executable Code Demonstrations
* [`notes/code/01_segfault_trap.c`](file:///Users/tushar/desktop/private/repos/operating-systems-from-scratch/phases/01-what-is-an-operating-system/notes/code/01_segfault_trap.c) — Demonstrating CPU MMU page fault traps and `SIGSEGV` signal handling.
