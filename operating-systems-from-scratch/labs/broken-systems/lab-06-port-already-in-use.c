// Symptom: Server fails to start with: bind failed: Address already in use (EADDRINUSE, errno 98/48).
// Task: Use 'ss -tulpn' or 'lsof -i :9999' to find the rogue process, or configure SO_REUSEADDR.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>

#define PORT 9999

int main(void) {
    int fd1 = socket(AF_INET, SOCK_STREAM, 0);
    struct sockaddr_in addr;
    memset(&addr, 0, sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_addr.s_addr = INADDR_ANY;
    addr.sin_port = htons(PORT);

    // Bind first instance
    if (bind(fd1, (struct sockaddr *)&addr, sizeof(addr)) < 0) {
        perror("first bind");
        return 1;
    }
    listen(fd1, 5);
    printf("[Lab 06] Process %d is listening on port %d.\n", getpid(), PORT);

    // Attempt to bind second socket to identical port
    int fd2 = socket(AF_INET, SOCK_STREAM, 0);
    // BUG: Missing SO_REUSEPORT or port collision!
    if (bind(fd2, (struct sockaddr *)&addr, sizeof(addr)) < 0) {
        perror("second bind failed as expected");
    }

    close(fd1);
    close(fd2);
    return 0;
}
