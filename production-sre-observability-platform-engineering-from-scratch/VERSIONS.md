# Software & Specification Versions

**Generation Date**: 2026-09-25  
**Canonical Repository**: `production-sre-observability-platform-engineering-from-scratch`

---

## 1. Version Governance Philosophy

Production engineering requires strict version discipline. When systems fail, mismatch between specification, API, implementation, and semantic conventions is a leading cause of broken telemetry, missing traces, silent metric dropping, and misrouted alerts.

In this repository, we deliberately categorize every telemetry and infrastructure component into its exact specification tier:

```text
Specification
   ↓ (Abstract protocol & data model definitions)
Semantic Conventions
   ↓ (Stable attribute keys, resource names, units)
API
   ↓ (Language-level interfaces with zero side effects)
SDK / Implementation
   ↓ (In-memory buffering, batching, export engines)
Telemetry Transport
   ↓ (Wire protocol: OTLP/gRPC, OTLP/HTTP, Prometheus Remote Write)
Telemetry Collector
   ↓ (Receivers, Processors, Connectors, Exporters)
Storage & Visualization Engine
     (Prometheus, Alertmanager, Tempo, Jaeger, Loki, Grafana)
```

---

## 2. Pinned Stable Versions

### Operating System & Core Runtimes
| Component | Pinned Version | Status / Notes |
|:---|:---|:---|
| **Python** | `3.11+` (tested on `3.11`, `3.12`, `3.14`) | Primary lab runtime for services, generators, chaos tools, CLI |
| **Docker Engine** | `26.0+` (tested on `29.7.x`) | Local container virtualization |
| **Docker Compose** | `v2.27+` | Local multi-service orchestration (Tier 1 Local Lab) |
| **Kubernetes** | `v1.30+` | Container orchestrator for production operations (Tier 2 Local K8s) |
| **K3d / Kind** | `v5.6+` / `v0.23+` | Reproducible lightweight local Kubernetes runtime |

### OpenTelemetry Ecosystem
| Component | Pinned Version | Tier / Type | Semantic Convention Status |
|:---|:---|:---|:---|
| **OpenTelemetry Specification** | `v1.34.0` | Specification | Stable Core (Traces, Metrics, OTLP). Logs Stable. |
| **OpenTelemetry Semantic Conventions** | `v1.26.0+` | Specification | **STABLE HTTP & DATABASE CONVENTIONS** (v1.26+ migration enforced) |
| **OpenTelemetry Python API** | `1.26.0+` | API | Stable interface |
| **OpenTelemetry Python SDK** | `1.26.0+` | SDK / Implementation | Stable batch processors, OTLP metric/trace exporters |
| **OpenTelemetry Collector Contrib** | `0.104.0+` | Telemetry Pipeline Engine | Production-grade OTLP receiver, memory_limiter, batch, Prometheus exporter |
| **OTLP Protocol** | `v1.3.1` (Protobuf / gRPC & HTTP) | Telemetry Transport | Stable binary and JSON telemetry format |

### Observability Backends & Monitoring
| Component | Pinned Version | Role | Stability / Notes |
|:---|:---|:---|:---|
| **Prometheus** | `v2.53.0+` | Time-Series Metrics Engine | TSDB, PromQL, Alerting evaluation engine |
| **Alertmanager** | `v0.27.0+` | Alert Routing & Deduplication | Grouping, inhibition, routing trees, silence engine |
| **Grafana** | `v11.1.0+` (compatible `v10.4+`) | Visualization & Dashboards | Native Prometheus, Tempo, Loki data sources |
| **Grafana Tempo / Jaeger** | `v2.5.0+` / `v1.57.0+` | Distributed Traces Storage | Native OTLP ingestion, TraceQL, trace visualization |
| **Grafana Loki** | `v3.1.0+` | Log Aggregation Engine | Machine-queryable log streams, LogQL |
| **PostgreSQL** | `16.3-alpine` | Relational State Store | Production ACID database with pg_stat_activity inspection |
| **Redis** | `7.2-alpine` | In-Memory Cache & Message Broker | High-throughput low-latency cache with connection pool metrics |

---

## 3. OpenTelemetry Semantic Conventions Migration Guide

> [!IMPORTANT]
> **Strict Enforcement**: This repository uses modern, stable OpenTelemetry Semantic Conventions (v1.25.0+).  
> All deprecated legacy attribute names have been eliminated from both code and collectors.

### HTTP Conventions (Client & Server)
| Deprecated (v1.20 and earlier) | Modern Stable (v1.26.0+) | Rationale |
|:---|:---|:---|
| `http.method` | `http.request.method` | Distinguishes request attributes from response attributes |
| `http.status_code` | `http.response.status_code` | Eliminates ambiguity between request status and response code |
| `http.target` | `url.path` + `url.query` | Structured URL parsing according to URI RFC specifications |
| `http.scheme` | `url.scheme` | Aligns with standard URL resource attribute schema |
| `http.host` | `server.address` + `server.port` | Disambiguates virtual hosts from network socket bindings |
| `http.client_ip` | `client.address` | Separates network remote IP from application-level proxies |
| `http.route` | `http.route` | **Retained**: Low-cardinality route template (e.g. `/orders/{id}`) |

### Database Conventions
| Deprecated | Modern Stable (v1.26.0+) | Rationale |
|:---|:---|:---|
| `db.type` | `db.system` | Identifies DBMS engine (`postgresql`, `redis`, `mysql`) |
| `db.statement` | `db.query.text` (sanitized) | Emphasizes sanitization of queries to prevent PII/credential leaks |
| `db.user` | `db.namespace` + user attributes | Isolates database tenant/namespace context |

### Resource Attributes
| Attribute | Stable Value Pattern | Example |
|:---|:---|:---|
| `service.name` | RFC 1123 compliant string | `checkout-service` |
| `service.namespace` | Logical domain boundary | `production-ecommerce` |
| `service.version` | SemVer or Git SHA | `1.4.2` |
| `service.instance.id` | Unique UUID or pod name | `checkout-service-7f4b9-8k2p` |
| `deployment.environment` | Runtime stage | `production`, `staging`, `lab-local` |

---

## 4. Signal Stability Matrix

| Signal | OpenTelemetry API | OpenTelemetry SDK | OTLP Export | Collector Status |
|:---|:---|:---|:---|:---|
| **Traces** | Stable | Stable | Stable | Production Ready |
| **Metrics** | Stable | Stable | Stable | Production Ready |
| **Logs** | Stable (Bridge API) | Stable | Stable | Production Ready |
| **Profiles** | Experimental (v0.1) | Experimental | Experimental | Educational Preview (Phase 204) |

---

## 5. Verification Commands

Verify that your local host satisfies these version baselines:

```bash
# Check Python
python3 --version  # Must be >= 3.11

# Check Docker & Docker Compose
docker --version          # Must be >= 26.0
docker compose version    # Must be >= v2.27

# Check Curl
curl --version            # Must support HTTP/1.1 and JSON formatting
```
