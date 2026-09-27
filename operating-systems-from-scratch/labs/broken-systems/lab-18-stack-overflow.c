// Symptom: Process aborts with SIGSEGV without any dynamic heap allocation. Register $rsp is at the boundary of stack memory.
// Task: Diagnose stack overflow in gdb, inspect stack frame size, and convert recursion to iteration.
#include <stdio.h>

void recursive_frame(int depth) {
    char stack_buffer[1024 * 16]; // 16 KB per stack frame
    stack_buffer[0] = (char)(depth & 0xFF);

    // BUG: Missing base condition! Consumes 8MB stack within ~500 frames -> crash
    if (depth % 50 == 0) {
        printf("Recursion depth: %d\n", depth);
    }
    recursive_frame(depth + 1);
}

int main(void) {
    printf("[Lab 18] Inducing Stack Overflow...\n");
    recursive_frame(1);
    return 0;
}
