# Complete Curriculum Roadmap: 22 Parts · 244 Phases

> **Motto**: Understand it. Instrument it. Measure it. Break it. Detect it. Debug it. Recover it. Automate it. Improve it. Operate it.

---

## The Three Converging Tracks

```text
Track A: Production SRE ──────────────┐
Track B: OpenTelemetry & Observability ┼──► Reliable, Observable, Operable Production Systems
Track C: Platform Engineering ────────┘
```

---

## PART I — PRODUCTION FOUNDATIONS (Phases 00 – 10)
*Focus: Operating system processes, TCP sockets, request lifecycles, and baseline system dynamics without telemetry magic.*

| Phase | Title | Primary Question | Track | Key Artifact |
|:---|:---|:---|:---|:---|
| **00** | Production Laboratory | What does a minimal running service stack look like at the OS layer? | Foundations | `docker-compose.yml`, baseline API & DB |
| **01** | What Does Production Mean? | Why is production different from code running on localhost? | SRE | Production impact taxonomy & guarantees |
| **02** | Development vs Production | What happens when concurrency, state, and partial failure appear? | SRE | 1-req vs 10k-concurrent comparison script |
| **03** | Production Failure Model | What are the 10 fundamental ways production systems fail? | SRE | Systematic failure taxonomy & taxonomy tests |
| **04** | Users Experience Symptoms | Why is database CPU a cause while checkout failure is a symptom? | SRE | Symptom vs Cause diagnostic matrix |
| **05** | Availability | Why is "99% uptime" a dangerous metric if calculated on ping? | SRE | Request-based availability calculation engine |
| **06** | Latency | Why does average latency lie about user experience? | SRE | Latency quantile engine (p50, p95, p99, p99.9) |
| **07** | Throughput | How do we separate request arrival rate from processing capacity? | SRE | Throughput vs concurrency experiment |
| **08** | Saturation | Which resource (CPU, memory, pool, disk) saturates first under load? | SRE | Resource saturation bottleneck hunter |
| **09** | Queueing Dynamics | Why does latency explode non-linearly past 75% utilization? | SRE | M/M/1 and M/M/c queueing simulator |
| **10** | Little's Law | How does dependency latency dictate required service concurrency? | SRE | $L = \lambda W$ validation engine |

---

## PART II — OBSERVABILITY FROM FIRST PRINCIPLES (Phases 11 – 30)
*Focus: Deriving logs, metrics, and traces from scratch before touching vendor tools.*

| Phase | Title | Primary Question | Track | Key Artifact |
|:---|:---|:---|:---|:---|
| **11** | Monitoring vs Observability | Can you debug an unknown-unknown state using static dashboards? | Observability | Interactive debugging scenario |
| **12** | Telemetry Signals | Which question does each signal answer best? | Observability | Signal Selection Framework matrix |
| **13** | Logs From First Principles | Why does `print()` fail in distributed production systems? | Observability | Minimal raw socket log stream |
| **14** | Structured Logging | How do machine-parseable JSON logs transform debugging? | Observability | Standardized JSON schema logger |
| **15** | Log Levels & Volume | When should you use DEBUG vs INFO vs WARN vs ERROR? | Observability | Operational log level filter & cost model |
| **16** | Correlation IDs | How do you track a single request across 5 independent processes? | Observability | HTTP correlation header propagator |
| **17** | Logging Failure Modes | What happens when logging crashes the disk or leaks credentials? | Observability | PII redaction & backpressure log handler |
| **18** | Metrics From First Principles | How do we count events and track rates without storing raw text? | Observability | In-memory atomic metric accumulator |
| **19** | Counters | Why must counters be strictly monotonic? | Observability | Monotonic counter & rate calculation |
| **20** | Gauges | What is safe to measure with a gauge, and what causes race conditions? | Observability | Bounded thread pool & queue gauge |
| **21** | Histograms | How do exponential and linear buckets capture tail latency? | Observability | Cumulative histogram bucket implementation |
| **22** | Metric Labels | How do dimensions add value, and where do they become dangerous? | Observability | Label dimension collector |
| **23** | Metric Cardinality | How does `user_id` cause exponential memory explosion? | Observability | Cardinality explosion simulator & safety guard |
| **24** | The RED Method | How do Rate, Errors, and Duration guide service diagnostics? | Observability | RED metric middleware |
| **25** | The USE Method | How do Utilization, Saturation, and Errors guide host diagnostics? | Observability | USE resource collector for Linux/cgroups |
| **26** | Four Golden Signals | How do Latency, Traffic, Errors, and Saturation synthesize health? | Observability | Golden signals composite health evaluator |
| **27** | Distributed Tracing Motivation | Why do logs fail to reconstruct causal flow across microservices? | Observability | Service chain causal reconstruction challenge |
| **28** | Spans & Hierarchies | What information must a span record to represent an operation? | Observability | Pure Python Span and SpanContext tree |
| **29** | Trace Context Propagation | How does W3C `traceparent` serialize state over HTTP? | Observability | W3C TraceContext parser & injector |
| **30** | The First Distributed Trace | Can we trace client -> gateway -> checkout -> db without third-party tools? | Observability | First-principles distributed trace visualizer |

