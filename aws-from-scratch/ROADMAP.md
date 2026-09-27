# Curriculum Roadmap: `aws-from-scratch`

> **Motto:** Understand it. Build it. Observe it. Break it. Recover it. Secure it. Scale it. Cost it. Ship it.

The curriculum is structured into **13 Thematic Modules** comprising **86 Deep Lessons (Phases 00 through 85)**. Every lesson derives cloud infrastructure from computer science primitives, injects deliberate failures, calculates cost vectors, and enforces strict teardown discipline.

---

## High-Level Curriculum Map

```text
Module 00: Cloud Foundations & Global Physical Infrastructure (Phases 00 - 02)
                            ↓
Module 01: Identity, Access Management & Cryptographic Security (Phases 03 - 04)
                            ↓
Module 02: Software-Defined Networking & VPC Architecture (Phases 05 - 12)
                            ↓
Module 03: Virtualized Compute & Persistent Block Storage (Phases 13 - 16)
                            ↓
Module 04: Distributed Object Storage & Edge Content Delivery (Phases 17 - 21)
                            ↓
Module 05: Layer 7 Load Balancing & Horizontal Elasticity (Phases 22 - 25)
                            ↓
Module 06: Managed Relational & Distributed Databases (Phases 26 - 32)
                            ↓
Module 07: Asynchronous Messaging & Event-Driven Systems (Phases 33 - 38)
                            ↓
Module 08: Serverless Compute & Container Orchestration (Phases 39 - 48)
                            ↓
Module 09: Observability, Encryption & Security Operations (Phases 49 - 56)
                            ↓
Module 10: Infrastructure as Code & Automated Reproducibility (Phases 57 - 60)
                            ↓
Module 11: System Reliability, Disaster Recovery & Cost Modeling (Phases 61 - 71)
                            ↓
Module 12: Production Projects, System Evolution & Capstones (Phases 72 - 85)
```

---

## Detailed Phase Breakdown

### Module 00: Cloud Foundations & Global Physical Infrastructure
| Phase | Title | Core Problem | Primitive / CS Concept | AWS Service / API | Hands-on Experiment |
|:---|:---|:---|:---|:---|:---|
| **00** | [Cloud Before AWS](phases/00-cloud-foundations/00-cloud-before-aws/docs/en.md) | Physical servers take weeks to procure; hardware sits idle | Virtualization, Hypervisors (KVM), Time-sharing | Cloud APIs vs Physical Datacenters | Trace hypervisor CPU/RAM scheduling |
| **01** | [AWS Global Infrastructure](phases/00-cloud-foundations/01-aws-global-infrastructure/docs/en.md) | Latency is bounded by speed of light; single DC can lose power | Physical geography, fiber latency, blast radius | Regions, Availability Zones, Edge PoPs | Ping across regions; measure latency |
| **02** | [AWS CLI, APIs, and Console](phases/00-cloud-foundations/02-aws-cli-apis-console/docs/en.md) | Clicking in web consoles is unrepeatable and obscures protocols | Signed HTTPS requests, REST APIs, SigV4 | AWS STS, AWS CLI v2, Boto3 | Inspect raw signed HTTP API payloads |

---

### Module 01: Identity, Access Management & Cryptographic Security
| Phase | Title | Core Problem | Primitive / CS Concept | AWS Service / API | Hands-on Experiment |
|:---|:---|:---|:---|:---|:---|
| **03** | [IAM From First Principles](phases/01-iam-and-security/03-iam-from-first-principles/docs/en.md) | Hardcoded passwords leak; programs need authenticated identity | Cryptographic authorization, Principals, RBAC | IAM Users, Roles, STS AssumeRole | Run `experiments/iam_simulator.py` |
| **04** | [IAM Policies](phases/01-iam-and-security/04-iam-policies/docs/en.md) | Broad admin permissions allow catastrophic data deletion | Boolean logic: Explicit Deny > Allow > Default Deny | JSON Policies, Conditions, SCPs | Deliberately trigger `AccessDenied` |

---

