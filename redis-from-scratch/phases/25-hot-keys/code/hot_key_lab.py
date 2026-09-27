#!/usr/bin/env python3
import socket
import random

def redis_cmd(*args):
    s = socket.create_connection(("localhost", 6379), timeout=2.0)
    msg = f"*{len(args)}\r\n" + "".join(f"${len(str(a).encode())}\r\n{str(a)}\r\n" for a in args)
    s.sendall(msg.encode())
    res = s.recv(4096).decode(errors="replace")
    s.close()
    return res.strip()

def run_hot_key_sharding():
    base_key = "hot:config_flag"
    num_shards = 4
    print(f"Mitigating Hot Key by replicating across {num_shards} key shards...")
    # Write same value to all shards
    for i in range(num_shards):
        redis_cmd("SET", f"{base_key}:{i}", "enabled_v2")

    # Readers randomly pick a shard, balancing load across cores/nodes
    print("Simulating 10 balanced client reads:")
    for client_id in range(10):
        chosen_shard = f"{base_key}:{random.randint(0, num_shards - 1)}"
        val = redis_cmd("GET", chosen_shard).split("\r\n")[-1]
        print(f"  Client {client_id:2d} read from {chosen_shard} -> {val}")

if __name__ == "__main__":
    try: run_hot_key_sharding()
    except Exception as e: print("Redis offline:", e)
