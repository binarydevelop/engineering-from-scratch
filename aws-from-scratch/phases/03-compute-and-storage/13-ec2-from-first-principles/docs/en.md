# Phase 13: EC2 From First Principles

## Motto
> An EC2 instance is a slice of physical CPU and memory booted from a snapshot, attached to an ENI and an EBS volume.

**Type:** Hands-on Lab & Virtual Machine Launch  
**Time Estimate:** ~60 minutes  
**Prerequisites:** Phase 11: Security Groups  
**AWS Services Involved:** Amazon EC2, Amazon Linux 2023, Nitro Hypervisor  
**Cost Vector:** A `t4g.micro` costs ~$0.0042/hour (~$3.00/month). Unattached stopped instances do not incur compute charges, but attached EBS volumes continue charging for storage.  

---

## Problem
You need to run arbitrary compiled binaries, system daemons, and custom software packages with root access on a Linux operating system.

---

## Prediction
Launching an EC2 instance will create a virtual machine, attach an Elastic Network Interface with a private IP, allocate an EBS root volume, and execute the User Data shell script on initial boot.

---

## Why this matters
EC2 is the foundational compute primitive in AWS. ECS, EKS, and even parts of RDS run on top of EC2 instances.

---

## First principles
AWS Nitro hypervisor partitions a physical server's CPU sockets into vCPUs (hardware hyperthreads) and assigns memory blocks. Storage and networking I/O are offloaded to dedicated PCIe Nitro accelerator cards, giving the guest OS near-native bare-metal performance.

---

## Mental model
```text
EC2 Nitro System Architecture:
Physical Rack Chassis
┌────────────────────────────────────────────────────────┐
│ Physical Motherboard & Intel/AMD/Graviton CPU Sockets  │
│ ┌────────────────────────────────────────────────────┐ │
│ │ Lightweight KVM Core Hypervisor                    │ │
│ └─────────────────────────┬──────────────────────────┘ │
│                           │ Offloaded via PCIe         │
│ ┌─────────────────────────▼──────────────────────────┐ │
│ │ AWS Nitro Card (VPC Networking & Security Groups)  │ │
│ │ AWS Nitro Card (EBS NVMe Storage Controller)       │ │
│ │ AWS Nitro Security Chip (Secure Boot & Hardware TPM│ │
│ └────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────┘
```

---

## Architecture before AWS
Provisioning a VMware ESXi or KVM virtual machine via vCenter or PXE netboot.

---

## Build the primitive
```python
# User Data bootstrap script
user_data = '''#!/bin/bash
dnf update -y
dnf install -y httpd
echo "Hello from EC2 $(hostname -f)" > /var/www/html/index.html
systemctl start httpd
systemctl enable httpd'''
print("Bootstrap User Data defined.")
```

---

## Use AWS
```bash
aws ec2 run-instances --image-id resolve:ssm:/aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-arm64 --instance-type t4g.micro --subnet-id $PUB_SUBNET_ID --security-group-ids $SG_ID --user-data file://scripts/userdata.sh --tag-specifications 'ResourceType=instance,Tags=[{Key=Project,Value=aws-from-scratch},{Key=Lesson,Value=13-ec2}]'
```

---

## Inspect it
```bash
aws ec2 describe-instances --filters 'Name=tag:Project,Values=aws-from-scratch' --query 'Reservations[].Instances[].[InstanceId,State.Name,PublicIpAddress,PrivateIpAddress,InstanceType]' --output table
```

---

## Measure it
Measure time from API call to HTTP 200 response (typically 60-120 seconds).

---

## Break it
Terminate the instance or stop the systemd daemon.

---

## Diagnose it
Status checks: Instance status check fails if OS kernel panics; System status check fails if physical host hardware fails.

---

## Recover it
Reboot the instance or launch a replacement via Auto Scaling.

---

## Security
Use AWS Systems Manager (SSM) Session Manager instead of opening SSH port 22 to the public internet.

---

## Cost
### Cost Warning
A `t4g.micro` costs ~$0.0042/hour (~$3.00/month). Unattached stopped instances do not incur compute charges, but attached EBS volumes continue charging for storage.

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
for id in $(aws ec2 describe-instances --filters 'Name=tag:Project,Values=aws-from-scratch' 'Name=instance-state-name,Values=running,stopped' --query 'Reservations[].Instances[].InstanceId' --output text); do aws ec2 terminate-instances --instance-ids $id; done
```

---

## Verify cleanup
```bash
aws ec2 describe-instances --filters 'Name=tag:Project,Values=aws-from-scratch' 'Name=instance-state-name,Values=running,pending' --query 'Reservations[].Instances[]' --output text
```

---

## Evidence
Record your laboratory findings using the mandatory evidence log template at `outputs/evidence-template.md`. Save your completed evidence log as `outputs/phase-13-evidence.md`.

---

## Questions for mastery
1. What is the difference between a System Status Check failure and an Instance Status Check failure?
2. Why does an EC2 instance get a new public IPv4 address when stopped and restarted, while its private IP remains identical?
3. How does Graviton (ARM64) architecture deliver up to 40% better price-performance compared to x86?

---

## When to use this
Use EC2 when you require full OS control, legacy monolithic software, custom kernel modules, or long-running predictable workloads.

---

## When not to use this
Avoid EC2 for simple stateless microservices or event-driven tasks where ECS Fargate or Lambda eliminates patching.

---

## What comes next
Phase 14: What Happens When EC2 Launches — Tracing the step-by-step lifecycle from API to booted OS.
