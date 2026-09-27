#!/usr/bin/env python3
import socket
import time

def run_pubsub_experiment():
    print("Testing Redis Pub/Sub Message Ephemerality:")
    # 1. Publish when NO SUBSCRIBERS are active
    s = socket.create_connection(("localhost", 6379))
    s.sendall(b"*3\r\n$7\r\nPUBLISH\r\n$11\r\nchat:alerts\r\n$13\r\nHello World 1\r\n")
    resp = s.recv(1024).decode()
    s.close()
    print("  Published with 0 subscribers. Return value (listener count):", resp.strip())

    print("\nTakeaway: The message was immediately discarded by Redis. When a worker is offline,")
    print("Pub/Sub provides ZERO durability. For persistent job processing, use Redis Streams.")

if __name__ == "__main__":
    try: run_pubsub_experiment()
    except Exception as e: print("Redis offline:", e)
