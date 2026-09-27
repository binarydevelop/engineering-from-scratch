# Solution: LAB-23 — Untrusted Certificate Authority

---

## 1. Failing Layer
**L5/6 (TLS / PKI)**

## 2. Root Cause Analysis
The failure occurs because:
> **Add internal enterprise Root CA certificate to /etc/ssl/certs.**

When the client initiates communication, the expected protocol interaction fails at the L5/6 (TLS / PKI) boundary. 

## 3. Diagnostic Trace
Using `curl -v / trust store`, we observe the definitive proof of failure:
- **Diagnostic Command**:
  ```bash
  curl -v / trust store
  ```
- **Evidence**:
  The output directly confirms that the target endpoint or route cannot be reached or resolved due to a state mismatch.

## 4. Surgical Remediation
To permanently resolve this issue:
```bash
# Remediation:
Add internal enterprise Root CA certificate to /etc/ssl/certs.
```

## 5. Production Connection
This incident pattern frequently manifests in production environments:
- **Cloud (AWS/GCP)**: Misconfigured Security Groups, missing VPC route table entries, or incorrect NAT gateways.
- **Containers (Docker/Kubernetes)**: Binding services to `127.0.0.1` inside containers, CNI routing table desynchronization, or kube-proxy iptables rules dropping packets.
- **Microservices**: DNS resolver timeouts, ephemeral port exhaustion during connection spikes, or stale client connection pools.
