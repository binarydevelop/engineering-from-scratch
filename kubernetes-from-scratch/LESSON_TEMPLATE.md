# Lesson Template: kubernetes-from-scratch

Use this canonical template when writing or completing any lesson in the curriculum. Every lesson must be driven by engineering problems, first principles, predictive experiments, intentional breakage, and observable evidence.

---

# Lesson [XX.Y]: [Title]

## Motto
> "[A concise, punchy single-sentence engineering truth summarizing the core mental model]"

## Problem
Describe the real-world distributed systems problem *before* any Kubernetes abstraction is mentioned.
- What engineering requirement are we trying to satisfy?
- What fails if we try to solve this with raw processes or basic Docker containers?
- What acute pain forces us to create a higher-level primitive?

## Prediction
Before executing a single command or writing any YAML, predict:
1. What will the client (CLI/HTTP) send over the wire?
2. What component in the control plane will receive the request?
3. Where will the desired state be stored?
4. Which controller or agent will observe the difference between desired and actual state?
5. What will be the observable intermediate states before the system reaches steady state?

## Why this matters
Explain the production consequences of not understanding this concept:
- What silent failures occur?
- What performance or reliability penalties are paid?
- Why does cargo-culting this abstraction lead to outages?

## First principles
Derive the concept from fundamental computer science and distributed systems principles:
- State storage, consistency, and consensus
- Control loops and feedback mechanisms
- Networking: routing, packet flow, encapsulation, and address translation
- Process isolation: namespaces, cgroups, and Linux kernel primitives

## Mental model
Provide a clear ASCII diagram illustrating the state flow, components, and boundaries:

```text
       DESIRED STATE (Declared)
                  │
                  ▼
         CONTROL COMPONENT
                  │  Observes diff
                  ▼
         ACTUAL STATE (Observed)
                  │
                  ▼
          RECONCILIATION ACTION
```

## Build the idea
Before using the built-in Kubernetes resource, build a small, simplified version of the concept (in Python or shell) or inspect raw primitives.
- Code reference: `code/simple_version.py` or equivalent.
- How does the raw logic behave under stress?

## Use Kubernetes
Now introduce the minimal Kubernetes API resource that models this concept.
- Manifest path: `manifests/resource.yaml`
- Explain every single field:
  - *Why does this field exist?*
  - *Who reads it?*
  - *What changes if we remove it?*
  - *How can we verify its effect?*

Execute the command:
```bash
kubectl apply -f manifests/resource.yaml
```

## Inspect the objects
Inspect the resulting state via the API:
```bash
kubectl get <resource> -o wide
kubectl describe <resource> <name>
kubectl get <resource> <name> -o json | jq .
```
Examine:
- `metadata.uid`, `metadata.generation`, `metadata.resourceVersion`
- `status.phase`, `status.conditions`

## Observe reconciliation
Trace how the controller reacted:
```bash
kubectl get events --sort-by='.metadata.creationTimestamp'
```
Identify:
- Which controller manager loop or node kubelet acted?
- What transition occurred between desired and actual state?

## Break it
Intentionally inject a realistic failure to observe how the system degrades:
- Kill the process / Pod
- Corrupt the configuration or credentials
- Sever network connectivity or partition a node
- Starve memory or CPU resources

Command to break:
```bash
# Fault injection command
```

## Debug it
Walk through the systematic debugging sequence without guessing:
```text
OBJECT -> STATUS -> CONDITIONS -> EVENTS -> OWNER -> POD -> CONTAINER -> LOGS -> NETWORK -> CONFIG -> STORAGE
```
Run diagnostic commands:
```bash
kubectl get ...
kubectl describe ...
kubectl logs ...
```
Document the exact error symptom, exit code, or failing condition.

## Recover it
Perform the remediation:
- Did the control plane recover the system automatically?
- Did manual intervention require fixing the declared specification or the underlying infrastructure?

Verify recovery:
```bash
kubectl get ...
```

## Modify it
Change a key parameter (e.g. replica count, probe threshold, resource limit, selector label) and predict the exact reconciliation steps before applying. Verify with `kubectl diff` and watch the transition live.

## Evidence
Document your findings in `outputs/evidence-template.md`:
- Pinned tool and cluster versions
- Timestamps and event traces
- Commands executed and verbatim outputs
- Proof that reconciliation occurred

## Questions for mastery
Reasoning-only questions (no memorization trivia):
1. *Scenario-based question testing boundary conditions.*
2. *Question probing failure modes and what component notices first.*
3. *Question contrasting this abstraction with an alternative approach.*

## What Kubernetes guarantees
List the exact operational and semantic guarantees provided by the API and controller for this abstraction.

## What Kubernetes does NOT guarantee
List common false assumptions developers make about what this abstraction handles (e.g. application data consistency, zero dropped packets during abrupt termination, instant node failover).

## When to use this
Precise criteria for when this pattern is the correct architectural choice.

## When not to use this
Simpler alternatives (e.g. single process, raw container, systemd, cloud serverless) where using this adds unnecessary accidental complexity.

## What comes next
Bridge to the next problem and lesson in the learning roadmap.
