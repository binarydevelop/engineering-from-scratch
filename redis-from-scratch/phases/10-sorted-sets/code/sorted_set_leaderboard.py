#!/usr/bin/env python3
import socket

def redis_cmd(*args):
    s = socket.create_connection(("localhost", 6379), timeout=2.0)
    msg = f"*{len(args)}\r\n" + "".join(f"${len(str(a).encode())}\r\n{str(a)}\r\n" for a in args)
    s.sendall(msg.encode())
    res = s.recv(4096).decode(errors="replace")
    s.close()
    return res.strip()

def run_sorted_set_experiments():
    board = "leaderboard:arcade"
    redis_cmd("DEL", board)
    print("1. Adding scores (ZADD):")
    redis_cmd("ZADD", board, "1500", "Alice", "2400", "Bob", "1800", "Charlie", "900", "Dave")

    print("\n2. Retrieving Rankings:")
    print("  Top 3 Players (ZREVRANGE 0 2 WITHSCORES):\n", redis_cmd("ZREVRANGE", board, "0", "2", "WITHSCORES"))
    print("  Charlie's 0-indexed Rank from top (ZREVRANK):", redis_cmd("ZREVRANK", board, "Charlie"))
    print("  Charlie's Score (ZSCORE):", redis_cmd("ZSCORE", board, "Charlie"))

    print("\n3. Dynamic Score Updates (ZINCRBY):")
    redis_cmd("ZINCRBY", board, "1000", "Dave")
    print("  Dave scored +1000 points! New rank:", redis_cmd("ZREVRANK", board, "Dave"))

if __name__ == "__main__":
    try: run_sorted_set_experiments()
    except Exception as e: print("Redis offline:", e)
