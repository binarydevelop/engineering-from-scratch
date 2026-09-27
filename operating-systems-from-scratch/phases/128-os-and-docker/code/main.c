// Phase 128: OS and Docker
// Motto: Docker is a packaging format and daemon that configures namespaces, cgroups, and overlayfs mounts.

#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

int main(void) {
    printf("[Phase 128: OS and Docker] Executing on Host (PID: %d)...\n", getpid());
    printf("Motto: Docker is a packaging format and daemon that configures namespaces, cgroups, and overlayfs mounts.\n");
    return 0;
}
