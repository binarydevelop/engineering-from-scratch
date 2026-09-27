// Phase 13: System Calls
// Motto: System calls are the defined diplomatic treaty between userspace and the operating system kernel.

#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

int main(void) {
    printf("[Phase 13: System Calls] Executing on Host (PID: %d)...\n", getpid());
    printf("Motto: System calls are the defined diplomatic treaty between userspace and the operating system kernel.\n");
    return 0;
}
