// Phase 07: exec() Deep Dive
// Motto: exec replaces the soul of a process while keeping its physical PID intact.

#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

int main(void) {
    printf("[Phase 07: exec() Deep Dive] Executing on Host (PID: %d)...\n", getpid());
    printf("Motto: exec replaces the soul of a process while keeping its physical PID intact.\n");
    return 0;
}
