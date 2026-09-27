// Phase 78: Signals
// Motto: A signal is a software interrupt delivered into userspace by rewriting the thread's stack frame.

#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

int main(void) {
    printf("[Phase 78: Signals] Executing on Host (PID: %d)...\n", getpid());
    printf("Motto: A signal is a software interrupt delivered into userspace by rewriting the thread's stack frame.\n");
    return 0;
}
