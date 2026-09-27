// Phase 106: init and PID 1
// Motto: If PID 1 dies, the kernel panics and the operating system halts immediately.

#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

int main(void) {
    printf("[Phase 106: init and PID 1] Executing on Host (PID: %d)...\n", getpid());
    printf("Motto: If PID 1 dies, the kernel panics and the operating system halts immediately.\n");
    return 0;
}
