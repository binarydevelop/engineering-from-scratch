// Phase 21: Threads From First Principles
// Motto: Threads share memory by default; processes isolate memory by default.

#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

int main(void) {
    printf("[Phase 21: Threads From First Principles] Executing on Host (PID: %d)...\n", getpid());
    printf("Motto: Threads share memory by default; processes isolate memory by default.\n");
    return 0;
}
