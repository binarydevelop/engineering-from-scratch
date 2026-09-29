#include <stdio.h>
#include <signal.h>
#include <stdlib.h>

void segfault_handler(int sig) {
    printf("[KERNEL TRAP] Caught signal %d (SIGSEGV)!\n", sig);
    printf("Hardware Action: The CPU MMU intercepted access to address 0x0.\n");
    printf("Kernel Action  : The OS refused invalid access and notified the process via a signal.\n");
    printf("Outcome        : Hardware stability preserved.\n");
    exit(0);
}

int main(void) {
    signal(SIGSEGV, segfault_handler);

    printf("================================================================\n");
    printf("TOPIC 01: HARDWARE MEMORY PROTECTION DEMONSTRATION\n");
    printf("================================================================\n");
    printf("Attempting to write to protected virtual address NULL (0x0)...\n");

    volatile int *bad_ptr = NULL;
    *bad_ptr = 42; // Hardware trap triggered here!

    return 0;
}