### Module 02: Software-Defined Networking & VPC Architecture
| Phase | Title | Core Problem | Primitive / CS Concept | AWS Service / API | Hands-on Experiment |
|:---|:---|:---|:---|:---|:---|
| **05** | [AWS Networking Before VPC](phases/02-networking-and-vpc/05-aws-networking-before-vpc/docs/en.md) | Need isolated private addressing without overlapping networks | IPv4, CIDR math, subnet masks, RFC 1918 | CIDR notation (`10.0.0.0/16`) | Calculate usable IPs (minus 5 AWS reserved) |
| **06** | [Build a VPC From First Principles](phases/02-networking-and-vpc/06-build-a-vpc-from-scratch/docs/en.md) | Servers need isolated network segment in the cloud | Overlay network, VXLAN encapsulation | Amazon VPC API (`CreateVpc`) | Create custom VPC with zero defaults |
| **07** | [Subnets](phases/02-networking-and-vpc/07-subnets/docs/en.md) | One large network lacks physical failure boundaries | Subnetting, Availability Zone binding | VPC Subnets (`CreateSubnet`) | Subdivide /16 into AZ-A and AZ-B subnets |
| **08** | [Route Tables](phases/02-networking-and-vpc/08-route-tables/docs/en.md) | Packets don't know where to go next | Routing table: destination CIDR -> next-hop | Route Tables, Local Route | Trace local packet hop within VPC |
| **09** | [Internet Gateway](phases/02-networking-and-vpc/09-internet-gateway/docs/en.md) | Private RFC 1918 IPs cannot route on the public internet | 1-to-1 NAT, default route (0.0.0.0/0) | Internet Gateway (IGW) | Attach IGW and add default public route |
| **10** | [Public vs Private Subnets](phases/02-networking-and-vpc/10-public-vs-private-subnets/docs/en.md) | Databases must not be reachable from public internet | Routing topology defines subnet publicity | Public vs Private Subnets | Compare routing tables side-by-side |
| **11** | [Security Groups](phases/02-networking-and-vpc/11-security-groups/docs/en.md) | Exposed ports accept arbitrary malicious TCP packets | Stateful packet filtering at hypervisor ENI | Security Groups (`AuthorizeSecurityGroupIngress`) | Break port rule; observe silent SYN timeout |
| **12** | [Network ACLs](phases/02-networking-and-vpc/12-network-acls/docs/en.md) | Need secondary stateless defense-in-depth boundary | Stateless subnet filtering, ephemeral ports | Network ACLs (NACLs) | Block ephemeral ports; observe return drop |

---

### Module 03: Virtualized Compute & Persistent Block Storage
| Phase | Title | Core Problem | Primitive / CS Concept | AWS Service / API | Hands-on Experiment |
|:---|:---|:---|:---|:---|:---|
| **13** | [EC2 From First Principles](phases/03-compute-and-storage/13-ec2-from-first-principles/docs/en.md) | Need general-purpose virtual machine on demand | Nitro hypervisor, vCPU, RAM, ENI | Amazon EC2 (`RunInstances`) | Launch minimal instance with User Data |
| **14** | [What Happens When EC2 Launches](phases/03-compute-and-storage/14-what-happens-when-ec2-launches/docs/en.md) | Cloud provisioning feels like magic | API request -> scheduler -> host allocation -> boot | EC2 Lifecycle, IMDSv2 metadata | Interrogate `http://169.254.169.254` |
| **15** | [EBS](phases/03-compute-and-storage/15-ebs/docs/en.md) | Instance-store disk data is wiped when instance stops | Network-attached SAN block storage, IOPS | Elastic Block Store (`gp3`, IOPS) | Attach volume, write file, detach & reattach |
| **16** | [AMIs and Immutable Servers](phases/03-compute-and-storage/16-amis-and-immutable-servers/docs/en.md) | Manual server configuration results in snowflake drift | Golden images, immutable infrastructure | Amazon Machine Images (AMI) | Bake configured instance into reusable AMI |

---

