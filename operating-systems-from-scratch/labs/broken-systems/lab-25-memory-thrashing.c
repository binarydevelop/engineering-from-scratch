// Symptom: System performance collapses, CPU time collapses into waiting on I/O, page fault rates skyrocket.
// Task: Diagnose memory thrashing with 'vmstat 1' (si/so, page in/out), calculate working set, and restructure memory access patterns.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define CHUNKS 32
#define CHUNK_SIZE (1024 * 1024) // 1 MB per chunk

int main(void) {
    printf("[Lab 25] Demonstrating Memory Thrashing Pattern (PID: %d)...\n", getpid());

    // Allocate 32 MB array of pointers
    char *pages[CHUNKS];
    for (int i = 0; i < CHUNKS; i++) {
        pages[i] = malloc(CHUNK_SIZE);
        if (pages[i]) memset(pages[i], 1, CHUNK_SIZE);
    }

    // BUG: Jumping randomly across a huge working set forces continuous TLB and page eviction
    printf("Accessing pages with thrashing stride...\n");
    for (int step = 0; step < 50; step++) {
        for (int i = 0; i < CHUNKS; i++) {
            int target = (i * 7) % CHUNKS;
            pages[target][0] += 1;
        }
    }

    for (int i = 0; i < CHUNKS; i++) {
        free(pages[i]);
    }
    printf("[Lab 25] Finished.\n");
    return 0;
}
