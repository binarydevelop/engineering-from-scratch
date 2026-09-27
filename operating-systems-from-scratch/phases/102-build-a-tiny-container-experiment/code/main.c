// Phase 102: Build a Tiny Container Experiment
// Motto: De-mystify Docker by writing 50 lines of C that construct the identical isolation box.

#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

int main(void) {
    printf("[Phase 102: Build a Tiny Container Experiment] Executing on Host (PID: %d)...\n", getpid());
    printf("Motto: De-mystify Docker by writing 50 lines of C that construct the identical isolation box.\n");
    return 0;
}
