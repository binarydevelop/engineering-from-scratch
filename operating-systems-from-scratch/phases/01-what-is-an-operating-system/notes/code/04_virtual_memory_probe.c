#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>
#include <mach/mach.h>

/**
 * Topic 04: Virtual Memory & Page Table Demonstrator
 * 
 * 1. Proves page size on current silicon (e.g. 16 KB on Apple Silicon vs 4 KB on x86).
 * 2. Proves that identical virtual addresses in two processes point to completely
 *    different physical RAM frames (Virtual Address Isolation).
 * 3. Proves Demand Paging: allocating 100 MB of virtual space does NOT consume
 *    physical RAM until pages are touched (Minor Page Faults).
 */

static size_t get_resident_memory_kb(void) {
    struct mach_task_basic_info info;
    mach_msg_type_number_t count = MACH_TASK_BASIC_INFO_COUNT;
    if (task_info(mach_task_self(), MACH_TASK_BASIC_INFO, (task_info_t)&info, &count) == KERN_SUCCESS) {
        return info.resident_size / 1024;
    }
    return 0;
}

int main(void) {
    printf("================================================================\n");
    printf("TOPIC 04: VIRTUAL MEMORY & PAGE TABLE PROBE\n");
    printf("================================================================\n");

    // 1. Detect Hardware Page Size
    int page_size = getpagesize();
    printf("[1] Hardware Page Size on this CPU: %d bytes (%.1f KB)\n", 
           page_size, (double)page_size / 1024);

    // 2. Demonstrate Virtual Address Duplication across Processes
    printf("\n[2] Virtual Memory Isolation (Parent vs Child):\n");
    int shared_named_var = 100;
    printf("  Initial Parent: &shared_named_var = %p, value = %d\n", 
           (void*)&shared_named_var, shared_named_var);

    pid_t pid = fork();
    if (pid == 0) {
        // Child Process
        shared_named_var = 999; // Triggers Copy-On-Write (COW) page fault
        printf("  [Child Process]  &shared_named_var = %p, value = %d (PID: %d)\n", 
               (void*)&shared_named_var, shared_named_var, getpid());
        exit(0);
    } else {
        wait(NULL);
        printf("  [Parent Process] &shared_named_var = %p, value = %d (PID: %d)\n", 
               (void*)&shared_named_var, shared_named_var, getpid());
        printf("  -> Notice: Both processes printed the EXACT SAME virtual pointer address,\n");
        printf("     but their Page Tables map to completely separate physical RAM frames!\n");
    }

    // 3. Demonstrate Demand Paging (Virtual vs Physical RSS)
    printf("\n[3] Demand Paging (Virtual Allocation vs Physical RSS):\n");
    size_t rss_before = get_resident_memory_kb();
    printf("  Physical RAM used before malloc: %zu KB\n", rss_before);

    size_t alloc_size = 50 * 1024 * 1024; // 50 Megabytes
    char *buffer = malloc(alloc_size);

    size_t rss_after_malloc = get_resident_memory_kb();
    printf("  Physical RAM used after 50MB malloc(): %zu KB (Virtually allocated, but NOT in RAM!)\n", 
           rss_after_malloc);

    // Now touch every page (write 1 byte per page) to trigger Minor Page Faults
    for (size_t i = 0; i < alloc_size; i += page_size) {
        buffer[i] = 1;
    }

    size_t rss_after_touch = get_resident_memory_kb();
    printf("  Physical RAM used after touching pages: %zu KB (MMU page faults populated RAM!)\n", 
           rss_after_touch);

    free(buffer);
    printf("================================================================\n");
    return 0;
}
