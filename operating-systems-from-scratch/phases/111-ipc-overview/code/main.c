// Phase 111: IPC Overview
// Motto: Inter-Process Communication is choosing between streaming pipes, network sockets, or zero-copy shared memory.

#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

int main(void) {
    printf("[Phase 111: IPC Overview] Executing on Host (PID: %d)...\n", getpid());
    printf("Motto: Inter-Process Communication is choosing between streaming pipes, network sockets, or zero-copy shared memory.\n");
    return 0;
}
