// Solution 25: Process memory in contiguous sequential blocks that fit within the hardware cache and RAM budget.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define CHUNKS 32
#define CHUNK_SIZE (1024 * 1024) // 1 MB per chunk

int main(void) {
    printf("[Solution 25] Running Locality-Friendly Sequential Processing...\n");

    char *pages[CHUNKS];
    for (int i = 0; i < CHUNKS; i++) {
        pages[i] = malloc(CHUNK_SIZE);
        if (pages[i]) memset(pages[i], 1, CHUNK_SIZE);
    }

    // Fix: Sequential processing finishes each working set chunk before moving to next
    for (int i = 0; i < CHUNKS; i++) {
        for (int step = 0; step < 50; step++) {
            pages[i][0] += 1;
        }
    }

    for (int i = 0; i < CHUNKS; i++) {
        free(pages[i]);
    }
    printf("[Solution 25] Completed with zero page thrashing.\n");
    return 0;
}
