// Phase 105: Boot Process Overview
// Motto: Booting is a relay race of trust: UEFI initializes hardware, loads bootloader, which starts kernel, which spawns init.

#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

int main(void) {
    printf("[Phase 105: Boot Process Overview] Executing on Host (PID: %d)...\n", getpid());
    printf("Motto: Booting is a relay race of trust: UEFI initializes hardware, loads bootloader, which starts kernel, which spawns init.\n");
    return 0;
}