---

## PART III — OPENTELEMETRY (Phases 31 – 54)
*Focus: Modern OpenTelemetry Specification, SDKs, Stable Semantic Conventions, and Collector pipelines.*

| Phase | Title | Primary Question | Track | Key Artifact |
|:---|:---|:---|:---|:---|
| **31** | Why OpenTelemetry? | What was the vendor lock-in problem before OTel? | Observability | Vendor-neutral architecture blueprint |
| **32** | OpenTelemetry Architecture | What is the strict boundary between API, SDK, and Collector? | Observability | OTel component dependency diagram & test |
| **33** | Resources & Identity | How does a service announce who it is and where it runs? | Observability | Semantic resource builder (`service.name`, etc.) |
| **34** | Instrumentation Scope | Why does telemetry need to identify the library that emitted it? | Observability | InstrumentationScope demonstration |
| **35** | Manual Tracing | How do you create rich domain spans with business context? | Observability | Manual OTel tracer with attributes & span events |
| **36** | Automatic Instrumentation | When does auto-instrumentation save time, and where does it fail? | Observability | Auto vs Manual comparison benchmark |
| **37** | Semantic Conventions Governance | Why is `http.request.method` strictly better than `http.method`? | Observability | Stable v1.26+ convention validation linter |
| **38** | HTTP Conventions | How do client and server spans map network operations? | Observability | HTTP client/server span instrumentor |
| **39** | Database Conventions | How do you trace database queries without leaking secrets? | Observability | Sanitized DB span instrumentor |
| **40** | Messaging Conventions | How do asynchronous queues propagate trace context? | Observability | Producer/Consumer trace linkage |
| **41** | Metrics with OpenTelemetry | How does OTel SDK aggregate counters, gauges, and histograms? | Observability | OTel Meter provider & metric instruments |
| **42** | OpenTelemetry Logs | How does the OTel Log Bridge API attach trace context to log records?| Observability | Trace-correlated JSON logger |
| **43** | Baggage & Context | What is the operational cost and privacy risk of Baggage? | Observability | Baggage propagator & security audit |
| **44** | Trace Sampling Strategies | Why is 100% trace capture unaffordable at scale? | Observability | Head sampler implementation (Ratio, ParentBased) |
| **45** | Tail Sampling | How do you ensure every 500 error trace is retained while dropping 200s? | Observability | Collector tail-based sampling configuration |
| **46** | OTLP Protocol | How does OpenTelemetry Protocol encode data over gRPC and HTTP? | Observability | OTLP Protobuf payload decoder |
| **47** | Collector From First Principles | Why do we need an out-of-process telemetry pipeline? | Observability | Architecture derivation & risk model |
| **48** | Collector Pipelines | How do receivers, processors, and exporters interact? | Observability | `otel-collector-config.yaml` pipeline definition |
| **49** | Collector Receivers | How does the collector accept OTLP, Prometheus, and file inputs? | Observability | Multi-receiver configuration & tests |
| **50** | Collector Processors | How do batching, memory limiter, and attribute redaction protect nodes?| Observability | Production processor chain |
| **51** | Collector Exporters | How do we route metrics to Prometheus and traces to Tempo? | Observability | Multi-backend exporter config |
| **52** | Collector Under Failure | What happens when backends are down? (Queueing vs dropping) | Observability | Downstream outage simulation & queue recovery |
| **53** | Collector Deployment Topologies | Agent vs Gateway vs Hybrid: Which topology fits your scale? | Observability | Topology comparison architecture matrix |
| **54** | Telemetry Pipeline Capacity | How much CPU and memory does observing the system consume? | Observability | Collector stress test & capacity sizing guide |

---

## PART IV — METRICS & PROMETHEUS (Phases 55 – 63)
*Focus: Prometheus TSDB, pull-based scraping, PromQL from first principles, and operational dashboards.*

| Phase | Title | Primary Question | Track | Key Artifact |
|:---|:---|:---|:---|:---|
| **55** | Prometheus Mental Model | How does Prometheus store time series in memory and on disk? | Observability | TSDB chunking and index model |
| **56** | Pull-Based Scraping | Why did Prometheus choose pull over push, and when does pull break? | Observability | Custom `/metrics` scraper |
| **57** | Time Series Representation | How do metric names, label sets, and timestamps form a series? | Observability | Time series matrix visualizer |
| **58** | PromQL Fundamentals | How do instant vectors and range vectors differ in practice? | Observability | PromQL query lab with 20 essential queries |
| **59** | Counter Rates & Extrapolation | Why is `rate()` mandatory, and how does it handle counter resets? | Observability | Counter reset simulation & rate verification |
| **60** | Histograms & Quantiles | Why is `histogram_quantile()` dangerous when buckets are misconfigured?| Observability | Latency percentile calculation lab |
| **61** | Recording Rules | When should you pre-calculate expensive PromQL aggregations? | Observability | `recording-rules.yaml` with SLO precomputations |
| **62** | Dashboard Design | What makes a dashboard an operational tool rather than art? | Observability | Production RED & Golden Signal dashboards |
| **63** | Dashboard Anti-Patterns | Why are 50-panel dashboards with unlabelled units harmful? | Observability | Dashboard refactoring lab & audit checklist |

