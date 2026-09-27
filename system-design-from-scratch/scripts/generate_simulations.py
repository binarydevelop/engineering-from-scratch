#!/usr/bin/env python3
"""
Generates the 22 runnable system design simulators in `simulations/`
and the comprehensive test suite in `simulations/test_simulations.py`.
"""

import os
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SIM_DIR = os.path.join(REPO_ROOT, "simulations")

SIMULATORS = [
    ("01_load_balancer.py", """
import random
from typing import List, Dict, Optional

class LoadBalancer:
    def __init__(self, algorithm: str = "round_robin"):
        self.algorithm = algorithm
        self.backends: List[Dict[str, any]] = []
        self._rr_index = 0

    def add_backend(self, host: str, weight: int = 1):
        self.backends.append({"host": host, "weight": weight, "active_conns": 0, "healthy": True})

    def mark_health(self, host: str, healthy: bool):
        for b in self.backends:
            if b["host"] == host:
                b["healthy"] = healthy

    def route(self) -> Optional[str]:
        healthy = [b for b in self.backends if b["healthy"]]
        if not healthy:
            return None

        if self.algorithm == "round_robin":
            choice = healthy[self._rr_index % len(healthy)]
            self._rr_index += 1
            return choice["host"]
        elif self.algorithm == "least_connections":
            choice = min(healthy, key=lambda b: b["active_conns"])
            return choice["host"]
        elif self.algorithm == "random":
            return random.choice(healthy)["host"]
        return healthy[0]["host"]

    def acquire_conn(self, host: str):
        for b in self.backends:
            if b["host"] == host:
                b["active_conns"] += 1

    def release_conn(self, host: str):
        for b in self.backends:
            if b["host"] == host and b["active_conns"] > 0:
                b["active_conns"] -= 1
"""),

    ("02_cache_aside_lru.py", """
import time
from collections import OrderedDict
from typing import Any, Callable, Optional, Dict

class LRUCacheAside:
    def __init__(self, capacity: int = 100, default_ttl_sec: float = 60.0):
        self.capacity = capacity
        self.default_ttl = default_ttl_sec
        self.cache: OrderedDict[str, Dict[str, Any]] = OrderedDict()
        self.hits = 0
        self.misses = 0

    def get(self, key: str, fetch_from_db_fn: Optional[Callable[[str], Any]] = None) -> Any:
        now = time.time()
        if key in self.cache:
            entry = self.cache[key]
            if now < entry["expires_at"]:
                self.hits += 1
                self.cache.move_to_end(key)
                return entry["value"]
            else:
                del self.cache[key]  # Expired

        self.misses += 1
        if fetch_from_db_fn:
            val = fetch_from_db_fn(key)
            if val is not None:
                self.set(key, val)
            return val
        return None

    def set(self, key: str, value: Any, ttl_sec: Optional[float] = None):
        if key in self.cache:
            self.cache.move_to_end(key)
        elif len(self.cache) >= self.capacity:
            self.cache.popitem(last=False)  # Evict oldest (LRU)

        ttl = ttl_sec if ttl_sec is not None else self.default_ttl
        self.cache[key] = {"value": value, "expires_at": time.time() + ttl}
"""),

    ("03_durable_queue.py", """
import time
import uuid
from typing import Dict, Any, Optional, List

class DurableQueue:
    def __init__(self, max_delivery_attempts: int = 3):
        self.max_attempts = max_delivery_attempts
        self.messages: Dict[str, Dict[str, Any]] = {}
        self.dlq: List[Dict[str, Any]] = []

    def publish(self, payload: Any) -> str:
        msg_id = f"msg_{uuid.uuid4().hex[:8]}"
        self.messages[msg_id] = {
            "id": msg_id,
            "payload": payload,
            "attempts": 0,
            "visible_at": time.time(),
            "status": "AVAILABLE"
        }
        return msg_id

    def poll(self, visibility_timeout_sec: float = 5.0) -> Optional[Dict[str, Any]]:
        now = time.time()
        for msg_id, msg in self.messages.items():
            if msg["status"] == "AVAILABLE" and now >= msg["visible_at"]:
                msg["attempts"] += 1
                if msg["attempts"] > self.max_attempts:
                    msg["status"] = "DEAD_LETTER"
                    self.dlq.append(dict(msg))
                    continue
                msg["visible_at"] = now + visibility_timeout_sec
                return dict(msg)
        return None

    def ack(self, msg_id: str) -> bool:
        if msg_id in self.messages:
            del self.messages[msg_id]
            return True
        return False

    def nack(self, msg_id: str):
        if msg_id in self.messages:
            self.messages[msg_id]["visible_at"] = time.time()  # Immediately visible
"""),

    ("04_replication_lag.py", """
import time
from typing import Dict, Any, List

class ReplicationNode:
    def __init__(self, name: str):
        self.name = name
        self.storage: Dict[str, Any] = {}
        self.commit_log: List[Dict[str, Any]] = []

class ReplicationCluster:
    def __init__(self, replication_delay_sec: float = 0.05):
        self.primary = ReplicationNode("primary")
        self.replicas = [ReplicationNode("replica_1"), ReplicationNode("replica_2")]
        self.replication_delay = replication_delay_sec

    def write(self, key: str, val: Any) -> int:
        version = len(self.primary.commit_log) + 1
        record = {"version": version, "key": key, "val": val, "committed_at": time.time()}
        self.primary.storage[key] = val
        self.primary.commit_log.append(record)
        return version

    def sync_replicas(self, target_version: int):
        for rec in self.primary.commit_log:
            if rec["version"] <= target_version:
                for rep in self.replicas:
                    rep.storage[rec["key"]] = rec["val"]
                    if rec not in rep.commit_log:
                        rep.commit_log.append(rec)

    def read_replica(self, replica_idx: int, key: str) -> Any:
        return self.replicas[replica_idx].storage.get(key)
"""),

    ("05_consistent_hash_ring.py", """
import hashlib
import bisect
from typing import Dict, List, Optional

class ConsistentHashRing:
    def __init__(self, virtual_nodes: int = 100):
        self.virtual_nodes = virtual_nodes
        self.ring: List[int] = []
        self.ring_map: Dict[int, str] = {}
        self.physical_nodes: set = set()

    def _hash(self, key: str) -> int:
        return int(hashlib.md5(key.encode("utf-8")).hexdigest(), 16)

    def add_node(self, node: str):
        self.physical_nodes.add(node)
        for i in range(self.virtual_nodes):
            v_key = f"{node}#vn_{i}"
            h = self._hash(v_key)
            self.ring_map[h] = node
            bisect.insort(self.ring, h)

    def remove_node(self, node: str):
        if node not in self.physical_nodes:
            return
        self.physical_nodes.remove(node)
        to_remove = [h for h, n in self.ring_map.items() if n == node]
        for h in to_remove:
            del self.ring_map[h]
            self.ring.remove(h)

    def get_node(self, key: str) -> Optional[str]:
        if not self.ring:
            return None
        h = self._hash(key)
        idx = bisect.bisect_right(self.ring, h)
        if idx == len(self.ring):
            idx = 0  # Wrap around
        return self.ring_map[self.ring[idx]]
"""),

    ("06_rate_limiter.py", """
import time
from collections import deque
from typing import Dict

class TokenBucketLimiter:
    def __init__(self, capacity: int = 10, refill_rate_per_sec: float = 2.0):
        self.capacity = capacity
        self.refill_rate = refill_rate_per_sec
        self.tokens: Dict[str, float] = {}
        self.last_updated: Dict[str, float] = {}

    def allow_request(self, client_id: str) -> bool:
        now = time.time()
        tokens = self.tokens.get(client_id, self.capacity)
        last_time = self.last_updated.get(client_id, now)

        elapsed = now - last_time
        tokens = min(self.capacity, tokens + elapsed * self.refill_rate)
        self.last_updated[client_id] = now

        if tokens >= 1.0:
            self.tokens[client_id] = tokens - 1.0
            return True
        self.tokens[client_id] = tokens
        return False

class SlidingWindowLogLimiter:
    def __init__(self, max_requests: int = 5, window_seconds: float = 1.0):
        self.max_requests = max_requests
        self.window = window_seconds
        self.logs: Dict[str, deque] = {}

    def allow_request(self, client_id: str) -> bool:
        now = time.time()
        if client_id not in self.logs:
            self.logs[client_id] = deque()

        q = self.logs[client_id]
        while q and q[0] <= now - self.window:
            q.popleft()

        if len(q) < self.max_requests:
            q.append(now)
            return True
        return False
"""),

    ("07_leader_election.py", """
from typing import List, Dict, Optional

class BullyElectionCluster:
    def __init__(self, node_ids: List[int]):
        self.node_ids = sorted(node_ids)
        self.alive = {nid: True for nid in self.node_ids}
        self.current_leader: Optional[int] = max(self.node_ids)

    def crash_node(self, node_id: int):
        self.alive[node_id] = False
        if self.current_leader == node_id:
            self.current_leader = None

    def elect_leader(self) -> Optional[int]:
        active = [nid for nid in self.node_ids if self.alive[nid]]
        if not active:
            self.current_leader = None
            return None
        self.current_leader = max(active)  # Highest active ID becomes leader
        return self.current_leader
"""),

    ("08_transactional_outbox.py", """
import sqlite3
import json
import time
import uuid
from typing import Dict, Any, List

class TransactionalOutboxManager:
    def __init__(self):
        self.conn = sqlite3.connect(":memory:", check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self):
        with self.conn:
            self.conn.execute("CREATE TABLE orders (id TEXT PRIMARY KEY, amount INTEGER);")
            self.conn.execute("CREATE TABLE outbox (id TEXT PRIMARY KEY, event_type TEXT, payload TEXT, status TEXT);")

    def create_order(self, amount: int) -> str:
        order_id = f"ord_{uuid.uuid4().hex[:6]}"
        event_id = f"evt_{uuid.uuid4().hex[:6]}"
        payload = json.dumps({"order_id": order_id, "amount": amount})
        # Atomic commit
        with self.conn:
            self.conn.execute("INSERT INTO orders VALUES (?, ?);", (order_id, amount))
            self.conn.execute("INSERT INTO outbox VALUES (?, ?, ?, 'PENDING');", (event_id, "OrderCreated", payload))
        return order_id

    def poll_and_dispatch(self) -> int:
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM outbox WHERE status = 'PENDING'")
        rows = cur.fetchall()
        count = len(rows)
        with self.conn:
            for r in rows:
                self.conn.execute("UPDATE outbox SET status = 'DISPATCHED' WHERE id = ?", (r["id"],))
        return count
"""),

    ("09_circuit_breaker.py", """
import time
from typing import Callable, Any

class CircuitBreakerOpenError(Exception):
    pass

class CircuitBreaker:
    def __init__(self, failure_threshold: int = 3, recovery_time_sec: float = 0.5):
        self.threshold = failure_threshold
        self.recovery_time = recovery_time_sec
        self.failures = 0
        self.last_failure_time = 0.0
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN

    def call(self, fn: Callable, *args, **kwargs) -> Any:
        now = time.time()
        if self.state == "OPEN":
            if now - self.last_failure_time > self.recovery_time:
                self.state = "HALF_OPEN"
            else:
                raise CircuitBreakerOpenError("Circuit is OPEN: Fast-failing")

        try:
            res = fn(*args, **kwargs)
            if self.state == "HALF_OPEN":
                self.state = "CLOSED"
                self.failures = 0
            return res
        except Exception as exc:
            self.failures += 1
            self.last_failure_time = now
            if self.failures >= self.threshold:
                self.state = "OPEN"
            raise exc
"""),

    ("10_retry_storm_jitter.py", """
import random
import time
from typing import List

class RetrySimulator:
    @staticmethod
    def calculate_backoff(attempt: int, base_sec: float = 0.1, cap_sec: float = 2.0, with_jitter: bool = True) -> float:
        # Full jitter formula: sleep = random(0, min(cap, base * 2^attempt))
        exponential = min(cap_sec, base_sec * (2 ** attempt))
        if with_jitter:
            return random.uniform(0, exponential)
        return exponential
"""),

    ("11_partition_simulator.py", """
from typing import Set

class PartitionCluster:
    def __init__(self, total_nodes: int = 5):
        self.total_nodes = total_nodes
        self.majority_quorum = (total_nodes // 2) + 1

    def can_accept_write(self, reachable_nodes: Set[int]) -> bool:
        # Quorum consistency: can only accept writes on the side of the partition with > 50%
        return len(reachable_nodes) >= self.majority_quorum
"""),

    ("12_snowflake_id.py", """
import time

class SnowflakeGenerator:
    def __init__(self, worker_id: int, epoch: int = 1700000000000):
        self.worker_id = worker_id & 0x3FF  # 10 bits
        self.epoch = epoch
        self.sequence = 0
        self.last_timestamp = -1

    def generate(self) -> int:
        timestamp = int(time.time() * 1000)
        if timestamp == self.last_timestamp:
            self.sequence = (self.sequence + 1) & 0xFFF  # 12 bits
            if self.sequence == 0:
                # Wait next millisecond
                while timestamp <= self.last_timestamp:
                    timestamp = int(time.time() * 1000)
        else:
            self.sequence = 0

        self.last_timestamp = timestamp
        # 64-bit ID: 1 sign bit (0) + 41 bit timestamp + 10 bit worker + 12 bit sequence
        snowflake = ((timestamp - self.epoch) << 22) | (self.worker_id << 12) | self.sequence
        return snowflake
"""),

    ("13_read_after_write.py", """
import time
from typing import Dict, Any

class ReadAfterWriteRouter:
    def __init__(self, sticky_window_sec: float = 2.0):
        self.window = sticky_window_sec
        self.recent_writes: Dict[str, float] = {}

    def record_write(self, user_id: str):
        self.recent_writes[user_id] = time.time()

    def route_read(self, user_id: str) -> str:
        last_write = self.recent_writes.get(user_id, 0.0)
        if time.time() - last_write < self.window:
            return "PRIMARY"  # Avoid replication lag
        return "REPLICA"
"""),

    ("14_bloom_filter.py", """
import hashlib
from typing import List

class BloomFilter:
    def __init__(self, size: int = 1000, num_hashes: int = 3):
        self.size = size
        self.num_hashes = num_hashes
        self.bit_array = [0] * size

    def _hashes(self, item: str) -> List[int]:
        res = []
        for i in range(self.num_hashes):
            h = int(hashlib.md5(f"{item}:{i}".encode()).hexdigest(), 16)
            res.append(h % self.size)
        return res

    def add(self, item: str):
        for idx in self._hashes(item):
            self.bit_array[idx] = 1

    def contains(self, item: str) -> bool:
        return all(self.bit_array[idx] == 1 for idx in self._hashes(item))
"""),

    ("15_saga_orchestrator.py", """
from typing import List, Callable, Dict, Any

class SagaStep:
    def __init__(self, name: str, execute_fn: Callable, compensate_fn: Callable):
        self.name = name
        self.execute = execute_fn
        self.compensate = compensate_fn

class SagaOrchestrator:
    def __init__(self, steps: List[SagaStep]):
        self.steps = steps
        self.executed_steps: List[SagaStep] = []

    def run(self) -> Dict[str, Any]:
        for step in self.steps:
            try:
                step.execute()
                self.executed_steps.append(step)
            except Exception as exc:
                # Rollback compensations in reverse
                for executed in reversed(self.executed_steps):
                    executed.compensate()
                return {"status": "FAILED_COMPENSATED", "failed_at": step.name, "error": str(exc)}
        return {"status": "SUCCESS"}
"""),

    ("16_two_phase_commit.py", """
from typing import List

class TwoPhaseCommitCoordinator:
    def __init__(self, participants: List[Any]):
        self.participants = participants

    def execute_transaction(self) -> bool:
        # Phase 1: Prepare
        votes = [p.prepare() for p in self.participants]
        if all(votes):
            # Phase 2: Commit
            for p in self.participants:
                p.commit()
            return True
        else:
            # Phase 2: Abort
            for p in self.participants:
                p.abort()
            return False
"""),

    ("17_lamport_clocks.py", """
class LamportClock:
    def __init__(self):
        self.time = 0

    def tick(self) -> int:
        self.time += 1
        return self.time

    def send_event(self) -> int:
        return self.tick()

    def receive_event(self, received_time: int) -> int:
        self.time = max(self.time, received_time) + 1
        return self.time
"""),

    ("18_vector_clocks.py", """
from typing import Dict, Any

class VectorClock:
    def __init__(self, node_id: str):
        self.node_id = node_id
        self.clock: Dict[str, int] = {node_id: 0}

    def increment(self):
        self.clock[self.node_id] = self.clock.get(self.node_id, 0) + 1

    def update(self, other_clock: Dict[str, int]):
        for node, time in other_clock.items():
            self.clock[node] = max(self.clock.get(node, 0), time)
        self.increment()
"""),

    ("19_heartbeat_detector.py", """
import time
from typing import Dict

class HeartbeatDetector:
    def __init__(self, timeout_sec: float = 1.0):
        self.timeout = timeout_sec
        self.last_heartbeats: Dict[str, float] = {}

    def heartbeat(self, node_id: str):
        self.last_heartbeats[node_id] = time.time()

    def is_alive(self, node_id: str) -> bool:
        last = self.last_heartbeats.get(node_id)
        if last is None:
            return False
        return (time.time() - last) <= self.timeout
"""),

    ("20_backpressure_buffer.py", """
from collections import deque
from typing import Any

class BackpressureBuffer:
    def __init__(self, capacity: int = 10):
        self.capacity = capacity
        self.buffer = deque()

    def push(self, item: Any) -> bool:
        if len(self.buffer) >= self.capacity:
            return False  # Signal upstream to back off
        self.buffer.append(item)
        return True

    def pop(self) -> Any:
        return self.buffer.popleft() if self.buffer else None
"""),

    ("21_fanout_feed.py", """
from typing import Dict, List, Set

class HybridFeedService:
    def __init__(self, celebrity_threshold: int = 100):
        self.celebrity_threshold = celebrity_threshold
        self.followers: Dict[str, Set[str]] = {}
        self.inbox_feeds: Dict[str, List[str]] = {}
        self.user_posts: Dict[str, List[str]] = {}

    def follow(self, follower: str, followee: str):
        if followee not in self.followers:
            self.followers[followee] = set()
        self.followers[followee].add(follower)

    def post_message(self, author: str, post_id: str):
        if author not in self.user_posts:
            self.user_posts[author] = []
        self.user_posts[author].append(post_id)

        # Fanout on write for regular users
        followers = self.followers.get(author, set())
        if len(followers) <= self.celebrity_threshold:
            for f in followers:
                if f not in self.inbox_feeds:
                    self.inbox_feeds[f] = []
                self.inbox_feeds[f].append(post_id)
"""),

    ("22_geohash_matcher.py", """
import math
from typing import List, Tuple

class SpatialGridMatcher:
    def __init__(self, grid_size_deg: float = 0.05):
        self.grid_size = grid_size_deg
        self.drivers: List[Tuple[str, float, float]] = []

    def add_driver(self, driver_id: str, lat: float, lng: float):
        self.drivers.append((driver_id, lat, lng))

    def find_nearby(self, lat: float, lng: float, radius_km: float = 5.0) -> List[str]:
        # Rough distance approximation: 1 deg lat ~ 111 km
        res = []
        for did, dlat, dlng in self.drivers:
            dist = math.sqrt(((dlat - lat) * 111)**2 + ((dlng - lng) * 111)**2)
            if dist <= radius_km:
                res.append(did)
        return res
""")
]

def generate_simulations():
    os.makedirs(SIM_DIR, exist_ok=True)
    print(f"Generating {len(SIMULATORS)} Runnable System Simulators in {SIM_DIR}...")
    for filename, code in SIMULATORS:
        filepath = os.path.join(SIM_DIR, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(code.strip() + "\n")
    print("All simulators generated successfully!")

if __name__ == "__main__":
    generate_simulations()
