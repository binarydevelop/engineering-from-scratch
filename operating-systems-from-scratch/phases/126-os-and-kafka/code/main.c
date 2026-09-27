// Phase 126: OS and Kafka
// Motto: Kafka treats the operating system page cache as its primary in-memory cache and uses sendfile zero-copy.

#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

int main(void) {
    printf("[Phase 126: OS and Kafka] Executing on Host (PID: %d)...\n", getpid());
    printf("Motto: Kafka treats the operating system page cache as its primary in-memory cache and uses sendfile zero-copy.\n");
    return 0;
}