---

## PART V — ALERTING (Phases 64 – 72)
*Focus: Alert philosophy, symptom-based alerting, Alertmanager routing trees, inhibition, and runbooks.*

| Phase | Title | Primary Question | Track | Key Artifact |
|:---|:---|:---|:---|:---|
| **64** | Why Alert? | What is the true cost of interrupting a human engineer? | SRE | Alert justification framework |
| **65** | Symptom vs Cause Alerting | Why should CPU > 85% rarely page, but error rate always alert? | SRE | Symptom-based alert conversion engine |
| **66** | Alert Actionability | What makes an alert actionable, and when should it be a ticket? | SRE | Actionability rubric & linter |
| **67** | Alertmanager Architecture | How does Alertmanager receive, deduplicate, and route alerts? | SRE | `alertmanager-config.yaml` routing tree |
| **68** | Alert Grouping | How do you turn 500 container crash alerts into 1 notification? | SRE | Grouping policy configuration & simulation |
| **69** | Alert Inhibition | How do you silence downstream alerts when the root network fails? | SRE | Inhibition rule validation lab |
| **70** | Silences & Maintenance | How do you safely suppress alerts during scheduled maintenance? | SRE | Alertmanager silence API automation |
| **71** | Alert Fatigue & Noise Reduction| How do you systematically measure and eliminate alert noise? | SRE | Page volume audit script & tuning lab |
| **72** | Runbooks as Code | What essential sections must every operational runbook contain? | SRE | Standard runbook template & alert links |

---

## PART VI — SLIs, SLOs & ERROR BUDGETS (Phases 73 – 83)
*Focus: Defining user-centric reliability, mathematical error budgets, and multi-window burn-rate alerting.*

| Phase | Title | Primary Question | Track | Key Artifact |
|:---|:---|:---|:---|:---|
| **73** | Reliability as a Product | How do you define reliability in terms of user happiness? | SRE | Critical User Journey mapping template |
| **74** | Service Level Indicators (SLIs) | How do you mathematically express Good Events / Total Events? | SRE | SLI evaluation library |
| **75** | Service Level Objectives (SLOs) | What rolling time windows and targets balance velocity and safety? | SRE | 30-day rolling window SLO calculator |
| **76** | SLO vs SLA | What is the legal/financial difference between internal and external targets?| SRE | SLA penalty vs SLO error budget comparison |
| **77** | Error Budgets | How does an error budget turn reliability into an engineering currency? | SRE | Error budget burn tracker |
| **78** | Burn Rate Intuition | What does a 14.4x burn rate mean in terms of time to outage? | SRE | Burn rate time-to-exhaustion formula |
| **79** | Multi-Window Multi-Burn-Rate | Why do single-window threshold alerts cause false alarms or late pages? | SRE | Production multi-window burn rate alert rules |
| **80** | Setting Realistic SLOs | Why is choosing "five nines" without business justification reckless? | SRE | SLO cost vs capability calculator |
| **81** | Batch & Data Freshness SLOs | How do you measure reliability for background processing systems? | SRE | Batch pipeline freshness SLI engine |
| **82** | Queue & Worker SLOs | How do you measure queue backlog age and consumer throughput? | SRE | Queue delay SLI calculator |
| **83** | SLO Review & Governance | What happens when an error budget is depleted? (Policy enforcement) | SRE | Error budget policy agreement & review script |

---

## PART VII — INCIDENT RESPONSE (Phases 84 – 95)
*Focus: Coordinated incident command, triage, rapid mitigation over root cause, and live simulations.*

| Phase | Title | Primary Question | Track | Key Artifact |
|:---|:---|:---|:---|:---|
| **84** | What Is an Incident? | When does an operational defect warrant declaring a SEV incident? | SRE | Severity matrix & declaration criteria |
| **85** | Incident Roles & Structure | What are the duties of Incident Commander, Ops Lead, and Comms Lead? | SRE | Role cards & incident protocol |
| **86** | Incident Lifecycle | How do you move from detection through stabilization to learning? | SRE | Incident lifecycle state machine |
| **87** | Triage: What Changed? | What are the first 4 diagnostic questions responders must ask? | SRE | Triage playbook & change correlation script |
| **88** | Mitigate Before Root Cause | Why must you roll back or shed traffic before understanding the bug? | SRE | Rapid mitigation decision tree |
| **89** | Incident Communication | How do you write clear, calm, transparent status updates? | SRE | Stakeholder update templates |
| **90** | Timeline Construction | How do you synthesize logs, traces, alerts, and commands into a timeline?| SRE | Automated timeline builder |
| **91** | Incident Simulation I | Can you mitigate a deployment error spike under pressure? | SRE Lab | Live scenario: Broken deploy rollback |
| **92** | Incident Simulation II | Can you identify and relieve database lock contention? | SRE Lab | Live scenario: Row lock exhaustion |
| **93** | Incident Simulation III | Can you detect and bypass a failing upstream DNS/dependency? | SRE Lab | Live scenario: DNS failure & timeout |
| **94** | Incident Simulation IV | Can you recover a system suffering from a cache stampede? | SRE Lab | Live scenario: Redis cache cold start |
| **95** | Incident Simulation V | Can you catch a silent queue backlog before business data is lost? | SRE Lab | Live scenario: Worker thread hang |

