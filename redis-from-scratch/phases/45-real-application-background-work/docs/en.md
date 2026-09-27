# Lesson 45.1: Real Application: Durable Background Worker Pipeline

## Motto
"A reliable job queue never loses a task when a worker process crashes mid-execution."

## Problem
Asynchronously processing image uploads, order fulfillment, and notification emails with at-least-once delivery guarantees.

## Prediction
What happens to an in-flight job if a worker server encounters an abrupt power loss?

## Why this matters
Demonstrates production job queuing using Redis Streams Consumer Groups and PEL recovery.

## First principles
See [projects/04-task-queue/](../../../projects/04-task-queue/) for the complete durable worker pipeline.

## Mental model
```text
  [ CLIENT ] ── TCP Socket ──► [ REDIS ENGINE CORE ] ──► [ SYSTEM SUBSYSTEM ]
```

## Build it
See [code/task_pipeline_app.py](../code/task_pipeline_app.py).

## Use Redis
Execute the lesson experiment:
```bash
./phases/45-real-application-background-work/experiments/run_experiment.sh
```

## Inspect it
Inspect server status, telemetry counters, and internal diagnostic logs.

## Measure it
Quantify latency percentiles, throughput, memory allocation, and failure impact.

## Break it
Inject network partitions, process terminations, or invalid commands.

## Debug it
Diagnose the failure using evidence from diagnostic tools.

## Modify it
Tune configuration thresholds and measure behavioral changes.

## Evidence
Record findings in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why are worker tasks required to be idempotent in an at-least-once delivery architecture?
2. How does a Dead Letter Queue (DLQ) prevent poisoned tasks from crashing workers in an infinite loop?

## When to use this
* Use Redis Streams for durable asynchronous workflows, webhooks, and transactional background pipelines.

## When not to use this
* Do not use Redis for multi-day task scheduling or workflows requiring complex directed acyclic graph (DAG) routing.

## What comes next
Proceed to the next phase in the curriculum progression.
