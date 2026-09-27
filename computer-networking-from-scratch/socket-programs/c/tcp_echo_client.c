/*
 * socket-programs/c/tcp_echo_client.c
 * POSIX C TCP Echo Client.
 * Demonstrates: socket(), connect(), write(), read(), close()
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>

#define SERVER_IP "127.0.0.1"
#define PORT 8888
#define BUFFER_SIZE 1024

int main(int argc, char *argv[]) {
    int sock_fd;
    struct sockaddr_in serv_addr;
    char buffer[BUFFER_SIZE];
    const char *server_ip = (argc > 1) ? argv[1] : SERVER_IP;
    int port = (argc > 2) ? atoi(argv[2]) : PORT;
    const char *message = (argc > 3) ? argv[3] : "Hello from C Client!\n";

    if ((sock_fd = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
        perror("Socket creation error");
        return -1;
    }

    memset(&serv_addr, 0, sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(port);

    if (inet_pton(AF_INET, server_ip, &serv_addr.sin_addr) <= 0) {
        perror("Invalid address or address not supported");
        close(sock_fd);
        return -1;
    }

    printf("Connecting to %s:%d...\n", server_ip, port);
    if (connect(sock_fd, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0) {
        perror("Connection Failed");
        close(sock_fd);
        return -1;
    }

    printf("[+] Connected successfully!\n");
    send(sock_fd, message, strlen(message), 0);

    ssize_t valread = read(sock_fd, buffer, sizeof(buffer) - 1);
    if (valread > 0) {
        buffer[valread] = '\0';
        printf("[+] Echo received: %s", buffer);
    }

    close(sock_fd);
    return 0;
}
