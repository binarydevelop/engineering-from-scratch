# Phase 00: Cloud Before AWS

## Motto
> The cloud is not magic: it is someone else's physical computers controlled by software APIs.

**Type:** Conceptual & Systems Exploration  
**Time Estimate:** ~45 minutes  
**Prerequisites:** Basic Linux processes and terminal commands  
**AWS Services Involved:** None (Foundational Physical Infrastructure)  
**Cost Vector:** Idle Physical Server: 100% of CapEx + ongoing power/cooling costs regardless of utilization. Cloud Compute: 100% variable OpEx billed per second.  

---

## Problem
Before cloud computing, deploying a backend application meant purchasing physical servers, waiting 6-12 weeks for delivery, racking and cabling them in a datacenter, configuring redundant power, and manually installing operating systems. Traffic surges caused weeks of downtime until new hardware arrived.

---

## Prediction
If hardware procurement takes 8 weeks, engineering teams will over-provision massively, leading to 80%+ idle server capacity and exorbitant capital expenditures.

---

## Why this matters
Understanding bare-metal physical constraints explains why cloud virtualization, resource pools, and on-demand APIs were invented.

---

## First principles
A computer is CPU registers, memory caches, DRAM, PCI buses, NICs, and persistent storage media. An OS kernel abstracts this hardware for userland processes. Hypervisors extend this abstraction by virtualizing CPU instruction sets (VT-x/AMD-V) and memory management units (EPT/NPT), allowing multiple isolated guest OS kernels to share one physical host.

---

## Mental model
```text
Physical Datacenter to Virtualization:
┌────────────────────────────────────────────────────────┐
│ Physical Server Host (64 Cores, 256GB RAM, Dual 10GbE) │
│ ┌────────────────────────────────────────────────────┐ │
│ │ Type-1 Hypervisor (Nitro / KVM / Xen)              │ │
│ └─────────────────────────┬──────────────────────────┘ │
│         ┌─────────────────┼─────────────────┐          │
│         ▼                 ▼                 ▼          │
│ ┌───────────────┐ ┌───────────────┐ ┌───────────────┐  │
│ │ Guest VM 1    │ │ Guest VM 2    │ │ Guest VM 3    │  │
│ │ (2 vCPU, 4GB) │ │ (4 vCPU, 8GB) │ │ (8 vCPU, 32GB)│  │
│ └───────────────┘ └───────────────┘ └───────────────┘  │
└────────────────────────────────────────────────────────┘
```

---

## Architecture before AWS
Organizations leased datacenter cages, maintained diesel backup generators, ran physical BGP routers, and bought Dell/HP rack servers with 3-year depreciation schedules.

---

## Build the primitive
```python
import os
print(f"Available Logical Cores: {os.cpu_count()}")
try:
    with open('/proc/cpuinfo') as f:
        print([line.strip() for line in f if 'model name' in line][0])
except Exception:
    print("Local CPU inspection completed.")
```

---

## Use AWS
```bash
aws ec2 describe-instance-types --instance-types t4g.micro --query 'InstanceTypes[0].[InstanceType,VCpuInfo.DefaultVCpus,MemoryInfo.SizeInMiB]' --output table
```

---

## Inspect it
```bash
aws ec2 describe-regions --query 'Regions[].[RegionName,Endpoint]' --output table
```

---

## Measure it
Measure latency between local loopback (127.0.0.1) and a remote server IP via ping.

---

## Break it
Simulate CPU core exhaustion locally using a multi-process spin loop.

---

## Diagnose it
Inspect 'top' or 'htop'; observe 100% CPU utilization and process scheduling throttling.

---

## Recover it
Apply OS cgroups or process nice values to constrain compute starvation.

---

## Security
Hypervisor escape vulnerabilities (Spectre, Meltdown, Rowhammer) represent the physical security perimeter between multitenant virtual machines.

---

## Cost
### Cost Warning
Idle Physical Server: 100% of CapEx + ongoing power/cooling costs regardless of utilization. Cloud Compute: 100% variable OpEx billed per second.

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
# No resources created in live AWS account for Phase 00.
```

---

## Verify cleanup
```bash
echo 'Account clean.'
```

---

## Evidence
Record your laboratory findings using the mandatory evidence log template at `outputs/evidence-template.md`. Save your completed evidence log as `outputs/phase-00-evidence.md`.

---

## Questions for mastery
1. Why does a 2-vCPU virtual machine not guarantee 100% of two physical hardware cores unless Dedicated Hosts are purchased?
2. What physical bottleneck prevents cloud providers from offering instantaneous provisioning of 100,000 servers in a single second?
3. How does hypervisor CPU time-sharing affect p99 latency compared to bare-metal hardware?

---

## When to use this
Whenever workloads have variable, unpredictable, or seasonal demand that cannot justify purchasing physical hardware.

---

## When not to use this
When regulatory requirements mandate sovereign on-prem hardware or when steady-state 24/7 compute at petabyte scale makes colo cheaper.

---

## What comes next
Phase 01: AWS Global Infrastructure — Understanding Regions, Availability Zones, and physical speed-of-light boundaries.
