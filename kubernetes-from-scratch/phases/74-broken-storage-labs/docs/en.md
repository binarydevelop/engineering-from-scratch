# Phase 74: Broken Storage Labs (4 Scenarios)

In this lab, 4 broken storage scenarios are deployed. Your objective is to diagnose storage binding, mount permissions, and persistence lifecycle failures.

---

## The 4 Broken Scenarios

### Scenario 74.1: `storage-pvc-pending`
- **Symptom**: PersistentVolumeClaim remains stuck in `Pending` indefinitely. Pod referencing it cannot start.
- **Diagnostic Command**: `kubectl describe pvc storage-pvc-pending`.
- **Diagnostic Challenge**: Identify why dynamic provisioning failed or why no PV matched.

### Scenario 74.2: `storage-permission-denied`
- **Symptom**: Pod fails with `CrashLoopBackOff` or `FailedMount`. Application logs report `IOError: [Errno 13] Permission denied: '/var/data/log.txt'`.
- **Diagnostic Challenge**: Why does a non-root container (e.g. UID 1000) fail to write to a newly mounted volume?

### Scenario 74.3: `storage-rwo-multi-attach-lock`
- **Symptom**: Two pods on different worker nodes attempt to attach the same `ReadWriteOnce` volume; the second pod hangs in `ContainerCreating`.
- **Diagnostic Challenge**: What does the `ReadWriteOnce` access mode actually enforce?

### Scenario 74.4: `storage-ephemeral-data-loss`
- **Symptom**: A database was deployed with an `emptyDir` volume. The pod restarted and all customer data vanished completely.
- **Diagnostic Challenge**: Distinguish the lifecycle of an ephemeral volume from a PersistentVolume.

---

## Separated Solutions & Remediation Guide

<details>
<summary><strong>Click to Expand Solutions Guide (Only after diagnosing!)</strong></summary>

### Solution 74.1: PVC Pending
- **Cause**: PVC specified `storageClassName: non-existent-fast-ssd` which does not exist in the cluster.
- **Fix**: Update `storageClassName` to a valid class (e.g. `standard`), or create the requested StorageClass.

### Solution 74.2: Volume Mount Permissions
- **Cause**: The storage volume is formatted and mounted as `root:root` (UID 0). The container runs as unprivileged user `UID 10001`.
- **Fix**: Configure `securityContext.fsGroup: 10001` in the Pod spec so kubelet automatically changes the volume ownership to the container group ID.

### Solution 74.3: ReadWriteOnce Concurrency
- **Cause**: `ReadWriteOnce` (RWO) means the volume can only be mounted with read-write permissions by a **single node at a time**, not multiple nodes.
- **Fix**: Use a `StatefulSet` with unique volumeClaimTemplates per replica, or use `ReadWriteMany` (RWX) storage like NFS.

### Solution 74.4: Ephemeral emptyDir Loss
- **Cause**: `emptyDir` storage is deleted the moment the Pod is deleted.
- **Fix**: Replace `emptyDir` with a `PersistentVolumeClaim` backed by durable storage.

</details>
