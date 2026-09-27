# Solution: LAB-16 — Reverse Proxy 502 Bad Gateway

---

## 1. Failing Layer
**L7 (Proxy / Upstream)**

## 2. Root Cause Analysis
The failure occurs because:
> **Fix backend process crash or verify proxy upstream IP:port.**

When the client initiates communication, the expected protocol interaction fails at the L7 (Proxy / Upstream) boundary. 

## 3. Diagnostic Trace
Using `proxy error logs / ss`, we observe the definitive proof of failure:
- **Diagnostic Command**:
  ```bash
  proxy error logs / ss
  ```
- **Evidence**:
  The output directly confirms that the target endpoint or route cannot be reached or resolved due to a state mismatch.

## 4. Surgical Remediation
To permanently resolve this issue:
```bash
# Remediation:
Fix backend process crash or verify proxy upstream IP:port.
```

## 5. Production Connection
This incident pattern frequently manifests in production environments:
- **Cloud (AWS/GCP)**: Misconfigured Security Groups, missing VPC route table entries, or incorrect NAT gateways.
- **Containers (Docker/Kubernetes)**: Binding services to `127.0.0.1` inside containers, CNI routing table desynchronization, or kube-proxy iptables rules dropping packets.
- **Microservices**: DNS resolver timeouts, ephemeral port exhaustion during connection spikes, or stale client connection pools.
