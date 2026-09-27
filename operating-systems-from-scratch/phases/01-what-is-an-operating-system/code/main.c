// Phase 01: What Is an Operating System?
// Motto: An operating system is a resource manager, an abstraction boundary, and a hardware protection arbiter.

#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

int main(void) {
    printf("[Phase 01: What Is an Operating System?] Executing on Host (PID: %d)...\n", getpid());
    printf("Motto: An operating system is a resource manager, an abstraction boundary, and a hardware protection arbiter.\n");
    return 0;
}
