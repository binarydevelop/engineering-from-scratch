# Learning Methodology: kubernetes-from-scratch

Welcome to **kubernetes-from-scratch**.

This repository is an **experimental, first-principles curriculum** designed for engineers who already know Docker and basic Linux networking, but want to deeply understand Kubernetes as an API-driven distributed control system rather than a collection of YAML templates to copy-paste.

The motto of this repository is:

> **Understand it. Build it. Schedule it. Observe it. Break it. Reconcile it. Recover it. Scale it. Ship it.**

---

## The Core Mental Model

> **Kubernetes is an API-driven distributed control system that continuously reconciles declared desired state with observed cluster state.**

If you think "Kubernetes is YAML," you will constantly struggle with outages, mysterious pending pods, selector mismatches, and cascading restarts. 
YAML is merely a serialization format for sending JSON declarations over an HTTP REST API to `kube-apiserver`. 

The real Kubernetes consists of:
1. An **API Server** that stores declarations in a persistent key-value store (`etcd`).
2. An array of autonomous **Controllers** running infinite control loops:
   $$\text{Desired State} - \text{Actual State} = \Delta \implies \text{Action}$$
3. A **Scheduler** that assigns unscheduled workloads to nodes with sufficient capacity.
4. A node agent (**kubelet**) that instructs local container runtimes to bring containers into existence and report actual status back to the API.

---

## The 12 Invariant Rules of Study

1. **Never copy-paste YAML blindly**: Typing manifests forces you to evaluate every field. Ask: *Why is this field here? Who reads it? What happens if I remove it?*
2. **Predict before applying**: Before running `kubectl apply`, write down what you expect to happen. Which controller will wake up? What events will fire? What intermediate states will the pod pass through?
3. **Inspect every object through the API**: A command returning exit code 0 does not mean your application is working. Verify with `kubectl get -o wide`, `kubectl describe`, and inspect the `status` block.
4. **Read events continuously**: Events are the event stream of the control plane. They tell you why the scheduler picked a node, why an image failed to pull, or why a readiness probe failed.
5. **Inspect owner references**: Trace the hierarchy of ownership (`metadata.ownerReferences`). A Pod is owned by a ReplicaSet, which is owned by a Deployment. Understanding this graph explains why deleting a Pod causes a new one to appear.
6. **Break resources deliberately**: You do not understand a Kubernetes primitive until you have intentionally killed its pods, broken its selectors, misconfigured its probes, exhausted its memory, and observed how it fails and recovers.
7. **Identify which component acted**: When a pod restarts, was it killed by the Linux kernel OOM-killer, terminated by kubelet due to a failed liveness probe, or replaced by the ReplicaSet controller?
8. **Distinguish desired state from actual state**: The `spec` is what you want. The `status` is what the cluster currently observes. The difference between them is why controllers exist.
9. **Debug before searching**: When a pod fails, walk through the systematic debugging sequence (`OBJECT -> STATUS -> CONDITIONS -> EVENTS -> OWNER -> POD -> CONTAINER -> LOGS -> NETWORK -> CONFIG -> STORAGE`) before searching online.
10. **Rebuild manifests from memory**: Once a lesson works, delete the directory and recreate the minimal working manifest from a blank terminal. If you cannot write it from memory, you rely on cargo-culting.
11. **Raw resources before Helm**: Never touch a Helm chart, Kustomize overlay, or operator until you have handwritten and debugged the underlying raw manifests. Packaging without understanding creates fragile systems.
12. **Never progress while reconciliation feels magical**: If an abstraction works and you cannot point to the exact controller loop that made it work, stop. Read the controller concept or run the Python simulator until the mechanics are transparent.

---

## The Learning Loop

Every lesson in this curriculum moves through this experimental cycle:

```text
       ┌───────────────────────────────┐
       │            PROBLEM            │
       │ (Distributed systems deficit) │
       └──────────────┬────────────────┘
                      ▼
       ┌───────────────────────────────┐
       │            PREDICT            │
       │ (State transition hypothesis) │
       └──────────────┬────────────────┘
                      ▼
       ┌───────────────────────────────┐
       │             BUILD             │
       │ (Write mini-code / manifest)  │
       └──────────────┬────────────────┘
                      ▼
       ┌───────────────────────────────┐
       │            INSPECT            │
       │ (Query API, status & events)  │
       └──────────────┬────────────────┘
                      ▼
       ┌───────────────────────────────┐
       │       OBSERVE CONTROLLER      │
       │ (Trace desired vs actual diff)│
       └──────────────┬────────────────┘
                      ▼
       ┌───────────────────────────────┐
       │             BREAK             │
       │ (Inject faults & kill actors) │
       └──────────────┬────────────────┘
                      ▼
       ┌───────────────────────────────┐
       │      WATCH RECONCILIATION     │
       │ (Observe control plane repair)│
       └──────────────┬────────────────┘
                      ▼
       ┌───────────────────────────────┐
       │        DEBUG & RECOVER        │
       │ (Root cause diagnosis tree)   │
       └──────────────┬────────────────┘
                      ▼
       ┌───────────────────────────────┐
       │            REBUILD            │
       │ (Reconstruct from memory)     │
       └───────────────────────────────┘
```

---

## The Mastery Quizzes: Reasoning vs. Memorization

Throughout the curriculum, quizzes test system reasoning, never syntax memorization.

### Examples:

* **Bad Quiz Question**: "What field in a Deployment spec sets the number of pods?"
* **Good Reasoning Question**: "You need exactly four replicas. One Pod is manually deleted with `kubectl delete pod`. Which Kubernetes component notices the deletion, how does it notice, what does it create in response, and why does the Deployment itself not directly create the replacement Pod?"

* **Bad Quiz Question**: "What is a ClusterIP Service?"
* **Good Reasoning Question**: "A client Pod attempts to connect to `payments:8080`. The Pods behind `payments` are being rolled out and their IP addresses are changing every 10 seconds. Trace the exact packet path from the client container's network namespace to the destination container's network namespace, explaining where DNS, virtual IPs, iptables/eBPF rules, and endpoints participate."

* **Bad Quiz Question**: "What is a readiness probe?"
* **Good Reasoning Question**: "A container process starts in 2 seconds, but requires 30 seconds to load a machine learning model into memory and establish its database pool. What happens to incoming user traffic during those 28 seconds if only a liveness probe is configured? Which probe prevents user errors, and how does the control plane act when that probe fails versus when a liveness probe fails?"

---

## Evidence-Based Learning

At the end of each lesson, record your empirical findings in `outputs/evidence-template.md`. 
Your evidence log documents:
1. The exact problem you solved.
2. The controller loop that reconciled the state.
3. The failure you injected and how you diagnosed it.
4. What guarantees Kubernetes provided—and critically, what guarantees it did *not* provide.
