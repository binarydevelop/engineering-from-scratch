// Phase 95: Namespaces From First Principles
// Motto: Namespaces virtualize system resources: what a process sees is no longer the entire truth of the machine.

#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

int main(void) {
    printf("[Phase 95: Namespaces From First Principles] Executing on Host (PID: %d)...\n", getpid());
    printf("Motto: Namespaces virtualize system resources: what a process sees is no longer the entire truth of the machine.\n");
    return 0;
}
