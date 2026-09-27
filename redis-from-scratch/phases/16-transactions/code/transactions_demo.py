#!/usr/bin/env python3
import socket

def redis_cmd(*args):
    s = socket.create_connection(("localhost", 6379), timeout=2.0)
    msg = f"*{len(args)}\r\n" + "".join(f"${len(str(a).encode())}\r\n{str(a)}\r\n" for a in args)
    s.sendall(msg.encode())
    res = s.recv(4096).decode(errors="replace")
    s.close()
    return res.strip()

def run_transaction_demo():
    print("1. Atomic Balance Transfer using MULTI / EXEC:")
    redis_cmd("SET", "acct:alice", "100")
    redis_cmd("SET", "acct:bob", "50")

    # Raw socket connection for multi-command transaction
    s = socket.create_connection(("localhost", 6379))
    def send(c): s.sendall(f"*{len(c)}\r\n" + "".join(f"${len(str(x))}\r\n{str(x)}\r\n" for x in c).encode()); return s.recv(1024).decode().strip()
    
    send(["MULTI"])
    send(["DECRBY", "acct:alice", "30"])
    send(["INCRBY", "acct:bob", "30"])
    exec_res = send(["EXEC"])
    s.close()
    
    print("  Transaction EXEC Result:\n ", exec_res)
    print("  Alice balance:", redis_cmd("GET", "acct:alice"))
    print("  Bob balance:  ", redis_cmd("GET", "acct:bob"))

    print("\n2. Testing No-Rollback on Runtime Error:")
    s = socket.create_connection(("localhost", 6379))
    send(["MULTI"])
    send(["SET", "tx:test", "hello"])
    send(["INCR", "tx:test"]) # Runtime type error!
    send(["SET", "tx:survivor", "alive"])
    res = send(["EXEC"])
    s.close()
    print("  EXEC with type error output:\n ", res)
    print("  tx:survivor key value ->", redis_cmd("GET", "tx:survivor"))
    print("  -> Crucial insight: 'tx:survivor' was SET despite the INCR error. Redis does NOT rollback!")

if __name__ == "__main__":
    try: run_transaction_demo()
    except Exception as e: print("Redis offline:", e)
