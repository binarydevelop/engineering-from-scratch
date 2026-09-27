/*
 * socket-programs/c/tcp_echo_server.c
 * POSIX C TCP Echo Server.
 * Demonstrates: socket(), setsockopt(SO_REUSEADDR), bind(), listen(), accept(), read(), write(), close()
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <errno.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <netinet/in.h>

#define PORT 8888
#define BUFFER_SIZE 1024
#define BACKLOG 128

int main(int argc, char *argv[]) {
    int server_fd, client_fd;
    struct sockaddr_in server_addr, client_addr;
    socklen_t client_len = sizeof(client_addr);
    char buffer[BUFFER_SIZE];
    int port = (argc > 1) ? atoi(argv[1]) : PORT;

    // 1. Create TCP stream socket
    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
        perror("socket failed");
        exit(EXIT_FAILURE);
    }

    // 2. Allow port reuse
    int opt = 1;
    if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt)) < 0) {
        perror("setsockopt failed");
        exit(EXIT_FAILURE);
    }

    // 3. Bind address
    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = INADDR_ANY; // 0.0.0.0
    server_addr.sin_port = htons(port);

    if (bind(server_fd, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0) {
        perror("bind failed");
        close(server_fd);
        exit(EXIT_FAILURE);
    }

    // 4. Listen
    if (listen(server_fd, BACKLOG) < 0) {
        perror("listen failed");
        close(server_fd);
        exit(EXIT_FAILURE);
    }

    printf("C TCP Echo Server listening on 0.0.0.0:%d (server_fd=%d)\n", port, server_fd);

    while (1) {
        // 5. Accept connection
        if ((client_fd = accept(server_fd, (struct sockaddr *)&client_addr, &client_len)) < 0) {
            perror("accept failed");
            continue;
        }

        char client_ip[INET_ADDRSTRLEN];
        inet_ntop(AF_INET, &client_addr.sin_addr, client_ip, sizeof(client_ip));
        printf("[+] Client connected: %s:%d (client_fd=%d)\n", client_ip, ntohs(client_addr.sin_port), client_fd);

        // 6. Echo read / write loop
        ssize_t bytes_read;
        while ((bytes_read = read(client_fd, buffer, sizeof(buffer) - 1)) > 0) {
            buffer[bytes_read] = '\0';
            printf("    Read %zd bytes: %s", bytes_read, buffer);
            if (write(client_fd, buffer, bytes_read) < 0) {
                perror("write failed");
                break;
            }
        }

        printf("[-] Connection closed for %s:%d\n", client_ip, ntohs(client_addr.sin_port));
        close(client_fd);
    }

    close(server_fd);
    return 0;
}
