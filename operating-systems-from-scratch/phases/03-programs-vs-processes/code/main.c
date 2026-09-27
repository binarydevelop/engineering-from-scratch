// Phase 03: Programs vs Processes
// Motto: A program is passive text on disk; a process is an active organism in kernel memory.

#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

int main(void) {
    printf("[Phase 03: Programs vs Processes] Executing on Host (PID: %d)...\n", getpid());
    printf("Motto: A program is passive text on disk; a process is an active organism in kernel memory.\n");
    return 0;
}
