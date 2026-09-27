// Phase 99: cgroups From First Principles
// Motto: Namespaces control what you can SEE; control groups control what you can USE.

#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

int main(void) {
    printf("[Phase 99: cgroups From First Principles] Executing on Host (PID: %d)...\n", getpid());
    printf("Motto: Namespaces control what you can SEE; control groups control what you can USE.\n");
    return 0;
}
