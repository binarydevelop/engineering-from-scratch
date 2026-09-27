# The 200+ Production Engineering Exercises Catalog

> **Motto**: Understand it. Instrument it. Measure it. Break it. Detect it. Debug it. Recover it. Automate it. Improve it. Operate it.

---

## Overview

This document catalogues the **200+ practical, hands-on engineering exercises** embedded throughout the curriculum. Every exercise requires running real commands, gathering empirical telemetry, formulating hypotheses, or writing code.

---

## 1. Production Fundamentals (Exercises 1 – 20)
1. **Socket Inspection**: Use `ss -tlpn` to inspect the listening socket state of `api-gateway`.
2. **File Descriptor Limits**: Query `ulimit -n` and calculate the maximum concurrent TCP connections supported.
3. **TCP Listen Backlog**: Inspect `/proc/sys/net/core/somaxconn` and verify socket queue behavior.
4. **Process Memory Allocation**: Measure RSS vs VZ memory consumption for a Python web worker.
5. **Stateful Container Restarts**: Stop PostgreSQL, verify that data volume mounts persist state across restarts.
6. **Contention Benchmark**: Run 1 sequential request vs 50 concurrent requests; plot p99 latency degradation.
7. **Failure Domain Audit**: Map the 10 failure domains for the baseline `checkout-service`.
8. **Symptom vs Cause Matrix**: Given 10 operational metrics, categorize each as a symptom or a cause.
9. **Request Availability Math**: Given 2,450,000 requests with 3,120 errors, compute exact percentage availability.
10. **Ping vs Request Test**: Drop database connection; show that ping succeeds while requests fail with HTTP 500.
11. **Skewed Latency Simulation**: Generate 990 fast requests (10ms) and 10 slow requests (2,000ms); compare mean vs p99.
12. **Bimodal Latency Distribution**: Construct a workload with cache hits vs cache misses; plot the bimodal histogram.
13. **Throughput Limit Identification**: Increase RPS until throughput plateaus; record the saturation point.
14. **First Bottleneck Hunt**: Run CPU burn while measuring database IOPS; identify which resource caps throughput.
15. **Queueing Latency Cliff**: Use Kingman's formula to calculate expected wait time at 50%, 75%, 90%, and 99% utilization.
16. **M/M/1 Queue Simulator**: Run the Python queue simulation; verify that queue length diverges asymptotically.
17. **Little's Law Validation**: Measure arrival rate $\lambda$ and latency $W$; prove that concurrency $L = \lambda W$.
18. **Dependency Latency Domino**: Double mock payment latency from 50ms to 100ms; observe concurrency doubling.
19. **Connection Pool Starvation**: Size connection pool to 5; send 25 concurrent requests; observe wait timeouts.
20. **Headroom Buffer Sizing**: Calculate required cluster capacity for 5,000 peak RPS with 40% headroom.

---

## 2. Logs & Structured Logging (Exercises 21 – 35)
21. **Raw Print Failure**: Emit 1,000 concurrent `print()` lines; observe stdout character interleaving.
22. **JSON Log Schema**: Implement a Python logging formatter emitting ISO-8601 timestamps and service identity.
23. **Log Level Operational Filter**: Configure log filters so DEBUG statements are dropped in production.
24. **Dynamic Log Level Elevation**: Send an HTTP POST to `/admin/log-level` to toggle DEBUG for 5 minutes.
25. **Correlation ID Generation**: Generate a UUID4 correlation ID at the API gateway and forward it in headers.
26. **Cross-Service Log Correlation**: Trace an order across 3 service logs using only `grep [correlation_id]`.
27. **PII Regex Redactor**: Write a log filter that scrubs 16-digit credit card numbers from error logs.
28. **Authorization Token Masking**: Scrub `Bearer eyJ...` tokens from outgoing request logs.
29. **Disk Saturation via Logging**: Generate 50,000 debug logs/second; measure scratch disk write bandwidth.
30. **Log Rotation Enforcement**: Configure Docker container log rotation to limit log files to 3x 50MB.
31. **Machine Parsing with jq**: Query structured JSON logs using `jq 'select(.level=="ERROR") | .message'`.
32. **Exception Stack Trace Formatting**: Serialize full Python exception tracebacks into a single JSON field.
33. **Log Sampling Implementation**: Implement a logger that emits 100% of ERROR logs but samples INFO logs at 10%.
34. **Contextvars Async Logger**: Use Python `contextvars` to maintain correlation IDs across async `await` points.
35. **Log Backpressure Handler**: Implement a non-blocking queue logger that drops debug logs when buffer fills.

