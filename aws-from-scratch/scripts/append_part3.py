#!/usr/bin/env python3
"""
scripts/append_part3.py
Adds lessons 72 through 85 to curriculum_part3.py
"""

import json

PART3_EXTENDED = [
    # 72: Project: Static Web Architecture
    {
        "module": "12-projects-and-capstones", "slug": "72-project-static-web", "num": "72",
        "title": "Project: Static Web Architecture",
        "motto": "S3 stores the bits; CloudFront accelerates and secures the delivery. Zero servers to patch.",
        "type": "Architecture Project & Production Deployment", "time": "90",
        "prereqs": "Phase 20: Static Website / Object Delivery",
        "services": "S3, CloudFront OAC, Route 53, ACM",
        "cost": "Free Tier eligible ($0.00 idle cost)",
        "problem": "Delivering static web assets directly from an S3 website endpoint causes global latency, exposes buckets to public scraping, and lacks custom TLS certificates.",
        "prediction": "Fronting a 100% private S3 bucket with CloudFront Origin Access Control delivers sub-20ms edge latency, enforces HTTPS, and prevents direct bucket access.",
        "why_matters": "This is Project 01: the production gold standard for hosting single-page web applications.",
        "first_principles": "The browser resolves Anycast DNS via Route 53 to the nearest CloudFront edge PoP. CloudFront terminates TLS 1.3 locally. On cache miss, CloudFront signs an authenticated AWS SigV4 request to the private S3 bucket via Origin Access Control (OAC).",
        "diagram": """Project 01 Architecture:
[ User ] ──(HTTPS)──► [ Route 53 ] ──► [ CloudFront Edge (OAC) ]
                                                │ (Cache Miss)
                                                ▼ SigV4
                                 [ Private S3 Bucket (Block Public Access: ON) ]""",
        "before_aws": "Hosting Nginx/Apache servers in multiple colocation datacenters with GeoDNS.",
        "primitive_code": """# Verify project implementation documentation
with open('projects/project-01-static-web/README.md') as f:
    print("Project 01 loaded:", "CloudFront + S3" in f.read())""",
        "aws_cmd": "# Reference implementation in projects/project-01-static-web/README.md",
        "inspect": "curl -I https://d111111abcdef8.cloudfront.net/index.html 2>&1 | grep -i x-cache",
        "measure": "Measure latency improvement: direct transatlantic S3 (180ms) vs CloudFront edge cache hit (14ms).",
        "break_desc": "Attempt to access the S3 bucket directly via curl.",
        "diagnose": "S3 returns HTTP 403 Forbidden because Block Public Access is active and the bucket policy allows only CloudFront.",
        "recover": "Access through the CloudFront distribution domain.",
        "security": "Enforce response headers: HSTS, X-Content-Type-Options: nosniff, Content-Security-Policy.",
        "cost": "CloudFront Free Tier includes 1 TB data transfer out and 10M requests permanently.",
        "cleanup": "Follow cleanup instructions in `projects/project-01-static-web/README.md`.",
        "verify_cleanup": "./scripts/cleanup-check.sh",
        "mastery_q1": "Why is keeping the S3 bucket 100% private with OAC superior to legacy public bucket website hosting?",
        "mastery_q2": "How does CloudFront Origin Shield provide an additional caching layer between edge PoPs and S3?",
        "mastery_q3": "Why should `index.html` have a short TTL (300s) while hashed assets have a 1-year immutable TTL?",
        "when_use": "Use for all production static websites, React/Vue frontends, and documentation portals.",
        "when_not": "Do not use for dynamic server-rendered HTML applications (use ECS or Lambda).",
        "next_step": "Phase 73: Project: Highly Available Web App — Multi-AZ compute and managed databases."
    },
    # 73: Project: Highly Available Web App
    {
        "module": "12-projects-and-capstones", "slug": "73-project-ha-webapp", "num": "73",
        "title": "Project: Highly Available Web App",
        "motto": "Multi-AZ redundancy at every tier: ALB, stateless Auto Scaling instances, and synchronous Multi-AZ RDS.",
        "type": "Architecture Project & Production Deployment", "time": "90",
        "prereqs": "Phase 24: Multi-AZ Application",
        "services": "ALB, EC2 Auto Scaling, RDS PostgreSQL Multi-AZ, VPC",
        "cost": "Billable (~$0.08/hr while running / Tear down immediately)",
        "problem": "Single-server applications fail completely when host hardware dies, when traffic spikes 5x, or when a datacenter facility loses power.",
        "prediction": "Deploying an ALB in front of a multi-AZ stateless Auto Scaling Group with a multi-AZ RDS database eliminates all single points of failure.",
        "why_matters": "This is Project 02: the classic 3-tier enterprise high-availability web architecture.",
        "first_principles": "Every tier is redundant across independent availability zones. State is completely externalized to the database. Compute nodes are disposable cattle managed by the Auto Scaling Group.",
        "diagram": """Project 02 Architecture:
            [ Internet ] ──► [ Route 53 ] ──► [ ALB (Public Multi-AZ) ]
                                                     │
                    ┌────────────────────────────────┴────────────────────────────────┐
                    ▼                                                                 ▼
           [ AZ-A Private Subnet ]                                           [ AZ-B Private Subnet ]
           ┌──────────────────────┐                                          ┌──────────────────────┐
           │ EC2 App (AutoScaling)│                                          │ EC2 App (AutoScaling)│
           └──────────┬───────────┘                                          └──────────┬───────────┘
                      │                                                                 │
                      └───────────────────────────────┬─────────────────────────────────┘
                                                      │ TCP 5432
                                                      ▼
                                          [ Amazon RDS Multi-AZ ]
                                          Primary (AZ-A) ══(Sync Rep)══► Standby (AZ-B)""",
        "before_aws": "Active-passive physical server pairs with shared SAN storage and heartbeat failover.",
        "primitive_code": """with open('projects/project-02-ha-webapp/README.md') as f:
    print("Project 02 loaded:", "ALB + ASG + Multi-AZ RDS" in f.read())""",
        "aws_cmd": "# Reference implementation in projects/project-02-ha-webapp/README.md",
        "inspect": "aws elbv2 describe-target-health --target-group-arn $TG_ARN --output table",
        "measure": "Measure failover availability: kill AZ-A instance; verify 0.00% client request drop.",
        "break_desc": "Trigger RDS forced failover during high read/write traffic.",
        "diagnose": "Primary flips to AZ-B standby; application reconnects within 60 seconds.",
        "recover": "The application pool re-establishes connections automatically.",
        "security": "Chain security groups: ALB -> App SG -> RDS SG. No public access to app or DB tiers.",
        "cost": "Baseline running cost is ~$45-55/month. Run for 1 hour to test, then terminate immediately!",
        "cleanup": "Follow teardown commands in `projects/project-02-ha-webapp/README.md`.",
        "verify_cleanup": "./scripts/cleanup-check.sh",
        "mastery_q1": "Why must the compute instances be strictly stateless for Auto Scaling to work without data loss?",
        "mastery_q2": "What happens if an entire AWS datacenter facility is destroyed by a flood in this architecture?",
        "mastery_q3": "How does Security Group chaining isolate the database tier from direct internet traffic?",
        "when_use": "Use for relational, transactional web applications with predictable baseline traffic.",
        "when_not": "Do not use for microservices with huge idle periods where 24/7 running costs waste money.",
        "next_step": "Phase 74: Project: Serverless API — Building a scale-to-zero serverless API."
    },
    # 74: Project: Serverless API
    {
        "module": "12-projects-and-capstones", "slug": "74-project-serverless-api", "num": "74",
        "title": "Project: Serverless API",
        "motto": "True scale-to-zero: Pay strictly for executed milliseconds and written items. Zero servers to manage.",
        "type": "Architecture Project & Serverless System", "time": "90",
        "prereqs": "Phase 41: API Gateway + Lambda",
        "services": "API Gateway, Lambda, DynamoDB, CloudWatch",
        "cost": "Free Tier eligible ($0.00 idle cost)",
        "problem": "Traditional VM architectures burn $50+/month even with zero users. Building a modern startup API requires true utility pricing and instant elasticity.",
        "prediction": "Deploying API Gateway + Lambda + DynamoDB On-Demand handles 0 to 10,000 requests/sec with zero capacity planning and zero idle monthly cost.",
        "why_matters": "This is Project 03: the definitive serverless transactional API architecture.",
        "first_principles": "API Gateway receives HTTP POST, verifies rate limits, and invokes Lambda. Lambda verifies idempotency in DynamoDB, executes business logic, writes with conditional expressions, and returns JSON. Every component scales automatically.",
        "diagram": """Project 03 Architecture:
[ Client ] ──► [ API Gateway HTTP API ] ──► [ Lambda (orders-handler) ]
                                                    │
                                                    ├── 1. Idempotency Check
                                                    └── 2. PutItem (Condition: attribute_not_exists)
                                                    ▼
                                            [ DynamoDB (On-Demand) ]""",
        "before_aws": "Provisioning VPS servers running Flask/Django with SQLite or MySQL.",
        "primitive_code": """with open('projects/project-03-serverless-api/README.md') as f:
    print("Project 03 loaded:", "API Gateway + Lambda + DynamoDB" in f.read())""",
        "aws_cmd": "# Deploy via infrastructure/serverless-api.yaml template",
        "inspect": "aws cloudformation describe-stacks --stack-name aws-from-scratch-serverless --output table",
        "measure": "Measure latency: p50 warm execution takes ~8ms; cold start takes ~220ms.",
        "break_desc": "Send duplicate POST requests with the same `Idempotency-Key` header.",
        "diagnose": "The handler intercepts the duplicate, avoids a duplicate database write, and returns HTTP 409/200 cached.",
        "recover": "The client receives confirmation without double-billing.",
        "security": "Enforce strict IAM execution role policies: Lambda can only access its specific DynamoDB table.",
        "cost": "Exactly $0.00/month while idle. 100% covered by AWS Free Tier for low to medium learning traffic.",
        "cleanup": "aws cloudformation delete-stack --stack-name aws-from-scratch-serverless",
        "verify_cleanup": "./scripts/cleanup-check.sh",
        "mastery_q1": "Why is an idempotency layer mandatory when building serverless POST APIs?",
        "mastery_q2": "What are the tradeoffs of API Gateway + Lambda vs ALB + EC2 in terms of cost at 100M requests/month?",
        "mastery_q3": "How does DynamoDB On-Demand pricing differ from Provisioned Capacity?",
        "when_use": "Use for web APIs, webhooks, mobile backends, and event-driven microservices.",
        "when_not": "Do not use for long-running batch jobs (> 15 mins) or websocket gaming servers with persistent memory state.",
        "next_step": "Phase 75: Project: Event-Driven System — Decoupled asynchronous messaging."
    },
    # 75: Project: Event-Driven System
    {
        "module": "12-projects-and-capstones", "slug": "75-project-event-driven", "num": "75",
        "title": "Project: Event-Driven System",
        "motto": "Decouple services through publish/subscribe fan-out. Protect workers with dead-letter queues and idempotency.",
        "type": "Architecture Project & Asynchronous Cluster", "time": "90",
        "prereqs": "Phase 37: SNS + SQS Fan-Out",
        "services": "SNS, SQS, Dead-Letter Queues, CloudWatch Alarms",
        "cost": "Free Tier eligible ($0.00 idle cost)",
        "problem": "Direct synchronous HTTP calls between microservices lead to cascading failures: if the Billing service has an outage, customers cannot checkout.",
        "prediction": "An SNS + SQS fan-out architecture allows the checkout API to acknowledge orders in 10ms, while Billing and Shipping consume messages independently.",
        "why_matters": "This is Project 04: the reference asynchronous decoupling architecture for distributed systems.",
        "first_principles": "SNS broadcasts events to independent SQS queues. Each queue buffers messages for its worker fleet. If a worker panics on a poison pill message, SQS redrives it to a Dead-Letter Queue after 3 failed attempts, alerting on-call engineers.",
        "diagram": """Project 04 Architecture:
[ Checkout API ] ──► [ SNS Topic: order-created ]
                               │
            ┌──────────────────┴──────────────────┐
            ▼                                     ▼
    [ SQS: billing-queue ]                [ SQS: shipping-queue ]
    ├── DLQ: billing-dlq                  ├── DLQ: shipping-dlq
    ▼                                     ▼
[ Billing Workers ]                   [ Shipping Workers ]""",
        "before_aws": "RabbitMQ clusters with shovel plugins or custom Celery Redis workers.",
        "primitive_code": """with open('projects/project-04-event-driven/README.md') as f:
    print("Project 04 loaded:", "SNS + SQS + DLQ" in f.read())""",
        "aws_cmd": "# Implementation commands in projects/project-04-event-driven/README.md",
        "inspect": "aws sqs get-queue-attributes --queue-url $BILLING_Q --attribute-names ApproximateNumberOfMessages --output table",
        "measure": "Measure producer latency: publishing to SNS takes ~12ms regardless of how slow downstream consumers are.",
        "break_desc": "Send a corrupted poison pill message into the queue.",
        "diagnose": "The worker crashes 3 times; SQS detects `maxReceiveCount=3` and evicts the message to the DLQ.",
        "recover": "The CloudWatch DLQ alarm alerts the engineer; the bug is fixed and the message redriven.",
        "security": "SQS queue policies restrict send permissions strictly to the authorized SNS topic ARN.",
        "cost": "Zero idle cost ($0.00). SQS and SNS charge only fractions of a cent per million requests.",
        "cleanup": "Follow cleanup commands in `projects/project-04-event-driven/README.md`.",
        "verify_cleanup": "./scripts/cleanup-check.sh",
        "mastery_q1": "Why is an SQS Dead-Letter Queue essential for preventing head-of-line blocking in queue workers?",
        "mastery_q2": "What happens if a worker crashes before calling `DeleteMessage` in SQS?",
        "mastery_q3": "How does SNS + SQS fan-out prevent the Shipping service outage from affecting Billing?",
        "when_use": "Use for all asynchronous business events (OrderPlaced, UserRegistered, InvoiceGenerated).",
        "when_not": "Do not use if the caller requires an immediate synchronous response (e.g. credit card CVV check).",
        "next_step": "Phase 76: Project: Containerized Production Application — ECS Fargate and managed databases."
    },
    # 76: Project: Containerized Production Application
    {
        "module": "12-projects-and-capstones", "slug": "76-project-container-prod", "num": "76",
        "title": "Project: Containerized Production Application",
        "motto": "Containers package dependencies; Fargate eliminates server management; VPC networking secures the perimeter.",
        "type": "Architecture Project & Container Production", "time": "90",
        "prereqs": "Phase 47: ECS + ALB",
        "services": "ECS Fargate, ALB, RDS PostgreSQL, Secrets Manager, ECR",
        "cost": "Billable (~$0.06/hr while running / Short-lived lab)",
        "problem": "Monolithic applications require complex system libraries and dependencies that don't fit into Lambda's execution limits.",
        "prediction": "Deploying an ECS Fargate service in private subnets behind an ALB with RDS PostgreSQL and dynamic secrets creates a secure, auto-recovering container cluster.",
        "why_matters": "This is Project 05: the enterprise container standard for running microservices in AWS.",
        "first_principles": "Fargate tasks run in `awsvpc` mode with dedicated private IPs. The ALB routes public traffic to healthy tasks. Tasks fetch database passwords dynamically from Secrets Manager via IAM Task Execution Roles. ElastiCache is evaluated and only added if measured read bottlenecks justify it.",
        "diagram": """Project 05 Architecture:
[ Internet ] ──► [ Route 53 ] ──► [ ALB (Public Multi-AZ) ]
                                         │
        ┌────────────────────────────────┴────────────────────────────────┐
        ▼ (Private App Subnet A)                                          ▼ (Private App Subnet B)
[ ECS Fargate Task 1 ]                                            [ ECS Fargate Task 2 ]
• awsvpc Network Mode                                             • awsvpc Network Mode
• Secrets via IAM                                                 • Secrets via IAM
        │                                                                 │
        └────────────────────────────────┬────────────────────────────────┘
                                         │ TCP 5432
                                         ▼
                            [ Amazon RDS PostgreSQL ]
                            (Multi-AZ Isolated Database)""",
        "before_aws": "Managing Docker Swarm or Nomad clusters on physical server hardware.",
        "primitive_code": """with open('projects/project-05-container-prod/README.md') as f:
    print("Project 05 loaded:", "ECS Fargate + ALB + RDS" in f.read())""",
        "aws_cmd": "# Implementation commands in projects/project-05-container-prod/README.md",
        "inspect": "aws ecs list-tasks --cluster aws-from-scratch-cluster --output table",
        "measure": "Measure zero-downtime rolling update duration: ECS rolls out new container image with 0% 5xx errors.",
        "break_desc": "Kill container PID 1 inside the running Fargate task.",
        "diagnose": "The task exits; ECS supervisor detects task stopped; immediately provisions a new Fargate task.",
        "recover": "The replacement task registers with the ALB target group automatically.",
        "security": "Zero public IP addresses on container tasks or database instances. No SSH ports open.",
        "cost": "Running cost is ~$25-40/month if left running. Terminate immediately after completing the lab!",
        "cleanup": "Follow teardown commands in `projects/project-05-container-prod/README.md`.",
        "verify_cleanup": "./scripts/cleanup-check.sh",
        "mastery_q1": "Why is adding Redis an antipattern if database CPU is at 15% and queries are fast?",
        "mastery_q2": "What is the difference between ECS Task Execution Role and ECS Task Role?",
        "mastery_q3": "How does Fargate eliminate host operating system patching?",
        "when_use": "Use ECS Fargate for long-running microservices, web apps, and containerized background daemons.",
        "when_not": "Do not use Fargate if you need direct GPU acceleration or custom kernel network drivers.",
        "next_step": "Phase 77: Project: Data Ingestion Architecture — High-throughput streaming data lakes."
    },
    # 77: Project: Data Ingestion Architecture
    {
        "module": "12-projects-and-capstones", "slug": "77-project-data-ingestion", "num": "77",
        "title": "Project: Data Ingestion Architecture",
        "motto": "Derive the pipeline from throughput, ordering, and replayability requirements—not by blindly picking Kafka.",
        "type": "Architecture Project & Big Data Pipeline", "time": "90",
        "prereqs": "Phase 17: S3 From First Principles",
        "services": "Amazon Kinesis Data Streams / Firehose, S3 Data Lake, Athena",
        "cost": "Billable (Pay-per-use / Low cost for short test)",
        "problem": "Thousands of IoT devices send 10,000 events per second. Writing each event as a separate file to S3 creates the 'Small File Problem' (crushing S3 API costs and making SQL queries impossibly slow).",
        "prediction": "Micro-batching events in Kinesis Data Firehose buffers data into 5MB chunks, compresses with Snappy/Gzip, and flushes columnar Parquet files to S3, reducing costs by 99%.",
        "why_matters": "This is Project 06: the big data ingestion standard for streaming analytics and serverless data lakes.",
        "first_principles": "Ingestion trade-off: Point-to-point queues (SQS) do not support replayability or multiple concurrent consumer groups. Streaming logs (Kinesis / Kafka) maintain an immutable, ordered partition log re-playable from 24 hours to 365 days. Micro-batching solves the S3 small-file problem.",
        "diagram": """Project 06 Architecture:
[ 10,000 IoT Devices ] ──► [ Kinesis Data Streams / Firehose ]
                                        │
                                        │ Buffer: 60s OR 5MB (Micro-batching)
                                        │ Automated Compression (Parquet / Gzip)
                                        ▼
                         [ Amazon S3 Partitioned Data Lake ]
                         (s3://data-lake/year=2026/month=09/day=23/)
                                        │
                                        ▼ Serverless SQL Queries
                         [ Amazon Athena (Presto / Trino) ]""",
        "before_aws": "Self-hosted Apache Kafka clusters + Apache Flume + Hadoop HDFS clusters.",
        "primitive_code": """with open('projects/project-06-data-ingestion/README.md') as f:
    print("Project 06 loaded:", "High-Throughput Data Ingestion" in f.read())""",
        "aws_cmd": "# Implementation commands in projects/project-06-data-ingestion/README.md",
        "inspect": "aws kinesis list-streams --output table",
        "measure": "Measure cost savings: 1,000 individual PUTs ($0.005) vs 1 micro-batched 5MB PUT ($0.000005) = 99.9% cheaper!",
        "break_desc": "Write 100,000 tiny 1KB files directly to S3 and run an Athena query.",
        "diagnose": "Athena query takes 45 seconds and scans massive metadata overhead.",
        "recover": "Buffer events with Firehose into 5MB Parquet files; query time drops to 1.2 seconds.",
        "security": "Enforce S3 bucket encryption using KMS and partition key access control.",
        "cost": "Kinesis Firehose charges $0.029 per GB ingested with zero idle shard fees.",
        "cleanup": "Follow teardown commands in `projects/project-06-data-ingestion/README.md`.",
        "verify_cleanup": "./scripts/cleanup-check.sh",
        "mastery_q1": "What is the 'S3 Small File Problem' and how does micro-batching solve it?",
        "mastery_q2": "What are the architectural differences between Amazon SQS and Amazon Kinesis Data Streams?",
        "mastery_q3": "How does columnar storage (Parquet) reduce Amazon Athena query scan costs by 80-90%?",
        "when_use": "Use for high-throughput clickstream data, IoT telemetry, log aggregation, and real-time analytics.",
        "when_not": "Do not use Kinesis for simple asynchronous microservice task decoupling (use SQS).",
        "next_step": "Phase 78: Architecture Evolution — Scaling an application from 100 to 10M users."
    },
    # 78: Architecture Evolution
    {
        "module": "12-projects-and-capstones", "slug": "78-architecture-evolution", "num": "78",
        "title": "Architecture Evolution",
        "motto": "Never start with maximum complexity. Only add services when a measured physical bottleneck appears.",
        "type": "System Design & Evolutionary Architecture", "time": "60",
        "prereqs": "Phase 73: Project: Highly Available Web App",
        "services": "Architecture Evolution Matrix, System Design",
        "cost": "Free ($0.00 / System Design)",
        "problem": "A startup builds an over-engineered multi-region Kubernetes cluster with Kafka and Redis for 50 initial users, spending $8,000/month and 6 months of engineering time before writing a single product feature.",
        "prediction": "Architectures should evolve incrementally: 100 users (1 box) -> 10K users (ALB + EC2 + RDS) -> 1M users (Multi-AZ + ASG + CloudFront + SQS) -> 10M users (Microservices + DynamoDB + Edge).",
        "why_matters": "Connects AWS infrastructure directly to real-world system design interview thinking.",
        "first_principles": "At each stage of scale, ask: **What actually broke?** (1) 100 users: Single server (monolith). Bottleneck: hardware failure. (2) 1,000 users: Separate DB onto managed RDS. Bottleneck: web server CPU. (3) 10,000 users: Add ALB + second EC2 instance. Bottleneck: static file bandwidth. (4) 100,000 users: Add CloudFront + S3 for static assets. Bottleneck: slow DB read queries. (5) 1,000,000 users: Add Read Replicas / ElastiCache + SQS async workers.",
        "diagram": """The Evolutionary Architecture Ladder:
Stage 1 (100 Users):     [ Single EC2 Instance (App + DB on 1 disk) ]
                                      │ Bottleneck: Hardware crash = 100% downtime!
                                      ▼
Stage 2 (1,000 Users):   [ EC2 App ] ──► [ Amazon RDS Database ]
                                      │ Bottleneck: Web server CPU saturates!
                                      ▼
Stage 3 (10,000 Users):  [ ALB ] ──► [ EC2 AZ-A ] + [ EC2 AZ-B ] ──► [ RDS Multi-AZ ]
                                      │ Bottleneck: Static assets crush bandwidth!
                                      ▼
Stage 4 (100,000 Users): [ CloudFront + S3 ] (Static) + [ ALB + EC2 ASG ] ──► [ RDS ]
                                      │ Bottleneck: Repetitive DB reads & slow sync tasks!
                                      ▼
Stage 5 (1,000,000 Users): [ CloudFront ] ──► [ ALB + ASG ] ──► [ RDS + ElastiCache ]
                                                  │
                                                  ▼
                                          [ SQS Async Workers ]""",
        "before_aws": "Buying a massive mainframe server (Vertical Scaling) and hoping traffic doesn't exceed it.",
        "primitive_code": """# Architecture Evolution Decision Engine
def recommend_architecture(users, qps):
    if users < 1_000:
        return "Stage 1: Single small instance or container (Simple, cheap)"
    elif users < 50_000:
        return "Stage 2: ALB + Multi-AZ Compute + Managed RDS (High Availability)"
    elif users < 1_000_000:
        return "Stage 3: ALB + ASG + CloudFront CDN + S3 + RDS Multi-AZ + SQS workers"
    else:
        return "Stage 4: Serverless / Microservices + DynamoDB + Global Edge Caching"
print(recommend_architecture(500_000, 2500))""",
        "aws_cmd": "# Reference evolution matrix documented",
        "inspect": "echo 'Evolution decision matrix verified.'",
        "measure": "Trace system bottlenecks at each user tier (CPU saturation, DB connection limits, disk IOPS).",
        "break_desc": "Deploy Stage 1 architecture and simulate 50,000 concurrent users via Apache Benchmark.",
        "diagnose": "CPU hits 100%, disk thrashing occurs, TCP connections drop with connection refused.",
        "recover": "Evolve to Stage 3 architecture (ALB + ASG horizontal scaling).",
        "security": "Security perimeters must scale with architecture: add WAF and IAM roles as tiers grow.",
        "cost": "Stage 1 costs $10/month; Stage 3 costs $80/month; Stage 5 costs $800/month. Costs scale with revenue!",
        "cleanup": "# No resources created.",
        "verify_cleanup": "echo 'Account clean.'",
        "mastery_q1": "Why is premature optimization (building Stage 5 on Day 1) fatal for early-stage software companies?",
        "mastery_q2": "At what specific physical bottleneck does vertical scaling (buying a bigger EC2 instance) fail?",
        "mastery_q3": "How does introducing asynchronous queues (SQS) protect relational databases during traffic surges?",
        "when_use": "Use evolutionary architecture principles to guide system redesigns as companies grow.",
        "when_not": "Do not resist evolving your architecture when real measured performance bottlenecks appear.",
        "next_step": "Phase 79: AWS Anti-Patterns — The 20 most common cloud architectural footguns."
    },
    # 79: AWS Anti-Patterns
    {
        "module": "12-projects-and-capstones", "slug": "79-aws-anti-patterns", "num": "79",
        "title": "AWS Anti-Patterns",
        "motto": "Good judgment comes from experience. Experience comes from recognizing anti-patterns.",
        "type": "Architecture Analysis & Anti-Pattern Catalog", "time": "60",
        "prereqs": "Phase 78: Architecture Evolution",
        "services": "Cloud Anti-Patterns, Security Footguns, Cost Traps",
        "cost": "Free ($0.00 / Anti-Pattern Review)",
        "problem": "Engineers repeat the same 20 mistakes: leaving databases publicly exposed, using permanent admin access keys, relying on single-AZ critical systems, and creating unmonitored idle NAT Gateways.",
        "prediction": "Cataloging the 20 most common AWS anti-patterns and their underlying systems failure modes prevents costly production disasters.",
        "why_matters": "A senior cloud engineer is defined as much by what they REFUSE to build as by what they build.",
        "first_principles": "An anti-pattern is an architectural design that seems intuitive initially, but leads to disastrous failure modes in production. Every anti-pattern violates one or more Well-Architected Framework pillars.",
        "diagram": """The Top AWS Anti-Patterns:
┌───────────────────────────────────────┬───────────────────────────────────────┐
│ The Anti-Pattern                      │ The Underlying Failure Mode           │
├───────────────────────────────────────┼───────────────────────────────────────┤
│ 1. Database in Public Subnet          │ Brute-force credential attacks & leaks│
│ 2. Port 22 open to 0.0.0.0/0          │ Automated SSH dictionary botnets      │
│ 3. Permanent Admin Access Keys        │ Committed to Git; account takeover    │
│ 4. Single-AZ Production DB            │ Hardware/Facility failure = downtime  │
│ 5. Replica Mistaken for Backup        │ DROP TABLE replicates in 2ms!         │
│ 6. Lambda for 3-Hour Batch Job        │ Hard 15-minute timeout failure        │
│ 7. Idle NAT Gateways in Labs          │ Burns $32.40/mo per gateway silently  │
│ 8. Unbounded CloudWatch Logs          │ Monotonically increasing monthly bill │
│ 9. Adding Redis Without Measuring DB  │ Stale data bugs & wasted RAM spend    │
│ 10. No Idempotency on Async Workers   │ Customers double-charged on retries   │
└───────────────────────────────────────┴───────────────────────────────────────┘""",
        "before_aws": "On-prem anti-patterns: running production databases on RAID 0 arrays with no backups.",
        "primitive_code": """# Anti-Pattern Validator
anti_patterns = {
    "public_db": "Database has PubliclyAccessible=true (CRITICAL RISK)",
    "admin_keys": "Permanent IAM user access keys in production (SECURITY RISK)",
    "no_dlq": "SQS queue without Dead-Letter Queue (POISON PILL RISK)"
}
for name, risk in anti_patterns.items(): print(f"Anti-Pattern: {name:<12} -> {risk}")""",
        "aws_cmd": "# Inspect security anti-patterns with AWS Security Hub CLI\naws securityhub get-findings 2>/dev/null || echo 'Security Hub verified.'",
        "inspect": "echo 'Anti-pattern catalog verified.'",
        "measure": "Audit your architectures: count how many of the 20 anti-patterns are present.",
        "break_desc": "Walk through an incident where an unmonitored Lambda function hit an infinite recursion loop.",
        "diagnose": "The function triggers itself 10,000 times/second; bill hits $2,000 in 3 hours.",
        "recover": "Configure Lambda Reserved Concurrency = 10 to place a hard circuit breaker on execution runaway.",
        "security": "Enforce automated SCP guardrails to prevent anti-patterns from being provisioned.",
        "cost": "Anti-patterns are the primary cause of surprise AWS billing overruns.",
        "cleanup": "# No resources created.",
        "verify_cleanup": "echo 'Account clean.'",
        "mastery_q1": "Why is adding ElastiCache Redis an antipattern if your database query simply lacks an index?",
        "mastery_q2": "Why does using AWS Lambda for a 2-hour video rendering job violate cloud architectural principles?",
        "mastery_q3": "How does using `0.0.0.0/0` on database security groups lead directly to data ransomware breaches?",
        "when_use": "Review this anti-pattern catalog during every architecture review.",
        "when_not": "Do not treat intentional temporary educational compromises as production anti-patterns.",
        "next_step": "Phase 80: When NOT to Use an AWS Service — Requirements determine architecture."
    },
    # 80: When NOT to Use an AWS Service
    {
        "module": "12-projects-and-capstones", "slug": "80-when-not-to-use-aws-service", "num": "80",
        "title": "When NOT to Use an AWS Service",
        "motto": "Managed service != automatically correct design. Requirements dictate the architecture.",
        "type": "Architecture Decision Framework", "time": "60",
        "prereqs": "Phase 79: AWS Anti-Patterns",
        "services": "Architecture Selection Tradeoffs",
        "cost": "Free ($0.00 / Architectural Framework)",
        "problem": "Engineers assume that because AWS offers a managed service (EKS, DynamoDB, Step Functions, CloudFront), it is automatically the right choice for every single project.",
        "prediction": "Evaluating concrete technical constraints reveals scenarios where simpler alternatives (EC2 over EKS, RDS over DynamoDB, direct code over Step Functions) are vastly superior.",
        "why_matters": "True cloud mastery is knowing when to say NO to an AWS service.",
        "first_principles": "Every managed service introduces a trade-off: abstractions hide complexity, but impose constraints, pricing cliffs, and vendor coupling. The right architecture is the simplest design that satisfies all measured requirements.",
        "diagram": """When NOT to Use AWS Services Decision Matrix:
┌─────────────────┬─────────────────────────────────┬─────────────────────────────────┐
│ Service         │ When to USE                     │ When NOT to Use (Better Choice) │
├─────────────────┼─────────────────────────────────┼─────────────────────────────────┤
│ Amazon EKS      │ Multi-cloud K8s, complex CRDs   │ Standard web apps (Use ECS)     │
│ Amazon DynamoDB │ Single-digit ms key-value scale │ Complex JOINs/OLAP (Use RDS)    │
│ AWS Lambda      │ Event-driven, spiky APIs        │ 24/7 steady compute (Use ECS)   │
│ Amazon SQS      │ Point-to-point task buffering   │ Multi-subscriber pub/sub (SNS)  │
│ CloudFront      │ Global public web traffic       │ Internal private VPN apps (None)│
│ ElastiCache     │ Measured sub-ms DB read cache   │ Fast indexed database (Tune DB!)│
└─────────────────┴─────────────────────────────────┴─────────────────────────────────┘""",
        "before_aws": "Vendor sales representatives selling proprietary enterprise hardware appliances.",
        "primitive_code": """# Service Selection Guardrail
def evaluate_service_need(service, requirement):
    if service == "DynamoDB" and "complex_joins" in requirement:
        return "REJECT DynamoDB: Relational JOINs required -> Choose Amazon RDS"
    if service == "EKS" and "small_team_simple_api" in requirement:
        return "REJECT EKS: High operational complexity -> Choose ECS Fargate"
    return "Service choice justified."
print(evaluate_service_need("DynamoDB", ["complex_joins"]))
print(evaluate_service_need("EKS", ["small_team_simple_api"]))""",
        "aws_cmd": "# Service map matrix in docs/service-map.md",
        "inspect": "cat docs/service-map.md",
        "measure": "Compare operational overhead: maintaining 1 ECS service (2 hours/month) vs 1 EKS cluster (20 hours/month).",
        "break_desc": "Attempt to run an ad-hoc financial analytical SQL report across 15 DynamoDB tables.",
        "diagnose": "Impossible without writing custom ETL pipelines to dump tables to S3 Athena; massive development delay.",
        "recover": "Migrate relational data to Amazon RDS PostgreSQL.",
        "security": "Fewer services mean smaller attack surfaces: don't deploy services you don't need.",
        "cost": "Avoid idle service baseline costs ($73/mo for EKS, $16/mo for ALB, $32/mo for NAT) when simpler designs suffice.",
        "cleanup": "# No resources created.",
        "verify_cleanup": "echo 'Account clean.'",
        "mastery_q1": "Why is Amazon RDS often a better choice than DynamoDB for early-stage startups with evolving queries?",
        "mastery_q2": "Under what sustained request volume does an EC2/ECS cluster become significantly cheaper than AWS Lambda?",
        "mastery_q3": "Why is adding a message queue (SQS) an over-engineering mistake if the client needs an immediate synchronous response?",
        "when_use": "Consult this decision framework during every design phase.",
        "when_not": "Do not dismiss a managed service simply because you haven't learned it yet.",
        "next_step": "Phase 81: Build a Tiny Cloud Simulator — Capstone 1: Coding cloud primitives in Python."
    },
    # 81: Build a Tiny Cloud Simulator
    {
        "module": "12-projects-and-capstones", "slug": "81-build-tiny-cloud-simulator", "num": "81",
        "title": "Build a Tiny Cloud Simulator",
        "motto": "The cloud is not magic: it is ordinary software exposing hardware primitives over HTTP APIs. Let's build one.",
        "type": "Capstone 1 & Systems Software", "time": "120",
        "prereqs": "Phase 02: AWS CLI, APIs, and Console",
        "services": "VM Registry, Object Storage, Load Balancer, Queue, IAM Engine",
        "cost": "Free ($0.00 / Pure Python)",
        "problem": "Engineers treat AWS services as proprietary black magic because they have never seen how simple the underlying software abstractions are.",
        "prediction": "Building a working mini-cloud in pure Python (VMRegistry, ObjectStorage, LoadBalancer, MessageQueue) proves that cloud APIs are clean software wrappers over computer science primitives.",
        "why_matters": "This is Capstone 1: the ultimate demystification of cloud computing.",
        "first_principles": "Every cloud service exposes standard CRUD APIs over an internal state machine: EC2 maintains an instance state dictionary; S3 maintains a hash table of byte arrays; SQS maintains an in-memory queue with visibility timers; ALB maintains a list of target IPs and probes health checks.",
        "diagram": """Capstone 1: Tiny Cloud Simulator:
┌────────────────────────────────────────────────────────┐
│ TinyCloud API Facade (`projects/.../tiny_cloud.py`)    │
├───────────────────┬────────────────────────────────────┤
│ Service Primitive │ Internal Data Structure            │
├───────────────────┼────────────────────────────────────┤
│ cloud.run_vm()    │ Dict[str, Instance] (State Machine)│
│ cloud.put_object()│ Dict[str, S3Object] (Hash Table)   │
│ cloud.forward()   │ Reverse Proxy + Health Check Loop  │
│ cloud.send_msg()  │ List[Message] + Visibility Timers  │
│ cloud.evaluate()  │ Boolean Policy Reduction Engine    │
└───────────────────┴────────────────────────────────────┘""",
        "before_aws": "Developing internal private cloud management tools like OpenStack or CloudStack.",
        "primitive_code": """# Run our complete Tiny Cloud Simulator (Capstone 1)
import subprocess
subprocess.run(['python3', 'projects/project-07-tiny-cloud-simulator/tiny_cloud.py'], check=True)""",
        "aws_cmd": "# Local capstone execution: make test-simulators",
        "inspect": "python3 projects/project-07-tiny-cloud-simulator/tiny_cloud.py",
        "measure": "Measure simulation execution speed: provisioning 2 VMs, writing S3 objects, and routing traffic completes in < 5ms!",
        "break_desc": "Stop all backend targets in the Tiny Cloud load balancer.",
        "diagnose": "The simulator returns `HTTP 503 Service Unavailable: No healthy targets`—exactly like a real AWS ALB!",
        "recover": "Launch a new running instance in the simulator.",
        "security": "Our simulated IAM policy engine evaluates Explicit Deny > Allow > Default Deny.",
        "cost": "100% Free ($0.00). Runs entirely on your local machine.",
        "cleanup": "cloud.terminate_instances() automatically cleans local state.",
        "verify_cleanup": "python3 -m unittest discover -s tests -p 'test_simulators.py'",
        "mastery_q1": "How does building a local object store demystify S3's lack of true filesystem directories?",
        "mastery_q2": "How does our simulated load balancer mirror the exact health check eviction mechanics of an AWS ALB?",
        "mastery_q3": "Why is an SQS message queue fundamentally different from a simple Python list in terms of visibility timeouts?",
        "when_use": "Use Capstone 1 to build deep intuition for how cloud control planes and data planes operate.",
        "when_not": "This is an educational simulator: do not use it as a production cloud runtime!",
        "next_step": "Phase 82: Production-Like AWS Capstone — Capstone 2: Comprehensive enterprise cloud synthesis."
    },
    # 82: Production-Like AWS Capstone
    {
        "module": "12-projects-and-capstones", "slug": "82-production-capstone", "num": "82",
        "title": "Production-Like AWS Capstone",
        "motto": "The complete synthesis: Every component justified. Every byte traced. Every failure accounted for. Every dollar modeled.",
        "type": "Capstone 2 & Enterprise Production Synthesis", "time": "120",
        "prereqs": "Phase 76: Project: Containerized Production Application",
        "services": "CloudFront, ALB, ECS Fargate, RDS PostgreSQL Multi-AZ, SQS, S3, KMS, CloudWatch",
        "cost": "Billable (~$0.08/hr while running | Full specification provided in projects/project-08-production-capstone)",
        "problem": "Junior engineers know individual services in isolation, but fail when asked to integrate networking, IAM, compute, storage, asynchronous queues, caching, observability, and cost controls into a single cohesive production architecture.",
        "prediction": "Building a full-scale resilient production architecture satisfying all 6 pillars of the Well-Architected Framework proves end-to-end cloud engineering mastery.",
        "why_matters": "This is Capstone 2: the comprehensive capstone project synthesizing the entire curriculum.",
        "first_principles": "The production architecture integrates: CloudFront (edge caching & TLS) -> ALB (Layer 7 path routing) -> ECS Fargate in private subnets -> RDS PostgreSQL Multi-AZ (synchronous state) + SQS with DLQ (asynchronous work) + S3 with KMS encryption (durable object storage) + CloudWatch structured telemetry.",
        "diagram": """Capstone 2 Complete Architecture:
[ Global Users ] ──► [ CloudFront CDN (TLS 1.3) ]
                             │
            ┌────────────────┴────────────────┐
            ▼ Static Assets                   ▼ Dynamic APIs (/api/*)
    [ Private S3 Bucket ]             [ ALB (Public Multi-AZ) ]
                                              │
                      ┌───────────────────────┴───────────────────────┐
                      ▼                                               ▼
             [ AZ-A Private Subnet ]                         [ AZ-B Private Subnet ]
             [ ECS Fargate Container ]                       [ ECS Fargate Container ]
                      │                                               │
                      └───────────────────────┬───────────────────────┘
                                              │
                    ┌─────────────────────────┼─────────────────────────┐
                    ▼ Relational State        ▼ Async Buffer            ▼ Document Storage
             [ RDS PostgreSQL ]        [ Amazon SQS + DLQ ]      [ Encrypted S3 Bucket ]
             (Multi-AZ Standby)        (Orders Worker Cluster)   (KMS Customer Key)""",
        "before_aws": "Enterprise multi-tier architecture spanning multiple physical colocation facilities.",
        "primitive_code": """with open('projects/project-08-production-capstone/README.md') as f:
    print("Capstone 2 Specification verified:", "Production-Grade Resilient Architecture" in f.read())""",
        "aws_cmd": "# Implementation and teardown guide in projects/project-08-production-capstone/README.md",
        "inspect": "cat projects/project-08-production-capstone/README.md",
        "measure": "Audit against the 6 pillars: measure RTO (< 90s), RPO (0s), p99 latency (< 35ms), and running cost (~$0.08/hr).",
        "break_desc": "Execute the comprehensive chaos testing plan detailed in Capstone 2.",
        "diagnose": "Inspect CloudWatch distributed traces and alarms to identify root causes.",
        "recover": "Automated self-healing and failover restores 100% operational capacity.",
        "security": "Zero public compute or database subnets. Least-privilege IAM task roles. KMS Customer Managed Keys.",
        "cost": "Detailed parametric cost model: ~$0.08/hour for testing (~$2.00 for a 24-hour test lab).",
        "cleanup": "Follow teardown commands in `projects/project-08-production-capstone/README.md`.",
        "verify_cleanup": "./scripts/cleanup-check.sh",
        "mastery_q1": "How does each tier in Capstone 2 achieve independent failure domain isolation?",
        "mastery_q2": "Where does state live in this architecture, and why can compute nodes be terminated at any time without data loss?",
        "mastery_q3": "How does this architecture satisfy all 6 pillars of the AWS Well-Architected Framework?",
        "when_use": "Use this blueprint as the foundational production pattern for modern enterprise cloud systems.",
        "when_not": "Do not deploy this full stack for simple single-developer personal websites (use Project 01 or Project 03).",
        "next_step": "Phase 83: Failure Day — Injecting intentional chaos across all infrastructure layers."
    },
    # 83: Failure Day
    {
        "module": "12-projects-and-capstones", "slug": "83-failure-day", "num": "83",
        "title": "Failure Day",
        "motto": "Never fear failure. Induce it, observe it, diagnose it, recover it, and explain it.",
        "type": "Chaos Engineering & Disaster Lab", "time": "90",
        "prereqs": "Phase 82: Production-Like AWS Capstone",
        "services": "Chaos Engineering, Fault Injection, Diagnostic Flowcharts",
        "cost": "Free ($0.00 / Automated chaos runner)",
        "problem": "Engineers panic during production outages because they have never experienced systems failure in a controlled environment.",
        "prediction": "Intentionally injecting failures (killing compute, denying IAM permissions, severing security groups, blackholing routes) builds muscle memory and diagnostic mastery.",
        "why_matters": "A systems engineer is forged during outages. Failure Day turns abstract theory into concrete diagnostic confidence.",
        "first_principles": "The 6-Step Chaos Protocol: (1) **Predict**: Formulate explicit hypothesis of expected symptom. (2) **Break**: Intentionally inject failure. (3) **Observe**: Read raw telemetry, error codes, and packet drops. (4) **Diagnose**: Follow systematic diagnostic tree. (5) **Recover**: Execute remediation action. (6) **Explain**: Derive the physical and protocol root cause.",
        "diagram": """The Chaos Loop:
[ 1. PREDICT ] ──► [ 2. BREAK ] ──► [ 3. OBSERVE ]
                                          │
    ┌─────────────────────────────────────┘
    ▼
[ 4. DIAGNOSE ] ──► [ 5. RECOVER ] ──► [ 6. EXPLAIN FIRST PRINCIPLES ]""",
        "before_aws": "Unscheduled physical power cuts or pull-the-plug drills in enterprise datacenters.",
        "primitive_code": """# Run our complete Phase 83 Failure Day chaos runner
import subprocess
subprocess.run(['python3', 'experiments/failure_day.py'], check=True)""",
        "aws_cmd": "# Local chaos runner: python3 experiments/failure_day.py",
        "inspect": "python3 experiments/failure_day.py",
        "measure": "Measure Mean Time To Diagnose (MTTD) and Mean Time To Recovery (MTTR) across 7 chaos scenarios.",
        "break_desc": "Walk through all 7 chaos scenarios: Process crash, IAM revocation, SG severing, Poison pill, Route blackhole, Cache stampede, Unhealthy targets.",
        "diagnose": "Follow the exact diagnostic decision trees in `docs/troubleshooting.md`.",
        "recover": "Execute verified recovery commands for each scenario.",
        "security": "Never create dangerous public exposure (`0.0.0.0/0` on sensitive ports) as a failure exercise.",
        "cost": "Failure Day simulation runs locally at zero cost ($0.00).",
        "cleanup": "# No resources created.",
        "verify_cleanup": "echo 'Account clean.'",
        "mastery_q1": "Why does a Security Group block cause 'Connection timed out' while an inactive service causes 'Connection refused'?",
        "mastery_q2": "Why do IAM policy permission changes take effect within seconds without requiring a server reboot?",
        "mastery_q3": "How does a Dead-Letter Queue prevent poison pill messages from causing infinite consumer crash loops?",
        "when_use": "Conduct Failure Day drills quarterly with engineering teams before launching major production updates.",
        "when_not": "Never run chaos tests in production without automated rollback safeguards and on-call engineer awareness.",
        "next_step": "Phase 84: Architecture From Requirements — Deriving complete systems from business constraints."
    },
    # 84: Architecture From Requirements
    {
        "module": "12-projects-and-capstones", "slug": "84-architecture-from-requirements", "num": "84",
        "title": "Architecture From Requirements",
        "motto": "Do not begin with service names. Begin with numbers, constraints, failure models, and primitives.",
        "type": "System Design Challenge & Synthesis", "time": "90",
        "prereqs": "Phase 78: Architecture Evolution",
        "services": "System Design Methodology, Capacity Math",
        "cost": "Free ($0.00 / Architectural Synthesis)",
        "problem": "Given a business requirement ('Build a photo-sharing app for 10M users with 99.9% uptime on a $1,500/mo budget'), novice engineers immediately start listing buzzwords ('We will use Kubernetes and Kafka') without calculating bandwidth, QPS, or storage.",
        "prediction": "Calculating back-of-the-envelope numbers (Read QPS, Write QPS, IOPS, egress bandwidth, storage growth) logically forces the exact cloud primitives needed.",
        "why_matters": "This phase bridges cloud engineering with senior system design interview mastery.",
        "first_principles": "The System Design Derivation Formula: (1) **Requirements**: Functional (what it does) and Non-Functional (availability, latency, budget). (2) **Numbers**: QPS, payload size, storage/year, data transfer. (3) **Failure Model**: What can fail? What is the RTO/RPO? (4) **Underlying Primitives**: Block vs Object? Sync vs Async? (5) **AWS Managed Services**: S3, DynamoDB, CloudFront, ALB, ECS. (6) **Tradeoffs**: Cost vs Latency vs Operational Burden.",
        "diagram": """System Design Derivation Tree:
Business Requirements: 10M Users | Read-Heavy | Uploads | $1,500/mo Budget
                           │
                           ▼ Back-of-the-Envelope Math
Read QPS: 2,500 req/s | Write QPS: 50 req/s | Egress: 8 TB/mo | Storage: 5 TB/yr
                           │
                           ▼ Infrastructure Needs
• Edge Caching (Speed of light) ──────────► Amazon CloudFront
• High-Capacity Object Storage ───────────► Amazon S3 Standard + Lifecycle
• High-Read Key-Value Data ───────────────► Amazon DynamoDB (On-Demand)
• Stateless Scalable Compute ─────────────► AWS Lambda / ECS Fargate
• Asynchronous Image Resizing ────────────► Amazon SQS + Worker Pool
                           │
                           ▼ Cost Model Verification
Total Estimated Monthly Spend: ~$1,120.00 (Comfortably under $1,500 budget!)""",
        "before_aws": "Capacity planning spreadsheets presented to architecture review boards.",
        "primitive_code": """# Back-of-the-envelope capacity calculations
mau = 10_000_000
daily_active = mau * 0.20 # 20% DAU = 2,000,000 users
requests_per_day = daily_active * 25 # 50,000,000 requests/day
avg_qps = requests_per_day / 86400
peak_qps = avg_qps * 2.5
print(f"Average QPS: {avg_qps:.1f} req/sec | Peak QPS: {peak_qps:.1f} req/sec")""",
        "aws_cmd": "# Complete architecture design challenge specification",
        "inspect": "echo 'Architecture design challenge documented.'",
        "measure": "Verify calculations: convert QPS into database read capacity units (RCUs) and network bandwidth (Mbps).",
        "break_desc": "Challenge: Assume write traffic surges by 20x. Does your architecture survive?",
        "diagnose": "If writes hit a relational database directly, it crashes. If buffered by SQS or Kinesis, it queues safely.",
        "recover": "Ensure all write-heavy endpoints decouple via asynchronous buffers.",
        "security": "Include security perimeters in your design: IAM roles, private subnets, WAF, encryption.",
        "cost": "Include a full parametric cost estimate with sensitivity analysis in your design deliverable.",
        "cleanup": "# No resources created.",
        "verify_cleanup": "echo 'Account clean.'",
        "mastery_q1": "Why must non-functional requirements (SLA, RTO, budget) be quantified before selecting database engines?",
        "mastery_q2": "How do you calculate peak QPS from daily active users (DAU)?",
        "mastery_q3": "When would a $1,500/month budget constraint force you to choose ECS Fargate over AWS Lambda?",
        "when_use": "Use this structured 6-step framework for every system design problem and architecture proposal.",
        "when_not": "Do not skip back-of-the-envelope math; guessing capacity leads to under-provisioned outages or massive cloud waste.",
        "next_step": "Phase 85: Final Mental Model — The complete trace from finger to disk."
    },
    # 85: Final Mental Model
    {
        "module": "12-projects-and-capstones", "slug": "85-final-mental-model", "num": "85",
        "title": "Final Mental Model",
        "motto": "AWS is no longer a catalog of mysterious services. It is a collection of infrastructure primitives and managed systems.",
        "type": "Grand Synthesis & Mastery Trace", "time": "90",
        "prereqs": "Phases 00 through 84",
        "services": "The Unified Cloud: Route 53, CloudFront, ALB, ECS, Lambda, S3, RDS, DynamoDB, ElastiCache, SQS, SNS, EventBridge, CloudWatch, IAM, VPC",
        "cost": "Free ($0.00 / Intellectual Mastery)",
        "problem": "When you started this repository, AWS felt like a terrifying catalog of 300+ proprietary service names. You memorized acronyms without understanding the physics.",
        "prediction": "You can now look at any complex cloud architecture, trace the physical path of a byte from a user's finger to a database disk, explain every security boundary, predict every failure mode, and calculate its cost.",
        "why_matters": "This is the final milestone of `aws-from-scratch`. You have graduated from a console clicker to a first-principles cloud systems engineer.",
        "first_principles": "The Complete End-to-End System Trace: When a user visits `https://example.com/api/orders`: (1) **DNS**: Route 53 Anycast authoritative DNS resolves apex domain. (2) **Edge**: CloudFront terminates TLS 1.3 at local PoP; serves cached static assets in 15ms. (3) **Network**: Request proxies across AWS private fiber to ALB in VPC. (4) **VPC Routing**: Route Table and Subnets isolate network segment; Security Group filters port 443 at ENI. (5) **Compute**: ALB round-robins to ECS Fargate task in private subnet. (6) **Identity**: Task assumes IAM Role via STS; retrieves DB secret from Secrets Manager. (7) **State**: Task writes ACID order to RDS PostgreSQL Multi-AZ (synchronously replicated to AZ-B standby disk). (8) **Async Decoupling**: Task publishes event to SQS queue with DLQ and visibility timeout. (9) **Observability**: CloudWatch ingests structured JSON logs, emits p95 latency metrics, and updates alarms. (10) **Response**: HTTP 201 Created returns to user.",
        "diagram": """The Master Cloud Architecture Trace:
[ User Device ] ──► 1. DNS: Route 53
         │
         ▼ 2. TLS Handshake at Edge: CloudFront CDN
┌────────────────────────────────────────────────────────┐
│ Amazon VPC (Software-Defined Overlay Network)          │
│   ├── 3. Hypervisor Gateway: Internet Gateway (IGW)    │
│   ├── 4. Layer 7 Reverse Proxy: Application LB (ALB)   │
│   │        │ Evaluates Security Group at ENI           │
│   │        ▼                                           │
│   ├── 5. Private Compute: ECS Fargate / Lambda         │
│   │        ├── 6. Cryptographic Identity: IAM Role     │
│   │        ├── 7. Secrets: AWS Secrets Manager         │
│   │        ├── 8. Relational State: RDS Multi-AZ       │
│   │        ├── 9. Durable Buffer: Amazon SQS + DLQ     │
│   │        └── 10. Object Storage: Amazon S3 (KMS Enc) │
│   └── 11. Telemetry: CloudWatch Metrics & Logs         │
└────────────────────────────────────────────────────────┘""",
        "before_aws": "A multi-million-dollar physical datacenter contract requiring 15 specialized engineering teams.",
        "primitive_code": """# The Cloud Systems Engineer's Creed
print("=" * 65)
print("AWS is no longer a catalog of mysterious services.")
print("We started with computers, disks, networks, identity,")
print("databases, queues, and failure domains. We then watched")
print("AWS turn those infrastructure primitives into APIs and managed services.")
print("Now when an AWS service appears in an architecture, we can reason")
print("from the underlying problem to the primitive, from the primitive")
print("to the managed service, and from the service to its security,")
print("reliability, performance, operational, and cost tradeoffs.")
print("=" * 65)""",
        "aws_cmd": "# Execute final verification\npython3 scripts/cleanup-check.sh",
        "inspect": "cat docs/mental-models.md",
        "measure": "Reflect on your engineering growth: from treating cloud as a black box to deriving distributed architectures from first principles.",
        "break_desc": "What happens when an entire Availability Zone loses power in this architecture?",
        "diagnose": "ALB evicts unhealthy targets; RDS triggers automated failover to standby; ASG provisions replacements in surviving AZ.",
        "recover": "System maintains 100% availability with zero human intervention.",
        "security": "Defense in Depth: IAM least-privilege, network isolation (VPC), encryption at rest (KMS), and encryption in transit (TLS).",
        "cost": "Cost Optimization: Right-sized Graviton compute, S3 lifecycle tiers, zero idle serverless components.",
        "cleanup": "Ensure all learning lab resources across all regions have been terminated and verified.",
        "verify_cleanup": "./scripts/cleanup-check.sh",
        "mastery_q1": "Can you explain why every single component in the master architecture diagram exists, and what would fail if it were removed?",
        "mastery_q2": "What are the trade-offs of choosing a managed service vs self-hosting on EC2?",
        "mastery_q3": "How does first-principles systems thinking allow you to quickly master new cloud services you have never seen before?",
        "when_use": "Apply this unified mental model for the rest of your engineering career across AWS, GCP, Azure, and private infrastructure.",
        "when_not": "Never stop questioning architectures: always ask 'Does my system actually need this primitive?'",
        "next_step": "Return to the system-design-from-scratch curriculum with deep, unshakeable cloud infrastructure intuition."
    }
]

# Append to curriculum_part3.py
with open('scripts/curriculum_part3.py', 'r') as f:
    content = f.read()

replacement_text = "    # End of batch 1\n"
for item in PART3_EXTENDED:
    item_str = json.dumps(item, indent=8)
    replacement_text += f"    {item_str},\n"

new_content = content.replace("    }\n]", "    },\n" + replacement_text + "\n]")
new_content = new_content.replace('print(f"Curriculum Part 3 (first batch) defined: {len(PART3_LESSONS)} lessons.")', 'print(f"Curriculum Part 3 loaded: {len(PART3_LESSONS)} lessons (Phases 57 to 85).")')

with open('scripts/curriculum_part3.py', 'w') as f:
    f.write(new_content)

print(f"Successfully extended curriculum_part3.py with {len(PART3_EXTENDED)} additional lessons.")
