# Solution: LAB-28 — Stale Client DNS Caching

---

## 1. Failing Layer
**L7 (DNS Resolver)**

## 2. Root Cause Analysis
The failure occurs because:
> **Lower TTL prior to migration and implement DNS TTL honoring in client.**

When the client initiates communication, the expected protocol interaction fails at the L7 (DNS Resolver) boundary. 

## 3. Diagnostic Trace
Using `dig vs client logs`, we observe the definitive proof of failure:
- **Diagnostic Command**:
  ```bash
  dig vs client logs
  ```
- **Evidence**:
  The output directly confirms that the target endpoint or route cannot be reached or resolved due to a state mismatch.

## 4. Surgical Remediation
To permanently resolve this issue:
```bash
# Remediation:
Lower TTL prior to migration and implement DNS TTL honoring in client.
```

## 5. Production Connection
This incident pattern frequently manifests in production environments:
- **Cloud (AWS/GCP)**: Misconfigured Security Groups, missing VPC route table entries, or incorrect NAT gateways.
- **Containers (Docker/Kubernetes)**: Binding services to `127.0.0.1` inside containers, CNI routing table desynchronization, or kube-proxy iptables rules dropping packets.
- **Microservices**: DNS resolver timeouts, ephemeral port exhaustion during connection spikes, or stale client connection pools.
