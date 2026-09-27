// Phase 49: Segmentation Faults
// Motto: A segfault is the hardware MMU catching your instruction violating the virtual memory treaty.

#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

int main(void) {
    printf("[Phase 49: Segmentation Faults] Executing on Host (PID: %d)...\n", getpid());
    printf("Motto: A segfault is the hardware MMU catching your instruction violating the virtual memory treaty.\n");
    return 0;
}
