// Phase 09: Build a Tiny Shell
// Motto: The shell is not magic; it is an ordinary userspace loop turning strings into processes.

#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

int main(void) {
    printf("[Phase 09: Build a Tiny Shell] Executing on Host (PID: %d)...\n", getpid());
    printf("Motto: The shell is not magic; it is an ordinary userspace loop turning strings into processes.\n");
    return 0;
}
