// Symptom: Client hangs for up to 120 seconds attempting to connect to a blackholed IP address.
// Task: Diagnose TCP SYN retransmissions using tcpdump or strace -T -e connect, and implement explicit timeouts.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>

int main(void) {
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    struct sockaddr_in target;
    memset(&target, 0, sizeof(target));
    target.sin_family = AF_INET;
    // 192.0.2.1 is TEST-NET-1 (RFC 5737), typically unroutable and will blackhole SYN packets
    inet_pton(AF_INET, "192.0.2.1", &target.sin_addr);
    target.sin_port = htons(81);

    printf("[Lab 12] Connecting to unreachable host without timeout...\n");
    // BUG: Default blocking connect will stall for 60-120 seconds waiting on TCP SYN retries!
    // Interrupt with Ctrl+C
    if (connect(sock, (struct sockaddr *)&target, sizeof(target)) < 0) {
        perror("connect failed");
    }

    close(sock);
    return 0;
}
