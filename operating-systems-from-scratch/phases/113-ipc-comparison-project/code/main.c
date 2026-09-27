// Phase 113: IPC Comparison Project
// Motto: Measure before choosing: pipes offer simple streaming; shared memory offers raw bandwidth.

#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

int main(void) {
    printf("[Phase 113: IPC Comparison Project] Executing on Host (PID: %d)...\n", getpid());
    printf("Motto: Measure before choosing: pipes offer simple streaming; shared memory offers raw bandwidth.\n");
    return 0;
}
