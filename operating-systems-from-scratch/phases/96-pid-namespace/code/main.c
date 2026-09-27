// Phase 96: PID Namespace
// Motto: A process has different PIDs in different namespaces; the kernel translates between views.

#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

int main(void) {
    printf("[Phase 96: PID Namespace] Executing on Host (PID: %d)...\n", getpid());
    printf("Motto: A process has different PIDs in different namespaces; the kernel translates between views.\n");
    return 0;
}