### Module 04: Distributed Object Storage & Content Delivery
| Phase | Title | Core Problem | Primitive / CS Concept | AWS Service / API | Hands-on Experiment |
|:---|:---|:---|:---|:---|:---|
| **17** | [S3 From First Principles](phases/04-object-storage-and-cdn/17-s3-from-first-principles/docs/en.md) | Hard drives cannot store petabytes of unstructured files | Distributed HTTP object store, key-value | Amazon S3 (`CreateBucket`, `PutObject`) | Compare object store vs POSIX filesystem |
| **18** | [S3 Operations](phases/04-object-storage-and-cdn/18-s3-operations/docs/en.md) | Managing millions of files via HTTP REST | HTTP verbs (PUT, GET, DELETE, HEAD) | S3 REST APIs, Content-Type, ETags | Inspect HTTP headers and MD5 checksums |
| **19** | [S3 Durability, Versioning, Lifecycle](phases/04-object-storage-and-cdn/19-s3-durability-versioning-lifecycle/docs/en.md) | Accidental file deletion or regulatory retention needs | 11 9's durability, versioning, tiered storage | S3 Versioning, Lifecycle Rules | Recover deleted object using VersionId |
| **20** | [Static Website / Object Delivery](phases/04-object-storage-and-cdn/20-static-website-object-delivery/docs/en.md) | Serving frontend assets securely without public buckets | Origin Access Control (OAC), private origins | S3 + CloudFront OAC | Configure OAC-only private bucket policy |
| **21** | [DNS and Route 53](phases/04-object-storage-and-cdn/21-dns-and-route-53/docs/en.md) | Humans remember domain names, not IP addresses | Authoritative DNS, A/CNAME/ALIAS records | Amazon Route 53 Hosted Zones | Trace DNS resolution tree via `dig` |

---

### Module 05: Load Balancing & Elastic Scaling
| Phase | Title | Core Problem | Primitive / CS Concept | AWS Service / API | Hands-on Experiment |
|:---|:---|:---|:---|:---|:---|
| **22** | [Load Balancing From Scratch](phases/05-load-balancing-and-scaling/22-load-balancing-from-scratch/docs/en.md) | Single server saturates; how does client choose backend? | Reverse proxying, socket multiplexing | Round-robin load balancing | Run `experiments/lb_healthcheck_lab.py` |
| **23** | [ALB](phases/05-load-balancing-and-scaling/23-alb/docs/en.md) | Need Layer 7 path routing, TLS offload, and health checks | HTTP header inspection, target pools | Application Load Balancer (ALB) | Evict failing target; observe zero errors |
| **24** | [Multi-AZ Application](phases/05-load-balancing-and-scaling/24-multi-az-application/docs/en.md) | A fire in one datacenter campus causes complete outage | Multi-datacenter physical redundancy | Cross-zone ALB + Multi-AZ EC2 | Terminate AZ-A instance; verify AZ-B serves |
| **25** | [Auto Scaling](phases/05-load-balancing-and-scaling/25-auto-scaling/docs/en.md) | Traffic surges overwhelm static instance pools | Elastic capacity controllers, target tracking | Auto Scaling Groups (ASG) | Inject CPU load; observe scale-out event |

---

### Module 06: Managed Databases & In-Memory Caching
| Phase | Title | Core Problem | Primitive / CS Concept | AWS Service / API | Hands-on Experiment |
|:---|:---|:---|:---|:---|:---|
| **26** | [RDS From First Principles](phases/06-databases-and-caching/26-rds-from-first-principles/docs/en.md) | Self-managing database OS patching and backup is error-prone | Managed relational engine, automated snapshots | Amazon RDS (PostgreSQL/MySQL) | Provision RDS instance; inspect parameters |
| **27** | [RDS Connectivity](phases/06-databases-and-caching/27-rds-connectivity/docs/en.md) | Database must be reachable by app but invisible to internet | DB Subnet Groups, private SG ingress | DB Subnet Groups, Security Groups | Restrict DB port to App SG ID only |
| **28** | [RDS Multi-AZ and Read Scaling](phases/06-databases-and-caching/28-rds-multi-az-and-read-scaling/docs/en.md) | Conflating high availability with read performance scaling | Synchronous block replication vs async replica | Multi-AZ Standby vs Read Replicas | Simulate primary failover; measure RTO |
| **29** | [DynamoDB From First Principles](phases/06-databases-and-caching/29-dynamodb-from-first-principles/docs/en.md) | Relational databases hit vertical write scaling limits | Distributed B-Tree / LSM, partition hashing | Amazon DynamoDB, Partition Key | Store key-value items with On-Demand billing |
| **30** | [DynamoDB Data Modeling](phases/06-databases-and-caching/30-dynamodb-data-modeling/docs/en.md) | Relational normalization causes table scans in NoSQL | Access-pattern-first single-table design | Composite Keys (PK + SK), GSI | Model 1-to-many relationship in 1 table |
| **31** | [DynamoDB Capacity and Hot Partitions](phases/06-databases-and-caching/31-dynamodb-capacity-hot-partitions/docs/en.md) | Skewed traffic saturates a single storage partition | Consistent hashing, throttling, WCU limits | DynamoDB WCU, Throttling | Run `experiments/hot_partition_lab.py` |
| **32** | [ElastiCache / Managed Redis](phases/06-databases-and-caching/32-elasticache-redis/docs/en.md) | Repetitive database queries exhaust disk I/O | In-memory key-value caching, TTL | Amazon ElastiCache (Redis/Valkey) | Run `benchmarks/benchmark_cache.py` |

