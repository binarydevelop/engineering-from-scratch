#!/usr/bin/env python3
import socket
import json
import time

def send_command(cmd, host="127.0.0.1", port=9999):
    s = socket.create_connection((host, port), timeout=3)
    s.sendall(f"{cmd}\n".encode())
    resp = s.recv(4096).decode()
    s.close()
    return resp.strip()

if __name__ == "__main__":
    print("Testing PING:")
    print(f" -> {send_command('PING')}")

    print("\nAppending 3 events over TCP:")
    for event in ["login:alice", "view_item:shoes", "add_cart:shoes"]:
        resp = send_command(f"APPEND {event}")
        print(f" Appended '{event}' -> Server Reply: {resp}")

    print("\nFetching events from offset 0:")
    resp = send_command("FETCH 0")
    print(f" Raw reply: {resp}")
