# Solution: LAB-18 — Unhealthy Load Balancer Backend

---

## 1. Failing Layer
**L7 (Load Balancing)**

## 2. Root Cause Analysis
The failure occurs because:
> **Enable active synthetic health check probes to evict dead node.**

When the client initiates communication, the expected protocol interaction fails at the L7 (Load Balancing) boundary. 

## 3. Diagnostic Trace
Using `lb metrics / access log`, we observe the definitive proof of failure:
- **Diagnostic Command**:
  ```bash
  lb metrics / access log
  ```
- **Evidence**:
  The output directly confirms that the target endpoint or route cannot be reached or resolved due to a state mismatch.

## 4. Surgical Remediation
To permanently resolve this issue:
```bash
# Remediation:
Enable active synthetic health check probes to evict dead node.
```

## 5. Production Connection
This incident pattern frequently manifests in production environments:
- **Cloud (AWS/GCP)**: Misconfigured Security Groups, missing VPC route table entries, or incorrect NAT gateways.
- **Containers (Docker/Kubernetes)**: Binding services to `127.0.0.1` inside containers, CNI routing table desynchronization, or kube-proxy iptables rules dropping packets.
- **Microservices**: DNS resolver timeouts, ephemeral port exhaustion during connection spikes, or stale client connection pools.
