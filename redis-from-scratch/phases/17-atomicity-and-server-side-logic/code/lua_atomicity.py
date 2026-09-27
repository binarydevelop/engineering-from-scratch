#!/usr/bin/env python3
import socket

def redis_cmd(*args):
    s = socket.create_connection(("localhost", 6379), timeout=2.0)
    msg = f"*{len(args)}\r\n" + "".join(f"${len(str(a).encode())}\r\n{str(a)}\r\n" for a in args)
    s.sendall(msg.encode())
    res = s.recv(4096).decode(errors="replace")
    s.close()
    return res.strip()

def run_lua_experiment():
    stock_key = "inventory:phone"
    redis_cmd("SET", stock_key, "2") # Only 2 in stock!

    # Atomic check-and-decrement script
    LUA_PURCHASE = """
    local current = tonumber(redis.call('GET', KEYS[1]) or 0)
    if current > 0 then
        redis.call('DECR', KEYS[1])
        return 1
    else
        return 0
    end
    """
    print("Testing Atomic Purchase via Lua script:")
    print("  Customer 1 attempt ->", "SUCCESS" if ":1" in redis_cmd("EVAL", LUA_PURCHASE, "1", stock_key) else "OUT OF STOCK")
    print("  Customer 2 attempt ->", "SUCCESS" if ":1" in redis_cmd("EVAL", LUA_PURCHASE, "1", stock_key) else "OUT OF STOCK")
    print("  Customer 3 attempt ->", "SUCCESS" if ":1" in redis_cmd("EVAL", LUA_PURCHASE, "1", stock_key) else "OUT OF STOCK")
    print("Final Stock in Redis:", redis_cmd("GET", stock_key))

if __name__ == "__main__":
    try: run_lua_experiment()
    except Exception as e: print("Redis offline:", e)