---

### Module 07: Asynchronous Messaging & Event-Driven Systems
| Phase | Title | Core Problem | Primitive / CS Concept | AWS Service / API | Hands-on Experiment |
|:---|:---|:---|:---|:---|:---|
| **33** | [Queues Before SQS](phases/07-messaging-and-events/33-queues-before-sqs/docs/en.md) | Downstream outage causes upstream client API failures | FIFO buffer, producer-consumer decoupling | Message Queues, Backpressure | Build Python in-memory queue consumer |
| **34** | [SQS](phases/07-messaging-and-events/34-sqs/docs/en.md) | Messages must survive machine crashes durably | Distributed queue, Visibility Timeout, DLQ | Amazon SQS (`SendMessage`, `ReceiveMessage`) | Run `experiments/sqs_visibility_lab.py` |
| **35** | [Idempotent Consumers](phases/07-messaging-and-events/35-idempotent-consumers/docs/en.md) | Network retries result in duplicate charges | At-least-once delivery, deduplication key | DynamoDB conditional put idempotency | Deduplicate duplicate SQS message receipt |
| **36** | [SNS](phases/07-messaging-and-events/36-sns/docs/en.md) | One event must notify multiple disparate services | Publish/Subscribe, push delivery | Amazon SNS Topics, Subscriptions | Broadcast event to multiple subscribers |
| **37** | [SNS + SQS Fan-Out](phases/07-messaging-and-events/37-sns-sqs-fan-out/docs/en.md) | Pub/sub subscribers crash if offline during broadcast | Buffering each subscriber independently | SNS -> SQS Fan-Out pattern | Publish to SNS; inspect independent queues |
| **38** | [EventBridge](phases/07-messaging-and-events/38-eventbridge/docs/en.md) | Need declarative content-based JSON routing | Event bus, pattern matching, schema registry | Amazon EventBridge Rules & Targets | Route order events by `detail.type` |

---

### Module 08: Serverless Compute & Container Orchestration
| Phase | Title | Core Problem | Primitive / CS Concept | AWS Service / API | Hands-on Experiment |
|:---|:---|:---|:---|:---|:---|
| **39** | [Lambda From First Principles](phases/08-serverless-and-containers/39-lambda-from-first-principles/docs/en.md) | Paying for 24/7 idle servers for infrequent tasks is wasteful | Ephemeral Firecracker micro-VMs, event compute | AWS Lambda (`CreateFunction`) | Deploy minimal function; measure billing ms |
| **40** | [Lambda Lifecycle](phases/08-serverless-and-containers/40-lambda-lifecycle/docs/en.md) | First request suffers latency spike | Cold init vs warm invoke, container reuse | Execution environments, concurrency | Measure cold start vs warm invocation |
| **41** | [API Gateway + Lambda](phases/08-serverless-and-containers/41-api-gateway-lambda/docs/en.md) | Need HTTP endpoint routing directly to serverless function | HTTP reverse proxy, payload transformation | Amazon API Gateway (HTTP API v2) | Deploy REST route backed by Lambda |
| **42** | [Step Functions Concept](phases/08-serverless-and-containers/42-step-functions-concept/docs/en.md) | Multi-step asynchronous workflows fail mid-execution | State machines, saga pattern, retry policies | AWS Step Functions (State Machine) | Trace order saga state transitions |
| **43** | [Containers on AWS](phases/08-serverless-and-containers/43-containers-on-aws/docs/en.md) | Docker container runs locally; where does it run in AWS? | Containerization vs virtualization | Containers in cloud architectures | Package lightweight HTTP app in Docker |
| **44** | [ECR](phases/08-serverless-and-containers/44-ecr/docs/en.md) | Where do private container images live securely? | Docker registry, OCI image distribution | Amazon Elastic Container Registry (ECR) | Build, tag, and push image to private ECR |
| **45** | [ECS](phases/08-serverless-and-containers/45-ecs/docs/en.md) | Container processes crash and need supervision | Task scheduler, desired count reconciliation | Amazon ECS (Task Definition, Service) | Deploy ECS service with 2 tasks |
| **46** | [Fargate](phases/08-serverless-and-containers/46-fargate/docs/en.md) | Managing EC2 clusters for containers is operational overhead | Serverless container capacity provider | ECS Fargate (`awsvpc` network mode) | Run task without managing underlying VMs |
| **47** | [ECS + ALB](phases/08-serverless-and-containers/47-ecs-alb/docs/en.md) | External clients need to access dynamic container tasks | Dynamic host port mapping, target group sync | ECS Service + ALB Target Group | Kill container task; watch ECS launch new one |
| **48** | [Kubernetes / EKS Overview](phases/08-serverless-and-containers/48-kubernetes-eks-overview/docs/en.md) | When is Kubernetes complexity justified over ECS? | Managed K8s control plane vs native ECS | Amazon EKS vs ECS tradeoffs | Reason through K8s vs ECS decision tree |

