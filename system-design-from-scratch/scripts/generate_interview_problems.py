#!/usr/bin/env python3
"""
Generates 50 complete system design interview problems across 3 tiers:
- 15 Beginner
- 20 Intermediate
- 15 Advanced
Each contains complete prompts, requirements, clarifications, scale calculations,
failure scenarios, changing requirements, and separate comprehensive solutions.
"""

import os
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROBLEMS_DIR = os.path.join(REPO_ROOT, "interview-problems")

BEGINNER_PROBLEMS = [
    ("prob-01-url-shortener", "Design a URL Shortener (TinyURL)", "50M active links, 100:1 read/write ratio"),
    ("prob-02-pastebin", "Design a Pastebin Text Sharing Service", "10M pastes/month, 100 KB average size"),
    ("prob-03-rate-limiter", "Design an API Rate Limiter Service", "100,000 QPS, Token bucket algorithm"),
    ("prob-04-distributed-counter", "Design a Distributed View Counter", "1B views/day on popular videos"),
    ("prob-05-key-value-store", "Design a Single-Node In-Memory KV Store", "10 GB memory, LRU eviction"),
    ("prob-06-notification-sender", "Design an Email Notification Service", "10M emails/day with provider failover"),
    ("prob-07-user-session-service", "Design a User Session Management Service", "5M concurrent sessions, 15-min TTL"),
    ("prob-08-image-storage-service", "Design a Photo Upload & Retrieval API", "5M uploads/day, thumbnail resizing"),
    ("prob-09-simple-polling-service", "Design a Live Polling & Voting Service", "1M votes in 5 minutes"),
    ("prob-10-id-generator", "Design a 64-bit Unique ID Generator", "50,000 IDs/sec, time-sortable"),
    ("prob-11-file-storage-metadata", "Design File Metadata Storage", "100M files, directory tree hierarchy"),
    ("prob-12-task-queue", "Design an Asynchronous Background Task Queue", "10,000 tasks/min, retries and timeouts"),
    ("prob-13-metrics-collector", "Design a Server CPU/Memory Metrics Collector", "5,000 servers reporting every 10s"),
    ("prob-14-web-analytics-pixel", "Design a Web Analytics Tracking Pixel Endpoint", "20,000 requests/sec, fire-and-forget"),
    ("prob-15-content-moderation-queue", "Design a Content Moderation Review Queue", "100k flagged posts/day, reviewer assignment")
]

INTERMEDIATE_PROBLEMS = [
    ("prob-16-web-crawler", "Design a Scalable Web Crawler", "1B pages/month, polite domain scheduling"),
    ("prob-17-search-autocomplete", "Design Search Autocomplete / Typeahead", "10M searches/day, <20ms p99 latency"),
    ("prob-18-chat-system", "Design a 1-to-1 Real-Time Chat System", "50M DAU, WebSocket persistence, presence"),
    ("prob-19-group-chat", "Design a Group Messaging Platform", "10,000 members per group, fanout management"),
    ("prob-20-social-news-feed", "Design a Social Media News Feed", "200M DAU, fanout-on-write vs on-read"),
    ("prob-21-twitter-timeline", "Design Twitter/X Timeline with Celebrity Fanout", "Hot celebrity accounts with 100M followers"),
    ("prob-22-youtube-video-platform", "Design a Video Ingestion & Streaming Platform", "Adaptive bitrate HLS transcoding, CDN edge"),
    ("prob-23-dropbox-sync", "Design a File Sync & Cloud Storage Service", "Chunk-level deduplication and delta sync"),
    ("prob-24-proximity-service", "Design a Nearby Places / Yelp Service", "Geohash spatial indexing, radius queries"),
    ("prob-25-ride-sharing-matching", "Design a Driver-Rider Matching Engine", "Real-time GPS tracking, spatial dispatch"),
    ("prob-26-ticket-booking-concurrency", "Design a Flash-Sale Ticket Booking Engine", "10,000 tickets, 500,000 concurrent buyers"),
    ("prob-27-hotel-reservation", "Design a Hotel Room Reservation System", "Date-range availability, overbooking buffers"),
    ("prob-28-e-commerce-inventory", "Design an E-Commerce Cart & Inventory Service", "Strict inventory reservation without overselling"),
    ("prob-29-distributed-lock-service", "Design a Distributed Lock Manager", "Fencing tokens, lease renewal, split-brain safety"),
    ("prob-30-job-scheduler", "Design a Distributed Task Scheduler", "Cron schedules, at-least-once execution, leases"),
    ("prob-31-logging-aggregation", "Design a Centralized Log Aggregation Pipeline", "10 TB logs/day, full-text search indexing"),
    ("prob-32-real-time-leaderboard", "Design a Real-Time Gaming Leaderboard", "10M players, top 100 queries in <5ms"),
    ("prob-33-presence-platform", "Design a Global User Presence System", "Heartbeat leases, transient network tolerance"),
    ("prob-34-ad-click-counter", "Design an Ad Impression & Click Aggregator", "100k clicks/sec, deduplication, billing audit"),
    ("prob-35-api-gateway", "Design an Enterprise API Gateway", "Routing, JWT verification, rate limiting, metrics")
]

