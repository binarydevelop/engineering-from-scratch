# Lesson 04: Kubernetes API

## Motto
> "YAML is not Kubernetes; YAML is merely serialized JSON sent over an HTTP REST API."

## Problem
Engineers memorize YAML indentation without understanding that every manifest is an HTTP request payload evaluated by a REST server.

## Prediction
Before executing any commands or applying manifests, predict:
1. What will the client CLI send over the network to the control plane?
2. Which control plane component receives and validates the request?
3. Where is the desired state persisted?
4. Which controller reconciliation loop or node agent notices the difference between desired and observed state?
5. What intermediate conditions and status transitions will occur before the system reaches steady state?

## Why this matters
Resource schemas, OpenAPI validation, JSON representation, and kube-apiserver endpoints.
Without understanding this primitive, engineers suffer from mysterious outages, unserviceable traffic drops, or accidental cluster-wide cascades.

## First principles
At the fundamental systems level:
- Declarative Desired State ($S_{desired}$) is stored in the persistent database.
- Observed Actual State ($S_{actual}$) is discovered via kernel telemetry and agent health checks.
- Reconciliation Loop executes: $\Delta = S_{desired} - S_{actual}$.
- Action is taken if and only if $\Delta \neq 0$.

## Mental model

```text
       DECLARED DESIRED STATE
       (spec in etcd)
             │
             ▼
     CONTROLLER RECONCILER
             │ Observes difference
             ▼
     OBSERVED ACTUAL STATE
     (status in cluster)
             │
             ▼
      REMEDIATION ACTION
```

## Build the idea
Before relying on the Kubernetes abstraction, run the simulated primitive or inspect raw state:
```bash
kubectl get pods -o json
kubectl get --raw /api/v1/namespaces/default/pods
```

## Use Kubernetes
Now apply the declarative Kubernetes API manifest representing this concept:

```bash
# Verify manifest syntax offline
kubectl apply --dry-run=client -f manifests/

# Apply to cluster
kubectl apply -f manifests/
```

## Inspect the objects
Inspect the live API state and conditions:
```bash
kubectl get all -o wide
kubectl describe <resource> <name>
```

## Observe reconciliation
Trace how the controller manager or kubelet acted:
```bash
kubectl get events --sort-by='.metadata.creationTimestamp'
```

## Break it
Inject a realistic failure into the working system:
- Intentionally terminate a component or container process
- Introduce a network or configuration mismatch
- Observe how the control plane reacts

## Debug it
Execute the 11-step diagnostic workflow:
```text
OBJECT -> STATUS -> CONDITIONS -> EVENTS -> OWNER -> POD -> CONTAINER -> LOGS -> NETWORK -> CONFIG -> STORAGE
```

## Recover it
Remediate the failure:
- Observe whether the controller self-heals automatically
- Apply the declarative correction if configuration was invalid

## Modify it
Alter a key parameter in the manifest, predict the delta, and observe the live transition with `kubectl diff` and `kubectl apply`.

## Evidence
Record your commands, verbatim outputs, events, and controller traces in `outputs/evidence-template.md`.

## Questions for mastery
1. What exact component in the control plane or node detects this state change?
2. What guarantee does Kubernetes provide for this abstraction under node failure?
3. What guarantee does Kubernetes NOT provide?

## What Kubernetes guarantees
- Continuous reconciliation toward declared desired state.
- Automated status reporting via `status.conditions`.
- Level-triggered self-healing when cluster state diverges.

## What Kubernetes does NOT guarantee
- Instantaneous zero-second recovery upon physical node hardware death.
- Application-level data consistency without appropriate stateful architecture.
- Prevention of bugs in application code or configuration.

## When to use this
Use this primitive when your architectural requirements match its design guarantees.

## When not to use this
Avoid this primitive when simpler abstractions (single process, raw container, basic systemd service, managed serverless) solve the problem without distributed systems overhead.

## What comes next
Proceed to the next phase in the curriculum roadmap.
