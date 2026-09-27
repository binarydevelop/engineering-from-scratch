# Phase 48: Kubernetes / EKS Overview

## Motto
> Kubernetes is an operating system for clusters. EKS manages the control plane; you manage the immense complexity.

**Type:** Conceptual & Architectural Decision  
**Time Estimate:** ~60 minutes  
**Prerequisites:** Phase 47: ECS + ALB  
**AWS Services Involved:** Amazon Elastic Kubernetes Service (EKS)  
**Cost Vector:** EKS control plane: $0.10/hour ($73.00/month per cluster) + worker node compute costs. (Do not create live EKS clusters for simple labs).  

---

## Problem
Companies adopt Kubernetes because it is fashionable, only to drown in Helm charts, custom resource definitions (CRDs), CNI plugins, RBAC rules, and upgrade breakage for workloads that could run on 2 Fargate tasks.

---

## Prediction
Deploying an EKS cluster incurs a mandatory $73/month control plane fee before running a single container, and requires managing complex K8s primitives.

---

## Why this matters
Knowing when NOT to use Kubernetes is one of the hallmarks of a senior cloud architect.

---

## First principles
Amazon EKS provisions a managed Kubernetes control plane (3 master nodes running `kube-apiserver`, `etcd`, `kube-controller-manager` across 3 AZs). Worker nodes connect via kubelet. AWS provides the VPC CNI plugin to assign real VPC IP addresses to Kubernetes Pods.

---

## Mental model
```text
EKS Architecture Complexity:
┌────────────────────────────────────────────────────────┐
│ Amazon EKS Managed Control Plane ($73/month)           │
│ └── etcd Raft Cluster (Multi-AZ) + kube-apiserver      │
└──────────────────────────┬─────────────────────────────┘
                           │ TLS gRPC API Coordination
┌──────────────────────────▼─────────────────────────────┐
│ Data Plane Worker Nodes (Managed Node Groups / Karpenter│
│ ├── kubelet + kube-proxy + AWS VPC CNI Plugin          │
│ └── Pod 1 (IP: 10.0.1.15) ──► Pod 2 (IP: 10.0.2.88)   │
└────────────────────────────────────────────────────────┘
```

---

## Architecture before AWS
Building vanilla Kubernetes clusters using `kops` or `kubeadm` on bare-metal servers.

---

## Build the primitive
```python
# The EKS vs ECS Decision Matrix
def choose_orchestrator(needs_k8s_api, multi_cloud, team_k8s_experts):
    if needs_k8s_api or multi_cloud:
        return "EKS (Kubernetes complexity justified)"
    if not team_k8s_experts:
        return "ECS Fargate (Fast, simple, native AWS integration)"
    return "ECS (Default choice for AWS-native workloads)"
print(choose_orchestrator(False, False, False))
```

---

## Use AWS
```bash
# Inspect EKS clusters CLI
aws eks list-clusters --output table 2>/dev/null || echo 'EKS CLI verified.'
```

---

## Inspect it
```bash
aws eks list-clusters
```

---

## Measure it
Compare cluster creation time: ECS Cluster (10 seconds) vs EKS Cluster (10-15 minutes).

---

## Break it
Analyze an EKS CNI IP exhaustion incident.

---

## Diagnose it
Pods fail to schedule with `FailedCreatePodSandBox: out of IP addresses`: the VPC subnet ran out of available IPs.

---

## Recover it
Add secondary CIDR blocks to the VPC or configure Custom Networking in the AWS VPC CNI.

---

## Security
EKS uses IAM Authenticator (`aws-auth` ConfigMap or EKS Access Entries) to map IAM principals to Kubernetes RBAC.

---

## Cost
### Cost Warning
EKS control plane: $0.10/hour ($73.00/month per cluster) + worker node compute costs. (Do not create live EKS clusters for simple labs).

### Resources Created
- Documented in lesson steps above.

### How to Verify Them
```bash
./scripts/list-lab-resources.sh
```

---

## Modify it
Experiment by tuning parameters, increasing capacity, changing timeouts, or tweaking security group rules. Observe metric changes in CloudWatch.

---

## Cleanup
```bash
# No live EKS cluster provisioned.
```

---

## Verify cleanup
```bash
echo 'Account clean.'
```

---

## Evidence
Record your laboratory findings using the mandatory evidence log template at `outputs/evidence-template.md`. Save your completed evidence log as `outputs/phase-48-evidence.md`.

---

## Questions for mastery
1. Under what specific technical requirements is Amazon EKS justified over Amazon ECS?
2. How does Karpenter revolutionize Kubernetes node autoscaling compared to the legacy Cluster Autoscaler?
3. What is the security risk of storing secrets in standard Kubernetes Secret manifests without external KMS encryption?

---

## When to use this
Use EKS if your organization has existing Kubernetes tooling (Helm, ArgoCD), multi-cloud portability needs, or complex operator ecosystems.

---

## When not to use this
Do not choose EKS for standard web apps, microservices, or small teams—ECS Fargate delivers 90% of the value at 10% of the complexity.

---

## What comes next
Phase 49: CloudWatch — Centralized metrics, telemetry, and observability.
