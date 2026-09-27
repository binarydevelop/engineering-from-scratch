#!/usr/bin/env python3
import socket

def redis_cmd(*args):
    s = socket.create_connection(("localhost", 6379), timeout=2.0)
    msg = f"*{len(args)}\r\n" + "".join(f"${len(str(a).encode())}\r\n{str(a)}\r\n" for a in args)
    s.sendall(msg.encode())
    res = s.recv(4096).decode(errors="replace")
    s.close()
    return res.strip()

def run_string_experiments():
    print("1. Text and Binary Safety:")
    redis_cmd("SET", "str:text", "Hello Systems")
    redis_cmd("APPEND", "str:text", " World")
    print("  GET str:text ->", redis_cmd("GET", "str:text"))
    print("  STRLEN str:text ->", redis_cmd("STRLEN", "str:text"))

    print("\n2. Atomic Counters:")
    redis_cmd("DEL", "str:counter")
    print("  INCR str:counter (uninitialized) ->", redis_cmd("INCR", "str:counter"))
    print("  INCRBY str:counter 10 ->", redis_cmd("INCRBY", "str:counter", "10"))
    print("  DECR str:counter ->", redis_cmd("DECR", "str:counter"))

    print("\n3. String Type Failure Mode:")
    redis_cmd("SET", "str:word", "not_a_number")
    print("  INCR on non-numeric string ->", redis_cmd("INCR", "str:word"))

if __name__ == "__main__":
    try: run_string_experiments()
    except Exception as e: print("Redis unavailable:", e)
