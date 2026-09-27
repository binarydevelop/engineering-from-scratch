// Phase 103: Capabilities
// Motto: Root is not an all-or-nothing key; Linux capabilities decompose superuser power into 40+ discrete locks.

#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

int main(void) {
    printf("[Phase 103: Capabilities] Executing on Host (PID: %d)...\n", getpid());
    printf("Motto: Root is not an all-or-nothing key; Linux capabilities decompose superuser power into 40+ discrete locks.\n");
    return 0;
}
