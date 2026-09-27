// Phase 65: The I/O Stack
// Motto: From userspace buffer through VFS, page cache, block layer, device driver, down to physical bus.

#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

int main(void) {
    printf("[Phase 65: The I/O Stack] Executing on Host (PID: %d)...\n", getpid());
    printf("Motto: From userspace buffer through VFS, page cache, block layer, device driver, down to physical bus.\n");
    return 0;
}
