# Core Architectural Mental Models

> "If you cannot draw the physical path of a byte and the logical path of authorization, you do not understand your architecture."

This document details the fundamental systems mental models required to reason through any AWS cloud architecture.

---

## 1. The End-to-End Request Path

Trace how a single HTTP request travels from a user's finger to a database disk and back:

```text
[ User Browser / Mobile App ]
             │
             │ 1. DNS Resolution Query: "api.example.com"
             ▼
   [ Route 53 (Anycast DNS) ] ──► Returns CloudFront Anycast IP
             │
             │ 2. HTTPS GET /orders (TLS Handshake at Edge)
             ▼
   [ CloudFront Edge PoP ]
             │ (Cache Miss)
             │ 3. Forward over private AWS fiber backbone
             ▼
   [ Application Load Balancer (ALB) ]
             │ 4. Terminate TLS, evaluate Layer 7 path rules (/orders)
             │ 5. Select healthy target via round-robin or least outstanding requests
             ▼
   [ VPC Route Table & Subnet ]
             │ 6. Hypervisor evaluates Security Group rules for ENI
             ▼
   [ EC2 / ECS Container / Lambda ]
             │ 7. Kernel TCP stack receives packet, notifies listening socket
             │ 8. Application process handles request, executes business logic
             │ 9. Dispatches query over TCP socket
             ▼
   [ RDS PostgreSQL / DynamoDB ]
             │ 10. Query executed, write-ahead log (WAL) flushed to EBS/SSD
             ▼
   [ Response Journey ]
   Database ──► App ──► ALB ──► CloudFront Edge (Cached) ──► User Browser
```

---

## 2. VPC Network Isolation & Packet Routing

A VPC is an isolated RFC 1918 virtual network mapped onto AWS's physical network via hypervisor encapsulation (Geneve / VXLAN overlays):

```text
AWS Region (e.g. us-east-1)
└── VPC: 10.0.0.0/16 (65,536 private IP addresses)
    │
    ├── Availability Zone A (Data Center Campus A)
    │   ├── Public Subnet A (10.0.1.0/24)
    │   │   ├── Route Table: 10.0.0.0/16 -> local, 0.0.0.0/0 -> igw-xxxx
    │   │   └── ALB Node A (Public IP: 54.x.x.x, Private IP: 10.0.1.15)
    │   │
    │   └── Private Subnet A (10.0.10.0/24)
    │       ├── Route Table: 10.0.0.0/16 -> local (NO ROUTE TO IGW)
    │       └── EC2 App Worker (Private IP: 10.0.10.42)
    │           └── Security Group: Allow TCP 8080 ONLY from ALB SG
    │
    └── Availability Zone B (Data Center Campus B - 10-50 km away)
        ├── Public Subnet B (10.0.2.0/24)
        │   ├── Route Table: 10.0.0.0/16 -> local, 0.0.0.0/0 -> igw-xxxx
        │   └── ALB Node B (Public IP: 52.x.x.x, Private IP: 10.0.2.88)
        │
        └── Private Subnet B (10.0.20.0/24)
            ├── Route Table: 10.0.0.0/16 -> local (NO ROUTE TO IGW)
            └── EC2 App Worker (Private IP: 10.0.20.77)
                └── Security Group: Allow TCP 8080 ONLY from ALB SG
```

### Key Realization:
Subnets **do not cross Availability Zones**. An AZ is an independent physical failure domain with isolated power, cooling, and networking. To make an application fault-tolerant, you must deploy resources across multiple subnets in multiple AZs.

---

## 3. Storage Hierarchy: Block vs Object vs File vs Key-Value

```text
┌───────────────┬───────────────────────────┬────────────────────────────┬─────────────────────────────┐
│ Storage Type  │ AWS Primitive             │ Access Method              │ Ideal Use Case              │
├───────────────┼───────────────────────────┼────────────────────────────┼─────────────────────────────┤
│ Block Storage │ EBS (Elastic Block Store) │ Block-level SCSI/NVMe      │ Operating system boot disks,│
│               │                           │ (512B - 4KB blocks)        │ relational database data dir│
├───────────────┼───────────────────────────┼────────────────────────────┼─────────────────────────────┤
│ Object Store  │ S3 (Simple Storage Serv)  │ HTTP REST API              │ Images, videos, backups,    │
│               │                           │ (GET, PUT, DELETE)         │ big data analytics lakes    │
├───────────────┼───────────────────────────┼────────────────────────────┼─────────────────────────────┤
│ File System   │ EFS (Elastic File System) │ NFSv4 network protocol     │ Shared POSIX filesystem     │
│               │                           │ (file handles, directories)│ mounted to multiple servers │
├───────────────┼───────────────────────────┼────────────────────────────┼─────────────────────────────┤
│ Distributed   │ DynamoDB                  │ HTTP JSON API              │ High-scale user profiles,   │
│ Key-Value     │                           │ (GetItem, PutItem by Key)  │ shopping carts, session keys│
└───────────────┴───────────────────────────┴────────────────────────────┴─────────────────────────────┘
```

