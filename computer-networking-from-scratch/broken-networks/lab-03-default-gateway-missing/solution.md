# Solution: LAB-03 — Default Gateway Missing

---

## 1. Failing Layer
**L3 (Routing)**

## 2. Root Cause Analysis
The failure occurs because:
> **Add default route: sudo ip route add default via <gateway_ip>.**

When the client initiates communication, the expected protocol interaction fails at the L3 (Routing) boundary. 

## 3. Diagnostic Trace
Using `ip route show`, we observe the definitive proof of failure:
- **Diagnostic Command**:
  ```bash
  ip route show
  ```
- **Evidence**:
  The output directly confirms that the target endpoint or route cannot be reached or resolved due to a state mismatch.

## 4. Surgical Remediation
To permanently resolve this issue:
```bash
# Remediation:
Add default route: sudo ip route add default via <gateway_ip>.
```

## 5. Production Connection
This incident pattern frequently manifests in production environments:
- **Cloud (AWS/GCP)**: Misconfigured Security Groups, missing VPC route table entries, or incorrect NAT gateways.
- **Containers (Docker/Kubernetes)**: Binding services to `127.0.0.1` inside containers, CNI routing table desynchronization, or kube-proxy iptables rules dropping packets.
- **Microservices**: DNS resolver timeouts, ephemeral port exhaustion during connection spikes, or stale client connection pools.