---

## 3. Metrics & Time Series (Exercises 36 – 50)
36. **Monotonic Counter Implementation**: Build a thread-safe Counter class; reject negative increments.
37. **Rate Extrapolation Math**: Simulate counter samples $(t_0=0, v=100)$ and $(t_1=60, v=700)$; calculate per-second rate.
38. **Counter Reset Recovery**: Simulate counter reset $(t_0=60, v=1000)$ -> $(t_1=120, v=50)$; compute correct rate.
39. **Thread-Safe Gauge**: Build a Gauge tracking active in-flight HTTP requests using `inc()` and `dec()`.
40. **Queue Backlog Gauge**: Instrument an in-memory queue to export current item count on scrape.
41. **Cumulative Histogram Buckets**: Implement histogram buckets (`0.01`, `0.05`, `0.1`, `0.5`, `1.0`, `+Inf`).
42. **Prometheus Text Serializer**: Format counters and histograms into valid Prometheus exposition syntax.
43. **Metric Label Dimensioning**: Add `method`, `route`, and `status` labels to `http_requests_total`.
44. **Cardinality Explosion Reproduction**: Inject randomized `user_id` into metric labels; measure memory growth.
45. **Cardinality Safety Guard**: Write a wrapper that rejects label values with high cardinality or UUID patterns.
46. **RED Middleware**: Build an ASGI middleware calculating Rate, Errors, and Duration for FastAPI.
47. **USE Resource Monitor**: Write a Python script querying `/proc/stat` and `/proc/meminfo` for USE metrics.
48. **Golden Signals Composite**: Compute a health score (0–100) combining Latency, Traffic, Errors, and Saturation.
49. **Prometheus Scraping Test**: Start Prometheus; scrape `/metrics` endpoint every 5 seconds.
50. **Instant Vector vs Range Vector**: Execute PromQL queries demonstrating instant vs range vector syntax.

---

## 4. Distributed Tracing & W3C Context (Exercises 51 – 65)
51. **Span Data Structure**: Build a Span class recording `trace_id`, `span_id`, start/end times, and attributes.
52. **Parent-Child Span Trees**: Create a root span with two child spans; verify `parent_span_id` linkage.
53. **W3C Traceparent Formatter**: Serialize a SpanContext into `00-{trace_id}-{span_id}-01`.
54. **W3C Traceparent Parser**: Parse incoming `traceparent` headers into trace and span identifiers.
55. **Tracecontext Extraction**: Extract parent context from incoming HTTP headers and resume trace.
56. **Async Span Propagation**: Propagate span context across Python `asyncio.create_task()` boundaries.
57. **Span Attributes Instrumentation**: Add `http.request.method` and `url.path` attributes to a span.
58. **Span Error Status Recording**: Catch an exception in business logic; set span status to `ERROR` with traceback.
59. **Span Events**: Record timed span events (`cache_miss`, `db_connection_acquired`) within an operation.
60. **Tracing Database Operations**: Wrap an SQL query in a child span with `db.system="postgresql"`.
61. **Tracing Queue Enqueue/Dequeue**: Trace a message from publisher to consumer via message headers.
62. **Trace Waterfall Visualizer**: Write an ASCII tree printer rendering trace span timelines in the terminal.
63. **Clock Drift Impact**: Simulate 200ms host clock skew; observe distorted span parent-child durations.
64. **Context Baggage Injection**: Inject tenant metadata into OTel Baggage; read it 3 hops downstream.
65. **Baggage Security Audit**: Verify that sensitive authorization tokens are never leaked into Baggage headers.

---

