CC ?= gcc
CFLAGS = -Wall -Wextra -pedantic -std=c11 -O2
TARGET = container-launcher

all: $(TARGET)

$(TARGET): container_launcher.c
	$(CC) $(CFLAGS) container_launcher.c -o $(TARGET)

clean:
	rm -f $(TARGET) *.o

.PHONY: all clean
