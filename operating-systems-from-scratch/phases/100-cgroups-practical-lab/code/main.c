// Phase 100: cgroups Practical Lab
// Motto: Docker is a CLI for cgroups: setting memory.max and cpu.max under the hood.

#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

int main(void) {
    printf("[Phase 100: cgroups Practical Lab] Executing on Host (PID: %d)...\n", getpid());
    printf("Motto: Docker is a CLI for cgroups: setting memory.max and cpu.max under the hood.\n");
    return 0;
}
