// Phase 46: malloc and Heap
// Motto: malloc is a userspace bookkeeping librarian; the kernel only deals in wholesale 4KB pages.

#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

int main(void) {
    printf("[Phase 46: malloc and Heap] Executing on Host (PID: %d)...\n", getpid());
    printf("Motto: malloc is a userspace bookkeeping librarian; the kernel only deals in wholesale 4KB pages.\n");
    return 0;
}
