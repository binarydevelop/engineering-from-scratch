// Phase 104: Virtual Machines vs Containers
// Motto: VMs virtualize the hardware and run separate kernels; containers share the host kernel and virtualize the OS view.

#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

int main(void) {
    printf("[Phase 104: Virtual Machines vs Containers] Executing on Host (PID: %d)...\n", getpid());
    printf("Motto: VMs virtualize the hardware and run separate kernels; containers share the host kernel and virtualize the OS view.\n");
    return 0;
}
