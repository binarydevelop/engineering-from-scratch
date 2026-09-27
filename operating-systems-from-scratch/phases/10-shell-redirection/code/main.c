// Phase 10: Shell Redirection
// Motto: By rewriting the file descriptor table before exec, the shell redirects I/O invisibly to the program.

#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

int main(void) {
    printf("[Phase 10: Shell Redirection] Executing on Host (PID: %d)...\n", getpid());
    printf("Motto: By rewriting the file descriptor table before exec, the shell redirects I/O invisibly to the program.\n");
    return 0;
}
