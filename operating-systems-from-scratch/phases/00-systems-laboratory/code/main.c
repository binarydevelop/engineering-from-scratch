// Phase 00: Systems Laboratory
// Motto: Your terminal is not just a command prompt; it is a live instrumentation console for the kernel.

#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

int main(void) {
    printf("[Phase 00: Systems Laboratory] Executing on Host (PID: %d)...\n", getpid());
    printf("Motto: Your terminal is not just a command prompt; it is a live instrumentation console for the kernel.\n");
    return 0;
}
