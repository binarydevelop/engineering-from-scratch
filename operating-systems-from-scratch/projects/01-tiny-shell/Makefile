CC ?= gcc
CFLAGS = -Wall -Wextra -pedantic -std=c11 -O2
TARGET = mini-shell

all: $(TARGET)

$(TARGET): shell.c
	$(CC) $(CFLAGS) shell.c -o $(TARGET)

clean:
	rm -f $(TARGET) *.o

.PHONY: all clean