## 5. OpenTelemetry SDK & Collector (Exercises 66 – 85)
66. **Resource Creation**: Initialize an OTel Resource with `service.name`, `service.version`, and `environment`.
67. **TracerProvider Setup**: Configure global TracerProvider with BatchSpanProcessor.
68. **MeterProvider Setup**: Configure global MeterProvider with PeriodicExportingMetricReader.
69. **OTLP gRPC Export**: Configure OTLPSpanExporter targeting `localhost:4317`.
70. **Console Exporter Fallback**: Implement graceful fallback to ConsoleSpanExporter when collector is unreachable.
71. **Collector Architecture Review**: Map out the Receiver -> Processor -> Exporter pipeline.
72. **Collector Memory Limiter**: Configure `memory_limiter` processor with 75% limit and 20% spike threshold.
73. **Batch Processor Tuning**: Benchmark batch timeouts of 100ms vs 1000ms on collector CPU utilization.
74. **Transform Processor Redaction**: Write OTTL statements to redact credit card numbers in span attributes.
75. **Multi-Backend Routing**: Configure collector to route metrics to Prometheus and traces to Tempo.
76. **Collector Stress Test**: Send 10,000 spans/second to collector; measure process memory and dropped spans.
77. **Collector Queue Exhaustion**: Stop Tempo backend; observe collector `queued_retry` buffer filling.
78. **Tail-Based Sampling Rule**: Configure collector to sample 100% of error spans and 1% of success spans.
79. **Head Sampling Benchmark**: Measure CPU savings of 10% head sampling vs 100% sampling in application.
80. **Collector Health Probe**: Query collector `/ready` endpoint on port 13133.
81. **Collector Internal Telemetry**: Scrape collector Prometheus metrics on port 8888.
82. **OTLP HTTP Receiver**: Test trace ingestion via `POST http://localhost:4318/v1/traces` with curl.
83. **Semantic Conventions Validation**: Write a test verifying that no deprecated OTel attribute keys exist.
84. **Database Query Sanitization**: Verify that raw SQL parameters are replaced with bind variables in spans.
85. **Collector Container Hardening**: Configure non-root user and read-only rootfs for the OTel Collector.

---

## 6. Prometheus & PromQL (Exercises 86 – 105)
86. **Scrape Config Configuration**: Configure `prometheus.yml` to scrape 5 distinct microservice targets.
87. **PromQL Error Rate Calculation**: Write PromQL query calculating percentage of 5xx errors over 5m.
88. **PromQL Quantile Calculation**: Compute p95 and p99 latency across all routes using `histogram_quantile`.
89. **Label Filtering & Regex**: Query metrics filtering by `service=~"checkout.*"` and `status!~"2.."`.
90. **Counter Reset Demonstration**: Restart an API container; verify that `rate()` handles the drop seamlessly.
91. **PromQL Rate Extrapolation**: Compare `rate(metric[1m])` vs `rate(metric[5m])` under bursty traffic.
92. **PromQL Aggregations**: Calculate total cluster RPS using `sum(rate(http_requests_total[1m])) by (service)`.
93. **USE Metric Queries**: Write PromQL queries for connection pool saturation and queue depth.
94. **Recording Rule Authoring**: Precompute p99 latency into `job:request_latency:p99` recording rule.
95. **Rule Syntax Validation**: Validate Prometheus rules using `promtool check rules alerts/prometheus-rules.yaml`.
96. **TSDB Block Inspection**: Inspect Prometheus data directory structure (`chunks_head`, `wal`, block dirs).
97. **Grafana Data Source Wiring**: Provision Prometheus as default datasource in Grafana programmatically.
98. **RED Dashboard Construction**: Build a Grafana dashboard with Rate, Error Rate, and Duration panels.
99. **Dashboard Unit Configuration**: Set panel display units to `req/sec`, `percent (0-100)`, and `milliseconds`.
100. **Dashboard Template Variables**: Add a `$service` dropdown variable filtering panels dynamically.
101. **USE Resource Dashboard**: Build a Grafana dashboard displaying database connection pool saturation %.
102. **Alert State Inspection**: Query Prometheus `/api/v1/alerts` to check firing and pending rules.
103. **Prometheus Head Chunk Compaction**: Force TSDB compaction via admin API (`POST /api/v1/admin/tsdb/clean_tombstones`).
104. **Prometheus Memory Sizing**: Calculate required RAM: `Series * (2 Bytes/sample) * Scrapes/Hour`.
105. **Prometheus High Availability**: Configure two redundant Prometheus instances scraping the same targets.

