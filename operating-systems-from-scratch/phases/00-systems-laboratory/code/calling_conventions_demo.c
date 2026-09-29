#include <stdio.h>
#include <stdint.h>
#include <inttypes.h>

/**
 * Day 001: Register & Calling Convention Mechanics (ARM64 / AArch64)
 * 
 * Objective: Demonstrate the physical contract between Caller and Callee.
 * 
 * On ARM64 (Apple Silicon / Linux AArch64):
 * - x0 - x7:   Argument / Return Value registers (Caller-saved)
 * - x9 - x15:  Corruptible temporary scratch registers (Caller-saved)
 * - x19 - x28: Callee-saved registers (Callee MUST preserve and restore)
 * - x29 (FP):  Frame Pointer
 * - x30 (LR):  Link Register (Return Address)
 * - SP:        Stack Pointer (Must maintain 16-byte alignment at call boundary)
 */

#if defined(__aarch64__) || defined(__arm64__)

// An assembly function that preserves callee-saved registers (x19, x20)
// and modifies them, then safely restores them before returning.
__attribute__((naked)) int64_t callee_saved_demo(int64_t a, int64_t b) {
    __asm__ volatile (
        // 1. Prologue: Allocate 32 bytes on stack (16-byte aligned)
        // Store Frame Pointer (x29) and Link Register (x30)
        "stp x29, x30, [sp, #-32]!\n\t"
        "mov x29, sp\n\t"

        // 2. Save callee-saved registers x19, x20 to stack
        "stp x19, x20, [sp, #16]\n\t"

        // 3. Callee freely uses x19 and x20 for scratch computation
        "mov x19, x0\n\t"        // x19 = a
        "mov x20, x1\n\t"        // x20 = b
        "add x0, x19, x20\n\t"   // x0 = a + b (return value)

        // 4. Epilogue: Restore callee-saved registers
        "ldp x19, x20, [sp, #16]\n\t"

        // 5. Restore FP and LR, deallocate stack frame
        "ldp x29, x30, [sp], #32\n\t"
        "ret\n\t"
    );
}

#else

int64_t callee_saved_demo(int64_t a, int64_t b) {
    return a + b;
}

#endif

int main(void) {
    printf("================================================================\n");
    printf("DAY 001: HARDWARE & REGISTER CALLING CONVENTIONS DECONSTRUCTION\n");
    printf("================================================================\n");

    int64_t val1 = 42;
    int64_t val2 = 58;
    int64_t result = callee_saved_demo(val1, val2);

    printf("Input Arguments : a = %" PRId64 ", b = %" PRId64 "\n", val1, val2);
    printf("Returned Value  : %" PRId64 " (Passed via Return Register x0 / rax)\n", result);
    printf("Contract Status : Callee-saved registers safely preserved across frame!\n");
    printf("================================================================\n");

    return 0;
}
