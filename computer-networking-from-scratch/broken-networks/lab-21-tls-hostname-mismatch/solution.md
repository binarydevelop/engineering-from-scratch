# Solution: LAB-21 — TLS Hostname Mismatch

---

## 1. Failing Layer
**L5/6 (TLS)**

## 2. Root Cause Analysis
The failure occurs because:
> **Regenerate certificate with correct Subject Alternative Name (SAN).**

When the client initiates communication, the expected protocol interaction fails at the L5/6 (TLS) boundary. 

## 3. Diagnostic Trace
Using `openssl s_client`, we observe the definitive proof of failure:
- **Diagnostic Command**:
  ```bash
  openssl s_client
  ```
- **Evidence**:
  The output directly confirms that the target endpoint or route cannot be reached or resolved due to a state mismatch.

## 4. Surgical Remediation
To permanently resolve this issue:
```bash
# Remediation:
Regenerate certificate with correct Subject Alternative Name (SAN).
```

## 5. Production Connection
This incident pattern frequently manifests in production environments:
- **Cloud (AWS/GCP)**: Misconfigured Security Groups, missing VPC route table entries, or incorrect NAT gateways.
- **Containers (Docker/Kubernetes)**: Binding services to `127.0.0.1` inside containers, CNI routing table desynchronization, or kube-proxy iptables rules dropping packets.
- **Microservices**: DNS resolver timeouts, ephemeral port exhaustion during connection spikes, or stale client connection pools.
