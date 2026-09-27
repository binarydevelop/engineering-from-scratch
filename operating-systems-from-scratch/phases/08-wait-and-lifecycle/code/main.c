// Phase 08: wait() and Process Lifecycle
// Motto: A dead process cannot rest until reaped; an uncollected child becomes a zombie in the kernel table.

#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

int main(void) {
    printf("[Phase 08: wait() and Process Lifecycle] Executing on Host (PID: %d)...\n", getpid());
    printf("Motto: A dead process cannot rest until reaped; an uncollected child becomes a zombie in the kernel table.\n");
    return 0;
}