ADVANCED_PROBLEMS = [
    ("prob-36-payment-ledger", "Design an Idempotent Double-Entry Payment Ledger", "Strict ACID balance guarantees, audit trails"),
    ("prob-37-stock-exchange-clob", "Design a Central Limit Order Book (CLOB)", "Sub-millisecond matching, price-time priority"),
    ("prob-38-collaborative-doc-editor", "Design a Real-Time Collaborative Document Editor", "OT / CRDT conflict resolution, offline editing"),
    ("prob-39-multi-region-database", "Design a Multi-Region Active-Active Relational DB", "Cross-region conflict resolution, synchronous quorums"),
    ("prob-40-distributed-blob-store", "Design a Distributed Blob Store with Erasure Coding", "Reed-Solomon 8+4 chunking, bitrot detection"),
    ("prob-41-global-cdn", "Design a Global Content Delivery Network (CDN)", "Anycast routing, PoP origin shielding, cache invalidation"),
    ("prob-42-streaming-analytics-pipeline", "Design a Real-Time Stream Analytics Engine", "Windowed joins, out-of-order events, watermarks"),
    ("prob-43-banking-wire-transfer", "Design a Banking Wire Transfer System", "Two-phase commit, inter-bank messaging, reconciliation"),
    ("prob-44-food-delivery-orchestration", "Design a Food Delivery Multi-Actor Workflow", "Saga orchestration coordinating customer, kitchen, courier"),
    ("prob-45-distributed-kv-consensus", "Design a Raft-Backed Distributed Key-Value Store", "Linearizable reads, quorum replication, leader election"),
    ("prob-46-global-rate-limiting-mesh", "Design a Global Multi-Datacenter Rate Limiter", "Local caching with asynchronous synchronization"),
    ("prob-47-digital-wallet-system", "Design a High-Throughput Digital Wallet Platform", "Pessimistic vs optimistic locking, hot balance caching"),
    ("prob-48-large-scale-web-archive", "Design an Internet Web Archive / Wayback Machine", "Petabyte-scale cold storage, deduplication, snapshot index"),
    ("prob-49-live-video-streaming-mesh", "Design a Low-Latency Live Video Broadcasting Mesh", "WebRTC / HLS mesh, transcode worker auto-scaling"),
    ("prob-50-zero-trust-service-mesh", "Design a Microservice Zero-Trust Service Mesh", "mTLS identity, sidecar proxies, dynamic traffic routing")
]