---

## PART VIII — POSTMORTEMS (Phases 96 – 100)
*Focus: Blameless postmortem culture, multi-factor causality, and high-leverage corrective actions.*

| Phase | Title | Primary Question | Track | Key Artifact |
|:---|:---|:---|:---|:---|
| **96** | Blameless Systems Thinking | Why is "human error" the beginning of the investigation, not the end? | SRE | Blameless interview guide |
| **97** | Multi-Factor Causality | How do triggers, technical bugs, and organizational conditions align? | SRE | Swiss Cheese model causal mapping |
| **98** | Corrective Actions That Work | Why is "remind engineers to be careful" an ineffective action item? | SRE | Hierarchy of Controls for engineering |
| **99** | Action Item Prioritization | How do you rank remediation work against product feature roadmaps? | SRE | Risk reduction ROI matrix |
| **100** | Recurring Incident Analysis | How do you identify systemic patterns across 20 incident postmortems? | SRE | Incident cluster analysis tool |

---

## PART IX — CAPACITY, SATURATION & OVERLOAD (Phases 101 – 114)
*Focus: Modeling capacity, load testing, connection pooling, queues, circuit breakers, and load shedding.*

| Phase | Title | Primary Question | Track | Key Artifact |
|:---|:---|:---|:---|:---|
| **101** | Capacity Planning Fundamentals | How do you calculate required CPU, memory, and IOPS from RPS? | SRE | Capacity sizing spreadsheet & calculator |
| **102** | Sizing Headroom | Why does operating at 95% capacity guarantee catastrophic failure? | SRE | Safe headroom modeling tool |
| **103** | Load Testing Methodologies | How do you construct realistic load tests with skewed traffic? | SRE | Async load testing engine (`load_generator.py`)|
| **104** | Finding the Saturation Cliff | At what exact concurrency does your service experience latency collapse?| SRE | Saturation curve benchmark runner |
| **105** | Database Connection Pools | What happens when connections are exhausted vs starved? | SRE | Connection pool stress test & tuner |
| **106** | Worker & Thread Pools | How do synchronous worker pools behave when downstream calls block? | SRE | Worker starvation simulation |
| **107** | Queue Backlog Dynamics | How long does it take to drain a queue when arrival rate exceeds capacity?| SRE | Queue drain time calculator |
| **108** | Backpressure | How does a service push back on clients to protect its own stability? | SRE | Backpressure middleware |
| **109** | Load Shedding | Why is returning HTTP 503 to 10% of users better than crashing for 100%? | SRE | Adaptive concurrency limiter / load shedder |
| **110** | Retry Storms & Jitter | How do retries without backoff turn a minor glitch into total collapse?| SRE | Retry storm simulator & exponential backoff |
| **111** | Distributed Timeout Budgets | Why must end-to-end deadlines decrease at each downstream hop? | SRE | Deadline propagation context handler |
| **112** | Circuit Breakers | How does a circuit breaker fail fast to allow dependencies to recover? | SRE | Production circuit breaker state machine |
| **113** | Bulkheads | How do you isolate resources so one failing customer doesn't down the app?| SRE | Bulkhead partition controller |
| **114** | Graceful Degradation | How do you design fallbacks so core journeys succeed without optional features?| SRE | Fallback strategy orchestrator |

---

## PART X — DEPLOYMENT RELIABILITY (Phases 115 – 123)
*Focus: Change management, health probes, graceful shutdown, canaries, and database migrations.*

| Phase | Title | Primary Question | Track | Key Artifact |
|:---|:---|:---|:---|:---|
| **115** | Change as Risk Event | Why are deployments responsible for 70%+ of production incidents? | SRE | Change risk assessment checklist |
| **116** | Health Checks Deep Dive | How do startup, liveness, and readiness probes differ in purpose? | SRE | Deep health probe implementation |
| **117** | Graceful Shutdown | How do you handle `SIGTERM` so zero in-flight requests are dropped? | SRE | Zero-downtime drain and shutdown handler |
| **118** | Rolling Deployments | How does capacity drop during a rolling update, and how do you size for it?| SRE | Rolling rollout capacity analyzer |
| **119** | Automated Rollback | How do you programmatically trigger an image rollback upon error spike?| SRE | Automated deployment health watcher |
| **120** | Canary Deployments | How do you compare error rates between canary and baseline traffic? | SRE | Canary progressive analysis script |
| **121** | Blue/Green Deployments | How do you manage database schema compatibility during blue/green switches?| SRE | Blue/Green router & state compatibility guide |
| **122** | Feature Flags & Blast Radius | How do you decouple code deployment from feature release? | SRE | Minimal feature flag engine with kill-switches |
| **123** | Database Migration Safety | How do you evolve schemas without locks (Expand and Contract pattern)? | SRE | Zero-downtime database migration lab |

