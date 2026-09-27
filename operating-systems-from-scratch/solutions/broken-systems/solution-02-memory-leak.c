// Solution 02: Explicitly free heap allocations when request processing completes.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define CHUNK_SIZE (1024 * 1024) // 1 MB

void process_request(int req_id) {
    char *buffer = malloc(CHUNK_SIZE);
    if (!buffer) return;
    memset(buffer, 'A', CHUNK_SIZE);
    printf("Processed request %d (allocated %d bytes)\n", req_id, CHUNK_SIZE);

    // Fix: Free allocated memory
    free(buffer);
}

int main(void) {
    printf("[Solution 02] Running leak-free daemon (PID: %d)...\n", getpid());
    for (int i = 0; i < 20; i++) {
        process_request(i);
        usleep(10000);
    }
    printf("[Solution 02] Finished with zero memory leaks.\n");
    return 0;
}
