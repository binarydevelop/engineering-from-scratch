// Solution 18: Convert unbounded recursion to an iterative loop with heap or fixed-size buffer.
#include <stdio.h>

void iterative_work(int max_depth) {
    printf("[Solution 18] Running iterative work (depth: %d)...\n", max_depth);
    // Fix: Single stack frame maintained; zero risk of stack overflow!
    for (int i = 1; i <= max_depth; i++) {
        if (i % 200 == 0) {
            printf("Completed iteration %d\n", i);
        }
    }
}

int main(void) {
    iterative_work(1000);
    printf("[Solution 18] Successfully executed without stack exhaustion.\n");
    return 0;
}
