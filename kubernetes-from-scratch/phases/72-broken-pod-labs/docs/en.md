# Phase 72: Broken Pod Labs (7 Scenarios)

In this lab, 7 broken pod scenarios are deployed. Your objective is to use the 11-step diagnostic workflow (`docs/kubectl-debugging.md`) to diagnose the exact root cause of each failure from symptoms alone, without looking at the solutions.

---

## The 7 Broken Scenarios

### Scenario 72.1: `pod-broken-image`
- **Symptom**: Pod status displays `ImagePullBackOff` or `ErrImagePull`.
- **Diagnostic Challenge**: Is it a misspelled image name, invalid tag, or private registry permission failure?

### Scenario 72.2: `pod-crashloop-exit1`
- **Symptom**: Pod enters `CrashLoopBackOff`, container exit code is `1`.
- **Diagnostic Challenge**: Inspect `--previous` logs to extract the application runtime exception.

### Scenario 72.3: `pod-completed-exit0`
- **Symptom**: Pod starts, runs for 1 second, and exits with code `0`. Kubelet repeatedly restarts it because `restartPolicy: Always`.
- **Diagnostic Challenge**: Why does a clean exit code 0 cause a service crash loop?

### Scenario 72.4: `pod-missing-configmap`
- **Symptom**: Pod is stuck in `CreateContainerConfigError`.
- **Diagnostic Challenge**: Which specific ConfigMap or environment key is preventing container initialization?

### Scenario 72.5: `pod-missing-secret`
- **Symptom**: Pod is stuck in `CreateContainerConfigError`.
- **Diagnostic Challenge**: Identify the missing Secret name from the event stream.

### Scenario 72.6: `pod-failed-mount`
- **Symptom**: Pod status is `ContainerCreating`, events show `FailedMount`.
- **Diagnostic Challenge**: Trace why the volume could not be mounted into the container path.

### Scenario 72.7: `pod-oom-killed`
- **Symptom**: Pod terminates abruptly with `OOMKilled` (Exit code 137).
- **Diagnostic Challenge**: Compare container memory limits against the workload's memory allocation behavior.

---

## Separated Solutions & Remediation Guide

<details>
<summary><strong>Click to Expand Solutions Guide (Only after diagnosing!)</strong></summary>

### Solution 72.1: `pod-broken-image`
- **Cause**: Image was specified as `nginx:non-existent-tag-9999`.
- **Fix**: Update image to a valid tag: `nginx:1.27-alpine`.

### Solution 72.2: `pod-crashloop-exit1`
- **Cause**: Application container executed command `sh -c "exit 1"`.
- **Fix**: Replace failing command with a valid foreground daemon process.

### Solution 72.3: `pod-completed-exit0`
- **Cause**: Command was `sh -c "echo Hello"`. In Kubernetes, web services require a continuous foreground process.
- **Fix**: For one-off batch scripts, use a `Job` instead of an infinite Pod, or keep the process running.

### Solution 72.4: `pod-missing-configmap`
- **Cause**: Manifest referenced `configMapRef: name: non-existent-config`.
- **Fix**: Create the referenced ConfigMap before creating the Pod: `kubectl create configmap non-existent-config --from-literal=KEY=val`.

### Solution 72.5: `pod-missing-secret`
- **Cause**: Manifest referenced `secretRef: name: non-existent-secret`.
- **Fix**: Create the Secret: `kubectl create secret generic non-existent-secret --from-literal=PASSWORD=pass`.

### Solution 72.6: `pod-failed-mount`
- **Cause**: Pod mounted a volume referencing a non-existent PersistentVolumeClaim.
- **Fix**: Ensure the PVC is created and in `Bound` status before mounting.

### Solution 72.7: `pod-oom-killed`
- **Cause**: Container was allocated a memory limit of `32Mi`, but attempted to allocate `64Mi`.
- **Fix**: Increase `resources.limits.memory` to `128Mi`.

</details>
