// Phase 92: perf Introduction
// Motto: Do not guess where CPU cycles vanish; let hardware counters trace every instruction and cache miss.

#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

int main(void) {
    printf("[Phase 92: perf Introduction] Executing on Host (PID: %d)...\n", getpid());
    printf("Motto: Do not guess where CPU cycles vanish; let hardware counters trace every instruction and cache miss.\n");
    return 0;
}
