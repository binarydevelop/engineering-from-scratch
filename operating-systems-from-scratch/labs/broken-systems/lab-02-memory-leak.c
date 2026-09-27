// Symptom: Resident set size (RSS) continuously grows until the kernel OOM killer terminates the process.
// Task: Diagnose memory growth using ps, pmap, or valgrind, identify the missing free(), and patch the leak.
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

    // BUG: Missing free(buffer); buffer leaked every request!
}

int main(void) {
    printf("[Lab 02] Running leaking daemon (PID: %d)...\n", getpid());
    for (int i = 0; i < 20; i++) {
        process_request(i);
        usleep(50000); // 50ms
    }
    printf("[Lab 02] Finished.\n");
    return 0;
}
