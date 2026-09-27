# Phase 73: Broken Networking Labs (6 Scenarios)

In this lab, 6 broken networking scenarios are deployed. Your objective is to isolate and diagnose why traffic cannot reach backend workloads.

---

## The 6 Broken Scenarios

### Scenario 73.1: `svc-selector-mismatch`
- **Symptom**: `curl http://broken-svc-1` hangs or returns immediately with connection failure.
- **Diagnostic Command**: `kubectl get endpoints broken-svc-1` reports `<none>`.
- **Diagnostic Challenge**: Compare the Service `spec.selector` against `kubectl get pods --show-labels`.

### Scenario 73.2: `svc-wrong-port`
- **Symptom**: Connection refused when hitting the Service port.
- **Diagnostic Challenge**: Is the port mismatch at the Service level (`spec.ports[*].port`) or the container level (`spec.ports[*].targetPort`)?

### Scenario 73.3: `svc-wrong-targetport`
- **Symptom**: Service has valid Endpoints, but requests time out or return connection refused.
- **Diagnostic Challenge**: Verify what port the container process is actually listening on using `netstat` or `ss`.

### Scenario 73.4: `app-bound-to-localhost`
- **Symptom**: The container process is running. Connecting inside the container (`curl 127.0.0.1:8080`) works! Connecting from outside or via Service IP fails!
- **Diagnostic Challenge**: Uncover why binding to `127.0.0.1` breaks container networking and why servers must bind to `0.0.0.0`.

### Scenario 73.5: `unready-pod-missing-endpoints`
- **Symptom**: Pod status is `Running`, but Service endpoints list is `<none>`.
- **Diagnostic Challenge**: Inspect `status.conditions` to see why the EndpointSlice controller excluded the pod.

### Scenario 73.6: `networkpolicy-denied`
- **Symptom**: Client pod can resolve DNS, but TCP packets to the backend service time out silently.
- **Diagnostic Challenge**: Check for an active `NetworkPolicy` dropping ingress traffic.

---

## Separated Solutions & Remediation Guide

<details>
<summary><strong>Click to Expand Solutions Guide (Only after diagnosing!)</strong></summary>

### Solution 73.1: Selector Mismatch
- **Cause**: Service specifies `selector: app: my-api`, while Pod has label `app: my-api-v1`.
- **Fix**: Update Service selector to match the Pod label: `kubectl set selector service broken-svc-1 app=my-api-v1`.

### Solution 73.2 & 73.3: Port Alignment
- **Cause**: Service `targetPort` was set to `9999` while Nginx listens on `80`.
- **Fix**: Align `targetPort: 80` in the Service manifest.

### Solution 73.4: The Localhost Trap
- **Cause**: Server process was started with `--host 127.0.0.1`. The loopback interface is isolated within the container's network namespace and does not listen on the `eth0` veth interface.
- **Fix**: Rebind the application listener to `0.0.0.0` (all network interfaces).

### Solution 73.5: Readiness Failure
- **Cause**: Readiness probe is querying `/healthz`, but the application only serves `/`.
- **Fix**: Correct the HTTP path in the readiness probe to `/`.

### Solution 73.6: NetworkPolicy Deny
- **Cause**: A default-deny NetworkPolicy was applied without an ingress rule allowing traffic from the client pod.
- **Fix**: Add an ingress rule allowing traffic from `podSelector: matchLabels: role: frontend`.

</details>
