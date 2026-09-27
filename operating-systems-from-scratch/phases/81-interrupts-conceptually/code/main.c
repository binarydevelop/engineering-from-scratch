// Phase 81: Interrupts Conceptually
// Motto: An interrupt is an electrical wire from hardware forcing the CPU to pause and execute an ISR.

#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

int main(void) {
    printf("[Phase 81: Interrupts Conceptually] Executing on Host (PID: %d)...\n", getpid());
    printf("Motto: An interrupt is an electrical wire from hardware forcing the CPU to pause and execute an ISR.\n");
    return 0;
}
