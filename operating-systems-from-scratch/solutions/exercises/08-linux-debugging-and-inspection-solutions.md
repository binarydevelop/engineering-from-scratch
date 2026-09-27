# Solutions: Track 8 Linux Diagnostic & Kernel Inspection Exercises

### Solution 8.5: Context Switches in `/proc/<pid>/status`
* **Voluntary Context Switch (`voluntary_ctxt_switches`):** Occurs when a task explicitly yields the processor or requests a blocking resource (e.g. `sleep()`, reading from disk, waiting on a mutex or network socket).
* **Involuntary Context Switch (`nonvoluntary_ctxt_switches`):** Occurs when the kernel scheduler's timer interrupt fires, the task's time-slice quantum expires, or a higher-priority task preempts it.

### Solution 8.8: Debugging Crashes in `gdb`
```bash
gcc -g -O0 lab-10-segmentation-fault.c -o segfault_demo
gdb ./segfault_demo
(gdb) run
# Program received signal SIGSEGV, Segmentation fault.
# 0x0000000000401142 in print_user (u=0x0) at lab-10-segmentation-fault.c:11
(gdb) bt
# #0  0x0000000000401142 in print_user (u=0x0)
# #1  0x0000000000401170 in main ()
(gdb) print u
# $1 = (struct UserRecord *) 0x0
```
**Finding:** Register points to `0x0` (NULL), confirming a null-pointer dereference exception.

### Solution 8.11: Memory Metrics Interpretation
* **Free Memory:** RAM completely unallocated and idle.
* **Available Memory:** The realistic estimate of RAM that can be given to new processes immediately without swapping, computed as Free + reclaimable Page Cache/Buffers.
* **Buff/Cache:** Memory utilized by the kernel to cache disk pages and directory metadata.
* **si/so (Swap In / Swap Out):** Non-zero values indicate physical RAM is exhausted and the kernel is forced to read/write memory pages to secondary disk storage.
