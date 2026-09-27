#!/usr/bin/env python3
"""
projects/02-leaderboard/leaderboard.py — Real-Time Gaming Leaderboard Engine

Demonstrates:
1. ZADD / ZINCRBY for high-frequency player score updates
2. ZREVRANGE for top-N global leaderboards
3. ZREVRANK for 0-indexed and 1-indexed relative rank lookups
4. ZSCORE for instant player points verification
5. Percentile calculation and paginated leaderboard queries
"""

import socket
import time
import random

REDIS_HOST = "localhost"
REDIS_PORT = 6379

def redis_cmd(*args):
    s = socket.create_connection((REDIS_HOST, REDIS_PORT), timeout=2.0)
    msg = f"*{len(args)}\r\n"
    for arg in args:
        s_arg = str(arg)
        msg += f"${len(s_arg.encode('utf-8'))}\r\n{s_arg}\r\n"
    s.sendall(msg.encode("utf-8"))
    
    # Read full response
    chunks = []
    while True:
        data = s.recv(4096)
        if not data:
            break
        chunks.append(data)
        if len(data) < 4096:
            break
    s.close()
    return b"".join(chunks).decode("utf-8", errors="replace")

class Leaderboard:
    def __init__(self, board_name="game:global_leaderboard"):
        self.name = board_name

    def record_score(self, player_id, score):
        return redis_cmd("ZADD", self.name, score, player_id)

    def increment_score(self, player_id, points):
        return redis_cmd("ZINCRBY", self.name, points, player_id)

    def get_top_players(self, limit=10):
        raw = redis_cmd("ZREVRANGE", self.name, 0, limit - 1, "WITHSCORES")
        lines = [line for line in raw.split("\r\n") if line and not line.startswith("*") and not line.startswith("$")]
        results = []
        for i in range(0, len(lines), 2):
            if i + 1 < len(lines):
                results.append((lines[i], float(lines[i+1])))
        return results

    def get_player_rank(self, player_id):
        raw = redis_cmd("ZREVRANK", self.name, player_id)
        if raw.startswith(":-1") or raw.startswith("$-1"):
            return None
        if raw.startswith(":"):
            return int(raw[1:].strip()) + 1 # 1-based rank
        return None

    def get_player_score(self, player_id):
        raw = redis_cmd("ZSCORE", self.name, player_id)
        if raw.startswith("$-1"):
            return None
        lines = [l for l in raw.split("\r\n") if l and not l.startswith("$")]
        return float(lines[0]) if lines else None

    def total_players(self):
        raw = redis_cmd("ZCARD", self.name)
        if raw.startswith(":"):
            return int(raw[1:].strip())
        return 0

def simulate_tournament(num_players=1000, num_events=5000):
    lb = Leaderboard("tourney:spring_2026")
    print(f"Clearing old tournament and seeding {num_players:,} players...")
    redis_cmd("DEL", lb.name)

    t0 = time.perf_counter()
    # Batch pipeline simulation: simulate matches
    for i in range(num_players):
        initial_score = random.randint(100, 2500)
        lb.record_score(f"player_{i:04d}", initial_score)
    seed_time = time.perf_counter() - t0
    print(f"Seeded {num_players:,} players in {seed_time:.2f}s ({num_players/seed_time:,.0f} ops/sec)")

    print(f"\nSimulating {num_events:,} high-frequency match victory point updates...")
    t0 = time.perf_counter()
    for _ in range(num_events):
        p = f"player_{random.randint(0, num_players-1):04d}"
        pts = random.choice([15, 25, 50, -10])
        lb.increment_score(p, pts)
    update_time = time.perf_counter() - t0
    print(f"Completed {num_events:,} score updates in {update_time:.2f}s ({num_events/update_time:,.0f} ops/sec)")

    print("\n" + "="*50)
    print("      TOURNAMENT LEADERBOARD (TOP 10 PLAYERS)")
    print("="*50)
    top_10 = lb.get_top_players(10)
    for rank, (player, score) in enumerate(top_10, 1):
        print(f"  #{rank:2d}  {player:15} : {score:8,.0f} pts")

    # Sample random player rank lookup
    sample_player = "player_0042"
    rank = lb.get_player_rank(sample_player)
    score = lb.get_player_score(sample_player)
    total = lb.total_players()
    print("\nTarget Player Inspection:")
    print(f"  • Player ID   : {sample_player}")
    print(f"  • Global Rank : #{rank:,} / {total:,} players")
    print(f"  • Points      : {score:,.0f}")
    if rank:
        pct = (1.0 - (rank / total)) * 100
        print(f"  • Percentile  : Top {100 - pct:.1f}%")

if __name__ == "__main__":
    simulate_tournament()