---

## PART XI — KUBERNETES IN PRODUCTION (Phases 124 – 136)
*Focus: Operating containerized production workloads, resource limits, OOMs, eviction, and disruption.*

| Phase | Title | Primary Question | Track | Key Artifact |
|:---|:---|:---|:---|:---|
| **124** | Kubernetes as Substrate | What does Kubernetes guarantee, and what does it NOT solve? | Platform | Production cluster operating model |
| **125** | Resource Requests & Limits | How do Linux cgroups enforce CPU throttling and memory limits? | Platform | Resource allocation testing manifests |
| **126** | CPU Throttling in Depth | Why does CFS quota throttling cause high latency even with low CPU usage?| Platform | CPU quota latency experiment |
| **127** | Memory Limits & OOMKilled | What happens inside the Linux kernel when a container exceeds limits? | Platform | Controlled OOM reproduction & inspection |
| **128** | Probe Anti-Patterns | How does a naive liveness probe create an unrecoverable restart loop? | Platform | Deadlock probe failure lab |
| **129** | Horizontal Pod Autoscaling | How does HPA calculate target replicas from custom metrics? | Platform | HPA configuration & metrics pipeline |
| **130** | Autoscaling Lag | Why does traffic spike faster than pods can pull images and start? | Platform | Warm headroom & cold start benchmark |
| **131** | Pod Disruption & Eviction | What happens during node drains and preemptible node termination? | Platform | Node drain disruption test |
| **132** | PodDisruptionBudgets | How do PDBs guarantee minimum availability during cluster maintenance? | Platform | PDB manifest & eviction protection lab |
| **133** | Fault Domains & Topology | How do you prevent all replicas from scheduling on the same rack or zone? | Platform | Topology spread constraints manifest |
| **134** | Operational Use of K8s Events | How do you query Kubernetes events as diagnostic evidence during incidents?| Platform | K8s event correlator script |
| **135** | Kubernetes Observability | How do you correlate container logs, pod metrics, and node stats? | Platform | Kubernetes telemetry correlation guide |
| **136** | OTel Collector on Kubernetes | Should you run the OTel Collector as a DaemonSet, a Sidecar, or a Gateway?| Platform | DaemonSet vs Gateway manifests |

---

## PART XII — RELIABILITY ENGINEERING (Phases 137 – 147)
*Focus: Redundancy, failure domains, critical path analysis, fan-out probability, and disaster recovery.*

| Phase | Title | Primary Question | Track | Key Artifact |
|:---|:---|:---|:---|:---|
| **137** | The Redundancy Fallacy | Why does adding a backup server often double your failure rate? | SRE | Redundancy math & split-brain model |
| **138** | Fault Domains | How do you map blast radius across process, host, rack, zone, and region?| SRE | Failure domain topology mapper |
| **139** | Dependency Availability Math | If a service calls 3 dependencies with 99.9% availability, what is its max?| SRE | Composite availability calculator ($A = \prod A_i$) |
| **140** | Critical Path Identification | Which dependencies can fail without impacting the user checkout? | SRE | Critical path audit script |
| **141** | Fan-Out Tail Latency | Why does calling 30 microservices in parallel guarantee high p99 latency?| SRE | Fan-out tail latency simulation ($1 - (1-p)^N$) |
| **142** | Caching as a Failure Domain | What happens to your database when your cache cluster crashes? | SRE | Cache-loss database load modeling |
| **143** | Replication Lag & Read Replicas| Why does reading from a replica cause silent data inconsistency bugs? | SRE | Read-after-write consistency validator |
| **144** | Disaster Recovery: RPO & RTO | How do you balance business recovery objectives with replication costs?| SRE | RPO/RTO calculation framework |
| **145** | The Backup Restore Drill | Why is an unverified backup simply an untested theory? | SRE | Automated database backup & restore test |
| **146** | Multi-Zone Resilience | How do you survive the loss of an entire cloud availability zone? | SRE | Multi-zone failover simulation |
| **147** | Multi-Region Realities | Why do most companies not need multi-region active-active architectures? | SRE | Multi-region latency & consistency trade-off audit |

---

## PART XIII — CHAOS & FAILURE ENGINEERING (Phases 148 – 157)
*Focus: Controlled failure experiments, hypothesis validation, blast radius control, and emergency aborts.*

