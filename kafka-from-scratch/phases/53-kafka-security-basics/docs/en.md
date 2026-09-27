# Lesson 53: Kafka Security Basics

## Motto
"An unauthenticated, unencrypted broker on the open internet is a global data leak."

## Problem
By default, Kafka communicates over unencrypted `PLAINTEXT`.
In this mode:
1. Anyone on the network can snoop sensitive payloads (credit cards, passwords) using standard packet capture tools.
2. Anyone can connect and produce garbage to any topic.
3. Anyone can read any topic or delete topics!
How is Kafka secured in production?

## Prediction
What are the three pillars of Kafka security?

## Why this matters
Securing Kafka requires understanding **Authentication** (who you are), **Authorization** (what you can do), and **Encryption** (protecting bytes in transit).

## First principles
* **Encryption in Transit (TLS / SSL):** Encrypts all socket communication between clients and brokers, and between brokers during inter-broker replication.
* **Authentication (SASL):** Verifies client identity.
  * `SASL_SSL` with `SCRAM-SHA-512` (username/password with salted hashes).
  * `mTLS` (Mutual TLS using client certificates).
  * `OAUTHBEARER` (JWT tokens via identity providers like Okta/Keycloak).
* **Authorization (ACLs):** Access Control Lists enforcing fine-grained permissions:
  * *"User Alice has READ permission on Topic orders in Group order-workers."*
  * *"User Bob has WRITE permission on Topic orders."*

## Mental model
```text
Client Connection Request
   │
   ▼
[ 1. TLS Handshake ]        ──► Encrypts wire bytes (Prevents sniffing)
   │
   ▼
[ 2. SASL Authentication ]   ──► Verifies User Identity ("I am service-billing")
   │
   ▼
[ 3. ACL Authorization ]     ──► Checks Permissions: Can "service-billing" WRITE to "orders"?
   ├── YES ──► Request Accepted!
   └── NO  ──► TopicAuthorizationException! (Access Denied)
```

## Build it
See [security_config_inspector.py](../code/security_config_inspector.py).
We inspect the security protocol mappings and ACL definitions.

## Use Kafka
Observe how Kafka maps listener security protocols: `PLAINTEXT`, `SSL`, `SASL_PLAINTEXT`, `SASL_SSL`.

## Inspect it
Check ACL rules using `kafka-acls.sh`.

## Measure it
Measure CPU overhead of TLS encryption (modern CPUs with AES-NI incur < 3% overhead).

## Break it
Attempt to write to an ACL-protected topic with an unauthorized principal; observe `TopicAuthorizationException`.

## Recover it
Grant appropriate topic write permission via `kafka-acls.sh`.

## Modify it
Document standard SASL/SCRAM configuration for enterprise Kafka.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. What is the difference between Authentication (SASL) and Authorization (ACLs)?
2. Why is Mutual TLS (mTLS) popular for service-to-service Kafka security in Kubernetes?

## Guarantees
* TLS guarantees data confidentiality and integrity on the wire.
* ACLs prevent unauthorized data access across tenants.

## Non-guarantees
* Transport TLS does not encrypt data at rest on broker disks (requires storage encryption or envelope payload encryption).

## When to use this
* In all production and staging environments without exception.

## When not to use this
* PLAINTEXT should be strictly restricted to local scratch containers.

## What comes next
In Phase 54, we study Observability: metrics, dashboards, and critical production alerts.
