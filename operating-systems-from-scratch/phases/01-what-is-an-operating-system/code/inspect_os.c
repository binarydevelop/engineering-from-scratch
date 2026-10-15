#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/resource.h>
#include <sys/utsname.h>

int global_initialized_var = 42;    // Data segment
int global_uninitialized_var;      // BSS segment

int main(void) {
    int local_stack_var = 100;      // Stack
    void *heap_allocated = malloc(1024); // Heap

    printf("=================================================================\n");
    printf("   OPERATING SYSTEM RESOURCE MANAGER & ABSTRACTION INSPECTION   \n");
    printf("=================================================================\n\n");

    // 1. Host Kernel Identity
    struct utsname os_info;
    if (uname(&os_info) == 0) {
        printf("[1. Kernel Identity & Hardware Boundary]\n");
        printf("    OS Sysname   : %s\n", os_info.sysname);
        printf("    Kernel Rel   : %s\n", os_info.release);
        printf("    Architecture : %s\n", os_info.machine);
    }

    // 2. Process Tree & Identification
    printf("\n[2. Process Context (Kernel task abstraction)]\n");
    printf("    Current PID  : %d\n", getpid());
    printf("    Parent PID   : %d (e.g. bash/zsh shell)\n", getppid());
    printf("    Page Size    : %ld bytes (MMU allocation grain)\n", sysconf(_SC_PAGESIZE));
    printf("    Online CPUs  : %ld cores\n", sysconf(_SC_NPROCESSORS_ONLN));

    // 3. Virtual Address Space Demonstration
    printf("\n[3. Virtual Address Space Illusion (Pointers are virtual!)]\n");
    printf("    Code (Text) Address : %p (read-only instruction memory)\n", (void*)main);
    printf("    Data Segment Address: %p (initialized globals)\n", (void*)&global_initialized_var);
    printf("    BSS Segment Address : %p (uninitialized globals)\n", (void*)&global_uninitialized_var);
    printf("    Heap Segment Address: %p (dynamically mapped RAM)\n", heap_allocated);
    printf("    Stack Segment Addr  : %p (local activation frame)\n", (void*)&local_stack_var);

    // 4. Resource Limits Arbitrated by Kernel
    struct rlimit rlim;
    printf("\n[4. Kernel Protection Arbitrations (rlimit)]\n");
    if (getrlimit(RLIMIT_NOFILE, &rlim) == 0) {
        printf("    Max Open FDs : cur=%llu, max=%llu\n", (unsigned long long)rlim.rlim_cur, (unsigned long long)rlim.rlim_max);
    }
    if (getrlimit(RLIMIT_STACK, &rlim) == 0) {
        printf("    Max Stack Sz : %llu KB\n", (unsigned long long)rlim.rlim_cur / 1024);
    }

    printf("\n=================================================================\n");
    free(heap_allocated);
    return 0;
}