| Phase | Title | Primary Question | Track | Key Artifact |
|:---|:---|:---|:---|:---|
| **148** | Why Inject Failure? | Why does happy-path testing fail to reveal recovery behavior? | SRE Lab | Chaos Engineering Principles charter |
| **149** | Process Termination Failure | How quickly does traffic reroute when a worker process receives `SIGKILL`?| SRE Lab | Sudden death failover experiment |
| **150** | Synthetic Dependency Latency | How does adding 200ms delay to payment affect gateway memory? | SRE Lab | Latency injection script (`latency_injector.py`)|
| **151** | Network Packet Loss & Jitter | What happens when 15% of packets are dropped between microservices? | SRE Lab | Safe iptables / tc packet loss experiment |
| **152** | Database Outage & Recovery | How does the API respond when PostgreSQL is temporarily stopped? | SRE Lab | Database partition experiment |
| **153** | Cache Eviction & Stampede | How does the service survive a sudden flush of all cached items? | SRE Lab | Cache stampede chaos test |
| **154** | Ephemeral Disk Exhaustion | How does the application behave when the scratch disk is 100% full? | SRE Lab | Disk full simulation script |
| **155** | CPU Saturation Chaos | How do tail latencies degrade under 100% background CPU burn? | SRE Lab | Controlled CPU stress script (`cpu_burn.py`) |
| **156** | Memory Leak Simulation | How does a gradual memory leak manifest in telemetry before OOM? | SRE Lab | Progressive memory leak script (`memory_leak.py`)|
| **157** | Formal Chaos Experiment Design | How do you author a production-grade chaos experiment with automated aborts?| SRE Lab | Chaos Experiment template & runner |

---

## PART XIV — PRODUCTION READINESS (Phases 158 – 165)
*Focus: Service ownership, dependency inventories, operational documentation, and toil reduction.*

| Phase | Title | Primary Question | Track | Key Artifact |
|:---|:---|:---|:---|:---|
| **158** | Production Readiness Review | How do you assess whether a service is safe to accept real traffic? | SRE | `PRODUCTION_READINESS_TEMPLATE.md` checklist |
| **159** | Operational Ownership | Who fixes this at 3 AM, and do they have the necessary context? | SRE | Service catalog ownership metadata |
| **160** | Dependency Inventory & Tiers | How do you classify Tier 1 vs Tier 3 dependencies? | SRE | Dependency mapping graph |
| **161** | Operational Documentation | What belongs in a production wiki versus an emergency runbook? | SRE | Operational documentation standards |
| **162** | Runbook Automation | How do you turn a 10-step manual runbook into a safe executable script?| SRE | Automated runbook executor |
| **163** | Identifying Operational Toil | What qualifies as toil vs legitimate engineering maintenance? | SRE | Google SRE toil definition & rubric |
| **164** | Toil Measurement & Auditing | How many engineering hours are wasted on repetitive tasks? | SRE | Weekly toil time tracking audit |
| **165** | Automation ROI Analysis | When is it cheaper to automate an operational task versus doing it manually?| SRE | Automation ROI calculation model |

---

## PART XV — PLATFORM ENGINEERING FOUNDATIONS (Phases 166 – 174)
*Focus: Platform as a product, cognitive load reduction, golden paths, platform contracts, and self-service.*

| Phase | Title | Primary Question | Track | Key Artifact |
|:---|:---|:---|:---|:---|
| **166** | Why Platform Engineering? | Why do central DevOps ticket queues become the biggest engineering bottleneck?| Platform | Platform value stream analysis |
| **167** | Platform as a Product | How do you treat internal software engineers as customer personas? | Platform | `PLATFORM_PRODUCT_TEMPLATE.md` document |
| **168** | Platform vs Infrastructure Team| How does a capability provider differ from a sysadmin ticket queue? | Platform | Platform capability operating model |
| **169** | The Platform API Interface | What is the ideal contract between developer intent and infrastructure?| Platform | Platform declarative interface design |
| **170** | True Self-Service | How do developers provision resources without filing an infrastructure ticket?| Platform | Self-service capability blueprint |
| **171** | Golden Paths | How do you make the secure, reliable way the easiest path to follow? | Platform | Golden Path architecture specification |
| **172** | The Escape Hatch Principle | Why must a platform allow teams to break out of opinionated constraints?| Platform | Escape hatch design guidelines |
| **173** | Abstraction Boundaries | How do you hide incidental complexity without hiding fundamental mechanics?| Platform | Platform abstraction leak test |
| **174** | Platform Service Contracts | Exactly what does the platform guarantee versus what the application owns?| Platform | Platform-to-App Service Level Agreement |

---

## PART XVI — BUILDING A MINI PLATFORM (Phases 175 – 188)
*Focus: Building a runnable developer platform from scratch: CLI, templates, CI, deployment, and catalogs.*

| Phase | Title | Primary Question | Track | Key Artifact |
|:---|:---|:---|:---|:---|
| **175** | The Canonical Service Template | What does a production-ready repository scaffold look like? | Platform | Production service template directory |
| **176** | The Service Bootstrap CLI | How can a developer scaffold a new service with one command? | Platform | `platform new-service` CLI tool |
| **177** | The CI Golden Path | How do you standardize linting, security scans, tests, and container builds?| Platform | Reusable GitHub/local CI pipeline template |
| **178** | The Declarative Deployment Spec| How can developers describe their workload in 15 lines of YAML? | Platform | Platform `service.yaml` manifest translator |
| **179** | Default Observability Wiring | How does a new service automatically get OTel, Prometheus, and logs? | Platform | Automated zero-touch telemetry injector |
| **180** | Baseline Paging Alerts | Which default alerts belong in every service, and which must be customized?| Platform | Baseline platform alert generator |
| **181** | The Secret Injection Interface | How do apps receive credentials without committing them to git? | Platform | Platform secret provider interface |
| **182** | Database-as-a-Service Lite | How can developers declare a PostgreSQL database dependency self-service?| Platform | Self-service database provisioner |
| **183** | Queue-as-a-Service Lite | How can developers provision an asynchronous Redis queue on demand? | Platform | Self-service queue provisioner |
| **184** | The Developer Platform Portal | What value does a central developer UI provide over CLI and git? | Platform | Minimal developer portal prototype |
| **185** | The Software Catalog | How do you track 100 microservices, their owners, and their dependencies?| Platform | Declarative software catalog parser |
| **186** | Production Readiness Scorecards | How do you automatically score a service's reliability and compliance? | Platform | Automated readiness scorecard evaluator |
| **187** | Measuring Platform Adoption | How do you prove the platform is actually saving engineering hours? | Platform | Adoption telemetry & metrics collector |
| **188** | Platform User Feedback Loops | How do you systematically interview internal developers to find friction?| Platform | Developer experience survey framework |

