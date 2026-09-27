# Production SRE & Platform Engineering Glossary

> **Motto**: Precise terminology creates clear thinking; sloppy definitions produce sloppy operations.

---

### Availability
The ratio of successful, valid requests or operations to total eligible requests over a defined time window:
$$\text{Availability} = \frac{\text{Successful Requests}}{\text{Total Valid Requests}}$$
Availability is NOT container uptime or ping response; a pod can run with 100% uptime while failing 100% of user checkout requests.

### Alert Fatigue
The desensitization of human responders caused by frequent, false, non-actionable, or flapping alarms. Alert fatigue directly leads to real SEV-1 outages being ignored.

### Baggage (OpenTelemetry)
A contextual key-value store propagated alongside trace context across microservice boundaries. Unlike trace span attributes (which are local to a span), baggage travels across the entire downstream call chain. It must never be used for large or high-sensitivity payloads.

### Backpressure
A resilience mechanism by which a downstream consumer signals to an upstream producer that it cannot keep pace with incoming work, causing the producer to throttle, buffer, or reject requests rather than collapsing under unbounded queue growth.

### Bulkhead
An architectural pattern that isolates critical resources (thread pools, connection pools, memory segments) into partitions so that a failure or runaway demand in one partition cannot starve or collapse the entire system.

### Burn Rate
The rate at which a service is consuming its error budget relative to its allowable rate under the SLO. A burn rate of 1.0 means the error budget will be exactly 100% depleted at the end of the compliance window (e.g. 30 days). A burn rate of 14.4 means 2% of the total monthly error budget is consumed in just 1 hour.

### Cardinality
The number of unique sets of label key-value pairs associated with a time series. In metrics systems like Prometheus, high cardinality (e.g. inserting `user_id` or `order_id` into a label) multiplies time series exponentially, causing memory exhaustion and crashes.

### Circuit Breaker
A client-side proxy state machine (Closed, Open, Half-Open) that monitors downstream calls. When failures cross a predefined threshold, the circuit trips to **Open**, immediately failing fast without sending network traffic, protecting both caller and downstream service from retry storms.

### Critical User Journey (CUJ)
A specific end-to-end workflow executed by a customer that directly delivers business value (e.g. "Add to Cart and Submit Payment"). SLOs must be anchored to CUJs rather than internal microservice infrastructure.

### Error Budget
The allowable amount of unreliability a service can accumulate over a defined time window while still meeting its Service Level Objective ($100\% - \text{SLO Target}$). It represents the currency balance between feature release velocity and reliability investments.

### Exemplar
A reference attached to a specific metric measurement that links directly to a distributed trace ID sampled during that measurement window, enabling instant 1-click correlation from metric spike to trace waterfall.

### Golden Path
A supported, opinionated, and heavily automated self-service path provided by an internal platform team that solves 80% of common engineering needs with minimal cognitive friction.

### Head Sampling vs Tail Sampling
* **Head Sampling**: A sampling decision made at the root span when a request begins (e.g. sample 5% of all requests). Fast and cheap, but risks dropping rare 500 error traces.
* **Tail Sampling**: A sampling decision deferred until an entire distributed trace has completed (typically inside the OpenTelemetry Collector). Ensures all traces with errors or high latency are retained while dropping boring successful traces.

### Little's Law
A fundamental queueing theorem stating that the average number of concurrent requests ($L$) in a stable system equals the long-term average effective arrival rate ($\lambda$) multiplied by the average time a request spends in the system ($W$):
$$L = \lambda W$$
If downstream latency doubles, required concurrency doubles.

### OTLP (OpenTelemetry Protocol)
The vendor-neutral wire protocol used by OpenTelemetry APIs, SDKs, and Collectors to serialize and transmit traces, metrics, and logs using Protocol Buffers over gRPC or HTTP.

### RED Method
A microservice operational diagnostic framework focusing on **Rate** (requests/sec), **Errors** (failed requests/sec), and **Duration** (latency distribution).

### Runbook
A living operational guide linked directly from a paging alert that provides the on-call engineer with immediate symptom verification, blast radius assessment, and step-by-step mitigation procedures.

### SLI (Service Level Indicator)
A carefully defined, quantitative measure of service performance delivered to users (e.g., ratio of HTTP POST `/checkout` requests returning $< 500$ within $500\text{ms}$).

### SLO (Service Level Objective)
A target reliability goal set over a specific rolling time window agreed upon between product and engineering (e.g., $99.9\%$ of valid requests meet the SLI over a rolling 30-day window).

### SLA (Service Level Agreement)
An explicit legal or business contract with external customers that specifies consequences, penalties, or financial refunds if reliability falls below a defined threshold.

### Toil
Operational work tied to running a production service that is manual, repetitive, automatable, tactical, lacking enduring engineering value, and scales linearly as the service grows.

### USE Method
A hardware and infrastructure diagnostic framework focusing on **Utilization** (percentage of time resource was busy), **Saturation** (queue depth or work waiting for resource), and **Errors** (hardware or low-level operating system error count).
