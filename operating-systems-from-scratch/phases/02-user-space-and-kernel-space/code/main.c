// Phase 02: User Space and Kernel Space
// Motto: Privilege separation is the foundation of computer security and hardware stability.

#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

int main(void) {
    printf("[Phase 02: User Space and Kernel Space] Executing on Host (PID: %d)...\n", getpid());
    printf("Motto: Privilege separation is the foundation of computer security and hardware stability.\n");
    return 0;
}
