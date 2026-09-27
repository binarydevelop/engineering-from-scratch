# Lesson 40.1: Redis Security Basics: Protected Mode, ACLs, and TLS

## Motto
"Redis is designed for trusted internal networks; exposing it to the open internet invites cryptominers within minutes."

## Problem
Thousands of unprotected Redis instances on the public internet are compromised daily via remote code execution and SSH key injection.

## Prediction
What is Redis Protected Mode and when does it refuse client connections?

## Why this matters
Understanding defense-in-depth (firewalls, VPC isolation, authentication, TLS, ACLs) is mandatory for production deployments.

## First principles
1. Protected Mode: Enabled by default, blocks external connections if no password is set. 2. ACLs (Redis 6.0+): Granular user permissions restricting command categories and key patterns. 3. Command Renaming / Disabling: Disabling `FLUSHALL` and `KEYS`.

## Mental model
```text
  [ CLIENT ] ── TCP Socket ──► [ REDIS ENGINE CORE ] ──► [ SYSTEM SUBSYSTEM ]
```

## Build it
See [code/redis_security.py](../code/redis_security.py).

## Use Redis
Execute the lesson experiment:
```bash
./phases/40-redis-security-basics/experiments/run_experiment.sh
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
1. How did historical attacks compromise Linux servers via unprotected Redis instances and RDB directory configuration (`CONFIG SET dir /root/.ssh`)?
2. What are the performance trade-offs of enabling TLS encryption on Redis connections?

## When to use this
* Always bind Redis strictly to private VPC network interfaces, enforce strong ACLs, and enable TLS for cross-node replication.

## When not to use this
* Never expose Redis directly to the public internet (0.0.0.0) without firewall isolation.

## What comes next
Proceed to the next phase in the curriculum progression.