---

### Module 09: Observability, Security Operations & Governance
| Phase | Title | Core Problem | Primitive / CS Concept | AWS Service / API | Hands-on Experiment |
|:---|:---|:---|:---|:---|:---|
| **49** | [CloudWatch](phases/09-observability-and-security/49-cloudwatch/docs/en.md) | Black-box systems fail silently without operator awareness | Time-series metrics, dimensional telemetry | Amazon CloudWatch Metrics | Publish custom application metric |
| **50** | [CloudWatch Logs](phases/09-observability-and-security/50-cloudwatch-logs/docs/en.md) | Logs scattered across 50 servers are lost on termination | Centralized log ingestion, retention policies | CloudWatch Log Groups & Streams | Set 7-day retention; query via Insights |
| **51** | [Metrics and Alarms](phases/09-observability-and-security/51-metrics-and-alarms/docs/en.md) | Engineers learn about outages from angry customer tweets | Threshold alerting, breached evaluation periods | CloudWatch Alarms (`PutMetricAlarm`) | Trigger synthetic error spike; verify alarm |
| **52** | [Distributed Tracing](phases/09-observability-and-security/52-distributed-tracing/docs/en.md) | Cannot find which microservice caused a 3-second delay | Trace ID propagation, spans, service graphs | AWS X-Ray / OpenTelemetry | Propagate `X-Amzn-Trace-Id` header |
| **53** | [Secrets Management](phases/09-observability-and-security/53-secrets-management/docs/en.md) | Storing database passwords in Git repositories is fatal | Secure secret storage, automated rotation | AWS Secrets Manager, SSM Parameter Store | Fetch secret dynamically via IAM role |
| **54** | [Encryption and KMS](phases/09-observability-and-security/54-encryption-kms/docs/en.md) | Data at rest stolen if physical drive is seized | Hardware Security Module, envelope encryption | AWS KMS (Customer Managed Key) | Encrypt plaintext data using KMS key |
| **55** | [CloudFront](phases/09-observability-and-security/55-cloudfront/docs/en.md) | Long round-trip times to origin server | Anycast routing, edge reverse proxy, caching | Amazon CloudFront Distributions | Inspect cache headers (`X-Cache: Hit`) |
| **56** | [WAF and Edge Security](phases/09-observability-and-security/56-waf-edge-security/docs/en.md) | Layer 7 SQL injection and DDoS attacks reach servers | Layer 7 Web Application Firewall rules | AWS WAF WebACLs, Rate Limiting | Block client after 100 requests/5min |

---

