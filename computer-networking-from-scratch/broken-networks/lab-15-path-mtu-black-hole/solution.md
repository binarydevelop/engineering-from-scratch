# Solution: LAB-15 — Path MTU Black Hole

---

## 1. Failing Layer
**L3 (MTU / ICMP)**

## 2. Root Cause Analysis
The failure occurs because:
> **Clamp MSS: iptables -t mangle -A POSTROUTING -p tcp --tcp-flags SYN,RST SYN -j TCPMSS --clamp-mss-to-pmtu.**

When the client initiates communication, the expected protocol interaction fails at the L3 (MTU / ICMP) boundary. 

## 3. Diagnostic Trace
Using `ping -M do -s 1472`, we observe the definitive proof of failure:
- **Diagnostic Command**:
  ```bash
  ping -M do -s 1472
  ```
- **Evidence**:
  The output directly confirms that the target endpoint or route cannot be reached or resolved due to a state mismatch.

## 4. Surgical Remediation
To permanently resolve this issue:
```bash
# Remediation:
Clamp MSS: iptables -t mangle -A POSTROUTING -p tcp --tcp-flags SYN,RST SYN -j TCPMSS --clamp-mss-to-pmtu.
```

## 5. Production Connection
This incident pattern frequently manifests in production environments:
- **Cloud (AWS/GCP)**: Misconfigured Security Groups, missing VPC route table entries, or incorrect NAT gateways.
- **Containers (Docker/Kubernetes)**: Binding services to `127.0.0.1` inside containers, CNI routing table desynchronization, or kube-proxy iptables rules dropping packets.
- **Microservices**: DNS resolver timeouts, ephemeral port exhaustion during connection spikes, or stale client connection pools.
