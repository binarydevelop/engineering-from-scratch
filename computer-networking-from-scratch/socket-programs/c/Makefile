CC ?= gcc
CFLAGS ?= -Wall -Wextra -O2

TARGETS = tcp_echo_server tcp_echo_client udp_echo_server udp_echo_client

all: $(TARGETS)

tcp_echo_server: tcp_echo_server.c
	$(CC) $(CFLAGS) -o $@ $<

tcp_echo_client: tcp_echo_client.c
	$(CC) $(CFLAGS) -o $@ $<

udp_echo_server: udp_echo_server.c
	$(CC) $(CFLAGS) -o $@ $<

udp_echo_client: udp_echo_client.c
	$(CC) $(CFLAGS) -o $@ $<

test: all
	@echo "All C binaries compiled successfully."

clean:
	rm -f $(TARGETS)
