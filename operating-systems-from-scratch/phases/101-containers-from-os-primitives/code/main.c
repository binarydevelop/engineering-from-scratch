// Phase 101: Containers From OS Primitives
// Motto: A container is a regular host process wearing namespaces, cgroups, chroot, and capability filters.

#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

int main(void) {
    printf("[Phase 101: Containers From OS Primitives] Executing on Host (PID: %d)...\n", getpid());
    printf("Motto: A container is a regular host process wearing namespaces, cgroups, chroot, and capability filters.\n");
    return 0;
}
