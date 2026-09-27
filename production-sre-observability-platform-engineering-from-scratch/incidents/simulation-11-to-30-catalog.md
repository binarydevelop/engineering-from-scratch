# Incident Response Simulation Scenarios Catalog (Simulations 11 – 30)

> **Motto**: You cannot practice incident response for the first time during an active customer outage. Drills build operational reflexes.

---

### Simulation 11: Cascading Timeout in Microservice Fan-Out
* **Scenario**: Gateway calls 8 downstream services in parallel. One non-critical recommendation engine latency spikes to 15s. Gateway thread pool exhausts waiting for the slow service.
* **Triage Signal**: Gateway p99 latency spikes to 15s; active concurrency gauge maxes out at 500 threads.
* **Mitigation**: Enable graceful degradation flag in gateway to drop recommendation calls and return empty array.

### Simulation 12: Split-Brain Master Election in Redis Cluster
* **Scenario**: Network blip partitions Redis nodes. Two nodes self-promote to master, accepting conflicting writes.
* **Triage Signal**: Data inconsistency alerts; write conflict counter increases in application logs.
* **Mitigation**: Enforce quorum check (`min-replicas-to-write 1`); isolate minority partition.

### Simulation 13: Memory Leak Slow Burn
* **Scenario**: API pods leak 25MB of RAM per hour due to uncollected database cursor handles. Every 6 hours, pods are terminated by Linux OOM killer.
* **Triage Signal**: Monotonic climb in container memory working set bytes; periodic restarts visible in `kubectl get pods`.
* **Mitigation**: Increase temporary memory ceiling; implement scheduled rolling restarts while fixing leak.

### Simulation 14: Third-Party Webhook Latency Cascade
* **Scenario**: External shipping partner API slows from 50ms to 5,000ms. Checkout workers block waiting for synchronous webhook responses.
* **Triage Signal**: Distributed trace shows 5s spent on span `shipping.calculate_rate`.
* **Mitigation**: Convert synchronous HTTP call into an asynchronous background queue job.

### Simulation 15: Database Index Drop Disaster
* **Scenario**: A developer accidentally runs `DROP INDEX idx_orders_user_id` in production instead of staging.
* **Triage Signal**: PostgreSQL CPU jumps to 100%; sequential scan count climbs on `orders` table.
* **Mitigation**: Recreate index concurrently: `CREATE INDEX CONCURRENTLY idx_orders_user_id ON orders(user_id);`.

### Simulation 16: Bad Feature Flag Payload
* **Scenario**: Product manager updates feature flag configuration with invalid JSON syntax. Service JSON parser crashes on startup.
* **Triage Signal**: Container crash loop immediately following feature flag update timestamp.
* **Mitigation**: Roll back feature flag configuration to previous version in feature flag management UI.

### Simulation 17: Kubernetes Node Eviction Storm
* **Scenario**: Cloud provider preemption drains 3 nodes simultaneously. Pods with missing PodDisruptionBudgets all terminate together.
* **Triage Signal**: 502 Bad Gateway spike on API Gateway; pod replica count drops to 0.
* **Mitigation**: Provision on-demand nodes immediately; configure PodDisruptionBudget (`minAvailable: 2`).

### Simulation 18: Client Retry Amplification (Thundering Herd)
* **Scenario**: Database momentary network reset causes 500 concurrent iOS apps to retry simultaneously with zero backoff.
* **Triage Signal**: Incoming traffic rate doubles from 500 RPS to 1,500 RPS immediately after recovery.
* **Mitigation**: Enable rate limiting / load shedding (HTTP 429) at API gateway to smooth the arrival wave.

### Simulation 19: Unrotated SSL Certificate Expiry
* **Scenario**: Internal mTLS certificate between gateway and payment service expires at midnight UTC.
* **Triage Signal**: Sudden jump to 100% SSL handshake errors in gateway logs.
* **Mitigation**: Force certificate renewal via secret vault automation; restart services to reload cert store.

### Simulation 20: Thread Pool Starvation via Synchronous I/O
* **Scenario**: Developer adds synchronous file logging inside an async route handler. Worker threads block, delaying event loop.
* **Triage Signal**: Event loop lag gauge climbs from 2ms to 2,500ms; CPU remains low (< 15%).
* **Mitigation**: Roll back release; offload blocking file operations to worker threadpool.

### Simulations 21 – 30 Overview
* **Sim 21 (DNS Resolver Timeout)**: Internal CoreDNS pod crash causes 5s lookup delays. Mitigation: Scale CoreDNS replicas and enable NodeLocal DNSCache.
* **Sim 22 (Kafka Consumer Group Rebalance Storm)**: Heartbeat timeout too aggressive, triggering continuous rebalance loops. Mitigation: Increase `max.poll.interval.ms`.
* **Sim 23 (Silent Data Corruption in Schema Migration)**: New migration writes float instead of integer. Mitigation: Revert migration script and run compensation script.
* **Sim 24 (Disk Inode Exhaustion)**: Millions of zero-byte session files exhaust filesystem inodes while disk space is 80% free. Mitigation: Clean up session directory with `find -delete`.
* **Sim 25 (BGP Route Flapping)**: Edge ingress experiences intermittent packet drops. Mitigation: Withdraw flapping route and reroute traffic via secondary transit provider.
* **Sim 26 (Cloud Quota Limit Breach)**: Autoscaling blocked by cloud provider regional vCPU limit. Mitigation: Request emergency quota increase or scale in secondary region.
* **Sim 27 (Corrupted Cache Key Invalidation)**: Cache purge script deletes root key, causing cold start stampede. Mitigation: Pre-warm cache using script before directing traffic.
* **Sim 28 (Elasticsearch Shard Unassigned Loop)**: Disk watermarks reached, making indices read-only. Mitigation: Delete old indices and adjust disk low/high watermarks.
* **Sim 29 (Slowloris Low-and-Slow Attack)**: Malicious clients hold hundreds of HTTP connections open sending 1 byte/minute. Mitigation: Enforce strict HTTP request header read timeouts.
* **Sim 30 (Upstream CDN Outage)**: CDN edge network experiences major routing blackout. Mitigation: Flip DNS records directly to origin load balancers (Origin Failover).
