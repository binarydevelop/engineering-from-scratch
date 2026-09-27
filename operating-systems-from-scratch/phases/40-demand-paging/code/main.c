// Phase 40: Demand Paging
// Motto: Do not load pages until the CPU demands them; laziness is the soul of operating systems efficiency.

#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

int main(void) {
    printf("[Phase 40: Demand Paging] Executing on Host (PID: %d)...\n", getpid());
    printf("Motto: Do not load pages until the CPU demands them; laziness is the soul of operating systems efficiency.\n");
    return 0;
}
