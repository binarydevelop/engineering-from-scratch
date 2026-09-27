// Phase 22: Process vs Thread
// Motto: Use processes when fault isolation matters; use threads when low-latency memory sharing matters.

#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

int main(void) {
    printf("[Phase 22: Process vs Thread] Executing on Host (PID: %d)...\n", getpid());
    printf("Motto: Use processes when fault isolation matters; use threads when low-latency memory sharing matters.\n");
    return 0;
}
