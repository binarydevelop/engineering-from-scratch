// Solution 24: Configure production-grade socket listen backlog (e.g. 128 or 1024) to absorb SYN bursts.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>

#define PORT 9988

int main(void) {
    int server_fd = socket(AF_INET, SOCK_STREAM, 0);
    int opt = 1;
    setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));

    struct sockaddr_in addr;
    memset(&addr, 0, sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_addr.s_addr = INADDR_ANY;
    addr.sin_port = htons(PORT);

    bind(server_fd, (struct sockaddr *)&addr, sizeof(addr));

    // Fix: Size backlog to accommodate burst handshake traffic
    listen(server_fd, 128);

    printf("[Solution 24] Server listening on port %d with backlog=128.\n", PORT);
    close(server_fd);
    return 0;
}