---

## 7. Alerting & Alertmanager (Exercises 106 – 120)
106. **Symptom Alert Rule**: Write an alert rule firing when checkout error rate > 1% for 2 minutes.
107. **Tail Latency Alert Rule**: Write an alert firing when p99 latency exceeds 500ms for 3 minutes.
108. **Alert Severity Labeling**: Assign `severity="critical"` (pager) vs `severity="warning"` (slack) labels.
109. **Runbook URL Linking**: Embed validated Markdown runbook links into alert annotations.
110. **Alertmanager Routing Tree**: Configure Alertmanager to route critical alerts to PagerDuty mock.
111. **Alert Grouping Policy**: Group alerts by `['alertname', 'service']` with `group_wait: 10s`.
112. **Alert Inhibition Rule**: Write an inhibition rule suppressing downstream service alerts when DB is down.
113. **Maintenance Silence Creation**: Use Alertmanager API to silence warnings during a 1-hour maintenance window.
114. **Silence Verification**: Trigger a simulated warning; verify that Alertmanager suppresses the notification.
115. **Alert Flapping Prevention**: Add `for: 2m` hold window to prevent an alert flapping on transient spikes.
116. **Alertmanager Webhook Mock**: Set up a local HTTP receiver to inspect Alertmanager webhook JSON payloads.
117. **Notification Template Authoring**: Customize Alertmanager text template to show user impact and runbook.
118. **Page Volume Audit**: Write a script analyzing firing alert counts to identify top noisy alerts.
119. **De-escalation Policy**: Configure Alertmanager to re-notify every 4 hours if critical alert remains firing.
120. **Runbook Triage Verification**: Follow an alert's runbook step-by-step during a simulated incident.

---

## 8. SLIs, SLOs & Error Budgets (Exercises 121 – 135)
121. **Critical User Journey Definition**: Map out the steps of the customer checkout user journey.
122. **SLI Specification**: Express the checkout availability SLI as a mathematical equation.
123. **Good/Total Event Counter**: Instrument `checkout-service` with `slo_good_events_total` and `slo_total_events_total`.
124. **Rolling Window Calculation**: Compute 30-day rolling SLI compliance using PromQL `increase()`.
125. **Error Budget Calculation**: Calculate allowable failures for 5,000,000 requests under a 99.9% SLO.
126. **Consumed Budget Tracking**: Calculate percentage of error budget consumed when 2,500 requests fail.
127. **Burn Rate Math**: Given a 2% error rate on a 99.9% SLO ($0.1\%$ allowable), calculate the burn rate (20x).
128. **14.4x Burn Rate Alert**: Write PromQL for a 1-hour critical burn rate alert with 5-minute short window check.
129. **6.0x Burn Rate Alert**: Write PromQL for a 6-hour warning burn rate alert with 30-minute short window check.
130. **1.0x Burn Rate Alert**: Write PromQL for a 3-day ticket burn rate alert with 2-hour short window check.
131. **SLO Dashboard Construction**: Build a Grafana dashboard showing compliance %, burn rate, and remaining budget.
132. **Batch Pipeline SLI**: Build an SLI measuring data warehouse sync freshness ($\le 24\text{ hours}$).
133. **Queue Processing SLI**: Build an SLI measuring consumer lag age ($\le 30\text{ seconds}$).
134. **Error Budget Depletion Simulation**: Run `load-tests/load_generator.py` with faults until budget reaches 0%.
135. **Error Budget Policy Drill**: Execute an error budget freeze: block new features and schedule reliability sprint.

---

