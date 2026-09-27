/*
 * socket-programs/c/udp_echo_client.c
 * POSIX C UDP Echo Client.
 * Demonstrates: socket(AF_INET, SOCK_DGRAM), sendto(), recvfrom(), close()
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>

#define SERVER_IP "127.0.0.1"
#define PORT 9999
#define BUFFER_SIZE 1024

int main(int argc, char *argv[]) {
    int sock_fd;
    char buffer[BUFFER_SIZE];
    struct sockaddr_in servaddr;
    const char *server_ip = (argc > 1) ? argv[1] : SERVER_IP;
    int port = (argc > 2) ? atoi(argv[2]) : PORT;
    const char *message = (argc > 3) ? argv[3] : "Hello UDP from C!\n";

    if ((sock_fd = socket(AF_INET, SOCK_DGRAM, 0)) < 0) {
        perror("socket creation failed");
        exit(EXIT_FAILURE);
    }

    memset(&servaddr, 0, sizeof(servaddr));
    servaddr.sin_family = AF_INET;
    servaddr.sin_port = htons(port);
    inet_pton(AF_INET, server_ip, &servaddr.sin_addr);

    sendto(sock_fd, (const char *)message, strlen(message), 0,
           (const struct sockaddr *)&servaddr, sizeof(servaddr));
    printf("Sent: %s", message);

    socklen_t len = sizeof(servaddr);
    ssize_t n = recvfrom(sock_fd, (char *)buffer, BUFFER_SIZE - 1, 0,
                         (struct sockaddr *)&servaddr, &len);
    if (n > 0) {
        buffer[n] = '\0';
        printf("Echo received: %s", buffer);
    }

    close(sock_fd);
    return 0;
}
