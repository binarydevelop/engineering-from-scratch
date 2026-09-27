"""
Pytest test suite covering all 22 runnable system design simulators.
"""

import sys
import os
import time
import importlib.util

SIM_DIR = os.path.dirname(os.path.abspath(__file__))

def _load_sim(filename: str, module_name: str):
    path = os.path.join(SIM_DIR, filename)
    spec = importlib.util.spec_from_file_location(module_name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def test_01_load_balancer():
    mod = _load_sim("01_load_balancer.py", "sim_01")
    lb = mod.LoadBalancer(algorithm="round_robin")
    lb.add_backend("app_1")
    lb.add_backend("app_2")

    assert lb.route() == "app_1"
    assert lb.route() == "app_2"
    assert lb.route() == "app_1"

    # Health check removal
    lb.mark_health("app_1", False)
    assert lb.route() == "app_2"
    assert lb.route() == "app_2"

def test_02_cache_aside_lru():
    mod = _load_sim("02_cache_aside_lru.py", "sim_02")
    cache = mod.LRUCacheAside(capacity=2)

    db = {"p1": "Product 1", "p2": "Product 2", "p3": "Product 3"}
    # Cache miss -> loads from DB
    val = cache.get("p1", lambda k: db.get(k))
    assert val == "Product 1"
    assert cache.misses == 1
    assert cache.hits == 0

    # Cache hit
    val = cache.get("p1")
    assert val == "Product 1"
    assert cache.hits == 1

    # LRU eviction
    cache.get("p2", lambda k: db.get(k))
    cache.get("p3", lambda k: db.get(k))
    # p1 should now be evicted
    assert cache.get("p1") is None

def test_03_durable_queue():
    mod = _load_sim("03_durable_queue.py", "sim_03")
    q = mod.DurableQueue(max_delivery_attempts=2)
    msg_id = q.publish({"order_id": 42})

    # Poll message
    msg = q.poll(visibility_timeout_sec=0.1)
    assert msg is not None
    assert msg["id"] == msg_id

    # Visible again after timeout
    time.sleep(0.12)
    msg2 = q.poll(visibility_timeout_sec=0.1)
    assert msg2 is not None
    assert msg2["attempts"] == 2

    # Timeout again -> routes to DLQ
    time.sleep(0.12)
    msg3 = q.poll()
    assert msg3 is None  # Moved to DLQ
    assert len(q.dlq) == 1
    assert q.dlq[0]["id"] == msg_id

def test_04_replication_lag():
    mod = _load_sim("04_replication_lag.py", "sim_04")
    cluster = mod.ReplicationCluster()
    v = cluster.write("user:101", "Alice")
    assert v == 1

    # Before replica sync -> stale read
    assert cluster.read_replica(0, "user:101") is None

    # After sync
    cluster.sync_replicas(v)
    assert cluster.read_replica(0, "user:101") == "Alice"

def test_05_consistent_hash_ring():
    mod = _load_sim("05_consistent_hash_ring.py", "sim_05")
    ring = mod.ConsistentHashRing(virtual_nodes=50)
    ring.add_node("node_A")
    ring.add_node("node_B")
    ring.add_node("node_C")

    assigned_1 = ring.get_node("user_session_9921")
    assert assigned_1 in ("node_A", "node_B", "node_C")

    # Consistent routing
    assert ring.get_node("user_session_9921") == assigned_1

def test_06_rate_limiter():
    mod = _load_sim("06_rate_limiter.py", "sim_06")
    tb = mod.TokenBucketLimiter(capacity=2, refill_rate_per_sec=1.0)
    assert tb.allow_request("client_1") is True
    assert tb.allow_request("client_1") is True
    assert tb.allow_request("client_1") is False

    sw = mod.SlidingWindowLogLimiter(max_requests=2, window_seconds=1.0)
    assert sw.allow_request("ip_1") is True
    assert sw.allow_request("ip_1") is True
    assert sw.allow_request("ip_1") is False

def test_07_leader_election():
    mod = _load_sim("07_leader_election.py", "sim_07")
    cluster = mod.BullyElectionCluster([1, 2, 3, 4, 5])
    assert cluster.current_leader == 5

    cluster.crash_node(5)
    new_leader = cluster.elect_leader()
    assert new_leader == 4

def test_08_transactional_outbox():
    mod = _load_sim("08_transactional_outbox.py", "sim_08")
    outbox = mod.TransactionalOutboxManager()
    oid = outbox.create_order(1500)
    assert oid.startswith("ord_")

    count = outbox.poll_and_dispatch()
    assert count == 1
    assert outbox.poll_and_dispatch() == 0

def test_09_circuit_breaker():
    mod = _load_sim("09_circuit_breaker.py", "sim_09")
    cb = mod.CircuitBreaker(failure_threshold=2, recovery_time_sec=0.1)

    def failing():
        raise RuntimeError("Service down")

    import pytest
    with pytest.raises(RuntimeError):
        cb.call(failing)
    with pytest.raises(RuntimeError):
        cb.call(failing)

    assert cb.state == "OPEN"
    # Should fast-fail
    with pytest.raises(mod.CircuitBreakerOpenError):
        cb.call(lambda: "ok")

def test_10_retry_storm_jitter():
    mod = _load_sim("10_retry_storm_jitter.py", "sim_10")
    backoff = mod.RetrySimulator.calculate_backoff(attempt=3, base_sec=0.1, cap_sec=2.0, with_jitter=True)
    assert 0 <= backoff <= 0.8

def test_11_partition_simulator():
    mod = _load_sim("11_partition_simulator.py", "sim_11")
    cluster = mod.PartitionCluster(total_nodes=5)
    # Majority quorum requires >= 3 nodes
    assert cluster.can_accept_write({1, 2, 3}) is True
    assert cluster.can_accept_write({4, 5}) is False

def test_12_snowflake_id():
    mod = _load_sim("12_snowflake_id.py", "sim_12")
    gen = mod.SnowflakeGenerator(worker_id=7)
    id1 = gen.generate()
    id2 = gen.generate()
    assert id2 > id1
    assert (id1 >> 12) & 0x3FF == 7

def test_13_read_after_write():
    mod = _load_sim("13_read_after_write.py", "sim_13")
    router = mod.ReadAfterWriteRouter(sticky_window_sec=0.1)
    router.record_write("user_42")
    assert router.route_read("user_42") == "PRIMARY"
    time.sleep(0.12)
    assert router.route_read("user_42") == "REPLICA"

def test_14_bloom_filter():
    mod = _load_sim("14_bloom_filter.py", "sim_14")
    bf = mod.BloomFilter(size=500, num_hashes=3)
    bf.add("test_key")
    assert bf.contains("test_key") is True
    assert bf.contains("non_existent_random_key_12345") is False

def test_15_saga_orchestrator():
    mod = _load_sim("15_saga_orchestrator.py", "sim_15")
    executed = []
    compensated = []

    s1 = mod.SagaStep("reserve", lambda: executed.append("reserve"), lambda: compensated.append("reserve"))
    def fail(): raise ValueError("charge failed")
    s2 = mod.SagaStep("charge", fail, lambda: compensated.append("charge"))

    orchestrator = mod.SagaOrchestrator([s1, s2])
    res = orchestrator.run()
    assert res["status"] == "FAILED_COMPENSATED"
    assert "reserve" in compensated

def test_16_two_phase_commit():
    mod = _load_sim("16_two_phase_commit.py", "sim_16")
    class Part:
        def __init__(self, vote): self.vote = vote; self.committed = False
        def prepare(self): return self.vote
        def commit(self): self.committed = True
        def abort(self): self.committed = False

    p1 = Part(True)
    p2 = Part(True)
    coord = mod.TwoPhaseCommitCoordinator([p1, p2])
    assert coord.execute_transaction() is True
    assert p1.committed is True and p2.committed is True

def test_17_lamport_clocks():
    mod = _load_sim("17_lamport_clocks.py", "sim_17")
    p1 = mod.LamportClock()
    p2 = mod.LamportClock()
    t1 = p1.send_event()
    t2 = p2.receive_event(t1)
    assert t2 > t1

def test_18_vector_clocks():
    mod = _load_sim("18_vector_clocks.py", "sim_18")
    v1 = mod.VectorClock("A")
    v1.increment()
    assert v1.clock["A"] == 1
    v2 = mod.VectorClock("B")
    v2.update(v1.clock)
    assert v2.clock["A"] == 1
    assert v2.clock["B"] == 1

def test_19_heartbeat_detector():
    mod = _load_sim("19_heartbeat_detector.py", "sim_19")
    detector = mod.HeartbeatDetector(timeout_sec=0.1)
    detector.heartbeat("node_1")
    assert detector.is_alive("node_1") is True
    time.sleep(0.12)
    assert detector.is_alive("node_1") is False

def test_20_backpressure_buffer():
    mod = _load_sim("20_backpressure_buffer.py", "sim_20")
    buf = mod.BackpressureBuffer(capacity=2)
    assert buf.push("item_1") is True
    assert buf.push("item_2") is True
    assert buf.push("overflow") is False  # Backpressure triggered

def test_21_fanout_feed():
    mod = _load_sim("21_fanout_feed.py", "sim_21")
    svc = mod.HybridFeedService(celebrity_threshold=2)
    svc.follow("alice", "bob")
    svc.post_message("bob", "post_100")
    assert "post_100" in svc.inbox_feeds["alice"]

def test_22_geohash_matcher():
    mod = _load_sim("22_geohash_matcher.py", "sim_22")
    matcher = mod.SpatialGridMatcher()
    matcher.add_driver("d1", 37.7749, -122.4194)  # San Francisco
    matcher.add_driver("d2", 40.7128, -74.0060)   # New York

    nearby = matcher.find_nearby(37.7750, -122.4190, radius_km=5.0)
    assert "d1" in nearby
    assert "d2" not in nearby
