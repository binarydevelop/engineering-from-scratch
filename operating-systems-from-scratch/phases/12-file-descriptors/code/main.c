// Phase 12: File Descriptors
// Motto: A file descriptor is simply an index into a per-process kernel array of pointers to open file objects.

#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

int main(void) {
    printf("[Phase 12: File Descriptors] Executing on Host (PID: %d)...\n", getpid());
    printf("Motto: A file descriptor is simply an index into a per-process kernel array of pointers to open file objects.\n");
    return 0;
}