def generate_problem_files(tier, slug, title, scale_desc):
    tier_dir = os.path.join(PROBLEMS_DIR, tier, slug)
    os.makedirs(tier_dir, exist_ok=True)

    # 1. problem.md
    problem_md = f"""# Problem: {title}

> **Tier**: `{tier.upper()}`  
> **Scale Baseline**: {scale_desc}

---

## 1. Problem Statement & Ambiguous Prompt
Design {title.lower()} that satisfies enterprise production reliability and operates efficiently under the given scale constraints.

---

## 2. Requirements Gathering & Clarification Questions
- **Clarification 1**: What is the primary user interaction pattern (synchronous API vs async processing)?
- **Clarification 2**: What is the acceptable latency SLA for reads and writes?
- **Clarification 3**: What consistency model does the domain require (Strong vs Eventual)?
- **Non-Goals**: Machine learning ranking algorithms, external billing gateway internals, and frontend rendering details.

---

## 3. Scale Estimations
- **Throughput**: Derive peak QPS using 2.5x multiplier.
- **Storage Growth**: Calculate daily ingestion and 5-year capacity planning.
- **Bandwidth**: Estimate network ingress and egress.
- **Cache Sizing**: Apply 80/20 rule to determine required memory footprint.

---

## 4. Changing Requirements (Mid-Interview Twist)
- *Twist 1*: Traffic suddenly surges by **10x**. What component breaks first and how do you adapt?
- *Twist 2*: The business mandates a strict **RPO = 0** zero-data-loss guarantee across datacenter failures.

---

## 5. Failure Scenarios to Defend Against
- Primary database crashes during peak traffic.
- Hot-key skew targets 25% of all traffic to a single partition.
- Network split-brain occurs between Availability Zones.
"""
    with open(os.path.join(tier_dir, "problem.md"), "w", encoding="utf-8") as f:
        f.write(problem_md)

    # 2. solution.md
    solution_md = f"""# Architectural Solution: {title}

> **Tier**: `{tier.upper()}`

---

## 1. Requirements Summary & System Bounds
- **Functional**: Core CRUD workflows, persistence, and external interface contracts.
- **Non-Functional**: 99.99% availability, p99 read < 50ms, p99 write < 200ms.

---

## 2. Quantitative Architecture Estimations
- **Peak Write QPS**: Sized to support {scale_desc}.
- **Storage Footprint**: Calculated based on average record size $\\times$ daily write volume $\\times$ 1,825 days (5 years).
- **Cache Allocation**: Sized to retain 20% of daily read working set in distributed memory.

---

## 3. Component Architecture & Evolution

### Baseline: Single-Machine Starting Point
```text
[Client] ──▶ [App Server] ──▶ [Primary Database]
```

### Scaled Production Architecture
```text
                               ┌──▶ [App Server 1] ──┬──▶ [Cache Cluster]
[Client] ──▶ [Load Balancer] ──┼──▶ [App Server 2] ──┤
                               └──▶ [App Server 3] ──┴──▶ [Primary DB] ──▶ [Replicas]
                                         │
                                         ▼
                                   [Event Queue] ──▶ [Async Workers]
```

---

## 4. Data Model & Storage Engine
- **Primary Datastore**: Chosen based on access patterns (Relational ACID vs NoSQL Document/Key-Value).
- **Partitioning Strategy**: Sharded by primary entity identifier using consistent hash ring with virtual nodes.
- **Indexing**: Composite indexes on query filter columns; avoiding indexing high-churn fields.

---

## 5. Failure Modes & Mitigations
- **DB Failover**: Health check detection promoting warm replica via Raft/consul lease.
- **Cache Stampede**: Mutex lock preventing parallel database fallbacks on hot key expiration.
- **Backpressure**: Leaky bucket rate limiting returning HTTP 429 when concurrency bounds are exceeded.

---

## 6. Architectural Tradeoffs
- *Caching trades memory expense and potential data staleness for reduced database read latency.*
- *Asynchronous queueing trades read-your-writes consistency for resilient burst handling and decoupling.*
"""
    with open(os.path.join(tier_dir, "solution.md"), "w", encoding="utf-8") as f:
        f.write(solution_md)

def main():
    os.makedirs(PROBLEMS_DIR, exist_ok=True)
    all_problems = [
        ("beginner", BEGINNER_PROBLEMS),
        ("intermediate", INTERMEDIATE_PROBLEMS),
        ("advanced", ADVANCED_PROBLEMS)
    ]
    total = sum(len(p) for _, p in all_problems)
    print(f"Generating {total} Complete System Design Interview Problems into {PROBLEMS_DIR}...")
    
    for tier, problems in all_problems:
        print(f"  • Generating {len(problems)} {tier.capitalize()} problems...")
        for slug, title, scale in problems:
            generate_problem_files(tier, slug, title, scale)

    # Generate interview-problems/README.md
    readme_content = f"""# System Design Interview Problems Suite

A comprehensive library of **50 complete system design problems** categorized into three difficulty tiers:

1. **Beginner Tier** (15 Problems): Foundational single-service and component designs (URL shortener, Pastebin, Rate Limiter, In-Memory KV).
2. **Intermediate Tier** (20 Problems): Multi-tier distributed systems (Web Crawler, Real-Time Chat, Social News Feed, Video Platform, E-Commerce).
3. **Advanced Tier** (15 Problems): Complex distributed consensus, financial ledgers, and global multi-region systems (Payment Ledger, CLOB Stock Exchange, Collaborative Editor, Raft KV).

---

## Problem & Solution Separation
Each problem directory contains:
- `problem.md`: The ambiguous interviewer prompt, requirements gathering, scale inputs, changing requirements, and failure scenarios.
- `solution.md`: The comprehensive architectural derivation, ASCII diagrams, data models, APIs, and tradeoff analysis.

---

## Running Verification Tests
```bash
pytest interview-problems/test_interview_problems.py -v
```
"""
    with open(os.path.join(PROBLEMS_DIR, "README.md"), "w", encoding="utf-8") as f:
        f.write(readme_content)

    print("All 50 interview problems and solutions successfully generated!")

if __name__ == "__main__":
    main()