### Module 10: Infrastructure as Code & Automated Reproducibility
| Phase | Title | Core Problem | Primitive / CS Concept | AWS Service / API | Hands-on Experiment |
|:---|:---|:---|:---|:---|:---|
| **57** | [Infrastructure as Code](phases/10-infrastructure-as-code/57-infrastructure-as-code/docs/en.md) | Manual clicking produces snowflakes that cannot be audited | Declarative configuration, idempotent graphs | IaC Primitives (CloudFormation/Terraform) | Compare imperative scripts vs declarative code |
| **58** | [IaC Fundamentals](phases/10-infrastructure-as-code/58-iac-fundamentals/docs/en.md) | Need state management and dependency resolution | Directed Acyclic Graph (DAG) of resources | CloudFormation Template Stacks | Deploy minimal stack; inspect change sets |
| **59** | [Rebuild VPC With IaC](phases/10-infrastructure-as-code/59-rebuild-vpc-with-iac/docs/en.md) | Manually created VPC cannot be reproduced in testing | Code-defined networking | `infrastructure/vpc-dual-az-baseline.yaml` | Deploy and teardown complete VPC in 3 mins |
| **60** | [Rebuild Application Stack With IaC](phases/10-infrastructure-as-code/60-rebuild-app-stack-iac/docs/en.md) | Application dependencies must deploy as a unified stack | Multi-tier orchestration | `infrastructure/serverless-api.yaml` | Deploy API Gateway + Lambda + DDB via CLI |

---

### Module 11: System Reliability, Disaster Recovery & Cost Modeling
| Phase | Title | Core Problem | Primitive / CS Concept | AWS Service / API | Hands-on Experiment |
|:---|:---|:---|:---|:---|:---|
| **61** | [Reliability From First Principles](phases/11-reliability-and-cost/61-reliability-first-principles/docs/en.md) | Hardware components have a non-zero MTBF | Mean Time To Failure (MTTF), blast radius | Failure Domains & Redundancy | Enumerate single points of failure |
| **62** | [Multi-AZ Reliability](phases/11-reliability-and-cost/62-multi-az-reliability/docs/en.md) | Whole datacenter facility failure | Independent power/cooling/transit zones | Multi-AZ Architecture | Model AZ failure and failover dynamics |
| **63** | [Backup vs Replication](phases/11-reliability-and-cost/63-backup-vs-replication/docs/en.md) | Replication instantly copies a `DROP TABLE` command! | Point-in-time recovery vs live replication | Snapshots (EBS/RDS) vs Replicas | Restore database from point-in-time snapshot |
| **64** | [RTO and RPO](phases/11-reliability-and-cost/64-rto-and-rpo/docs/en.md) | Businesses need quantified downtime/data loss bounds | Recovery Time Objective, Recovery Point Objective | Disaster Recovery Tiers | Calculate RTO/RPO for backup vs standby |
| **65** | [Disaster Recovery](phases/11-reliability-and-cost/65-disaster-recovery/docs/en.md) | Regional catastrophe (earthquake / power grid failure) | Backup/Restore, Pilot Light, Warm Standby | Cross-Region Replication concepts | Design cross-region recovery strategy |
| **66** | [Cost From First Principles](phases/11-reliability-and-cost/66-cost-from-first-principles/docs/en.md) | Cloud bills spiral without resource consumption models | Idle time vs request volume vs data transfer | AWS Billing Dimensions | Deconstruct AWS monthly cost statement |
| **67** | [AWS Pricing Exercise](phases/11-reliability-and-cost/67-aws-pricing-exercise/docs/en.md) | Estimates based on guesswork lead to 10x cost overruns | Parametric modeling, AWS Pricing Calculator | Official Pricing Calculator | Model 10M request web app monthly cost |
| **68** | [Cost Optimization](phases/11-reliability-and-cost/68-cost-optimization/docs/en.md) | Paying for over-provisioned, idle cloud capacity | Right-sizing, Graviton, Savings Plans, TTLs | AWS Compute Optimizer, Lifecycle | Identify and terminate orphaned EBS/EIPs |
| **69** | [Tagging and Resource Inventory](phases/11-reliability-and-cost/69-tagging-resource-inventory/docs/en.md) | Cannot attribute costs or find rogue resources | Metadata tagging, cost allocation tags | Resource Groups, Tagging API | Run `./scripts/list-lab-resources.sh` |
| **70** | [Shared Responsibility Model](phases/11-reliability-and-cost/70-shared-responsibility-model/docs/en.md) | Customers assume AWS secures OS and application data | Security OF the cloud vs Security IN the cloud | AWS Compliance Boundaries | Map who patches OS vs who secures S3 |
| **71** | [Well-Architected Review](phases/11-reliability-and-cost/71-well-architected-review/docs/en.md) | Architecture passes happy-path tests but fails audits | 6 Pillars: Ops, Security, Reliability, Perf, Cost, Sus | AWS Well-Architected Tool | Conduct 6-pillar audit on lab system |

