# Phase 122: Kubernetes Policy-as-Code: Admission Controllers, OPA Gatekeeper, and Kyverno

## 1. Why This Matters for MAANG & Senior/Staff Roles
In multi-tenant enterprise Kubernetes clusters, relying on developer goodwill to prevent security violations (e.g., running containers as root, omitting resource limits, pulling images from untrusted registries) leads directly to cluster compromise or node starvation. Policy-as-Code enforces declarative governance at the API server admission phase before resources are persisted to etcd.

---

## 2. Core Concepts & Architecture Deep-Dive
### Dynamic Admission Control Lifecycle
1. Request arrives at `kube-apiserver` -> Authentication & Authorization (RBAC).
2. **Mutating Admission Webhook**: Modifies the object (e.g., injects sidecar, default resource limits).
3. Object Schema Validation.
4. **Validating Admission Webhook**: Accepts or rejects object based on policy.
5. Resource written to etcd.

### OPA Gatekeeper vs Kyverno
- **OPA Gatekeeper**:
  - Uses general-purpose Open Policy Agent engine and Rego declarative query language.
  - Employs `ConstraintTemplate` (defines logic) and `Constraint` (applies to specific resources).
  - Highly expressive, enterprise standard, but Rego has a steep learning curve.
- **Kyverno**:
  - Kubernetes-native policy engine configured purely in standard Kubernetes YAML.
  - Validates, mutates, generates resources, and verifies container image signatures (Cosign) without learning a specialized programming language.

---

## 3. High-Value Interview Angle & Failure Modes
### Interview Questions & Production Policies
- **"How do you prevent noisy-neighbor node eviction in a shared cluster?"**:
  Enforce a validating policy requiring all container specs in `Pod` or `Deployment` manifests to explicitly specify both `resources.requests` and `resources.limits` for CPU and memory.
- **"How do you enforce that only signed images run in production?"**:
  Deploy Kyverno with Cosign keyless image verification policy. When an unsigned image or untrusted registry image is deployed, admission webhook blocks creation immediately.

---

## 4. Hands-On Practice & Implementation Drills
### Kyverno Policy Manifest Example
```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: require-non-root-and-limits
spec:
  validationFailureAction: Enforce
  rules:
  - name: validate-run-as-non-root
    match:
      any:
      - resources:
          kinds:
          - Pod
    validate:
      message: "Running as root is forbidden. Set securityContext.runAsNonRoot to true."
      pattern:
        spec:
          securityContext:
            runAsNonRoot: true
  - name: validate-resource-limits
    match:
      any:
      - resources:
          kinds:
          - Pod
    validate:
      message: "CPU and Memory limits are mandatory for all production containers."
      pattern:
        spec:
          containers:
          - resources:
              limits:
                memory: "?*"
                cpu: "?*"
```

---

## 5. Key Takeaways & Cheat Sheet
- Validating Admission Webhooks block non-compliant resources before etcd storage.
- Policy-as-Code prevents misconfigurations, security breaches, and resource starvation.
- OPA Gatekeeper uses Rego; Kyverno uses native Kubernetes YAML.
- Key knowledge for DevSecOps, SRE, and staff infrastructure interviews.
