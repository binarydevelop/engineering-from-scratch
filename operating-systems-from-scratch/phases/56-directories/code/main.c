// Phase 56: Directories
// Motto: A directory is simply a special file whose contents are an array of name-to-inode mappings.

#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

int main(void) {
    printf("[Phase 56: Directories] Executing on Host (PID: %d)...\n", getpid());
    printf("Motto: A directory is simply a special file whose contents are an array of name-to-inode mappings.\n");
    return 0;
}