---

## PART XVII — DEVELOPER EXPERIENCE (Phases 189 – 194)
*Focus: Measuring and optimizing cognitive load, time to first deploy, local dev environments, and support.*

| Phase | Title | Primary Question | Track | Key Artifact |
|:---|:---|:---|:---|:---|
| **189** | Quantifying Cognitive Load | How many concepts must a junior engineer know to ship an API change? | Platform | Cognitive load concept mapping index |
| **190** | Time to First Deploy (TTFD) | Can a new engineer ship a working endpoint to staging on Day 1? | Platform | TTFD benchmark runner & audit |
| **191** | Reproducible Local Dev | Why does "works on my machine" destroy developer velocity? | Platform | Containerized reproducible dev environment |
| **192** | Ephemeral Preview Environments | How do pull request environments accelerate change validation? | Platform | Ephemeral preview environment lifecycle manager|
| **193** | Task-Oriented Documentation | How do you write platform documentation developers actually read? | Platform | Task-first developer documentation site |
| **194** | Platform Support Burden | Why is high support volume a sign of poor platform design? | Platform | Support ticket categorization & friction audit |

---

## PART XVIII — DELIVERY & CHANGE SAFETY (Phases 195 – 200)
*Focus: CI/CD reliability, deployment metrics, progressive delivery, and automated rollbacks.*

| Phase | Title | Primary Question | Track | Key Artifact |
|:---|:---|:---|:---|:---|
| **195** | CI/CD Pipeline as Production | Why must build and deployment systems have their own SLOs? | Platform | CI/CD pipeline latency and failure monitor |
| **196** | Deployment Frequency vs Safety | Does shipping 20 times a day increase or decrease production risk? | Platform | DORA metrics calculator (DF, LT, CFR, MTTR) |
| **197** | Tracking Change Failure Rate | What percentage of deployments require a rollback, hotfix, or patch? | Platform | Change failure attribution script |
| **198** | Mean Time to Rollback (MTTR) | How long does it take from alert trigger to restored traffic? | Platform | Fast rollback benchmark lab |
| **199** | Progressive Delivery Pipelines | How do you combine feature flags, canaries, and metrics analysis? | Platform | Progressive delivery orchestration script |
| **200** | Automated Rollback Controllers | When should an automated controller abort a rollout without human input?| Platform | Automated metric-driven rollout abort guard |

---

## PART XIX — ADVANCED OBSERVABILITY (Phases 201 – 208)
*Focus: Trace-log correlation, exemplars, profiling, telemetry governance, privacy, and cost.*

| Phase | Title | Primary Question | Track | Key Artifact |
|:---|:---|:---|:---|:---|
| **201** | Trace-to-Log Correlation | How do you jump from a slow span directly to its corresponding logs? | Observability | OTel trace context log correlation engine |
| **202** | Trace-to-Metric Correlation | How do you link a Prometheus latency spike directly to trace samples? | Observability | Trace-to-metric diagnostic workflow |
| **203** | Metrics Exemplars | How do exemplars attach specific trace IDs to Prometheus histograms? | Observability | Prometheus exemplar generator & scraper |
| **204** | Continuous Profiling Concepts | When do metrics and traces fail to identify CPU and memory bottlenecks?| Observability | CPU flamegraph & memory allocation profiler |
| **205** | Telemetry Governance | How do you enforce naming conventions across 50 engineering teams? | Observability | OTel semantic convention validation pipeline |
| **206** | Telemetry Privacy & PII | How do you ensure sensitive credit cards and tokens never hit backends? | Observability | OpenTelemetry regex redaction processor |
| **207** | Telemetry Cost Modeling | How much does sending 100,000 spans/sec cost in storage and network? | Observability | Telemetry cost calculator |
| **208** | Adaptive Sampling Strategies | How do you adjust sample rates dynamically during traffic surges? | Observability | Adaptive collector sampling policy |

---

## PART XX — BROKEN PRODUCTION LABS (Phases 209 – 223)
*Focus: 40+ Hands-on broken production scenarios where the learner investigates, diagnoses, and fixes real defects. Solutions separated in `broken-systems/solutions/`.*

