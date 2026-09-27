# Lesson 169: Debugging Lab: DNS Failure

> **Motto**: Diagnosing external dependency outages caused by DNS resolution failures differentiates network drops from DNS crashes.

---

## Motto
"Diagnosing external dependency outages caused by DNS resolution failures differentiates network drops from DNS crashes."

## Problem
An API suddenly fails when calling a payment provider; error logs report `getaddrinfo failed: Name or service not known`.

## Prediction
Using `dig`, `nslookup`, and `/etc/resolv.conf` inspection isolates DNS server unreachability or expired domain records.

## Why this matters
Understanding DNS resolution failure paths prevents misdiagnosing DNS outages as application code bugs.

## First principles
App calls `api.stripe.com` -> OS queries DNS resolver -> Resolver unreachable / NXDOMAIN -> App raises SocketError.

## Mental model
```text
Outbound Call -> OS calls getaddrinfo() -> DNS Timeout / NXDOMAIN -> Connection fails before TCP handshake even starts!
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Linux DNS resolution diagnostics (`dig`, `resolvectl`) and application DNS caching.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/169-debugging-lab-dns-failure/tests/ -v
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
- **Failure Injection**: Simulate DNS failure by pointing resolver to an invalid IP; attempt external API call; observe immediate resolution error.
- Execute the experiment script:
```bash
python phases/169-debugging-lab-dns-failure/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Diagnose with `dig`; inspect `/etc/resolv.conf`; restore DNS configuration; verify external connectivity recovers.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Python's `socket.getaddrinfo()` is blocking and performs DNS resolution synchronously; high DNS latency spikes API latency.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Use local caching DNS resolvers (e.g. `systemd-resolved`, `dnsmasq`) to avoid repeated network DNS roundtrips per request.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Configure external dependency fallback IPs or secondary DNS nameservers to maintain resilience during provider DNS outages.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. What is the operational meaning of a `getaddrinfo failed` error in application logs?
2. How do you use the `dig` command to determine whether a DNS resolution failure is caused by an invalid record versus an unreachable nameserver?
3. Why can DNS resolution latency directly degrade backend API response times?

## What comes next
Having understood debugging lab: dns failure, we next discover its inherent boundaries and transition to **Broken Backend Lab Set**.
