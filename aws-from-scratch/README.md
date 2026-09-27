# AWS from Scratch

> **Understand it. Build it. Observe it. Break it. Recover it. Secure it. Scale it. Cost it. Ship it.**

An engineering curriculum designed to teach Amazon Web Services deeply from **first principles** through hands-on implementation, experiments, measurement, failure injection, debugging, architecture evolution, cost analysis, and progressively more realistic cloud systems.

Inspired by the first-principles philosophy of [`ai-engineering-from-scratch`](https://github.com/rohitg00/ai-engineering-from-scratch).

---

## The Philosophy: Stop Memorizing Service Catalogs

Most cloud training materials teach AWS as an overwhelming catalog of proprietary brand names:
> *"Amazon SQS is a fully managed message queuing service that enables you to decouple and scale microservices..."*

This approach produces engineers who can pass multiple-choice certification exams, but who panic when an Application Load Balancer returns HTTP 502, when an EC2 instance in a private subnet cannot reach GitHub, or when a surprise $3,000 NAT Gateway bill arrives at the end of the month.

**This repository takes the opposite path:**

```text
       [ Concrete Systems Problem ]
                    ↓
     [ Underlying Infrastructure Need ]
                    ↓
        [ Simplest Possible Solution ]
                    ↓
          [ Physical Limitations ]
                    ↓
        [ AWS Primitive / Managed Service ]
                    ↓
     [ Security, Reliability & Cost Tradeoffs ]
```

### The Test of True Understanding
When you finish this repository and look at an architecture containing:
```text
Route 53 ──► CloudFront ──► ALB ──► ECS / Lambda ──► RDS / DynamoDB ──► SQS ──► S3
                                │
                        CloudWatch & IAM
```

You will not see "a collection of AWS products." You will see:
- **Where data lives** (block, object, relational, or distributed key-value)
- **Where state lives** (and why compute instances must be stateless)
- **How bytes physically travel** (DNS queries, TLS termination, TCP handshakes, reverse proxying, hypervisor ENIs)
- **What security perimeters exist** (least-privilege IAM roles, security groups, private subnets)
- **What fails when an Availability Zone loses power** (and how automatic failover works)
- **What costs money while completely idle** (and how to design zero-cost serverless alternatives)
- **Whether each service is even necessary** (or if a simpler primitive is superior)

---

## The Infrastructure Progression

```text
               [ Physical Computer ]
                        ↓
             [ Virtual Machine (KVM) ]
                        ↓
             [ Cloud APIs & Control Plane ]
                        ↓
            [ Regions & Availability Zones ]
                        ↓
          [ Identity & Access Management (IAM) ]
                        ↓
           [ Virtual Private Cloud (VPC) ]
                        ↓
           [ Compute (EC2 / Nitro Enclaves) ]
                        ↓
         [ Persistent Storage (EBS & Amazon S3) ]
                        ↓
       [ Databases (Amazon RDS & Amazon DynamoDB) ]
                        ↓
           [ Load Balancing (ALB / Reverse Proxy) ]
                        ↓
          [ Horizontal Elasticity (Auto Scaling) ]
                        ↓
         [ Asynchronous Messaging (SQS, SNS, EventBridge) ]
                        ↓
          [ Serverless Compute (AWS Lambda & Firecracker) ]
                        ↓
         [ Container Orchestration (Amazon ECS & Fargate) ]
                        ↓
              [ Observability & Telemetry (CloudWatch) ]
                        ↓
         [ Encryption & Secrets (AWS KMS & Secrets Manager) ]
                        ↓
         [ Reliability, Chaos Testing & Disaster Recovery ]
                        ↓
             [ Cloud Financial Engineering (FinOps) ]
                        ↓
        [ Production Well-Architected Systems Architecture ]
```

---

## Who This Is For

- **Backend & Systems Engineers** who want to stop treating cloud infrastructure as a black box and build deep intuition for real-world distributed systems.
- **Full-Stack Engineers** transitioning into platform, DevOps, or senior infrastructure roles.
- **Developers Preparing for Real-World Cloud Architecture** who want deep first-principles mastery rather than superficial certification memorization.

### Prerequisites
- Proficiency in **Python 3.12+** (used for local primitive implementations and AWS SDK automation).
- Basic understanding of **Docker, processes, ports, HTTP/1.1, and relational databases**.
- Familiarity with the terminal (`bash`/`zsh`, `curl`, `jq`, `git`).
- **An AWS Account** that you control (see Account Security and Cost Safety below).

---

## CRITICAL: Cost Safety Guardrails (Zero-Surprise Protocol)

> **AWS experiments can cost real money.** Idle resources accrue continuous financial liability.

Before launching any live lab, follow the mandatory [COST_SAFETY.md](COST_SAFETY.md) protocol:
1. **Never leave infrastructure running:** Every lesson provides explicit `## Cleanup` and `## Verify cleanup` commands.
2. **Set up an AWS Zero-Spend Budget & Billing Alarm:** Sends automated email alerts if monthly estimated charges exceed $1.00 or $5.00.
3. **No expensive NAT Gateways:** NAT Gateways cost ~$32.40/month per gateway while completely idle. We teach secure, modern alternatives (VPC Endpoints and public jumpboxes) that keep your lab bill at **$0.00**.
4. **Mandatory Lab Resource Tagging:** All lab resources must be tagged with `Project=aws-from-scratch`.
5. **Run the Automated Scanner:** Use `./scripts/list-lab-resources.sh` to find lingering resources across all services.

---

## CRITICAL: Account Security Guardrails (Zero-Trust Protocol)

Before touching live AWS APIs, read [SECURITY.md](SECURITY.md):
1. **NEVER use the AWS root user for daily learning labs.**
2. **Root account must have MFA enabled and zero active access keys.**
3. **NEVER create permanent administrator access keys (`AKIA...`).**
4. **Use IAM Identity Center (SSO) or short-lived temporary STS tokens (`ASIA...`).**
5. **NEVER commit credentials, private keys, or `.env` files to Git.** (Our pre-configured `.gitignore` protects against this).

---

## The Core Learning Loop

Every lesson in this repository executes this rigorous 15-step cycle:

```text
Problem ──► Predict ──► First Principles ──► Build Primitive ──► Use AWS
   │
Inspect ──► Measure ──► Break ──────────► Diagnose ─────────► Recover
   │
Secure  ──► Cost    ──► Automate ───────► Clean Up ─────────► Verify Cleanup
```

---

## Repository Structure

```text
aws-from-scratch/
├── README.md               # You are here
├── ROADMAP.md              # Complete 86-phase syllabus and learning paths
├── LEARNING.md             # The learning contract and diagnosis principles
├── LESSON_TEMPLATE.md      # The 23-point blueprint for every lesson
├── VERSIONS.md             # Verified tool versions and AWS API baseline (Sept 2026)
├── COST_SAFETY.md          # Zero-surprise AWS billing guardrails & alarm setup
├── SECURITY.md             # Account hardening & least-privilege threat model
├── CONTRIBUTING.md         # Contribution guidelines and standards
├── Makefile                # Educationally explicit automation targets
├── requirements.txt        # Minimal Python dependencies (boto3, pydantic, etc.)
│
├── scripts/
│   ├── check-environment.sh    # Verifies local tool versions
│   ├── check-aws-identity.sh   # Inspects caller identity and enforces zero-root rule
│   ├── list-lab-resources.sh   # Read-only discovery of tagged lab resources
│   └── cleanup-check.sh        # Confirms account returned to zero-cost baseline
│
├── docs/
│   ├── glossary.md             # Maps AWS terminology to CS and networking primitives
│   ├── mental-models.md        # Core architectural diagrams and packet paths
│   ├── troubleshooting.md      # Systematic diagnostic trees for cloud failures
│   └── service-map.md          # Problem -> Primitive -> AWS Service matrix
│
├── experiments/
│   ├── iam_simulator.py        # First-principles IAM boolean evaluation engine
│   ├── sqs_visibility_lab.py   # At-least-once delivery, timeout & DLQ simulation
│   ├── lb_healthcheck_lab.py   # Reverse proxy, health probing & target eviction
│   ├── hot_partition_lab.py    # Partition hashing skew & DynamoDB throttling
│   └── failure_day.py          # Phase 83 chaos testing and recovery runner
│
├── benchmarks/
│   ├── benchmark_lb.py         # Measures load balancer overhead vs direct connect
│   └── benchmark_cache.py      # Measures in-memory cache speedup vs DB queries
│
├── policies/                   # Production-grade least-privilege IAM policy templates
├── infrastructure/             # Validated CloudFormation templates (VPC, ALB, Serverless)
├── projects/                   # Comprehensive end-to-end production projects
├── phases/                     # 86 deep lessons organized into 13 thematic modules
└── outputs/
    └── evidence-template.md    # Mandatory lab evidence template
```

---

## How to Begin Safely

### Step 1: Clone and Check Local Environment
```bash
git clone https://github.com/your-username/aws-from-scratch.git
cd aws-from-scratch

# Run environment verification check
./scripts/check-environment.sh
```

### Step 2: Install Python Dependencies in a Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Step 3: Verify AWS Identity Safety
```bash
./scripts/check-aws-identity.sh
```
*(If no AWS credentials are configured yet, that's completely fine! You can run all conceptual labs and Python simulators in Phases 00, 03, 05, 22, 33, and 81 with zero AWS account required).*

### Step 4: Run the Local Simulators
```bash
make test-simulators
```

### Step 5: Begin Phase 00
Start your journey at [phases/00-cloud-foundations/00-cloud-before-aws/docs/en.md](phases/00-cloud-foundations/00-cloud-before-aws/docs/en.md).

---

## Final Standard: What You Will Gain

When you complete this repository:

1. **You will never treat AWS as a service catalog again.** When someone says "Amazon SQS", you will think: *an asynchronous, distributed, at-least-once FIFO/standard buffer with visibility timeouts and dead-letter queue semantics.*
2. **You will be able to design architectures from business constraints.** Given 10M users, 99.9% availability, and a $200/month budget, you will derive the exact primitives needed, calculate the capacity, and prove the failure modes before provisioning a single resource.
3. **You will be able to diagnose production outages systematically.** You will look at a `timed out` error, know whether a Security Group dropped the SYN packet or a Route Table lacked a default route, and recover the system without panic.
4. **You will control your cloud bills.** You will understand idle costs, data transfer economics, and right-sizing, ensuring your infrastructure is lean, sustainable, and financially sound.
