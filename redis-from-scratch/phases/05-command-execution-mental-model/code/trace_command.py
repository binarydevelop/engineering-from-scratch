#!/usr/bin/env python3
import socket
import time

def trace_execution():
    print("Tracing the life of a command: SET engine:model 'single_threaded'")
    s = socket.create_connection(("localhost", 6379), timeout=2.0)
    
    # Send SET
    cmd = b"*3\r\n$3\r\nSET\r\n$12\r\nengine:model\r\n$15\r\nsingle_threaded\r\n"
    t0 = time.perf_counter()
    s.sendall(cmd)
    resp = s.recv(1024)
    rtt_us = (time.perf_counter() - t0) * 1e6
    s.close()
    
    print(f"Server response: {resp.decode().strip()} (Round-trip time: {rtt_us:.1f} µs)")
    print("\nExecution Steps in Redis Core (server.c):")
    print("  1. kqueue/epoll wakes aeEventLoop on socket readable")
    print("  2. readQueryFromClient() reads bytes into client query buffer")
    print("  3. processInputBuffer() tokenizes RESP into argv array")
    print("  4. processCommand() looks up 'setCommand' in server.commands dict")
    print("  5. setCommand() inserts key & value SDS into db[0].dict")
    print("  6. addReply() buffers '+OK\r\n' to client output buffer")
    print("  7. writeToClient() flushes bytes back into TCP socket")

if __name__ == "__main__":
    try:
        trace_execution()
    except Exception as e:
        print(f"Note: Redis offline ({e}).")
