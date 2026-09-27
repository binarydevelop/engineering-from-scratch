// Phase 97: Mount Namespace
// Motto: A mount namespace gives a process its own private mount table and filesystem tree.

#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

int main(void) {
    printf("[Phase 97: Mount Namespace] Executing on Host (PID: %d)...\n", getpid());
    printf("Motto: A mount namespace gives a process its own private mount table and filesystem tree.\n");
    return 0;
}