## 9. Incident Response & War Rooms (Exercises 136 – 150)
136. **Incident Declaration Protocol**: Practice declaring a SEV-1 incident in Slack and opening a war room.
137. **Role Assignment Drill**: Assign Incident Commander, Operations Lead, and Communications Lead.
138. **First Triage Questions**: Execute the 4 immediate triage checks within 3 minutes of an alert page.
139. **Mitigate First Drill**: Execute an immediate image rollback before diagnosing the root cause.
140. **Status Page Communication**: Draft an external status update describing customer impact without speculation.
141. **Incident Timeline Construction**: Reconstruct a timestamped incident timeline from metrics, logs, and git commits.
142. **Simulated Deployment Outage**: Triage and mitigate a 28% error spike caused by a bad code release.
143. **Simulated Row Lock Outage**: Query `pg_stat_activity`, locate blocking PID, and terminate it.
144. **Simulated DNS Failure**: Detect DNS timeout in trace waterfalls; switch to fallback endpoint.
145. **Simulated Cache Stampede**: Detect DB CPU saturation; warm Redis cache and restore service.
146. **Simulated Queue Starvation**: Detect consumer lag climb; restart stalled worker process.
147. **War Room Communication Hygiene**: Practice strict verbal command protocols during a simulated outage.
148. **Incident Handover Drill**: Practice handing over Incident Commander baton to the next shift lead.
149. **Post-Incident Stabilization**: Verify that error rate remains $< 0.05\%$ for 30 consecutive minutes.
150. **Blameless Postmortem Drafting**: Author a complete postmortem using `POSTMORTEM_TEMPLATE.md`.

---

## 10. Capacity, Queues & Overload (Exercises 151 – 165)
151. **Peak Traffic Forecasting**: Given 1,000 baseline RPS with 20% monthly growth, forecast peak RPS in 6 months.
152. **Headroom Buffer Sizing**: Calculate required compute cores for 4,000 RPS operating at 60% max utilization.
153. **Load Test Ramp-Up**: Run load test ramping from 10 RPS to 200 RPS; identify the exact saturation point.
154. **Latency Percentile Analysis**: Extract p50, p90, p95, p99, and p99.9 latency from load test output.
155. **Database Pool Saturation**: Satiate PostgreSQL pool slots; observe request queueing and client timeouts.
156. **Bounded Connection Acquisition Timeout**: Implement 250ms connection acquisition timeout in database client.
157. **Worker Thread Starvation**: Block 10 worker threads with synchronous sleep; observe queue backup.
158. **Queue Drain Time Math**: Calculate drain time for 100,000 messages arriving at 500/s processed at 400/s.
159. **Backpressure Implementation**: Implement an HTTP 429 Too Many Requests response when concurrency exceeds 100.
160. **Adaptive Concurrency Limiter**: Implement Little's Law based dynamic concurrency limit adjusting to latency.
161. **Exponential Backoff Simulator**: Implement retry loop with exponential backoff and randomized full jitter.
162. **Retry Storm Amplification**: Simulate 500 clients retrying without backoff; plot traffic multiplication curve.
163. **Distributed Deadline Budgeting**: Decrement request deadline at each microservice hop; abort expired requests.
164. **Circuit Breaker State Machine**: Build a circuit breaker with CLOSED, OPEN, and HALF-OPEN states.
165. **Bulkhead Resource Isolation**: Partition thread pools so background jobs cannot starve checkout threads.

---

## 11. Deployment Safety & Kubernetes (Exercises 166 – 180)
166. **Readiness Probe Deepening**: Implement a `/ready` probe that verifies database pool health.
167. **Liveness Probe Isolation**: Ensure `/healthz` only checks local event loop health, not downstream services.
168. **Startup Probe Configuration**: Configure `startupProbe` allowing 30s for database cache pre-warming.
169. **Graceful SIGTERM Handling**: Register SIGTERM signal handler; drain active sockets before process exit.
170. **Rolling Update Capacity Sizing**: Sizing replica counts during rolling updates (`maxSurge: 1`, `maxUnavailable: 0`).
171. **Canary Progressive Analysis**: Route 5% traffic to canary; query Prometheus comparing error rates.
172. **Automated Rollback Script**: Write a script that checks canary error rate and executes rollback if $> 0.5\%$.
173. **Database Expand-and-Contract**: Execute a 5-stage zero-downtime database column migration.
174. **CFS Quota Throttling Inspection**: Inspect `/sys/fs/cgroup/cpu/cpu.stat` for `nr_throttled` count.
175. **OOMKilled Reproduction**: Allocate memory exceeding cgroup limit; inspect kernel `dmesg` for OOM event.
176. **HPA Configuration**: Configure Horizontal Pod Autoscaler targeting 60% average CPU utilization.
177. **Autoscaling Lag Measurement**: Measure time from traffic spike to new pod accepting live traffic.
178. **PodDisruptionBudget Protection**: Configure PDB with `minAvailable: 2`; attempt node drain.
179. **TopologySpreadConstraints**: Configure pod anti-affinity across availability zones.
180. **Kubernetes Event Auditing**: Use `kubectl get events --sort-by=.metadata.creationTimestamp` during incident.

