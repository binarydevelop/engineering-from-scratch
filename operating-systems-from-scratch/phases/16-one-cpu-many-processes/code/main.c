// Phase 16: One CPU, Many Processes
// Motto: Time-sharing turns a single physical processor into the illusion of dozens of virtual processors.

#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

int main(void) {
    printf("[Phase 16: One CPU, Many Processes] Executing on Host (PID: %d)...\n", getpid());
    printf("Motto: Time-sharing turns a single physical processor into the illusion of dozens of virtual processors.\n");
    return 0;
}