---

## 4. Compute Abstraction Spectrum

```text
Operational Control: HIGH                                   Operational Control: LOW
Configuration Burden: HIGH                                 Configuration Burden: LOW
───────────────────────────────────────────────────────────────────────────────────►
  EC2 (Virtual Machines)   ECS / EKS (Containers)    Lambda (Event-Driven Micro-VM)
───────────────────────────────────────────────────────────────────────────────────►
• Full Linux OS control    • Packaged Docker image   • Pure function code
• Manage patching & AMI    • Manage CPU/Mem limits   • Ephemeral micro-VM per invoke
• Always-on billing        • Always-on task billing  • Billed strictly per millisecond
• Boot time: 1-5 minutes   • Start time: 2-30 secs   • Cold start: 50-800ms
```

---

## 5. Asynchronous Decoupling Spectrum

How should two services communicate?

```text
1. DIRECT SYNCHRONOUS HTTP (Tight Coupling):
   Service A ─────────(HTTP POST)────────► Service B
   * Risk: If Service B crashes, Service A crashes or drops client requests.

2. DURABLE POINT-TO-POINT BUFFER (SQS):
   Service A ──► [ SQS Queue (Durable Buffer) ] ──► Service B (Polls at own pace)
   * Benefit: Service B can crash, restart 2 hours later, and process all backlogged messages.

3. ONE-TO-MANY PUBLISH/SUBSCRIBE (SNS + SQS Fan-Out):
   OrderPlaced ──► [ SNS Topic ]
                         ├──► [ SQS Billing ] ──► Billing Service
                         ├──► [ SQS Shipping ] ──► Shipping Service
                         └──► [ SQS Analytics ] ──► Analytics Service
   * Benefit: Zero coupling between publisher and multiple independent consumers.

4. CONTENT-BASED EVENT ROUTING (EventBridge):
   OrderEvent ──► [ EventBridge Bus ] ──(Evaluate Rules on JSON Body)──► Target Services
   * Benefit: Routes based on payload attributes without code changes.
```

---

## 6. IAM Policy Evaluation Logic

AWS evaluates permissions on every single API request using this strict precedence tree:

```text
                         [ Incoming API Request ]
                                    │
                                    ▼
                     Is there an EXPLICIT DENY
                   in any applicable policy statement?
                                    │
                    ┌───────────────┴───────────────┐
                   YES                              NO
                    │                               │
                    ▼                               ▼
            [ REJECT: DENIED ]           Is there an EXPLICIT ALLOW
                                       in Identity or Resource policy?
                                                    │
                                    ┌───────────────┴───────────────┐
                                   YES                              NO
                                    │                               │
                                    ▼                               ▼
                      Does a Permission Boundary,          [ REJECT: DENIED ]
                     Session Policy, or SCP block it?       (Default Deny)
                                    │
                    ┌───────────────┴───────────────┐
                   YES                              NO
                    │                               │
                    ▼                               ▼
            [ REJECT: DENIED ]             [ AUTHORIZED: ALLOW ]
```

---

## 7. State, Ephemerality, and Scaling

The cardinal rule of cloud elasticity:
> **Compute instances must be stateless. State must be externalized to durable storage.**

If you write uploaded user files to `/var/www/uploads/` on an EC2 instance:
1. When traffic surges, Auto Scaling launches a second instance. Users hitting Instance B cannot see files uploaded to Instance A!
2. When traffic drops, Auto Scaling terminates Instance A. **All user files are permanently destroyed.**

**The Correct Cloud Architecture:**
- Compute nodes (EC2/ECS/Lambda) are disposable cattle.
- Ephemeral state (session caches) lives in **ElastiCache Redis**.
- Relational state lives in **RDS Multi-AZ**.
- Unstructured files live in **S3**.
- Transient work lives in **SQS**.
