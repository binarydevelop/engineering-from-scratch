# Lesson 48.1: Capstone 2: Resilient Production Topology Laboratory

## Motto
"Production engineering is not about hoping things work; it is about verifying behavior when things fail."

## Problem
Designing and testing a complete multi-container resilient infrastructure: Primary + Replica + Sentinel + App + Database with automated chaos failure injection.

## Prediction
What happens to in-flight application requests during the 5-second window while Sentinel executes automatic failover?

## Why this matters
Proves the learner can build, observe, and maintain highly available production topologies.

## First principles
Uses `docker-compose.yml` to orchestrate multi-node topologies, simulating primary kills, network partition splits, and evaluating application reconnection behavior.

## Mental model
```text
  [ CLIENT ] ── TCP Socket ──► [ REDIS ENGINE CORE ] ──► [ SYSTEM SUBSYSTEM ]
```

## Build it
See [code/resilient_topology_lab.py](../code/resilient_topology_lab.py).

## Use Redis
Execute the lesson experiment:
```bash
./phases/48-production-like-redis-lab/experiments/run_experiment.sh
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
1. How should client connection pools handle socket timeout errors during active Sentinel failovers?
2. What telemetry metrics prove that a failover succeeded cleanly?

## When to use this
* Deploy this architecture for mission-critical services requiring automated failover and 99.99% uptime.

## When not to use this
* Do not over-engineer simple internal prototypes with Sentinel until high-availability SLAs require it.

## What comes next
Proceed to the next phase in the curriculum progression.
