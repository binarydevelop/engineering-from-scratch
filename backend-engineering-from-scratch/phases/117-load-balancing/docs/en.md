# Lesson 117: Load Balancing

> **Motto**: Load balancing distributes incoming traffic across multiple backend instances to maximize throughput and ensure high availability.

---

## Motto
"Load balancing distributes incoming traffic across multiple backend instances to maximize throughput and ensure high availability."

## Problem
Routing all traffic to a single server instance creates a single point of failure and caps system capacity.

## Prediction
Employing load balancing algorithms (Round Robin, Least Connections, IP Hash) shares traffic fairly across healthy instances.

## Why this matters
Load balancing enables zero-downtime deployments and allows services to scale horizontally to meet demand.

## First principles
Load Balancer -> Health Check -> Distributes requests only to Healthy Replicas (Round Robin / Least Connections).

## Mental model
```text
Clients ──> Load Balancer ──┬──> Instance A (Healthy)
                             ├──> Instance B (Healthy)
                             └──> Instance C (Unhealthy - DROPPED FROM ROTATION)
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Nginx upstream load balancing and AWS Application Load Balancer configurations.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/117-load-balancing/tests/ -v
```

## Inspect it
Observe state directly using operating system, network, or database inspection:
- Inspect raw bytes, socket buffers, or table schemas
- Verify that request transformations match protocol specifications

## Measure it
Quantify latency and resource consumption:
- Measure response latency percentiles (p50, p95, p99)
- Profile memory allocations and database connection usage under load

## Break it
Inject an intentional failure to observe divergence from expected behavior:
- **Failure Injection**: Simulate 3 backend instances; kill Instance B; observe load balancer detects failure and routes 100% of traffic to A and C.
- Execute the experiment script:
```bash
python phases/117-load-balancing/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Verify zero dropped client requests during backend instance failure.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Least Connections algorithm is superior to Round Robin when request processing duration varies significantly.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Sticky Sessions (session affinity) bind users to specific instances, but undermine horizontal scaling and fair distribution.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Active health checks query instances periodically (e.g. every 5s); passive health checks detect failures on live traffic.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. What are the differences between Round Robin and Least Connections load balancing algorithms?
2. How does a load balancer detect and remove an unhealthy backend instance from its active routing pool?
3. Why do 'sticky sessions' make horizontal auto-scaling and rolling deployments difficult?

## What comes next
Having understood load balancing, we next discover its inherent boundaries and transition to **Stateless Backend**.
