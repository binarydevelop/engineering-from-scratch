// Phase 60: Buffered I/O
// Motto: System calls are expensive; buffering amortizes kernel crossing costs into bulk transfers.

#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

int main(void) {
    printf("[Phase 60: Buffered I/O] Executing on Host (PID: %d)...\n", getpid());
    printf("Motto: System calls are expensive; buffering amortizes kernel crossing costs into bulk transfers.\n");
    return 0;
}
