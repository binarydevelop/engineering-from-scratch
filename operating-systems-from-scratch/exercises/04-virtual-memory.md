# Track 4: Virtual Memory, Paging & Address Translation Exercises

> **Motto:** Two processes can both read address `0x7ffee4b2`, but their electrons travel to completely different physical silicon capacitors.

All solutions are located in `solutions/exercises/04-virtual-memory-solutions.md`.

---

### Exercise 4.1: Inspecting Virtual Address Ranges
Write a C program that prints the addresses of:
1. `main` function (Text/Code segment)
2. A global uninitialized integer (BSS segment)
3. A global initialized string (Data segment)
4. A dynamic buffer allocated with `malloc(1024)` (Heap)
5. A local stack variable (Stack)
Verify that Text < Data < BSS < Heap < Stack in virtual address space.

### Exercise 4.2: Proving Address Space Isolation
Write two separate programs that run concurrently. Have both programs print the memory address of a global variable and write different values to it. Explain why both programs can print the exact same virtual pointer without overwriting each other's data.

### Exercise 4.3: Manual Page Table Offset Calculation
Given a 32-bit virtual address system with 4KB ($2^{12}$ bytes) page size:
1. How many bits are used for the page offset?
2. How many bits are used for the virtual page number (VPN)?
3. For virtual address `0x0001A4B0`, calculate the VPN and the byte offset.

### Exercise 4.4: Inspecting Virtual Memory Mappings (`/proc/<pid>/maps`)
Write a C program that allocates 16MB of memory and calls `getchar()`. In another terminal, inspect `/proc/<pid>/maps` on Linux (or `vmmap` on macOS). Identify the permissions (`r-xp`, `rw-p`) for the code, heap, and library segments.

### Exercise 4.5: Anonymous Memory Mapping with `mmap`
Write a program that allocates 1MB of memory using `mmap()` with `MAP_ANONYMOUS | MAP_PRIVATE` rather than `malloc()`. Write data to the region, verify it, and release it using `munmap()`.

### Exercise 4.6: File-Backed Memory Mapping
Create a 1KB text file. Use `mmap()` with `MAP_SHARED` to map the file into process memory. Mutate bytes directly via pointer dereference without calling `write()`. Verify that the changes persist to the file on disk after `msync()` and `munmap()`.

### Exercise 4.7: Memory Protection Violation (`mprotect`)
Allocate a page using `mmap()`. Change its protection to read-only using `mprotect(ptr, 4096, PROT_READ)`. Attempt to write to the page. Verify that the kernel sends `SIGSEGV` and examine the crash in `gdb`.

### Exercise 4.8: The Resident Set Size (RSS) Illusion
Allocate 100MB of heap memory using `malloc(100 * 1024 * 1024)`. Inspect `VIRT` and `RES` in `top`. Observe that `VIRT` increases by 100MB, but `RES` (physical memory) remains near 0 until pages are actually written to (Demand Paging!).

### Exercise 4.9: Observing Minor Page Faults
Write a program that uses `getrusage(RUSAGE_SELF, &usage)` to record `ru_minflt` before and after touching 1,000 newly allocated pages. Verify that touching each virgin page causes exactly one minor page fault.

### Exercise 4.10: Copy-on-Write (COW) Verification
Allocate a 10MB buffer and fill it with data. Record the process RSS memory. Call `fork()`. Observe that total system physical memory does not double! Modify 1MB of data in the child and measure the minor page faults and RSS increase.

### Exercise 4.11: Heap Expansion via `sbrk` / `brk`
Write a minimal C program using the raw `sbrk(0)` and `sbrk(4096)` system calls to manually expand the heap data break pointer by 1 page. Print the break address before and after.

### Exercise 4.12: Building a Tiny Bump Allocator
Implement your own minimal `my_malloc(size_t size)` function using a pre-allocated static buffer of 64KB. Track a pointer to the next free byte. Implement 8-byte memory alignment.

### Exercise 4.13: Building a Free-List Allocator
Extend Exercise 4.12 by adding block headers:
`struct BlockHeader { size_t size; int is_free; struct BlockHeader *next; };`
Implement `my_free(void *ptr)` that marks blocks as free and coalesces adjacent free blocks.

### Exercise 4.14: Detecting Memory Leaks with Valgrind
Write a program that leaks 3 different heap allocations:
1. Definitely lost (pointer discarded)
2. Indirectly lost (struct containing pointers discarded)
3. Still reachable (pointer exists at exit)
Run the binary under `valgrind --leak-check=full` and interpret the diagnostic report.

### Exercise 4.15: ASLR Demonstration
Write a program that prints the address of `&main` and `&stack_var`. Run the program 5 times consecutively. Observe how the addresses change randomly on each run due to Address Space Layout Randomization (ASLR).

### Exercise 4.16: Memory Locking with `mlock`
Allocate a 4KB sensitive buffer (e.g. cryptographic key). Use `mlock()` to lock the page in physical RAM, preventing the OS kernel from ever swapping it to disk. Verify with `/proc/<pid>/status` (`VmLck`).

### Exercise 4.17: Huge Pages Concept
Research and explain Linux Huge Pages (2MB vs 4KB). Why do databases like PostgreSQL and Redis achieve lower TLB miss rates when configured with Transparent Huge Pages (THP)?

### Exercise 4.18: Stack Guard Page Verification
Using `pthread_attr_setguardsize()`, configure a thread stack with a 4KB guard page. Cause a stack overflow and verify that the CPU traps on the guard page to prevent stack-heap collision.

### Exercise 4.19: Simulating Thrashing
In Python, simulate an LRU frame cache with 10 physical frames. Run a memory access loop with a working set of 12 pages. Show that the hit ratio collapses to near zero (thrashing), compared to an access loop with a working set of 8 pages.

### Exercise 4.20: Zero-Copy Transfers (`sendfile`)
Compare copying a 10MB file to a socket using:
1. `read()` from disk into userspace buffer + `write()` from userspace into socket (4 context switches, 2 CPU copies).
2. `sendfile()` system call (2 context switches, 0 userspace CPU copies).
Measure the CPU utilization and speedup.
