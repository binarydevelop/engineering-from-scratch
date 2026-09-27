// Phase 05: Process Creation
// Motto: Every process on a Unix system has an ancestor, forming a single unified process tree rooted at PID 1.

#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

int main(void) {
    printf("[Phase 05: Process Creation] Executing on Host (PID: %d)...\n", getpid());
    printf("Motto: Every process on a Unix system has an ancestor, forming a single unified process tree rooted at PID 1.\n");
    return 0;
}
