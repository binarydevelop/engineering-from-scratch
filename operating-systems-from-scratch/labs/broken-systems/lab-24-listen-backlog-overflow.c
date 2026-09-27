// Symptom: Clients experience ECONNREFUSED or connection timeouts during brief bursts of incoming traffic.
// Task: Diagnose listen queue overflow with 'ss -lnt' (Send-Q vs Recv-Q), and configure appropriate listen backlog depth.
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

    // BUG: Setting backlog queue to 1 means only 1 pending connection can wait before kernel drops SYNs!
    listen(server_fd, 1);

    printf("[Lab 24] Server listening on port %d with backlog=1 (vulnerable to SYN drops!)\n", PORT);
    printf("Inspect listen queue with: ss -lnt '( sport = :%d )'\n", PORT);

    sleep(2);
    close(server_fd);
    return 0;
}
