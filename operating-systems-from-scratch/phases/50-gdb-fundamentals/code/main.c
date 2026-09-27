// Phase 50: gdb Fundamentals
// Motto: A debugger lets you freeze time, inspect registers, and inspect the physical machine state.

#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

int main(void) {
    printf("[Phase 50: gdb Fundamentals] Executing on Host (PID: %d)...\n", getpid());
    printf("Motto: A debugger lets you freeze time, inspect registers, and inspect the physical machine state.\n");
    return 0;
}
