// Phase 43: Thrashing
// Motto: Thrashing occurs when the machine spends 99% of its time swapping pages and 1% doing useful work.

#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

int main(void) {
    printf("[Phase 43: Thrashing] Executing on Host (PID: %d)...\n", getpid());
    printf("Motto: Thrashing occurs when the machine spends 99% of its time swapping pages and 1% doing useful work.\n");
    return 0;
}
