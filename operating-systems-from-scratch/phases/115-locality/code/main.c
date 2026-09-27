// Phase 115: Locality
// Motto: Spatial locality keeps the cache line warm; jumping strides turns execution into cache-miss stalls.

#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

int main(void) {
    printf("[Phase 115: Locality] Executing on Host (PID: %d)...\n", getpid());
    printf("Motto: Spatial locality keeps the cache line warm; jumping strides turns execution into cache-miss stalls.\n");
    return 0;
}
