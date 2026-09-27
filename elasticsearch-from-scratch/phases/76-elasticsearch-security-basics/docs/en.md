# Lesson 76.1: Elasticsearch Security Basics

## Motto
"Never run Elasticsearch unauthenticated: enforce TLS on transport and HTTP, configure RBAC roles, and use API keys."

## Problem
Over the past decade, tens of thousands of unsecured Elasticsearch clusters with port 9200 exposed were compromised by ransomware bots that wiped indices and left ransom notes.

## Prediction
What happens if you try to bootstrap an Elasticsearch 8.x production cluster on a network interface without configuring TLS on port 9300?

## Why this matters
In Elasticsearch 8.x, **X-Pack Security is mandatory** for production clustering. Transport TLS protects node-to-node communication; HTTP TLS and RBAC protect client endpoints.

## First principles
The Security Triad:
1. **Transport TLS (Port 9300):** Encrypts inter-node cluster communication and authenticates nodes via a trusted Certificate Authority (CA).
2. **HTTP TLS (Port 9200):** Encrypts REST client traffic.
3. **Role-Based Access Control (RBAC):** Users are granted Roles. Roles enforce Index Privileges (read, write, manage) and Cluster Privileges (`monitor`, `manage`).

## Mental model
```text
Client (HTTPS :9200) ──► Basic Auth / API Key ──► Authenticated User
                                                        │
                                        Assigned Role: "catalog_reader"
                                        Privileges: read on "products_*" only
                                                        │
Node-to-Node (:9300) ──► Mutual TLS with CA Certificates (Zero Snooping!)
```

## Build it
See `code/rbac_permission_sim.py` demonstrating RBAC privilege enforcement in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/76-elasticsearch-security-basics/experiments/run_experiment.sh
```

## Inspect it
Create an application role with read-only index privileges:
```bash
curl -X POST http://localhost:9200/_security/role/read_products -H "Content-Type: application/json" -d '{
  "cluster": ["monitor"],
  "indices": [
    {
      "names": ["products_*"],
      "privileges": ["read", "view_index_metadata"]
    }
  ]
}'
```

## Measure it
Inspect TLS handshake latency vs raw plaintext HTTP.

## Break it
Attempt to write to an index using a read-only role: observe `security_exception: action [indices:data/write/index] is unauthorized`.

## Recover it
Grant appropriate write privileges or create dedicated API keys for ingest services.

## Modify it
Generate an API Key for automated backend microservices: `POST /_security/api_key`.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does Elasticsearch 8.x refuse to join a cluster across multiple network interfaces if Transport TLS is disabled?
2. What is the difference between cluster privileges and index privileges?

## Guarantees
* RBAC guarantees that users cannot read or modify indices outside their assigned role permissions.

## Non-guarantees
* Security features cannot protect against someone possessing the `elastic` superuser password.

## When to use this
* Every staging and production deployment without exception.

## When not to use this
* Isolated, single-node offline unit test runners.

## What comes next
In Phase 77, we establish Observability and metrics monitoring.
