// Phase 14: strace Laboratory
// Motto: When code fails silently, strace reveals the raw truth the application tried to hide.

#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

int main(void) {
    printf("[Phase 14: strace Laboratory] Executing on Host (PID: %d)...\n", getpid());
    printf("Motto: When code fails silently, strace reveals the raw truth the application tried to hide.\n");
    return 0;
}
