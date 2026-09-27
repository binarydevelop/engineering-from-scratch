CC ?= gcc
CFLAGS = -Wall -Wextra -pedantic -std=c11 -pthread -O2
TARGET = http-server

all: $(TARGET)

$(TARGET): server.c
	$(CC) $(CFLAGS) server.c -o $(TARGET)

clean:
	rm -f $(TARGET) *.o

.PHONY: all clean