---

### Module 12: Production Projects, System Evolution & Capstones
| Phase | Title | Core Problem | Primitive / CS Concept | Project Directory | Key Artifact |
|:---|:---|:---|:---|:---|:---|
| **72** | [Project: Static Web Architecture](phases/12-projects-and-capstones/72-project-static-web/docs/en.md) | Fast, secure global frontend hosting with zero servers | Edge caching, OAC, private origin | `projects/project-01-static-web` | Private S3 + CloudFront Distribution |
| **73** | [Project: Highly Available Web App](phases/12-projects-and-capstones/73-project-ha-webapp/docs/en.md) | Scalable resilient 3-tier web application | Multi-AZ ALB, stateless ASG, RDS Multi-AZ | `projects/project-02-ha-webapp` | Multi-AZ Web Stack Architecture |
| **74** | [Project: Serverless API](phases/12-projects-and-capstones/74-project-serverless-api/docs/en.md) | Zero-idle-cost transactional API with high elasticity | Micro-VM compute, NoSQL single-table | `projects/project-03-serverless-api` | API Gateway + Lambda + DynamoDB |
| **75** | [Project: Event-Driven System](phases/12-projects-and-capstones/75-project-event-driven/docs/en.md) | Asynchronous decoupled microservices | Pub/Sub, queue buffering, poison redrive | `projects/project-04-event-driven` | SNS + SQS Fan-Out Cluster |
| **76** | [Project: Containerized Production App](phases/12-projects-and-capstones/76-project-container-prod/docs/en.md) | Container orchestration without VM management | Fargate serverless tasks, private subnets | `projects/project-05-container-prod` | ECS Fargate + ALB + RDS + Secrets |
| **77** | [Project: Data Ingestion Architecture](phases/12-projects-and-capstones/77-project-data-ingestion/docs/en.md) | High-throughput streaming data into queryable lake | Partition logging, micro-batching, columnar S3 | `projects/project-06-data-ingestion` | Kinesis/Firehose -> S3 Data Lake |
| **78** | [Architecture Evolution](phases/12-projects-and-capstones/78-architecture-evolution/docs/en.md) | Evolving from 100 users to 10M users incrementally | Bottleneck identification, scaling bottlenecks | Systematic Architecture Walkthrough | Evolution decision matrix |
| **79** | [AWS Anti-Patterns](phases/12-projects-and-capstones/79-aws-anti-patterns/docs/en.md) | Common cloud architectural mistakes and footguns | Premature complexity, exposed endpoints | Anti-Pattern Analysis Guide | 20 Anti-Patterns and Remedies |
| **80** | [When NOT to Use an AWS Service](phases/12-projects-and-capstones/80-when-not-to-use-aws-service/docs/en.md) | Managed service != automatically correct choice | Simplicity, operational fit, cost cliffs | Service Selection Guardrails | When to pick simple alternatives |
| **81** | [Build a Tiny Cloud Simulator](phases/12-projects-and-capstones/81-build-tiny-cloud-simulator/docs/en.md) | Demystifying cloud APIs as plain software wrappers | In-memory registries, mock APIs | `projects/project-07-tiny-cloud-simulator` | Fully working local Python cloud |
| **82** | [Production-Like AWS Capstone](phases/12-projects-and-capstones/82-production-capstone/docs/en.md) | Complete enterprise-grade production architecture | Comprehensive 6-pillar synthesis | `projects/project-08-production-capstone` | Full production architecture package |
| **83** | [Failure Day](phases/12-projects-and-capstones/83-failure-day/docs/en.md) | Chaos testing and disaster diagnosis | Fault injection, observability verification | `experiments/failure_day.py` | 7 Chaos failure experiments |
| **84** | [Architecture From Requirements](phases/12-projects-and-capstones/84-architecture-from-requirements/docs/en.md) | Derive infrastructure from business constraints | Numbers -> primitives -> services | Architectural Design Challenge | Complete architectural specification |
| **85** | [Final Mental Model](phases/12-projects-and-capstones/85-final-mental-model/docs/en.md) | The ultimate realization: AWS is no longer a mystery | Unified systems understanding | End-to-end trace from finger to disk | The First-Principles Cloud Engineer |
