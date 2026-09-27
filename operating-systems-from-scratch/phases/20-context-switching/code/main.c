// Phase 20: Context Switching
// Motto: Concurrency is not free; every context switch taxes the machine in saved registers, pipeline flushes, and cache misses.

#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

int main(void) {
    printf("[Phase 20: Context Switching] Executing on Host (PID: %d)...\n", getpid());
    printf("Motto: Concurrency is not free; every context switch taxes the machine in saved registers, pipeline flushes, and cache misses.\n");
    return 0;
}
