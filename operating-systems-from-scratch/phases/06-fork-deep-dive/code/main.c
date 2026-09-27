// Phase 06: fork() Deep Dive
// Motto: One call, two returns: fork clones the calling process while preserving memory isolation.

#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

int main(void) {
    printf("[Phase 06: fork() Deep Dive] Executing on Host (PID: %d)...\n", getpid());
    printf("Motto: One call, two returns: fork clones the calling process while preserving memory isolation.\n");
    return 0;
}
