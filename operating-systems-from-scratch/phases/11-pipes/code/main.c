// Phase 11: Pipes
// Motto: A pipe is an in-memory kernel ring buffer connecting two file descriptors across address spaces.

#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

int main(void) {
    printf("[Phase 11: Pipes] Executing on Host (PID: %d)...\n", getpid());
    printf("Motto: A pipe is an in-memory kernel ring buffer connecting two file descriptors across address spaces.\n");
    return 0;
}
