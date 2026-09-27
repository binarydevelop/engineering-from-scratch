# Lesson 62: Real-Time Aggregation

## Motto
"A stream has no end; aggregations require windows in time."

## Problem
In a batch system, you compute: `SELECT count(*) FROM pageviews GROUP BY page_id;`
In an event stream, records never stop arriving.
How do you compute counts, averages, and sums across an infinite stream?
You must slice time into **Windows**.

## Prediction
What is the difference between a Tumbling Window and a Sliding Window?

## Why this matters
Real-time dashboards, fraud velocity checks ("more than 3 login failures in 60 seconds"), and sensor monitoring all rely on windowed aggregations.

## First principles
* **Tumbling Window:** Fixed-size, non-overlapping, contiguous time intervals (e.g. [10:00-10:05), [10:05-10:10)).
* **Sliding Window:** Fixed-size, overlapping intervals advancing by an increment (e.g. 5-minute window advancing every 1 minute).
* **Session Window:** Dynamic window demarcated by periods of inactivity (e.g. user web session closing after 30 minutes of idle time).
* **Watermarks & Late Data:** What happens when an event with timestamp 10:04 AM arrives at 10:08 AM? The system must define an allowed lateness threshold.

## Mental model
```text
Tumbling Windows (10-second non-overlapping blocks):
Timeline: 00:00 ────────► 00:10 ────────► 00:20 ────────► 00:30
          [ Window 1 ]    [ Window 2 ]    [ Window 3 ]
          (Counts: 42)    (Counts: 58)    (Counts: 91)
```

## Build it
See [tumbling_window_aggregator.py](../code/tumbling_window_aggregator.py).
We implement a tumbling window aggregator that calculates event counts per key over 10-second intervals.

## Use Kafka
Stream events with timestamps into the windowed aggregator.

## Inspect it
Observe windows close and emit consolidated metrics.

## Measure it
Compare memory usage of tumbling windows vs sliding windows.

## Break it
Send a late-arriving event past the window boundary and observe late-event handling.

## Recover it
Configure allowed lateness grace periods (`grace()`).

## Modify it
Change window size from 10 seconds to 1 minute.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why do sliding windows require significantly more memory than tumbling windows?
2. How does a streaming engine decide when a window is permanently closed for late-arriving data?

## Guarantees
* Bounded, deterministic windowed calculations over unbounded event streams.

## Non-guarantees
* Events arriving after the allowed lateness threshold are dropped or sent to a late-data topic.

## When to use this
* Rate limiting, live traffic meters, clickstream dashboards, fraud scoring.

## When not to use this
* Workloads where historical data requires arbitrary retrospective aggregation across years.

## What comes next
In Phase 63, we examine When Kafka Is the WRONG Tool.