| Phase | Lab ID | Broken Production Condition | Diagnostic Clue |
|:---|:---|:---|:---|
| **209** | Lab 01 | Broken Alert: Constant CPU paging while users are unaffected | CPU alert has no symptom correlation |
| **210** | Lab 02 | Broken Dashboard: 40 graphs on one screen with no diagnostic flow | High cognitive load, no RED/USE hierarchy |
| **211** | Lab 03 | Missing Trace Context: Upstream gateway drops W3C traceparent | Trace waterfalls show disconnected orphan spans |
| **212** | Lab 04 | High Cardinality Metric: `user_id` injected into Prometheus label | Prometheus memory climbs to OOM |
| **213** | Lab 05 | Logging Explosion: DEBUG logging enabled in production exhausts disk | Disk space alert fires; disk I/O saturated |
| **214** | Lab 06 | Collector Overload: Unbounded OTel Collector queue drops traces | `otelcol_processor_dropped_spans` climbs |
| **215** | Lab 07 | Bad SLO: Measuring pod uptime while checkout API is returning 500 | Pod is healthy, but customer experience is failing |
| **216** | Lab 08 | Alert Storm: Single PostgreSQL outage triggers 120 simultaneous pages | Alertmanager lacks grouping and inhibition rules |
| **217** | Lab 09 | Liveness Probe Death Loop: Slow startup causes container restart loop | Container killed before database cache is warm |
| **218** | Lab 10 | Cascading Retry Storm: Client retries overwhelm recovering service | Downstream traffic is 10x normal rate |
| **219** | Lab 11 | Autoscaling Failure: HPA scales API pods but PostgreSQL saturates | Increasing pods increases database lock contention |
| **220** | Lab 12 | Noisy Neighbor: Background report generation starves checkout API | Shared thread pool exhausts memory |
| **221** | Lab 13 | Broken Platform Abstraction: Leaky YAML generator causes pod failure | Generated manifest contains invalid port spec |
| **222** | Lab 14 | Platform Ticket Queue: "Self-service" requires manual approval ticket | Process analysis reveals human gating step |
| **223** | Lab 15-40| Complete Broken Systems Suite (26 additional realistic broken systems)| Full matrix of real-world failures |

---

## PART XXI — PROJECTS (Phases 224 – 235)
*Focus: 12 Substantial, end-to-end engineering projects building real tools, pipelines, platforms, and frameworks.*

| Phase | Project | Project Title & Deliverable | Primary Track |
|:---|:---|:---|:---|
| **224** | Project 01 | **Instrument a Backend Service from Scratch**: Add OTel SDK, logs, metrics, traces | Observability |
| **225** | Project 02 | **Production OTel Collector Pipeline**: Configure routing, batching, filtering | Observability |
| **226** | Project 03 | **Production Observability Dashboard Suite**: Build RED, USE, and Golden Signal views | Observability |
| **227** | Project 04 | **SLO Platform Lite**: Calculate error budgets, burn rates, and evaluate compliance | SRE |
| **228** | Project 05 | **Production Alerting Engine**: Build Prometheus alert rules & Alertmanager routing | SRE |
| **229** | Project 06 | **Interactive Incident Simulator**: Automated failure injection & timeline generator | SRE |
| **230** | Project 07 | **Production Capacity Planner**: Model traffic, compute headroom, and forecast bottlenecks | SRE |
| **231** | Project 08 | **Production Readiness CLI**: Automated linter evaluating PRR checklists | Platform |
| **232** | Project 09 | **Service Bootstrap Platform**: CLI generating production-compliant microservices | Platform |
| **233** | Project 10 | **Internal Developer Platform Lite**: Declarative self-service interface | Platform |
| **234** | Project 11 | **Microservice Software Catalog**: Track service metadata, ownership, and SLO status | Platform |
| **235** | Project 12 | **End-to-End Golden Path**: From `platform new-service` to deployed observable system | Platform |

---

## PART XXII — CAPSTONES (Phases 236 – 243)
*Focus: Comprehensive capstone challenges testing complete production mastery.*

| Phase | Capstone | Capstone Challenge Title |
|:---|:---|:---|
| **236** | Capstone 1 | **The Resilient Production Service**: Multi-tier architecture with full OTel, SLOs, and graceful shutdown |
| **237** | Capstone 2 | **Failure-Driven SRE Challenge**: 8 live failure scenarios tested under real load with postmortems |
| **238** | Capstone 3 | **Kubernetes Production Platform**: Multi-service cluster with HPA, PDBs, Collector DaemonSet, and canaries |
| **239** | Capstone 4 | **The Self-Service Internal Developer Platform**: Declarative developer API for compute, DB, and observability |
| **240** | Capstone 5 | **Platform Product Evaluation**: Measuring TTFD, cognitive load reduction, and developer satisfaction |
| **241** | Capstone 6 | **The Major Outage War Room**: Simulated multi-system SEV-1 incident with incomplete evidence |
| **242** | Capstone 7 | **Enterprise Reliability Program**: Designing a 6-month SRE transformation for a 30-service organization |
| **243** | Final Challenge | **The Staff Production Engineering Challenge**: Complete end-to-end audit, overhaul, and platform construction |