---

## 12. Chaos Engineering (Exercises 181 – 195)
181. **Chaos Experiment Authoring**: Write an experiment plan with hypothesis, blast radius, and abort conditions.
182. **Process Termination Chaos**: Kill worker process with `SIGKILL`; verify automated container restart.
183. **Synthetic Latency Injection**: Inject 1,500ms delay into payment service; observe circuit breaker tripping.
184. **Packet Loss Simulation**: Simulate 10% packet drop; observe TCP retransmissions and latency inflation.
185. **Database Partition Chaos**: Stop PostgreSQL; verify that API Gateway returns HTTP 503 instead of crashing.
186. **Cache Flush Chaos**: Flush Redis cache under load; observe database connection pool response.
187. **Disk Space Exhaustion**: Allocate sparse file filling scratch disk; observe logging failure behavior.
188. **CPU Saturation Chaos**: Run 100% CPU burn across all cores; observe impact on p99 histogram buckets.
189. **Progressive Memory Leak**: Leak 20MB/s; track memory working set until alert fires before OOM.
190. **Emergency Abort Verification**: Trigger chaos script and execute emergency stop; verify instant recovery.
191. **DNS Resolution Blackout**: Block DNS UDP port 53; observe client timeout cascade.
192. **Cascading Failure Chaos**: Inject latency into Service C; observe whether Service A and B isolate the failure.
193. **Automated Abort Controller**: Build a background watchdog that aborts chaos if error rate $> 25\%$.
194. **Post-Chaos State Validation**: Run test suite after chaos experiment to prove zero corrupted state.
195. **GameDay Simulation**: Execute a scheduled 2-hour GameDay with unannounced failure injections.

---

## 13. Platform Engineering & Golden Paths (Exercises 196 – 210)
196. **Golden Path Service Scaffolding**: Run `platform new-service`; verify that generated code compiles and tests pass.
197. **Declarative Manifest Generation**: Run `platform generate-manifests`; translate `service.yaml` to K8s Deployment.
198. **Production Readiness Scorecard**: Run `platform scorecard`; audit service directory against PRR checklist.
199. **Software Catalog Registration**: Register a new service in `platform/catalog/services.yaml`.
200. **Self-Service Database Provisioning**: Declare PostgreSQL dependency in `service.yaml`; verify credential injection.
201. **Zero-Touch Telemetry Verification**: Verify that a bootstrapped service automatically exports RED metrics.
202. **Default Alert Provisioning**: Generate baseline Prometheus alert rules automatically from service metadata.
203. **Platform Escape Hatch Test**: Eject manifests using `platform eject`; verify custom container build works.
204. **Cognitive Load Concept Count**: Count required infrastructure concepts before and after platform adoption.
205. **Time to First Deploy Benchmark**: Measure time required to take a new service from idea to running in staging.
206. **CI Golden Path Pipeline**: Build a reusable CI pipeline running linter, unit tests, and security CVE scans.
207. **Developer Support Ticket Audit**: Categorize 20 developer support tickets to identify platform friction points.
208. **Task-Oriented Documentation**: Write a 1-page guide: *"How to add a Redis cache to your microservice"*.
209. **Developer NPS Survey**: Draft a 5-question Developer Experience survey measuring platform satisfaction.
210. **The Staff Production Transformation Plan**: Author the executive roadmap for Phase 243.
