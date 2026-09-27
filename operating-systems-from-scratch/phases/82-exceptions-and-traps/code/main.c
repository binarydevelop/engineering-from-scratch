// Phase 82: Exceptions and Traps
// Motto: Interrupts come from hardware asynchronously; faults and traps are born synchronously inside CPU instructions.

#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

int main(void) {
    printf("[Phase 82: Exceptions and Traps] Executing on Host (PID: %d)...\n", getpid());
    printf("Motto: Interrupts come from hardware asynchronously; faults and traps are born synchronously inside CPU instructions.\n");
    return 0;
}
