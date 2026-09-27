# Lesson 26.1: Pub/Sub: Ephemeral Messaging vs. Durable Queuing

## Motto
"Redis Pub/Sub is fire-and-forget: if a subscriber is offline for one millisecond, that message is lost forever."

## Problem
Engineers often use Redis Pub/Sub for background jobs or payment notifications, only to discover that unacknowledged messages vanish if a worker restarts or encounters network blips.

## Prediction
If a subscriber disconnects and the publisher sends 5 messages, will the subscriber receive them upon reconnecting?

## Why this matters
Pub/Sub is designed for real-time notifications (chat, live UI alerts), NOT durable event-driven processing.

## First principles
In Redis Pub/Sub, the server maintains no buffer or historical queue of messages. If zero subscribers are listening to a channel, the message is discarded immediately by the server.

## Mental model
```text
  [ CLIENT WORKERS ] ── TCP Socket ──► [ REDIS ENGINE ] ──► [ LOCK / LOG / STREAM ]
```

## Build it
See [code/pubsub_lab.py](../code/pubsub_lab.py).

## Use Redis
Execute the lesson experiment:
```bash
./phases/26-pub-sub/experiments/run_experiment.sh
```

## Inspect it
Inspect command return codes, internal data structures, and memory.

## Measure it
Quantify latency, concurrency race conditions, and throughput.

## Break it
Inject network delays, TTL expirations, or ungraceful client terminations.

## Debug it
Diagnose the failure using logs and atomic status returns.

## Modify it
Tune timeouts, concurrency levels, or batch sizes and observe shifts.

## Evidence
Record findings in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does Redis Pub/Sub consume very little memory compared to Redis Streams?
2. What happens to Redis server memory if a connected subscriber is too slow to read incoming messages?

## When to use this
* Use Pub/Sub for ephemeral real-time broadcasts: live sports score push alerts, chat notifications.

## When not to use this
* Never use Pub/Sub for financial transactions, task queues, or events requiring at-least-once delivery.

## What comes next
Proceed to the next phase in the curriculum progression.
