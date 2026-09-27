# Lesson 50: Broker Failure Scenarios

## Motto
"Chaos is not an emergency; chaos is a scheduled Tuesday afternoon test."

## Problem
In theory, distributed replication provides high availability.
In practice, unless you systematically inject failures and measure recovery behavior, you do not know how your cluster responds.
What happens when:
* A follower dies?
* A leader dies?
* Two out of three replicas die?
* A broker reboots after 10 minutes offline?

## Prediction
What happens to consumer read traffic when a non-leader follower broker is killed?

## Why this matters
Rigorous failure injection transforms theoretical confidence into operational certainty.

## First principles
| Failure Scenario | Immediate Impact | Automatic Recovery |
| :--- | :--- | :--- |
| **Follower Dies** | Zero client disruption; ISR drops follower after `replica.lag.time.max.ms` | Follower catches up upon restart and rejoins ISR |
| **Leader Dies** | In-flight writes retry; KRaft elects new leader from ISR in <100ms | Clients refresh metadata and resume on new leader |
| **2 of 3 Brokers Die** | If `min.insync.replicas=2` and `acks=all`, writes are REJECTED | Restoring 1 broker allows writes to resume |
| **Disk Exhaustion** | Broker halts log appends and fences itself | Add disk space or alter retention |

## Mental model
```text
The Failure Loop:
PREDICT ──► BREAK ──► OBSERVE ──► DIAGNOSE ──► RECOVER ──► EXPLAIN
```

## Build it
See [chaos_broker_failure.py](../code/chaos_broker_failure.py).
We execute automated failure injection against cluster nodes.

## Use Kafka
Run failure drills against our 3-broker KRaft cluster.

## Inspect it
Observe broker logs and client retry logging during failure events.

## Measure it
Measure exact client interruption duration for each scenario.

## Break it
Execute hard `docker stop` on active nodes.

## Recover it
Execute `docker start` and monitor ISR healing.

## Modify it
Inject simulated packet delay on broker network interfaces using `tc` or Docker network latency.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does killing a follower cause zero write errors for clients with `acks=1`?
2. What is the difference between graceful broker shutdown (`SIGTERM`) and hard crash (`SIGKILL`)?

## Guarantees
* KRaft automatically coordinates leader election without human intervention.

## Non-guarantees
* Availability is not maintained if surviving replica count falls below `min.insync.replicas` for `acks=all`.

## When to use this
* Game days, chaos engineering, disaster recovery testing.

## When not to use this
* Directly on un-backed-up production environments without failover readiness.

## What comes next
In Phase 51, we study Consumer Failure Scenarios and diagnose rebalance storms and deadlocks.
