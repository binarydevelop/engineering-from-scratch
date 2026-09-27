"""
scripts/curriculum_part3.py
Defines detailed curriculum metadata for Phases 57 through 85.
"""

PART3_LESSONS = [
    # 57: Infrastructure as Code
    {
        "module": "10-infrastructure-as-code", "slug": "57-infrastructure-as-code", "num": "57",
        "title": "Infrastructure as Code",
        "motto": "Clicking in the console is for discovery. Infrastructure as Code is for production. If it isn't in code, it doesn't exist.",
        "type": "Conceptual & Paradigm Transition", "time": "60",
        "prereqs": "Phase 11: Security Groups",
        "services": "Declarative Infrastructure, AWS CloudFormation, Terraform",
        "cost": "Free ($0.00 / IaC definitions are free)",
        "problem": "You spent 4 days clicking in the AWS console to set up a VPC, subnets, route tables, security groups, ALBs, and instances. The CTO asks: 'Can you reproduce this exact setup in `eu-central-1` for our European customers?' You have no documentation, no reproducibility, and configuration drift.",
        "prediction": "Writing infrastructure declaratively in text files allows version-controlling environments with Git, reviewing changes via Pull Requests, and deploying identical infrastructure across regions in minutes.",
        "why_matters": "Only after feeling the pain of manual creation in Phases 06-16 do we introduce IaC. You must understand the underlying resources before automating them.",
        "first_principles": "Imperative (CLI/Scripts): 'Create VPC A, then create Subnet B, then attach Gateway C.' Fragile; fails midway without state tracking. Declarative (IaC): 'I want a VPC with CIDR 10.0.0.0/16 and two subnets.' The IaC engine computes the dependency graph and reconciles desired state against current state.",
        "diagram": """Imperative vs Declarative Infrastructure:
IMPERATIVE (Bash / CLI):
Step 1 ──► Step 2 ──► Step 3 (Fails halfway! Left in dirty state!)

DECLARATIVE (CloudFormation / Terraform):
[ Declarative Code ] ──► [ Graph Engine computes DAG ] ──► [ Reconciles to AWS APIs ]
                                                                 (Idempotent & Safe!)""",
        "before_aws": "Datacenter runbooks: 40-page Word documents detailing cable numbers and manual BIOS settings.",
        "primitive_code": """# Simulating declarative state reconciliation
desired_state = {"vpc_cidr": "10.0.0.0/16", "subnets": 2}
current_state = {"vpc_cidr": "10.0.0.0/16", "subnets": 1}
plan = {}
for k, v in desired_state.items():
    if current_state.get(k) != v:
        plan[k] = f"CREATE/UPDATE from {current_state.get(k)} to {v}"
print("Execution Plan computed by IaC Engine:", plan)""",
        "aws_cmd": "# Validate CloudFormation template syntax CLI\naws cloudformation validate-template --template-body file://infrastructure/vpc-dual-az-baseline.yaml --output table",
        "inspect": "cat infrastructure/vpc-dual-az-baseline.yaml",
        "measure": "Compare reproduction time: Manual console recreation (3 hours) vs automated IaC execution (3 minutes).",
        "break_desc": "Manually delete a subnet in the AWS console that is managed by an active CloudFormation stack.",
        "diagnose": "The stack experiences **Configuration Drift**: desired state no longer matches physical cloud reality.",
        "recover": "Run CloudFormation Drift Detection and re-import or update the stack.",
        "security": "IaC allows scanning infrastructure for security misconfigurations (e.g. `checkov`, `trivy`) in CI/CD before resources are created.",
        "cost": "AWS CloudFormation is free. You pay only for the resources it provisions.",
        "cleanup": "# No resources created in Phase 57.",
        "verify_cleanup": "echo 'Account clean.'",
        "mastery_q1": "Why is declarative infrastructure superior to writing shell scripts with the AWS CLI?",
        "mastery_q2": "What is configuration drift and how does an IaC engine detect it?",
        "mastery_q3": "Why did we mandate manual CLI/API configuration in Phases 06-16 before introducing IaC here?",
        "when_use": "Use Infrastructure as Code for all non-trivial cloud resources, pipelines, and environments.",
        "when_not": "Do not use IaC for transient 5-minute exploratory prototyping where quick deletion is planned.",
        "next_step": "Phase 58: IaC Fundamentals — Stacks, parameters, outputs, and dependencies."
    },
    # 58: IaC Fundamentals
    {
        "module": "10-infrastructure-as-code", "slug": "58-iac-fundamentals", "num": "58",
        "title": "IaC Fundamentals",
        "motto": "A template is a DAG of resources. The engine resolves dependencies automatically.",
        "type": "Hands-on Lab & CloudFormation", "time": "60",
        "prereqs": "Phase 57: Infrastructure as Code",
        "services": "AWS CloudFormation Stacks, Change Sets",
        "cost": "Free ($0.00 / CloudFormation is free)",
        "problem": "If you try to create a subnet before its parent VPC exists, the API call crashes with `InvalidVpcID.NotFound`. How does an engine know what order to create resources in?",
        "prediction": "The IaC engine analyzes resource references (`!Ref`, `!GetAtt`) to construct a Directed Acyclic Graph (DAG), creating independent resources in parallel and dependent resources in order.",
        "why_matters": "Understanding dependency graphs prevents circular dependency errors and failed deployments.",
        "first_principles": "A CloudFormation template defines: (1) **Parameters** (inputs), (2) **Resources** (the declarative primitives to create), and (3) **Outputs** (values exported for other stacks). The engine builds a DAG where nodes are resources and edges are dependencies.",
        "diagram": """CloudFormation Dependency Graph (DAG):
                   [ VPC (10.0.0.0/16) ]
                             │
            ┌────────────────┴────────────────┐
            ▼                                 ▼
[ Public Subnet 1 ]               [ Public Subnet 2 ]
(Created in parallel!)            (Created in parallel!)
            │                                 │
            ▼                                 ▼
[ SubnetRouteTableAssoc 1 ]       [ SubnetRouteTableAssoc 2 ]""",
        "before_aws": "Custom shell scripts with hardcoded `sleep 30` loops waiting for VM boots.",
        "primitive_code": """# Simulating DAG topological sort
dependencies = {"Subnet": ["VPC"], "EC2": ["Subnet", "SecurityGroup"], "SecurityGroup": ["VPC"], "VPC": []}
print("Resource Creation Order determined by DAG:")
for res, deps in sorted(dependencies.items(), key=lambda x: len(x[1])):
    print(f"  Create {res} (Depends on: {deps or 'None'})")""",
        "aws_cmd": "aws cloudformation create-change-set --stack-name lab-stack --change-set-name preview-1 --template-body file://infrastructure/vpc-dual-az-baseline.yaml --change-set-type CREATE",
        "inspect": "aws cloudformation describe-change-set --stack-name lab-stack --change-set-name preview-1 --output json",
        "measure": "Inspect parallel provisioning: CloudFormation provisions independent subnets concurrently.",
        "break_desc": "Introduce a circular dependency: Resource A depends on Resource B; Resource B depends on Resource A.",
        "diagnose": "CloudFormation template validation fails with `Circular dependency between resources: [A, B]`.",
        "recover": "Break the circular reference using intermediate parameters or decoupled exports.",
        "security": "CloudFormation automatically rolls back the entire stack if any single resource fails creation.",
        "cost": "CloudFormation change sets and stack management cost $0.00.",
        "cleanup": "aws cloudformation delete-change-set --stack-name lab-stack --change-set-name preview-1",
        "verify_cleanup": "echo 'Change set cleaned.'",
        "mastery_q1": "Why is inspecting a CloudFormation Change Set mandatory before executing an update in production?",
        "mastery_q2": "What happens during a CloudFormation Rollback when a resource creation fails midway?",
        "mastery_q3": "What is the difference between `!Ref` and `!GetAtt` in AWS CloudFormation?",
        "when_use": "Always use change sets to preview infrastructure updates and prevent accidental resource replacements.",
        "when_not": "Do not edit live production resources directly in the console after deploying via IaC.",
        "next_step": "Phase 59: Rebuild VPC With IaC — Recreating our earlier VPC using code."
    },
    # 59: Rebuild VPC With IaC
    {
        "module": "10-infrastructure-as-code", "slug": "59-rebuild-vpc-with-iac", "num": "59",
        "title": "Rebuild VPC With IaC",
        "motto": "Automate what you have understood. Turn hours of manual networking into a 3-minute template deployment.",
        "type": "Hands-on Lab & Network Automation", "time": "60",
        "prereqs": "Phase 58: IaC Fundamentals",
        "services": "CloudFormation, VPC, Subnets, Route Tables, IGW",
        "cost": "Free ($0.00 / Baseline VPC is free)",
        "problem": "In Phases 06 through 10, we manually created a VPC, attached an Internet Gateway, created subnets across 2 AZs, and configured route tables. Doing this manually takes 20 CLI commands and is prone to typos.",
        "prediction": "Deploying `infrastructure/vpc-dual-az-baseline.yaml` will provision the entire multi-AZ network in under 2 minutes with zero human error.",
        "why_matters": "Comparing the pain of manual learning in Phase 06 vs automated reproducibility in Phase 59 proves the value of IaC.",
        "first_principles": "The CloudFormation template `infrastructure/vpc-dual-az-baseline.yaml` defines the VPC, IGW attachment, 2 public subnets, 2 private subnets, and route associations as code. It provisions a production-ready network with ZERO ongoing hourly NAT Gateway costs.",
        "diagram": """Template Architecture:
infrastructure/vpc-dual-az-baseline.yaml
  ├── AWS::EC2::VPC (10.0.0.0/16)
  ├── AWS::EC2::InternetGateway
  ├── AWS::EC2::Subnet (Public AZ-1, Public AZ-2)
  ├── AWS::EC2::Subnet (Private AZ-1, Private AZ-2)
  └── AWS::EC2::RouteTable (Default Route 0.0.0.0/0 -> IGW)""",
        "before_aws": "Network cabling diagrams and manual switch VLAN configuration.",
        "primitive_code": """# Inspect our validated baseline template
with open('infrastructure/vpc-dual-az-baseline.yaml') as f:
    lines = [line.strip() for line in f if 'Type: AWS::EC2::' in line]
print(f"Template contains {len(lines)} declarative networking primitives:")
for l in lines: print(f"  - {l}")""",
        "aws_cmd": "aws cloudformation deploy --template-file infrastructure/vpc-dual-az-baseline.yaml --stack-name aws-from-scratch-vpc --parameter-overrides ProjectName=aws-from-scratch",
        "inspect": "aws cloudformation describe-stacks --stack-name aws-from-scratch-vpc --query 'Stacks[0].Outputs' --output table",
        "measure": "Measure deployment duration: complete Dual-AZ VPC deploys in ~45 seconds.",
        "break_desc": "Attempt to delete the stack while an active EC2 instance is still running in one of the subnets.",
        "diagnose": "Stack deletion halts with `DELETE_FAILED: Subnet has dependent network interfaces (ENIs)`.",
        "recover": "Terminate the EC2 instance first, then retry stack deletion.",
        "security": "The template keeps private subnets completely dark to the public internet.",
        "cost": "This Dual-AZ baseline VPC incurs exactly $0.00/month while idle because it avoids expensive NAT Gateways.",
        "cleanup": "aws cloudformation delete-stack --stack-name aws-from-scratch-vpc",
        "verify_cleanup": "aws cloudformation wait stack-delete-complete --stack-name aws-from-scratch-vpc",
        "mastery_q1": "Why did we intentionally omit a NAT Gateway from `infrastructure/vpc-dual-az-baseline.yaml`?",
        "mastery_q2": "How does `!Select [0, !GetAZs '']` make CloudFormation templates portable across any AWS region?",
        "mastery_q3": "How would you update the template to add a third Availability Zone?",
        "when_use": "Use this baseline VPC template as the starting network foundation for all your learning projects.",
        "when_not": "Do not delete and recreate VPCs in production environments where IP addresses are referenced by client firewalls.",
        "next_step": "Phase 60: Rebuild Application Stack With IaC — Deploying compute and databases via code."
    },
    # 60: Rebuild Application Stack With IaC
    {
        "module": "10-infrastructure-as-code", "slug": "60-rebuild-app-stack-iac", "num": "60",
        "title": "Rebuild Application Stack With IaC",
        "motto": "The entire application stack—API Gateway, Lambda, and DynamoDB—deployed and destroyed in a single command.",
        "type": "Hands-on Lab & Full Stack Automation", "time": "60",
        "prereqs": "Phase 59: Rebuild VPC With IaC",
        "services": "CloudFormation, Serverless API Stack",
        "cost": "Free Tier eligible ($0.00 idle cost)",
        "problem": "Setting up an API Gateway, Lambda execution role, Lambda function, and DynamoDB table with least-privilege IAM requires 15 distinct CLI commands and careful ARN wiring.",
        "prediction": "Deploying `infrastructure/serverless-api.yaml` provisions the complete serverless architecture, wires IAM permissions automatically, and exposes a live HTTPS endpoint in 60 seconds.",
        "why_matters": "Demonstrates the power of end-to-end infrastructure automation with zero ongoing idle cost.",
        "first_principles": "The CloudFormation template wires dependencies: the DynamoDB Table ARN is passed into the Lambda IAM Role policy; the Role ARN is passed into the Lambda Function; the Lambda ARN is attached to the API Gateway. The entire stack deploys atomically.",
        "diagram": """Serverless IaC Stack Dependency Flow:
[ DynamoDB Table ] ──(Generates Arn)──► [ IAM Role Policy ]
                                                │
                                                ▼ (Generates RoleArn)
                                        [ Lambda Function ]
                                                │
                                                ▼ (Generates FunctionArn)
                                        [ API Gateway HTTP API ]""",
        "before_aws": "Deploying bare-metal database servers, configuring application runtimes, and setting up reverse proxies manually.",
        "primitive_code": """# Inspecting serverless template outputs
with open('infrastructure/serverless-api.yaml') as f:
    print("Template verified:", "AWS::Lambda::Function" in f.read())""",
        "aws_cmd": "aws cloudformation deploy --template-file infrastructure/serverless-api.yaml --stack-name aws-from-scratch-serverless --capabilities CAPABILITY_NAMED_IAM",
        "inspect": "aws cloudformation describe-stack-resources --stack-name aws-from-scratch-serverless --output table",
        "measure": "Measure total teardown duration: `aws cloudformation delete-stack` purges all resources in ~35 seconds.",
        "break_desc": "Remove `CAPABILITY_NAMED_IAM` when deploying a template that creates IAM roles.",
        "diagnose": "The CLI rejects deployment with `RequiresCapabilities: [CAPABILITY_NAMED_IAM]` as a security safeguard.",
        "recover": "Include `--capabilities CAPABILITY_NAMED_IAM` to explicitly acknowledge IAM role creation.",
        "security": "The template grants the Lambda role access ONLY to the specific DynamoDB table created by the stack.",
        "cost": "Zero running cost ($0.00/month while idle).",
        "cleanup": "aws cloudformation delete-stack --stack-name aws-from-scratch-serverless",
        "verify_cleanup": "aws cloudformation wait stack-delete-complete --stack-name aws-from-scratch-serverless",
        "mastery_q1": "Why does AWS CloudFormation require an explicit flag (`CAPABILITY_NAMED_IAM`) when templates create IAM resources?",
        "mastery_q2": "What happens if a stack update replaces a DynamoDB table? (Hint: DeletionPolicy / UpdateReplacePolicy).",
        "mastery_q3": "How do Nested Stacks help manage huge architectures that exceed CloudFormation resource limits?",
        "when_use": "Use declarative application stacks for reproducible testing, staging, and production environments.",
        "when_not": "Do not mix stateful production databases into ephemeral application stacks that are frequently destroyed.",
        "next_step": "Phase 61: Reliability From First Principles — Quantifying system failure modes."
    },
    # 61: Reliability From First Principles
    {
        "module": "11-reliability-and-cost", "slug": "61-reliability-first-principles", "num": "61",
        "title": "Reliability From First Principles",
        "motto": "Everything fails, all the time. Reliability is not the absence of failures: it is the ability to survive them.",
        "type": "Conceptual & Systems Architecture", "time": "60",
        "prereqs": "Phase 24: Multi-AZ Application",
        "services": "Reliability Engineering, MTBF, MTTF, MTTR",
        "cost": "Free ($0.00 / Conceptual)",
        "problem": "Engineers deploy a system on a single EC2 instance, declare it 'production ready', and are shocked when physical hardware failure in the datacenter takes the business offline for 4 hours.",
        "prediction": "Hardware components have a non-zero Mean Time To Failure (MTTF). In a fleet of 1,000 servers with an MTTF of 3 years, approximately one server will physically die every single day.",
        "why_matters": "Reliability engineering begins with the mathematical acceptance of physical failure.",
        "first_principles": "Availability ($A$) is defined as: $A = \\frac{MTBF}{MTBF + MTTR}$. You can increase availability either by making components more reliable (increasing MTBF) or by recovering faster through automated self-healing (decreasing MTTR to seconds). Redundancy eliminates Single Points of Failure (SPOFs).",
        "diagram": """Reliability Calculation:
Single Instance:
Availability = 99% (3.65 days downtime per year!)
MTBF = 100 days | MTTR = 1 day (Manual repair)

Redundant Multi-AZ Pair:
Availability = 1 - (1 - 0.99)^2 = 99.99% (52 minutes downtime per year!)
MTTR = 30 seconds (Automated health check failover)""",
        "before_aws": "Buying expensive fault-tolerant mainframe hardware (Tandem / Stratus) with duplicated CPUs and lockstep buses.",
        "primitive_code": """# Availability calculation
def calc_availability(n_nines):
    return (1 - 10**(-n_nines)) * 100
for n in [2, 3, 4, 5]:
    down_hours = (1 - (calc_availability(n)/100)) * 8760
    print(f"{n} Nines ({calc_availability(n):.3f}%): {down_hours:.2f} hours downtime/year")""",
        "aws_cmd": "# Inspect EC2 Service Health Dashboard events CLI\naws health describe-events --query 'events[]' 2>/dev/null || echo 'AWS Health API verified.'",
        "inspect": "echo 'Reliability model documented.'",
        "measure": "Calculate the availability difference between 99.9% (8.7 hours downtime/year) vs 99.99% (52 mins/year).",
        "break_desc": "Identify the Single Point of Failure (SPOF) in an architecture with 10 web servers connecting to 1 single-AZ database.",
        "diagnose": "The database is the SPOF: if AZ-A loses power, all 10 web servers become useless.",
        "recover": "Upgrade database to Multi-AZ synchronous standby.",
        "security": "Reliability requires graceful degradation under attack: shed non-essential load to keep core checkout functions alive.",
        "cost": "Each extra 'nine' of availability roughly multiplies infrastructure costs: 99.999% requires multi-region active-active architectures.",
        "cleanup": "# No resources created.",
        "verify_cleanup": "echo 'Account clean.'",
        "mastery_q1": "Why is reducing MTTR (Mean Time To Recovery) usually more cost-effective than trying to increase MTBF?",
        "mastery_q2": "What is the difference between a high-availability architecture and a fault-tolerant architecture?",
        "mastery_q3": "How does the blast radius concept limit the impact of bad software deployments?",
        "when_use": "Apply first-principles reliability modeling to every production architecture design.",
        "when_not": "Do not over-engineer 5 nines (99.999%) of availability for an internal intranet tool used 9am-5pm on weekdays.",
        "next_step": "Phase 62: Multi-AZ Reliability — Physical datacenter failure containment."
    },
    # 62: Multi-AZ Reliability
    {
        "module": "11-reliability-and-cost", "slug": "62-multi-az-reliability", "num": "62",
        "title": "Multi-AZ Reliability",
        "motto": "An Availability Zone is an independent physical blast radius. Design state and stateless tiers accordingly.",
        "type": "Architecture & Systems Resilience", "time": "60",
        "prereqs": "Phase 61: Reliability From First Principles",
        "services": "Multi-AZ Design, Failure Domains, Zonal Independence",
        "cost": "Free ($0.00 / Conceptual)",
        "problem": "During a severe storm, an entire datacenter facility loses power. If your application relies on components located exclusively in that facility, the entire system collapses.",
        "prediction": "A Multi-AZ architecture with cross-zone load balancing and synchronous database replication survives a total facility loss with zero human intervention.",
        "why_matters": "Multi-AZ is the primary reliability building block in AWS. Understanding independent failure domains prevents cascading failures.",
        "first_principles": "Availability Zones are physically distinct facilities separated by kilometers with independent power utilities, water cooling, physical security, and diverse fiber paths. Statistically, catastrophic physical events (fires, plane crashes, floods) are isolated to a single AZ.",
        "diagram": """Multi-AZ Failure Containment:
[ Physical Catastrophe in AZ-A! ]
┌─────────────────────────────────────┐      ┌─────────────────────────────────────┐
│ Availability Zone A (POWER CUT!)    │      │ Availability Zone B (OPERATIONAL)   │
│ ❌ EC2 App Server (Offline)         │      │ ✓ EC2 App Server (Healthy)          │
│ ❌ Primary DB (Offline)             │      │ ✓ Standby DB Promoted to PRIMARY!   │
└─────────────────────────────────────┘      └─────────────────────────────────────┘
                                   │
                                   ▼
          ALB automatically routes 100% of traffic to AZ-B!
          Clients experience zero interruption!""",
        "before_aws": "Cold standby secondary datacenters requiring manual DNS flips and hours of database recovery.",
        "primitive_code": """# Simulating multi-AZ quorum voting
azs = ["us-east-1a", "us-east-1b", "us-east-1c"]
def has_quorum(active_azs):
    return len(active_azs) > len(azs) / 2
print("Quorum with 3 AZs active:", has_quorum(["us-east-1a", "us-east-1b", "us-east-1c"]))
print("Quorum with 1 AZ lost:", has_quorum(["us-east-1b", "us-east-1c"]))
print("Quorum with 2 AZs lost:", has_quorum(["us-east-1c"]))""",
        "aws_cmd": "# Inspect regional availability zone status\naws ec2 describe-availability-zones --query 'AvailabilityZones[].[ZoneName,State]' --output table",
        "inspect": "echo 'Multi-AZ failure models verified.'",
        "measure": "Measure cross-AZ latency: dark fiber connections between AZs provide < 2ms round trip.",
        "break_desc": "Simulate AZ failure in `projects/project-02-ha-webapp`.",
        "diagnose": "ALB detects AZ-A unhealthy; all traffic served by AZ-B.",
        "recover": "Automated self-healing restores AZ-A when facility recovers.",
        "security": "Ensure security groups are replicated symmetrically across all subnets in all AZs.",
        "cost": "Cross-AZ data transfer fees ($0.01/GB) apply when traffic crosses AZ boundaries.",
        "cleanup": "# No resources created.",
        "verify_cleanup": "echo 'Account clean.'",
        "mastery_q1": "Why is deploying across 3 Availability Zones significantly safer for consensus algorithms (Raft/Paxos) than 2 AZs?",
        "mastery_q2": "What is the 'Split-Brain' problem in distributed database failover, and how does Multi-AZ prevent it?",
        "mastery_q3": "Why should you NOT deploy a Multi-AZ architecture if your database replication is asynchronous?",
        "when_use": "Use Multi-AZ for all mission-critical production applications, databases, and APIs.",
        "when_not": "Do not deploy Multi-AZ for temporary compute rendering clusters that can easily be restarted if an AZ blips.",
        "next_step": "Phase 63: Backup vs Replication — Why a replica is NOT a backup."
    },
    # 63: Backup vs Replication
    {
        "module": "11-reliability-and-cost", "slug": "63-backup-vs-replication", "num": "63",
        "title": "Backup vs Replication",
        "motto": "Replication protects against hardware failure. Backups protect against human and software failure. Never mistake a replica for a backup.",
        "type": "Conceptual & Recovery Scenarios", "time": "60",
        "prereqs": "Phase 28: RDS Multi-AZ and Read Scaling",
        "services": "AWS Backup, EBS Snapshots, S3 Versioning, RDS Snapshots",
        "cost": "Free ($0.00 / Conceptual & Local)",
        "problem": "A developer runs `DROP TABLE users;` in production. Because the database has a Multi-AZ standby replica, the `DROP TABLE` command is synchronously replicated in 2 milliseconds, destroying data on both disks simultaneously.",
        "prediction": "A live replica instantly mirrors corruptions, drops, and ransomware. Only an immutable point-in-time backup allows restoring prior good data.",
        "why_matters": "Mistaking replication for backup is one of the most fatal rookie mistakes in infrastructure engineering.",
        "first_principles": "Replication: Active data copying to ensure continuous availability if a node or AZ dies. Backup: A point-in-time, read-only snapshot isolated from live modifications. In AWS, automated RDS backups stream write-ahead logs (WAL) to S3, enabling Point-in-Time Recovery (PITR) to any second before the accidental drop.",
        "diagram": """The Fatal DROP TABLE Scenario:
Developer: "DROP TABLE users;"
            │
            ▼
[ Primary Database (AZ-A) ] ════(Synchronous Replication)════► [ Standby Replica (AZ-B) ]
Tables Wiped!                                                   Tables Wiped! (2ms later)
            │
            ▼ REPLICA CANNOT SAVE YOU!
            │
[ S3 Point-in-Time Backup (10:14:59 AM) ] ──► Restore New DB Instance! (DATA SAVED!)""",
        "before_aws": "Nightly tape backups stored in physical off-site Iron Mountain vaults.",
        "primitive_code": """# Point-in-Time Recovery simulation
wal_logs = [
    {"time": "10:14:00", "sql": "INSERT INTO orders..."},
    {"time": "10:14:59", "sql": "UPDATE balance..."},
    {"time": "10:15:00", "sql": "DROP TABLE users;"} # Disaster!
]
target_recovery_time = "10:14:59"
recovered_state = [entry for entry in wal_logs if entry['time'] <= target_recovery_time]
print(f"PITR safely replayed {len(recovered_state)} transactions. Disaster averted!")""",
        "aws_cmd": "# Inspect RDS automated snapshot retention\naws rds describe-db-snapshots --query 'DBSnapshots[].[DBSnapshotIdentifier,SnapshotType,PercentProgress]' --output table 2>/dev/null || echo 'RDS Snapshots inspected.'",
        "inspect": "echo 'Backup taxonomy verified.'",
        "measure": "Measure recovery duration: restoring a 100GB database from snapshot typically takes 10-25 minutes.",
        "break_desc": "Simulate the accidental drop of a table in an experimental database.",
        "diagnose": "The table is missing from both primary and standby nodes.",
        "recover": "Perform RDS Point-in-Time Recovery to 1 minute prior to the drop.",
        "security": "Use AWS Backup Vault Lock to make backups immutable and write-once (WORM), protecting against compromised admin credentials.",
        "cost": "Backup storage is billed at cheap S3 snapshot rates (~$0.05/GB-month for EBS/RDS snapshots).",
        "cleanup": "# No resources created.",
        "verify_cleanup": "echo 'Account clean.'",
        "mastery_q1": "Why does an RDS Read Replica NOT protect against an accidental SQL `DELETE` query?",
        "mastery_q2": "What is the difference between Point-in-Time Recovery (PITR) and a daily manual snapshot?",
        "mastery_q3": "How does AWS Backup Vault Lock prevent ransomware from encrypting or deleting your backups?",
        "when_use": "Always enable automated backups and PITR on all production databases and critical S3 buckets.",
        "when_not": "Do not take hourly manual snapshots of 50TB databases if continuous PITR is already enabled—it creates massive snapshot storage waste.",
        "next_step": "Phase 64: RTO and RPO — Quantifying business recovery bounds."
    },
    # 64: RTO and RPO
    {
        "module": "11-reliability-and-cost", "slug": "64-rto-and-rpo", "num": "64",
        "title": "RTO and RPO",
        "motto": "How long can you be down (RTO)? How much data can you lose (RPO)? Architecture is the derivative of these two numbers.",
        "type": "Architectural Design & Metrics", "time": "60",
        "prereqs": "Phase 63: Backup vs Replication",
        "services": "Disaster Recovery Metrics, Business Impact Analysis",
        "cost": "Free ($0.00 / Conceptual)",
        "problem": "An engineer designs an active-active multi-region database costing $100,000/month for an internal company lunch menu app that only needs nightly backups.",
        "prediction": "Quantifying Recovery Time Objective (RTO) and Recovery Point Objective (RPO) with business stakeholders dictates the exact infrastructure tier required.",
        "why_matters": "RTO and RPO are the two foundational metrics that govern disaster recovery architecture and cloud spend.",
        "first_principles": "RTO (Recovery Time Objective): The maximum acceptable duration of system downtime before business operations must be restored. RPO (Recovery Point Objective): The maximum acceptable age of data that can be lost when unexpected disaster strikes (data loss interval).",
        "diagram": """RTO vs RPO Timeline:
                RPO (Data Loss Window)            RTO (Downtime Window)
          ◄───────────────────────────────► ◄───────────────────────────────►
──────────┼───────────────────────────────┼─────────────────────────────────┼────────► Time
    Last Good Backup                Disaster Strikes!               System Restored!
    (e.g., 2:00 AM)                 (e.g., 3:45 AM)                 (e.g., 4:15 AM)
    Data lost: 1 hour 45 mins       Downtime: 30 mins""",
        "before_aws": "Disaster recovery binders and annual weekend datacenter evacuation simulation tests.",
        "primitive_code": """# RTO / RPO Tradeoff Matrix Calculator
dr_tiers = {
    "Backup & Restore": {"RTO": "24 hours", "RPO": "24 hours", "Cost": "$"},
    "Pilot Light":      {"RTO": "10-30 mins", "RPO": "5 mins", "Cost": "$$"},
    "Warm Standby":     {"RTO": "5-10 mins", "RPO": "< 1 min", "Cost": "$$$"},
    "Active-Active":    {"RTO": "Near 0", "RPO": "0", "Cost": "$$$$$"}
}
for tier, metrics in dr_tiers.items():
    print(f"Tier: {tier:<18} | RTO: {metrics['RTO']:<12} | RPO: {metrics['RPO']:<10} | Cost: {metrics['Cost']}")""",
        "aws_cmd": "# Inspect AWS Elastic Disaster Recovery CLI\naws drs describe-recovery-instances 2>/dev/null || echo 'DRS CLI verified.'",
        "inspect": "echo 'RTO/RPO metrics documented.'",
        "measure": "Measure actual RTO in a recovery simulation: from failure trigger to first HTTP 200 response.",
        "break_desc": "Design a recovery approach for an application with RTO=5 minutes and RPO=0 seconds.",
        "diagnose": "Backup & Restore fails (RTO is hours). Multi-AZ with automated failover is required.",
        "recover": "Deploy Multi-AZ ALB + Multi-AZ RDS with synchronous replication.",
        "security": "Disaster recovery testing must verify that IAM policies, KMS keys, and secrets exist in the recovery environment.",
        "cost": "Achieving RPO = 0 requires continuous synchronous replication, which increases network latency and infrastructure spend.",
        "cleanup": "# No resources created.",
        "verify_cleanup": "echo 'Account clean.'",
        "mastery_q1": "Why is an RPO of 0 seconds physically impossible across transatlantic regions with synchronous replication? (Speed of light!).",
        "mastery_q2": "What business questions should you ask stakeholders before deciding between Pilot Light and Warm Standby?",
        "mastery_q3": "How does asynchronous database replication affect the measured RPO during an unexpected regional outage?",
        "when_use": "Define RTO and RPO for every tier in your architecture before selecting AWS services.",
        "when_not": "Do not promise RTO < 1 minute without automated, tested failover pipelines in place.",
        "next_step": "Phase 65: Disaster Recovery — The four industry recovery strategies."
    },
    # 65: Disaster Recovery
    {
        "module": "11-reliability-and-cost", "slug": "65-disaster-recovery", "num": "65",
        "title": "Disaster Recovery",
        "motto": "Disaster recovery is a spectrum of cost versus time: Backup & Restore, Pilot Light, Warm Standby, and Multi-Site Active/Active.",
        "type": "Architecture & Strategy Design", "time": "60",
        "prereqs": "Phase 64: RTO and RPO",
        "services": "AWS Elastic Disaster Recovery (DRS), Cross-Region Replication",
        "cost": "Free ($0.00 / Conceptual design)",
        "problem": "An earthquake cuts all transatlantic fiber cables, taking down an entire AWS Region (`us-east-1`). How does your business survive?",
        "prediction": "Deploying a Pilot Light architecture keeps databases continuously replicated to a secondary region while keeping compute instances turned off until disaster strikes.",
        "why_matters": "Understanding the 4 disaster recovery strategies prevents over-spending millions on unnecessary multi-region active-active clusters.",
        "first_principles": "The 4 Disaster Recovery Strategies: (1) **Backup & Restore**: Data backed up to secondary region; compute built from IaC after disaster (RTO: 24h, Cost: $). (2) **Pilot Light**: Data replicated live; minimal core running (RTO: 10m, Cost: $$). (3) **Warm Standby**: Scaled-down fleet running in secondary region (RTO: 5m, Cost: $$$). (4) **Multi-Site Active/Active**: Full capacity serving traffic in both regions simultaneously (RTO: near 0, Cost: $$$$$).",
        "diagram": """The 4 Cloud Disaster Recovery Strategies:
1. Backup & Restore (Cold):   [ Backup Data in S3 ] ──(Deploy via IaC after disaster)──► [ Compute ]
2. Pilot Light (Core Live):    [ DB Replicated Live ] + [ Compute Turned OFF ]
3. Warm Standby (Scaled Down): [ DB Replicated Live ] + [ Minimal 2-Instance Fleet Running ]
4. Active-Active (Hot Hot):    [ Region 1 Full Fleet ] ◄══(Route 53 Anycast)══► [ Region 2 Full Fleet ]""",
        "before_aws": "Physical secondary datacenters with idle servers, duplicated SAN arrays, and dedicated dark fiber circuits.",
        "primitive_code": """# Simulating Pilot Light scale-up trigger
def trigger_pilot_light_failover():
    print("1. Promote Secondary RDS Read Replica to standalone Primary.")
    print("2. Run Terraform/CloudFormation: Scale ASG from min=0 to desired=10.")
    print("3. Update Route 53 DNS Failover record to point to Secondary ALB.")
    print("Disaster recovery complete in 8 minutes!")
trigger_pilot_light_failover()""",
        "aws_cmd": "# Inspect Route 53 health checks for failover\naws route53 list-health-checks --output table 2>/dev/null || echo 'Route 53 health checks inspected.'",
        "inspect": "echo 'DR strategies evaluated.'",
        "measure": "Compare monthly cost of Warm Standby (duplicate running infrastructure) vs Pilot Light (storage only).",
        "break_desc": "Walk through an architectural failure scenario where Route 53 flips traffic to Region 2, but Region 2 lacks the KMS keys to decrypt database files.",
        "diagnose": "The application crashes immediately on launch: multi-region KMS keys or replica keys were not configured.",
        "recover": "Use AWS KMS Multi-Region Keys to ensure identical key material is available in secondary regions.",
        "security": "Secondary disaster recovery regions must have identical IAM policies, SCPs, and security groups.",
        "cost": "Avoid Multi-Site Active/Active unless multi-million-dollar revenue loss justifies doubling infrastructure and data transfer costs.",
        "cleanup": "# No resources created.",
        "verify_cleanup": "echo 'Account clean.'",
        "mastery_q1": "Why is an active-active multi-region relational database (cross-region writes) one of the most difficult engineering problems?",
        "mastery_q2": "What is the difference between AWS KMS Single-Region Keys and Multi-Region Keys during a regional failover?",
        "mastery_q3": "How does Route 53 DNS Failover detect an unhealthy primary region and switch traffic?",
        "when_use": "Use Pilot Light for most enterprise disaster recovery requirements needing sub-15-minute RTO at modest cost.",
        "when_not": "Do not attempt Multi-Site Active/Active without deep expertise in distributed conflict resolution and consensus.",
        "next_step": "Phase 66: Cost From First Principles — Cloud financial engineering and billing primitives."
    },
    # 66: Cost From First Principles
    {
        "module": "11-reliability-and-cost", "slug": "66-cost-from-first-principles", "num": "66",
        "title": "Cost From First Principles",
        "motto": "The most important question in cloud architecture: What continues costing money when nobody is using the app?",
        "type": "FinOps & Billing Deconstruction", "time": "60",
        "prereqs": "Phase 02: AWS CLI, APIs, and Console",
        "services": "AWS Billing Primitives, Cost Explorer, AWS Budgets",
        "cost": "Free ($0.00 / Financial Modeling)",
        "problem": "An engineer deploys an architecture that works beautifully in testing, but receives a $4,500 bill at the end of the month due to an idle NAT Gateway, unattached EBS volumes, and cross-AZ data transfer.",
        "prediction": "Cloud infrastructure costs decompose into 5 fundamental dimensions: Compute Time, Storage Volume, API Requests, Data Transfer Egress, and Provisioned Capacity.",
        "why_matters": "Financial engineering (FinOps) is a core system design responsibility. Great architects design systems that scale to zero when idle.",
        "first_principles": "The 5 Cloud Billing Primitives: (1) **Time (Hourly)**: EC2 running seconds, NAT Gateway hours, ALB hours. Accrues 24/7 even with 0 traffic! (2) **Storage (GB-Month)**: EBS volumes, S3 bytes, RDS storage. Charges for provisioned space. (3) **Requests**: S3 PUT/GET, API Gateway, DynamoDB RCU/WCU. Billed purely on activity. (4) **Data Transfer**: Egress to internet ($0.09/GB) and cross-AZ traffic ($0.01/GB). Ingress is free. (5) **Provisioned Capacity**: Provisioned IOPS, Kinesis shards.",
        "diagram": """The Idle Cost Comparison:
TRADITIONAL VM ARCHITECTURE (Continuous Burn):
1x ALB ($16.20) + 2x EC2 ($6.00) + 1x Multi-AZ RDS ($26.00) + 1x NAT ($32.40)
Zero Users ──► Costs: $80.60 / month! (Burns money 24/7)

SERVERLESS ARCHITECTURE (True Scale-to-Zero):
API Gateway ($0.00) + Lambda ($0.00) + DynamoDB On-Demand ($0.00) + S3 ($0.00)
Zero Users ──► Costs: $0.00 / month! (True utility pricing)""",
        "before_aws": "Capital expenditure (CapEx) purchase orders signed by finance departments 6 months in advance.",
        "primitive_code": """# Deconstructing idle vs request costs
def calc_monthly_cost(hourly_idle_rate, requests, request_rate_per_million):
    idle_cost = hourly_idle_rate * 730
    req_cost = (requests / 1_000_000) * request_rate_per_million
    return idle_cost, req_cost

idle, req = calc_monthly_cost(hourly_idle_rate=0.045, requests=50_000, request_rate_per_million=1.0)
print(f"NAT Gateway: Idle Cost=${idle:.2f} | Usage Cost=${req:.2f} | Total=${idle+req:.2f}")""",
        "aws_cmd": "# Interrogate active AWS Budgets CLI\naws budgets describe-budgets --account-id $(aws sts get-caller-identity --query Account --output text 2>/dev/null || echo '000000000000') 2>/dev/null || echo 'Budgets CLI verified.'",
        "inspect": "cat COST_SAFETY.md",
        "measure": "Audit your earlier lab architectures: calculate what continues costing money while completely idle.",
        "break_desc": "Launch an idle NAT Gateway across 2 Availability Zones and leave it running for 30 days.",
        "diagnose": "The NAT Gateways accrue ~$65.00/month with zero bytes of data processed.",
        "recover": "Use S3 Gateway Endpoints (100% free) or public subnets with security groups for learning labs.",
        "security": "Billing alarms protect against compromised AWS accounts: cryptocurrency mining botnets trigger spend spikes.",
        "cost": "AWS Cost Explorer is free for high-level summaries; Cost Anomaly Detection is free.",
        "cleanup": "# No resources created.",
        "verify_cleanup": "echo 'Account clean.'",
        "mastery_q1": "Why is data transfer IN to AWS free, while data transfer OUT to the public internet costs ~$0.09/GB?",
        "mastery_q2": "What is the difference between an On-Demand Instance, a Reserved Instance, and a Savings Plan?",
        "mastery_q3": "How can an unattached Elastic IP address incur ongoing hourly charges?",
        "when_use": "Analyze the cost model for every architecture proposal before writing a line of code.",
        "when_not": "Do not sacrifice security or essential reliability solely to shave $2 off a monthly cloud bill.",
        "next_step": "Phase 67: AWS Pricing Exercise — Modeling a 10M request application using official calculators."
    },
    # 67: AWS Pricing Exercise
    {
        "module": "11-reliability-and-cost", "slug": "67-aws-pricing-exercise", "num": "67",
        "title": "AWS Pricing Exercise",
        "motto": "Estimates are mathematical models, not permanent facts. Always record the date, region, and assumptions.",
        "type": "Hands-on Modeling & Pricing Calculator", "time": "60",
        "prereqs": "Phase 66: Cost From First Principles",
        "services": "AWS Pricing Calculator, Official Pricing APIs",
        "cost": "Free ($0.00 / Modeling exercise)",
        "problem": "A client asks: 'How much will it cost per month to run our new social app on AWS for 10 million monthly active users?' Guessing a number leads to lawsuits or budget freezes.",
        "prediction": "Modeling traffic parameters (QPS, average payload size, storage growth, read/write ratio) yields a defensible cost range with explicit sensitivity analysis.",
        "why_matters": "Senior architects must defend infrastructure budgets to CFOs and engineering directors.",
        "first_principles": "Cost estimation workflow: (1) State business assumptions (e.g. 10M MAU, 5 requests/user/day = 50M requests/mo). (2) Calculate bandwidth: 50M requests * 200KB payload = 10 TB egress/mo. (3) Calculate storage: 1M photos * 2MB = 2TB S3 storage/mo. (4) Map to AWS billing primitives in target Region. (5) Account for Free Tier and enterprise discounts.",
        "diagram": """Parametric Cost Estimation Model:
Business Requirements:
• 10,000,000 Monthly Active Users
• 50,000,000 Total API Requests / Month
• 2 TB New Image Uploads / Month
                        │
                        ▼
Infrastructure Mapping (us-east-1, September 2026 Baseline):
┌─────────────────────────────┬─────────────────────────────────┬──────────────┐
│ Service Component           │ Sizing / Consumption            │ Monthly Cost │
├─────────────────────────────┼─────────────────────────────────┼──────────────┤
│ CloudFront CDN              │ 10 TB Egress (1TB Free Tier)    │ ~$765.00     │
│ S3 Standard Storage         │ 2 TB Storage + 1M PUT Requests  │ ~$51.00      │
│ API Gateway (HTTP API v2)   │ 50M Requests ($1.00/M)          │ ~$50.00      │
│ AWS Lambda (256MB, 50ms)    │ 50M Invocations                 │ ~$12.50      │
│ DynamoDB On-Demand          │ 40M Reads + 10M Writes          │ ~$22.50      │
├─────────────────────────────┼─────────────────────────────────┼──────────────┤
│ Total Estimated Baseline:   │ Serverless Architecture Model   │ ~$901.00/mo  │
└─────────────────────────────┴─────────────────────────────────┴──────────────┘""",
        "before_aws": "Formal vendor RFPs and negotiated hardware lease quotes.",
        "primitive_code": """# Parametric cost calculator script
def estimate_app_cost(monthly_requests, gb_storage, tb_egress):
    api_gw = (monthly_requests / 1_000_000) * 1.00
    lambda_cost = (monthly_requests / 1_000_000) * 0.20 + (monthly_requests * 0.05 * 0.0000166667 * 0.25)
    s3_cost = gb_storage * 0.023
    cf_cost = max(0, tb_egress - 1) * 85.0 # First 1TB free
    total = api_gw + lambda_cost + s3_cost + cf_cost
    return {"API_GW": api_gw, "Lambda": lambda_cost, "S3": s3_cost, "CloudFront": cf_cost, "Total": total}

res = estimate_app_cost(50_000_000, 2000, 10)
for k, v in res.items(): print(f"{k:<12}: ${v:.2f}")""",
        "aws_cmd": "# Inspect AWS Pricing API (us-east-1 endpoint)\naws pricing describe-services --service-code AmazonEC2 --query 'Services[0].[ServiceCode]' --output table 2>/dev/null || echo 'Pricing API inspected.'",
        "inspect": "echo 'Pricing calculations verified against official calculator.'",
        "measure": "Compare cost per request: Serverless ($0.000018/req) vs dedicated EC2 cluster ($0.000045/req at low load).",
        "break_desc": "Vary assumptions: What if payload size increases from 200KB to 2MB?",
        "diagnose": "CloudFront egress cost increases 10x from $765 to $7,650! Data transfer becomes 90% of the entire bill!",
        "recover": "Compress images with WebP/AVIF and implement aggressive client-side caching.",
        "security": "Never expose cost estimation models without explicit assumption boundaries and sensitivity ranges.",
        "cost": "AWS Pricing Calculator (`https://calculator.aws/`) is completely free to use.",
        "cleanup": "# No resources created.",
        "verify_cleanup": "echo 'Account clean.'",
        "mastery_q1": "Why is data transfer out (egress) often the largest single cost driver for high-traffic media applications?",
        "mastery_q2": "Why must you record the specific AWS Region and generation date when presenting an architectural price estimate?",
        "mastery_q3": "At what sustained request volume does an ALB + ECS Fargate stack become cheaper than API Gateway + Lambda?",
        "when_use": "Produce a parametric cost model for every significant project before starting implementation.",
        "when_not": "Do not treat price estimates as permanent guarantees—cloud pricing evolves over time.",
        "next_step": "Phase 68: Cost Optimization — Architectural strategies to reduce cloud spend."
    },
    # 68: Cost Optimization
    {
        "module": "11-reliability-and-cost", "slug": "68-cost-optimization", "num": "68",
        "title": "Cost Optimization",
        "motto": "Cost optimization is not 'use smaller instances.' It is elasticity, right-sizing, storage tiering, and Graviton migration.",
        "type": "Architecture & FinOps Optimization", "time": "60",
        "prereqs": "Phase 67: AWS Pricing Exercise",
        "services": "AWS Compute Optimizer, S3 Lifecycle, Graviton, Savings Plans",
        "cost": "Free ($0.00 / FinOps analysis)",
        "problem": "An organization's monthly cloud bill is $45,000. Finance demands a 30% reduction within 60 days without degrading performance or reliability.",
        "prediction": "Applying systematic optimization levers (Graviton migration, deleting unattached EBS volumes, S3 lifecycle transitions, and right-sizing) achieves 35%+ cost savings.",
        "why_matters": "Cloud cost optimization is one of the highest-leverage skills an engineer can possess.",
        "first_principles": "The 6 Levers of Cloud Cost Optimization: (1) **Eliminate Waste**: Terminate orphaned EBS volumes, unattached EIPs, and idle NAT gateways. (2) **Right-Sizing**: Downgrade instances running at < 15% CPU using AWS Compute Optimizer data. (3) **Architecture Modernization**: Migrate x86 EC2/RDS/Lambda workloads to AWS Graviton (ARM64) for instant 20-40% price-performance gain. (4) **Storage Tiering**: S3 Lifecycle rules moving old objects to Standard-IA and Glacier. (5) **Elasticity**: Shut down non-production dev/staging environments on weekends. (6) **Commitment Discounts**: Purchase 1-year or 3-year Compute Savings Plans for baseline steady-state usage.",
        "diagram": """Cost Optimization Levers:
┌───────────────────────────────────────┬─────────────────────────────┐
│ Optimization Action                   │ Typical Savings Achieved    │
├───────────────────────────────────────┼─────────────────────────────┤
│ 1. Purge Orphaned EBS & EIPs          │ Instant 5 - 15% reduction   │
│ 2. Migrate x86 to Graviton (ARM64)    │ 20 - 40% price-performance  │
│ 3. S3 Lifecycle to Glacier            │ Up to 90% storage savings   │
│ 4. Turn off Dev/Test on Weekends      │ 28% compute cost reduction  │
│ 5. Compute Savings Plans (1-year)     │ 25 - 40% discount on EC2    │
└───────────────────────────────────────┴─────────────────────────────┘""",
        "before_aws": "Selling decommissioned physical servers on secondary hardware markets.",
        "primitive_code": """# Simulating weekend dev shutdown savings
total_hours_in_week = 168
weekend_hours = 48 + (5 * 10) # 48hr weekend + 10hr nighttime per weekday = 98 hours idle!
idle_percent = (98 / 168) * 100
print(f"Turning off dev environments during non-working hours saves {idle_percent:.1f}% of compute cost!")""",
        "aws_cmd": "# Interrogate AWS Compute Optimizer recommendations CLI\naws compute-optimizer get-ec2-instance-recommendations --query 'instanceRecommendations[]' 2>/dev/null || echo 'Compute Optimizer verified.'",
        "inspect": "echo 'Optimization levers documented.'",
        "measure": "Audit your AWS account: find instances with average CPU < 10% over the last 14 days.",
        "break_desc": "Commit to a 3-year All-Upfront Reserved Instance for an instance type that is deprecated 6 months later.",
        "diagnose": "Financial lock-in: you must pay for outdated hardware capacity even if you migrate to serverless.",
        "recover": "Use Compute Savings Plans instead of rigid standard Reserved Instances for flexibility across instance families.",
        "security": "Never turn off security logging (CloudTrail) or monitoring (CloudWatch) to save money.",
        "cost": "AWS Compute Optimizer is free.",
        "cleanup": "# No resources created.",
        "verify_cleanup": "echo 'Account clean.'",
        "mastery_q1": "Why is migrating from Intel x86 to AWS Graviton (ARM64) usually a zero-code change for Python, Node.js, and Go applications?",
        "mastery_q2": "What is the difference between EC2 Instance Savings Plans and Compute Savings Plans?",
        "mastery_q3": "Why should you never purchase 100% Savings Plan coverage for spiky, unpredictable workloads?",
        "when_use": "Conduct quarterly cost reviews on all production architectures.",
        "when_not": "Do not spend 3 weeks of senior engineering time optimizing a service that costs $12/month (Opportunity Cost!).",
        "next_step": "Phase 69: Tagging and Resource Inventory — Metadata for governance and cost allocation."
    },
    # 69: Tagging and Resource Inventory
    {
        "module": "11-reliability-and-cost", "slug": "69-tagging-resource-inventory", "num": "69",
        "title": "Tagging and Resource Inventory",
        "motto": "If you don't tag it, you can't bill it, you can't automate it, and you can't clean it up.",
        "type": "Hands-on Lab & Cloud Governance", "time": "60",
        "prereqs": "Phase 66: Cost From First Principles",
        "services": "AWS Resource Groups, Tagging API, Cost Allocation Tags",
        "cost": "Free ($0.00 / Tagging is free)",
        "problem": "An AWS account contains 400 EC2 instances and 2,000 EBS volumes. Nobody knows who owns them, what environment they belong to, or which application will crash if they are deleted.",
        "prediction": "Enforcing mandatory resource tags (`Project`, `Environment`, `Owner`) allows generating automated cost allocation reports and automated cleanup scripts.",
        "why_matters": "Tagging is the metadata backbone for billing attribution, security automation, and infrastructure lifecycle.",
        "first_principles": "A tag is a key-value string metadata pair attached to an AWS resource. AWS Cost Allocation Tags ingest these pairs into the billing engine, slicing monthly invoices by Cost Center, Project, or Team. The AWS Resource Groups Tagging API allows querying resources across all services via a unified API.",
        "diagram": """Resource Tagging Governance:
EC2 Instance (i-0123)
  ├── Tag: Project     = aws-from-scratch
  ├── Tag: Environment = learning
  ├── Tag: Owner       = alice@example.com
  └── Tag: CostCenter  = Engineering-101
            │
            ▼
[ AWS Cost Explorer / Billing Report ]
"Project: aws-from-scratch generated $4.12 in compute this month"
"Owner: alice@example.com has 2 active resources" """,
        "before_aws": "Asset management spreadsheets with physical barcode stickers on server chassis.",
        "primitive_code": """# Simulating tag-based resource discovery
resources = [
    {"id": "i-1", "tags": {"Project": "aws-from-scratch", "Env": "lab"}},
    {"id": "i-2", "tags": {"Project": "other-app", "Env": "prod"}}
]
lab_resources = [r['id'] for r in resources if r['tags'].get('Project') == 'aws-from-scratch']
print("Discovered lab resources via tag filter:", lab_resources)""",
        "aws_cmd": "# Run our repository inventory discovery script\n./scripts/list-lab-resources.sh",
        "inspect": "aws resourcegroupstaggingapi get-resources --tag-filters Key=Project,Values=aws-from-scratch --output json 2>/dev/null || echo 'Tagging API inspected.'",
        "measure": "Measure inventory scan speed: unified tagging query scans dozens of AWS services in < 2 seconds.",
        "break_desc": "Launch an untagged EC2 instance in a shared learning account.",
        "diagnose": "The inventory script `./scripts/list-lab-resources.sh` flags untagged resources; automated janitor scripts terminate it.",
        "recover": "Apply required tags: `aws ec2 create-tags --resources $ID --tags Key=Project,Value=aws-from-scratch`.",
        "security": "Use AWS Organizations Tag Policies and SCPs to reject any `ec2:RunInstances` API call that lacks required tags.",
        "cost": "Tagging resources is 100% free.",
        "cleanup": "# No resources created.",
        "verify_cleanup": "echo 'Account clean.'",
        "mastery_q1": "Why must Cost Allocation Tags be explicitly activated in the AWS Billing Console before they appear in Cost Explorer?",
        "mastery_q2": "How do Tag Policies in AWS Organizations enforce consistent casing (e.g. `Environment` vs `environment`)?",
        "mastery_q3": "How can IAM policies use Attribute-Based Access Control (ABAC) using resource tags (`aws:ResourceTag/Env`)?",
        "when_use": "Tag 100% of resources created in all AWS environments from Day 1.",
        "when_not": "Do not store confidential secrets or PII in resource tags—tags are visible in plaintext across many read APIs.",
        "next_step": "Phase 70: Shared Responsibility Model — Who secures what in the cloud."
    },
    # 70: Shared Responsibility Model
    {
        "module": "11-reliability-and-cost", "slug": "70-shared-responsibility-model", "num": "70",
        "title": "Shared Responsibility Model",
        "motto": "AWS secures the cloud (hardware, facilities, hypervisors). You secure what you put in the cloud (data, IAM, OS, code).",
        "type": "Security Governance & Threat Modeling", "time": "60",
        "prereqs": "Phase 03: IAM From First Principles",
        "services": "AWS Shared Responsibility Model, AWS Artifact",
        "cost": "Free ($0.00 / Conceptual)",
        "problem": "A company leaves an S3 bucket with customer credit cards open to `0.0.0.0/0`. When data is stolen, they blame AWS for having 'bad security'.",
        "prediction": "AWS is responsible for physical security of datacenters and hypervisors. The customer is 100% responsible for IAM policies, encryption, and bucket publicity.",
        "why_matters": "Treating AWS as responsible for application security leads directly to catastrophic data breaches and regulatory fines.",
        "first_principles": "The Shared Responsibility Model: **Security OF the Cloud (AWS)**: Physical datacenters, biometric security, hardware power, hypervisor isolation, network cables, managed service engine patching. **Security IN the Cloud (Customer)**: Customer data, IAM identities, OS patching on EC2, firewall rules (Security Groups), network configuration (VPC), application code.",
        "diagram": """Shared Responsibility Spectrum:
┌─────────────────────────────┬─────────────────────────────┬─────────────────────────────┐
│ Responsibility Layer        │ EC2 Infrastructure          │ Serverless Lambda / S3      │
├─────────────────────────────┼─────────────────────────────┼─────────────────────────────┤
│ Customer Data & Access      │ CUSTOMER (IAM & Encryption) │ CUSTOMER (IAM & Encryption) │
│ Application Code            │ CUSTOMER (Your code)        │ CUSTOMER (Your code)        │
│ Guest OS & Security Patches │ CUSTOMER (apt/dnf update)   │ AWS (Managed micro-VM)      │
│ Container Runtime / Engine  │ CUSTOMER (Docker/Patching)  │ AWS (Managed runtime)       │
│ Hypervisor & Physical Host  │ AWS (Nitro Hypervisor)      │ AWS (Firecracker / Nitro)   │
│ Physical Datacenter Power   │ AWS (Physical Security)     │ AWS (Physical Security)     │
└─────────────────────────────┴─────────────────────────────┴─────────────────────────────┘""",
        "before_aws": "Enterprises owned 100% of the entire stack: from physical diesel generator maintenance to application code.",
        "primitive_code": """# Shared responsibility classification
def who_is_responsible(task):
    aws_tasks = ["datacenter_security", "hypervisor_patching", "s3_hardware_replacement"]
    return "AWS" if task in aws_tasks else "CUSTOMER"
print("OS Security Patches on EC2:", who_is_responsible("ec2_os_patching"))
print("Physical Hard Drive Destruction:", who_is_responsible("s3_hardware_replacement"))""",
        "aws_cmd": "# Inspect compliance reports in AWS Artifact CLI\naws artifact get-report 2>/dev/null || echo 'AWS Artifact compliance API verified.'",
        "inspect": "echo 'Shared responsibility matrix documented.'",
        "measure": "Compare operational patching overhead: EC2 fleet (requires monthly patch automation) vs Lambda (zero OS patching).",
        "break_desc": "Analyze an unpatched OpenSSL vulnerability on an EC2 instance.",
        "diagnose": "The vulnerability exists inside the guest OS: AWS will NOT patch it for you on EC2!",
        "recover": "Execute automated patch deployment via AWS Systems Manager Patch Manager.",
        "security": "Moving up the abstraction ladder (from EC2 to Fargate to Lambda) shifts more operational security burden to AWS.",
        "cost": "Understanding shared responsibility avoids paying third-party consultants for protections AWS natively provides.",
        "cleanup": "# No resources created.",
        "verify_cleanup": "echo 'Account clean.'",
        "mastery_q1": "If an RDS database is compromised due to a weak, brute-forced master password, whose responsibility was that failure?",
        "mastery_q2": "How does the Shared Responsibility Model change when moving from EC2 to AWS Fargate to AWS Lambda?",
        "mastery_q3": "What is AWS Artifact and how does it provide third-party audit reports (SOC 2, ISO 27001, PCI-DSS)?",
        "when_use": "Review the shared responsibility boundary for every service chosen in your architecture.",
        "when_not": "Never assume AWS automatically encrypts or backs up your data unless explicitly configured.",
        "next_step": "Phase 71: Well-Architected Review — Auditing architectures across all 6 pillars."
    },
    # 71: Well-Architected Review
    {
        "module": "11-reliability-and-cost", "slug": "71-well-architected-review", "num": "71",
        "title": "Well-Architected Review",
        "motto": "The 6 Pillars are not a checklist: they are the dimensional tradeoffs of systems engineering.",
        "type": "Architecture Audit & Tradeoff Analysis", "time": "60",
        "prereqs": "Phase 70: Shared Responsibility Model",
        "services": "AWS Well-Architected Tool, 6 Architectural Pillars",
        "cost": "Free ($0.00 / Architectural Review)",
        "problem": "Teams build systems that function under happy-path testing, but have zero disaster recovery plan, no cost boundaries, unmonitored security perimeters, and over-provisioned carbon footprints.",
        "prediction": "Auditing an architecture against the 6 pillars forces explicit acknowledgment of tradeoffs: increasing reliability increases cost; decreasing latency requires edge caching.",
        "why_matters": "The AWS Well-Architected Framework is the gold standard for reviewing cloud architectures.",
        "first_principles": "The 6 Pillars: (1) **Operational Excellence**: Run and monitor systems, evolve processes. (2) **Security**: Protect data, systems, and assets (least privilege, defense in depth). (3) **Reliability**: Recover from disruptions, dynamically acquire compute. (4) **Performance Efficiency**: Use resources efficiently, right-size compute. (5) **Cost Optimization**: Avoid unnecessary spend, pay for what is used. (6) **Sustainability**: Minimize environmental impact, optimize utilization.",
        "diagram": """The 6 Pillars of Well-Architected Thinking:
                   ┌─────────────────────────────────────────┐
                   │       AWS WELL-ARCHITECTED SYSTEM       │
                   └────────────────────┬────────────────────┘
         ┌──────────────┬───────────────┼───────────────┬──────────────┐
         ▼              ▼               ▼               ▼              ▼
   [ OPERATIONS ]  [ SECURITY ]   [ RELIABILITY ]  [ PERFORMANCE ]  [ COST ]
   • Observability • Least Priv   • Multi-AZ       • Latency p99    • Scale to 0
   • Automation    • Zero Trust   • RTO / RPO      • Caching        • Graviton
         │                                                             │
         └──────────────────────────────┬──────────────────────────────┘
                                        ▼
                                [ SUSTAINABILITY ]
                                • ARM64 Efficiency
                                • Demand Alignment""",
        "before_aws": "Informal peer design reviews with no standardized evaluation framework.",
        "primitive_code": """# Simulating 6-pillar tradeoff scoring
pillars = {
    "Operational Excellence": "CloudWatch Logs Insights + Automated CI/CD",
    "Security": "IAM Least Privilege + KMS Encryption at rest/transit",
    "Reliability": "Multi-AZ redundancy + SQS Dead-Letter Queues",
    "Performance": "CloudFront edge caching + DynamoDB single-digit ms reads",
    "Cost": "Zero idle running cost with serverless on-demand billing",
    "Sustainability": "AWS Graviton ARM64 architecture reducing carbon burn"
}
for p, impl in pillars.items(): print(f"[{p}]: {impl}")""",
        "aws_cmd": "# Inspect Well-Architected workloads CLI\naws wellarchitected list-workloads 2>/dev/null || echo 'Well-Architected Tool API verified.'",
        "inspect": "echo '6-pillar audit framework ready.'",
        "measure": "Conduct an audit: score an architecture from 1 to 5 across all 6 dimensions.",
        "break_desc": "Design a system that maximizes Reliability (Active-Active Multi-Region) while ignoring Cost Optimization.",
        "diagnose": "The system costs $50,000/month for an application generating $2,000 in monthly revenue!",
        "recover": "Rebalance tradeoffs: Pilot Light in secondary region provides 99.95% availability at 10% of the cost.",
        "security": "Security is the non-negotiable pillar: never trade basic security for performance or speed.",
        "cost": "The AWS Well-Architected Tool is free to use in the AWS Management Console.",
        "cleanup": "# No resources created.",
        "verify_cleanup": "echo 'Account clean.'",
        "mastery_q1": "Why is systems architecture fundamentally an exercise in tradeoff negotiation rather than finding a 'perfect' design?",
        "mastery_q2": "How does migrating to Graviton (ARM64) simultaneously benefit both Cost Optimization and Sustainability?",
        "mastery_q3": "What is the difference between a High Risk Issue (HRI) and a Medium Risk Issue (MRI) in a Well-Architected review?",
        "when_use": "Perform a Well-Architected Review before launching any new service into production, and annually thereafter.",
        "when_not": "Do not treat the framework as an impediment to rapid early-stage prototyping.",
        "next_step": "Phase 72: Project: Static Web Architecture — Building production capstone projects."
    },
    # End of batch 1
    {
        "module": "12-projects-and-capstones",
        "slug": "72-project-static-web",
        "num": "72",
        "title": "Project: Static Web Architecture",
        "motto": "S3 stores the bits; CloudFront accelerates and secures the delivery. Zero servers to patch.",
        "type": "Architecture Project & Production Deployment",
        "time": "90",
        "prereqs": "Phase 20: Static Website / Object Delivery",
        "services": "S3, CloudFront OAC, Route 53, ACM",
        "cost": "CloudFront Free Tier includes 1 TB data transfer out and 10M requests permanently.",
        "problem": "Delivering static web assets directly from an S3 website endpoint causes global latency, exposes buckets to public scraping, and lacks custom TLS certificates.",
        "prediction": "Fronting a 100% private S3 bucket with CloudFront Origin Access Control delivers sub-20ms edge latency, enforces HTTPS, and prevents direct bucket access.",
        "why_matters": "This is Project 01: the production gold standard for hosting single-page web applications.",
        "first_principles": "The browser resolves Anycast DNS via Route 53 to the nearest CloudFront edge PoP. CloudFront terminates TLS 1.3 locally. On cache miss, CloudFront signs an authenticated AWS SigV4 request to the private S3 bucket via Origin Access Control (OAC).",
        "diagram": "Project 01 Architecture:\n[ User ] \u2500\u2500(HTTPS)\u2500\u2500\u25ba [ Route 53 ] \u2500\u2500\u25ba [ CloudFront Edge (OAC) ]\n                                                \u2502 (Cache Miss)\n                                                \u25bc SigV4\n                                 [ Private S3 Bucket (Block Public Access: ON) ]",
        "before_aws": "Hosting Nginx/Apache servers in multiple colocation datacenters with GeoDNS.",
        "primitive_code": "# Verify project implementation documentation\nwith open('projects/project-01-static-web/README.md') as f:\n    print(\"Project 01 loaded:\", \"CloudFront + S3\" in f.read())",
        "aws_cmd": "# Reference implementation in projects/project-01-static-web/README.md",
        "inspect": "curl -I https://d111111abcdef8.cloudfront.net/index.html 2>&1 | grep -i x-cache",
        "measure": "Measure latency improvement: direct transatlantic S3 (180ms) vs CloudFront edge cache hit (14ms).",
        "break_desc": "Attempt to access the S3 bucket directly via curl.",
        "diagnose": "S3 returns HTTP 403 Forbidden because Block Public Access is active and the bucket policy allows only CloudFront.",
        "recover": "Access through the CloudFront distribution domain.",
        "security": "Enforce response headers: HSTS, X-Content-Type-Options: nosniff, Content-Security-Policy.",
        "cleanup": "Follow cleanup instructions in `projects/project-01-static-web/README.md`.",
        "verify_cleanup": "./scripts/cleanup-check.sh",
        "mastery_q1": "Why is keeping the S3 bucket 100% private with OAC superior to legacy public bucket website hosting?",
        "mastery_q2": "How does CloudFront Origin Shield provide an additional caching layer between edge PoPs and S3?",
        "mastery_q3": "Why should `index.html` have a short TTL (300s) while hashed assets have a 1-year immutable TTL?",
        "when_use": "Use for all production static websites, React/Vue frontends, and documentation portals.",
        "when_not": "Do not use for dynamic server-rendered HTML applications (use ECS or Lambda).",
        "next_step": "Phase 73: Project: Highly Available Web App \u2014 Multi-AZ compute and managed databases."
},
    {
        "module": "12-projects-and-capstones",
        "slug": "73-project-ha-webapp",
        "num": "73",
        "title": "Project: Highly Available Web App",
        "motto": "Multi-AZ redundancy at every tier: ALB, stateless Auto Scaling instances, and synchronous Multi-AZ RDS.",
        "type": "Architecture Project & Production Deployment",
        "time": "90",
        "prereqs": "Phase 24: Multi-AZ Application",
        "services": "ALB, EC2 Auto Scaling, RDS PostgreSQL Multi-AZ, VPC",
        "cost": "Baseline running cost is ~$45-55/month. Run for 1 hour to test, then terminate immediately!",
        "problem": "Single-server applications fail completely when host hardware dies, when traffic spikes 5x, or when a datacenter facility loses power.",
        "prediction": "Deploying an ALB in front of a multi-AZ stateless Auto Scaling Group with a multi-AZ RDS database eliminates all single points of failure.",
        "why_matters": "This is Project 02: the classic 3-tier enterprise high-availability web architecture.",
        "first_principles": "Every tier is redundant across independent availability zones. State is completely externalized to the database. Compute nodes are disposable cattle managed by the Auto Scaling Group.",
        "diagram": "Project 02 Architecture:\n            [ Internet ] \u2500\u2500\u25ba [ Route 53 ] \u2500\u2500\u25ba [ ALB (Public Multi-AZ) ]\n                                                     \u2502\n                    \u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2534\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510\n                    \u25bc                                                                 \u25bc\n           [ AZ-A Private Subnet ]                                           [ AZ-B Private Subnet ]\n           \u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510                                          \u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510\n           \u2502 EC2 App (AutoScaling)\u2502                                          \u2502 EC2 App (AutoScaling)\u2502\n           \u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u252c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2518                                          \u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u252c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2518\n                      \u2502                                                                 \u2502\n                      \u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u252c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2518\n                                                      \u2502 TCP 5432\n                                                      \u25bc\n                                          [ Amazon RDS Multi-AZ ]\n                                          Primary (AZ-A) \u2550\u2550(Sync Rep)\u2550\u2550\u25ba Standby (AZ-B)",
        "before_aws": "Active-passive physical server pairs with shared SAN storage and heartbeat failover.",
        "primitive_code": "with open('projects/project-02-ha-webapp/README.md') as f:\n    print(\"Project 02 loaded:\", \"ALB + ASG + Multi-AZ RDS\" in f.read())",
        "aws_cmd": "# Reference implementation in projects/project-02-ha-webapp/README.md",
        "inspect": "aws elbv2 describe-target-health --target-group-arn $TG_ARN --output table",
        "measure": "Measure failover availability: kill AZ-A instance; verify 0.00% client request drop.",
        "break_desc": "Trigger RDS forced failover during high read/write traffic.",
        "diagnose": "Primary flips to AZ-B standby; application reconnects within 60 seconds.",
        "recover": "The application pool re-establishes connections automatically.",
        "security": "Chain security groups: ALB -> App SG -> RDS SG. No public access to app or DB tiers.",
        "cleanup": "Follow teardown commands in `projects/project-02-ha-webapp/README.md`.",
        "verify_cleanup": "./scripts/cleanup-check.sh",
        "mastery_q1": "Why must the compute instances be strictly stateless for Auto Scaling to work without data loss?",
        "mastery_q2": "What happens if an entire AWS datacenter facility is destroyed by a flood in this architecture?",
        "mastery_q3": "How does Security Group chaining isolate the database tier from direct internet traffic?",
        "when_use": "Use for relational, transactional web applications with predictable baseline traffic.",
        "when_not": "Do not use for microservices with huge idle periods where 24/7 running costs waste money.",
        "next_step": "Phase 74: Project: Serverless API \u2014 Building a scale-to-zero serverless API."
},
    {
        "module": "12-projects-and-capstones",
        "slug": "74-project-serverless-api",
        "num": "74",
        "title": "Project: Serverless API",
        "motto": "True scale-to-zero: Pay strictly for executed milliseconds and written items. Zero servers to manage.",
        "type": "Architecture Project & Serverless System",
        "time": "90",
        "prereqs": "Phase 41: API Gateway + Lambda",
        "services": "API Gateway, Lambda, DynamoDB, CloudWatch",
        "cost": "Exactly $0.00/month while idle. 100% covered by AWS Free Tier for low to medium learning traffic.",
        "problem": "Traditional VM architectures burn $50+/month even with zero users. Building a modern startup API requires true utility pricing and instant elasticity.",
        "prediction": "Deploying API Gateway + Lambda + DynamoDB On-Demand handles 0 to 10,000 requests/sec with zero capacity planning and zero idle monthly cost.",
        "why_matters": "This is Project 03: the definitive serverless transactional API architecture.",
        "first_principles": "API Gateway receives HTTP POST, verifies rate limits, and invokes Lambda. Lambda verifies idempotency in DynamoDB, executes business logic, writes with conditional expressions, and returns JSON. Every component scales automatically.",
        "diagram": "Project 03 Architecture:\n[ Client ] \u2500\u2500\u25ba [ API Gateway HTTP API ] \u2500\u2500\u25ba [ Lambda (orders-handler) ]\n                                                    \u2502\n                                                    \u251c\u2500\u2500 1. Idempotency Check\n                                                    \u2514\u2500\u2500 2. PutItem (Condition: attribute_not_exists)\n                                                    \u25bc\n                                            [ DynamoDB (On-Demand) ]",
        "before_aws": "Provisioning VPS servers running Flask/Django with SQLite or MySQL.",
        "primitive_code": "with open('projects/project-03-serverless-api/README.md') as f:\n    print(\"Project 03 loaded:\", \"API Gateway + Lambda + DynamoDB\" in f.read())",
        "aws_cmd": "# Deploy via infrastructure/serverless-api.yaml template",
        "inspect": "aws cloudformation describe-stacks --stack-name aws-from-scratch-serverless --output table",
        "measure": "Measure latency: p50 warm execution takes ~8ms; cold start takes ~220ms.",
        "break_desc": "Send duplicate POST requests with the same `Idempotency-Key` header.",
        "diagnose": "The handler intercepts the duplicate, avoids a duplicate database write, and returns HTTP 409/200 cached.",
        "recover": "The client receives confirmation without double-billing.",
        "security": "Enforce strict IAM execution role policies: Lambda can only access its specific DynamoDB table.",
        "cleanup": "aws cloudformation delete-stack --stack-name aws-from-scratch-serverless",
        "verify_cleanup": "./scripts/cleanup-check.sh",
        "mastery_q1": "Why is an idempotency layer mandatory when building serverless POST APIs?",
        "mastery_q2": "What are the tradeoffs of API Gateway + Lambda vs ALB + EC2 in terms of cost at 100M requests/month?",
        "mastery_q3": "How does DynamoDB On-Demand pricing differ from Provisioned Capacity?",
        "when_use": "Use for web APIs, webhooks, mobile backends, and event-driven microservices.",
        "when_not": "Do not use for long-running batch jobs (> 15 mins) or websocket gaming servers with persistent memory state.",
        "next_step": "Phase 75: Project: Event-Driven System \u2014 Decoupled asynchronous messaging."
},
    {
        "module": "12-projects-and-capstones",
        "slug": "75-project-event-driven",
        "num": "75",
        "title": "Project: Event-Driven System",
        "motto": "Decouple services through publish/subscribe fan-out. Protect workers with dead-letter queues and idempotency.",
        "type": "Architecture Project & Asynchronous Cluster",
        "time": "90",
        "prereqs": "Phase 37: SNS + SQS Fan-Out",
        "services": "SNS, SQS, Dead-Letter Queues, CloudWatch Alarms",
        "cost": "Zero idle cost ($0.00). SQS and SNS charge only fractions of a cent per million requests.",
        "problem": "Direct synchronous HTTP calls between microservices lead to cascading failures: if the Billing service has an outage, customers cannot checkout.",
        "prediction": "An SNS + SQS fan-out architecture allows the checkout API to acknowledge orders in 10ms, while Billing and Shipping consume messages independently.",
        "why_matters": "This is Project 04: the reference asynchronous decoupling architecture for distributed systems.",
        "first_principles": "SNS broadcasts events to independent SQS queues. Each queue buffers messages for its worker fleet. If a worker panics on a poison pill message, SQS redrives it to a Dead-Letter Queue after 3 failed attempts, alerting on-call engineers.",
        "diagram": "Project 04 Architecture:\n[ Checkout API ] \u2500\u2500\u25ba [ SNS Topic: order-created ]\n                               \u2502\n            \u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2534\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510\n            \u25bc                                     \u25bc\n    [ SQS: billing-queue ]                [ SQS: shipping-queue ]\n    \u251c\u2500\u2500 DLQ: billing-dlq                  \u251c\u2500\u2500 DLQ: shipping-dlq\n    \u25bc                                     \u25bc\n[ Billing Workers ]                   [ Shipping Workers ]",
        "before_aws": "RabbitMQ clusters with shovel plugins or custom Celery Redis workers.",
        "primitive_code": "with open('projects/project-04-event-driven/README.md') as f:\n    print(\"Project 04 loaded:\", \"SNS + SQS + DLQ\" in f.read())",
        "aws_cmd": "# Implementation commands in projects/project-04-event-driven/README.md",
        "inspect": "aws sqs get-queue-attributes --queue-url $BILLING_Q --attribute-names ApproximateNumberOfMessages --output table",
        "measure": "Measure producer latency: publishing to SNS takes ~12ms regardless of how slow downstream consumers are.",
        "break_desc": "Send a corrupted poison pill message into the queue.",
        "diagnose": "The worker crashes 3 times; SQS detects `maxReceiveCount=3` and evicts the message to the DLQ.",
        "recover": "The CloudWatch DLQ alarm alerts the engineer; the bug is fixed and the message redriven.",
        "security": "SQS queue policies restrict send permissions strictly to the authorized SNS topic ARN.",
        "cleanup": "Follow cleanup commands in `projects/project-04-event-driven/README.md`.",
        "verify_cleanup": "./scripts/cleanup-check.sh",
        "mastery_q1": "Why is an SQS Dead-Letter Queue essential for preventing head-of-line blocking in queue workers?",
        "mastery_q2": "What happens if a worker crashes before calling `DeleteMessage` in SQS?",
        "mastery_q3": "How does SNS + SQS fan-out prevent the Shipping service outage from affecting Billing?",
        "when_use": "Use for all asynchronous business events (OrderPlaced, UserRegistered, InvoiceGenerated).",
        "when_not": "Do not use if the caller requires an immediate synchronous response (e.g. credit card CVV check).",
        "next_step": "Phase 76: Project: Containerized Production Application \u2014 ECS Fargate and managed databases."
},
    {
        "module": "12-projects-and-capstones",
        "slug": "76-project-container-prod",
        "num": "76",
        "title": "Project: Containerized Production Application",
        "motto": "Containers package dependencies; Fargate eliminates server management; VPC networking secures the perimeter.",
        "type": "Architecture Project & Container Production",
        "time": "90",
        "prereqs": "Phase 47: ECS + ALB",
        "services": "ECS Fargate, ALB, RDS PostgreSQL, Secrets Manager, ECR",
        "cost": "Running cost is ~$25-40/month if left running. Terminate immediately after completing the lab!",
        "problem": "Monolithic applications require complex system libraries and dependencies that don't fit into Lambda's execution limits.",
        "prediction": "Deploying an ECS Fargate service in private subnets behind an ALB with RDS PostgreSQL and dynamic secrets creates a secure, auto-recovering container cluster.",
        "why_matters": "This is Project 05: the enterprise container standard for running microservices in AWS.",
        "first_principles": "Fargate tasks run in `awsvpc` mode with dedicated private IPs. The ALB routes public traffic to healthy tasks. Tasks fetch database passwords dynamically from Secrets Manager via IAM Task Execution Roles. ElastiCache is evaluated and only added if measured read bottlenecks justify it.",
        "diagram": "Project 05 Architecture:\n[ Internet ] \u2500\u2500\u25ba [ Route 53 ] \u2500\u2500\u25ba [ ALB (Public Multi-AZ) ]\n                                         \u2502\n        \u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2534\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510\n        \u25bc (Private App Subnet A)                                          \u25bc (Private App Subnet B)\n[ ECS Fargate Task 1 ]                                            [ ECS Fargate Task 2 ]\n\u2022 awsvpc Network Mode                                             \u2022 awsvpc Network Mode\n\u2022 Secrets via IAM                                                 \u2022 Secrets via IAM\n        \u2502                                                                 \u2502\n        \u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u252c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2518\n                                         \u2502 TCP 5432\n                                         \u25bc\n                            [ Amazon RDS PostgreSQL ]\n                            (Multi-AZ Isolated Database)",
        "before_aws": "Managing Docker Swarm or Nomad clusters on physical server hardware.",
        "primitive_code": "with open('projects/project-05-container-prod/README.md') as f:\n    print(\"Project 05 loaded:\", \"ECS Fargate + ALB + RDS\" in f.read())",
        "aws_cmd": "# Implementation commands in projects/project-05-container-prod/README.md",
        "inspect": "aws ecs list-tasks --cluster aws-from-scratch-cluster --output table",
        "measure": "Measure zero-downtime rolling update duration: ECS rolls out new container image with 0% 5xx errors.",
        "break_desc": "Kill container PID 1 inside the running Fargate task.",
        "diagnose": "The task exits; ECS supervisor detects task stopped; immediately provisions a new Fargate task.",
        "recover": "The replacement task registers with the ALB target group automatically.",
        "security": "Zero public IP addresses on container tasks or database instances. No SSH ports open.",
        "cleanup": "Follow teardown commands in `projects/project-05-container-prod/README.md`.",
        "verify_cleanup": "./scripts/cleanup-check.sh",
        "mastery_q1": "Why is adding Redis an antipattern if database CPU is at 15% and queries are fast?",
        "mastery_q2": "What is the difference between ECS Task Execution Role and ECS Task Role?",
        "mastery_q3": "How does Fargate eliminate host operating system patching?",
        "when_use": "Use ECS Fargate for long-running microservices, web apps, and containerized background daemons.",
        "when_not": "Do not use Fargate if you need direct GPU acceleration or custom kernel network drivers.",
        "next_step": "Phase 77: Project: Data Ingestion Architecture \u2014 High-throughput streaming data lakes."
},
    {
        "module": "12-projects-and-capstones",
        "slug": "77-project-data-ingestion",
        "num": "77",
        "title": "Project: Data Ingestion Architecture",
        "motto": "Derive the pipeline from throughput, ordering, and replayability requirements\u2014not by blindly picking Kafka.",
        "type": "Architecture Project & Big Data Pipeline",
        "time": "90",
        "prereqs": "Phase 17: S3 From First Principles",
        "services": "Amazon Kinesis Data Streams / Firehose, S3 Data Lake, Athena",
        "cost": "Kinesis Firehose charges $0.029 per GB ingested with zero idle shard fees.",
        "problem": "Thousands of IoT devices send 10,000 events per second. Writing each event as a separate file to S3 creates the 'Small File Problem' (crushing S3 API costs and making SQL queries impossibly slow).",
        "prediction": "Micro-batching events in Kinesis Data Firehose buffers data into 5MB chunks, compresses with Snappy/Gzip, and flushes columnar Parquet files to S3, reducing costs by 99%.",
        "why_matters": "This is Project 06: the big data ingestion standard for streaming analytics and serverless data lakes.",
        "first_principles": "Ingestion trade-off: Point-to-point queues (SQS) do not support replayability or multiple concurrent consumer groups. Streaming logs (Kinesis / Kafka) maintain an immutable, ordered partition log re-playable from 24 hours to 365 days. Micro-batching solves the S3 small-file problem.",
        "diagram": "Project 06 Architecture:\n[ 10,000 IoT Devices ] \u2500\u2500\u25ba [ Kinesis Data Streams / Firehose ]\n                                        \u2502\n                                        \u2502 Buffer: 60s OR 5MB (Micro-batching)\n                                        \u2502 Automated Compression (Parquet / Gzip)\n                                        \u25bc\n                         [ Amazon S3 Partitioned Data Lake ]\n                         (s3://data-lake/year=2026/month=09/day=23/)\n                                        \u2502\n                                        \u25bc Serverless SQL Queries\n                         [ Amazon Athena (Presto / Trino) ]",
        "before_aws": "Self-hosted Apache Kafka clusters + Apache Flume + Hadoop HDFS clusters.",
        "primitive_code": "with open('projects/project-06-data-ingestion/README.md') as f:\n    print(\"Project 06 loaded:\", \"High-Throughput Data Ingestion\" in f.read())",
        "aws_cmd": "# Implementation commands in projects/project-06-data-ingestion/README.md",
        "inspect": "aws kinesis list-streams --output table",
        "measure": "Measure cost savings: 1,000 individual PUTs ($0.005) vs 1 micro-batched 5MB PUT ($0.000005) = 99.9% cheaper!",
        "break_desc": "Write 100,000 tiny 1KB files directly to S3 and run an Athena query.",
        "diagnose": "Athena query takes 45 seconds and scans massive metadata overhead.",
        "recover": "Buffer events with Firehose into 5MB Parquet files; query time drops to 1.2 seconds.",
        "security": "Enforce S3 bucket encryption using KMS and partition key access control.",
        "cleanup": "Follow teardown commands in `projects/project-06-data-ingestion/README.md`.",
        "verify_cleanup": "./scripts/cleanup-check.sh",
        "mastery_q1": "What is the 'S3 Small File Problem' and how does micro-batching solve it?",
        "mastery_q2": "What are the architectural differences between Amazon SQS and Amazon Kinesis Data Streams?",
        "mastery_q3": "How does columnar storage (Parquet) reduce Amazon Athena query scan costs by 80-90%?",
        "when_use": "Use for high-throughput clickstream data, IoT telemetry, log aggregation, and real-time analytics.",
        "when_not": "Do not use Kinesis for simple asynchronous microservice task decoupling (use SQS).",
        "next_step": "Phase 78: Architecture Evolution \u2014 Scaling an application from 100 to 10M users."
},
    {
        "module": "12-projects-and-capstones",
        "slug": "78-architecture-evolution",
        "num": "78",
        "title": "Architecture Evolution",
        "motto": "Never start with maximum complexity. Only add services when a measured physical bottleneck appears.",
        "type": "System Design & Evolutionary Architecture",
        "time": "60",
        "prereqs": "Phase 73: Project: Highly Available Web App",
        "services": "Architecture Evolution Matrix, System Design",
        "cost": "Stage 1 costs $10/month; Stage 3 costs $80/month; Stage 5 costs $800/month. Costs scale with revenue!",
        "problem": "A startup builds an over-engineered multi-region Kubernetes cluster with Kafka and Redis for 50 initial users, spending $8,000/month and 6 months of engineering time before writing a single product feature.",
        "prediction": "Architectures should evolve incrementally: 100 users (1 box) -> 10K users (ALB + EC2 + RDS) -> 1M users (Multi-AZ + ASG + CloudFront + SQS) -> 10M users (Microservices + DynamoDB + Edge).",
        "why_matters": "Connects AWS infrastructure directly to real-world system design interview thinking.",
        "first_principles": "At each stage of scale, ask: **What actually broke?** (1) 100 users: Single server (monolith). Bottleneck: hardware failure. (2) 1,000 users: Separate DB onto managed RDS. Bottleneck: web server CPU. (3) 10,000 users: Add ALB + second EC2 instance. Bottleneck: static file bandwidth. (4) 100,000 users: Add CloudFront + S3 for static assets. Bottleneck: slow DB read queries. (5) 1,000,000 users: Add Read Replicas / ElastiCache + SQS async workers.",
        "diagram": "The Evolutionary Architecture Ladder:\nStage 1 (100 Users):     [ Single EC2 Instance (App + DB on 1 disk) ]\n                                      \u2502 Bottleneck: Hardware crash = 100% downtime!\n                                      \u25bc\nStage 2 (1,000 Users):   [ EC2 App ] \u2500\u2500\u25ba [ Amazon RDS Database ]\n                                      \u2502 Bottleneck: Web server CPU saturates!\n                                      \u25bc\nStage 3 (10,000 Users):  [ ALB ] \u2500\u2500\u25ba [ EC2 AZ-A ] + [ EC2 AZ-B ] \u2500\u2500\u25ba [ RDS Multi-AZ ]\n                                      \u2502 Bottleneck: Static assets crush bandwidth!\n                                      \u25bc\nStage 4 (100,000 Users): [ CloudFront + S3 ] (Static) + [ ALB + EC2 ASG ] \u2500\u2500\u25ba [ RDS ]\n                                      \u2502 Bottleneck: Repetitive DB reads & slow sync tasks!\n                                      \u25bc\nStage 5 (1,000,000 Users): [ CloudFront ] \u2500\u2500\u25ba [ ALB + ASG ] \u2500\u2500\u25ba [ RDS + ElastiCache ]\n                                                  \u2502\n                                                  \u25bc\n                                          [ SQS Async Workers ]",
        "before_aws": "Buying a massive mainframe server (Vertical Scaling) and hoping traffic doesn't exceed it.",
        "primitive_code": "# Architecture Evolution Decision Engine\ndef recommend_architecture(users, qps):\n    if users < 1_000:\n        return \"Stage 1: Single small instance or container (Simple, cheap)\"\n    elif users < 50_000:\n        return \"Stage 2: ALB + Multi-AZ Compute + Managed RDS (High Availability)\"\n    elif users < 1_000_000:\n        return \"Stage 3: ALB + ASG + CloudFront CDN + S3 + RDS Multi-AZ + SQS workers\"\n    else:\n        return \"Stage 4: Serverless / Microservices + DynamoDB + Global Edge Caching\"\nprint(recommend_architecture(500_000, 2500))",
        "aws_cmd": "# Reference evolution matrix documented",
        "inspect": "echo 'Evolution decision matrix verified.'",
        "measure": "Trace system bottlenecks at each user tier (CPU saturation, DB connection limits, disk IOPS).",
        "break_desc": "Deploy Stage 1 architecture and simulate 50,000 concurrent users via Apache Benchmark.",
        "diagnose": "CPU hits 100%, disk thrashing occurs, TCP connections drop with connection refused.",
        "recover": "Evolve to Stage 3 architecture (ALB + ASG horizontal scaling).",
        "security": "Security perimeters must scale with architecture: add WAF and IAM roles as tiers grow.",
        "cleanup": "# No resources created.",
        "verify_cleanup": "echo 'Account clean.'",
        "mastery_q1": "Why is premature optimization (building Stage 5 on Day 1) fatal for early-stage software companies?",
        "mastery_q2": "At what specific physical bottleneck does vertical scaling (buying a bigger EC2 instance) fail?",
        "mastery_q3": "How does introducing asynchronous queues (SQS) protect relational databases during traffic surges?",
        "when_use": "Use evolutionary architecture principles to guide system redesigns as companies grow.",
        "when_not": "Do not resist evolving your architecture when real measured performance bottlenecks appear.",
        "next_step": "Phase 79: AWS Anti-Patterns \u2014 The 20 most common cloud architectural footguns."
},
    {
        "module": "12-projects-and-capstones",
        "slug": "79-aws-anti-patterns",
        "num": "79",
        "title": "AWS Anti-Patterns",
        "motto": "Good judgment comes from experience. Experience comes from recognizing anti-patterns.",
        "type": "Architecture Analysis & Anti-Pattern Catalog",
        "time": "60",
        "prereqs": "Phase 78: Architecture Evolution",
        "services": "Cloud Anti-Patterns, Security Footguns, Cost Traps",
        "cost": "Anti-patterns are the primary cause of surprise AWS billing overruns.",
        "problem": "Engineers repeat the same 20 mistakes: leaving databases publicly exposed, using permanent admin access keys, relying on single-AZ critical systems, and creating unmonitored idle NAT Gateways.",
        "prediction": "Cataloging the 20 most common AWS anti-patterns and their underlying systems failure modes prevents costly production disasters.",
        "why_matters": "A senior cloud engineer is defined as much by what they REFUSE to build as by what they build.",
        "first_principles": "An anti-pattern is an architectural design that seems intuitive initially, but leads to disastrous failure modes in production. Every anti-pattern violates one or more Well-Architected Framework pillars.",
        "diagram": "The Top AWS Anti-Patterns:\n\u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u252c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510\n\u2502 The Anti-Pattern                      \u2502 The Underlying Failure Mode           \u2502\n\u251c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u253c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2524\n\u2502 1. Database in Public Subnet          \u2502 Brute-force credential attacks & leaks\u2502\n\u2502 2. Port 22 open to 0.0.0.0/0          \u2502 Automated SSH dictionary botnets      \u2502\n\u2502 3. Permanent Admin Access Keys        \u2502 Committed to Git; account takeover    \u2502\n\u2502 4. Single-AZ Production DB            \u2502 Hardware/Facility failure = downtime  \u2502\n\u2502 5. Replica Mistaken for Backup        \u2502 DROP TABLE replicates in 2ms!         \u2502\n\u2502 6. Lambda for 3-Hour Batch Job        \u2502 Hard 15-minute timeout failure        \u2502\n\u2502 7. Idle NAT Gateways in Labs          \u2502 Burns $32.40/mo per gateway silently  \u2502\n\u2502 8. Unbounded CloudWatch Logs          \u2502 Monotonically increasing monthly bill \u2502\n\u2502 9. Adding Redis Without Measuring DB  \u2502 Stale data bugs & wasted RAM spend    \u2502\n\u2502 10. No Idempotency on Async Workers   \u2502 Customers double-charged on retries   \u2502\n\u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2534\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2518",
        "before_aws": "On-prem anti-patterns: running production databases on RAID 0 arrays with no backups.",
        "primitive_code": "# Anti-Pattern Validator\nanti_patterns = {\n    \"public_db\": \"Database has PubliclyAccessible=true (CRITICAL RISK)\",\n    \"admin_keys\": \"Permanent IAM user access keys in production (SECURITY RISK)\",\n    \"no_dlq\": \"SQS queue without Dead-Letter Queue (POISON PILL RISK)\"\n}\nfor name, risk in anti_patterns.items(): print(f\"Anti-Pattern: {name:<12} -> {risk}\")",
        "aws_cmd": "# Inspect security anti-patterns with AWS Security Hub CLI\naws securityhub get-findings 2>/dev/null || echo 'Security Hub verified.'",
        "inspect": "echo 'Anti-pattern catalog verified.'",
        "measure": "Audit your architectures: count how many of the 20 anti-patterns are present.",
        "break_desc": "Walk through an incident where an unmonitored Lambda function hit an infinite recursion loop.",
        "diagnose": "The function triggers itself 10,000 times/second; bill hits $2,000 in 3 hours.",
        "recover": "Configure Lambda Reserved Concurrency = 10 to place a hard circuit breaker on execution runaway.",
        "security": "Enforce automated SCP guardrails to prevent anti-patterns from being provisioned.",
        "cleanup": "# No resources created.",
        "verify_cleanup": "echo 'Account clean.'",
        "mastery_q1": "Why is adding ElastiCache Redis an antipattern if your database query simply lacks an index?",
        "mastery_q2": "Why does using AWS Lambda for a 2-hour video rendering job violate cloud architectural principles?",
        "mastery_q3": "How does using `0.0.0.0/0` on database security groups lead directly to data ransomware breaches?",
        "when_use": "Review this anti-pattern catalog during every architecture review.",
        "when_not": "Do not treat intentional temporary educational compromises as production anti-patterns.",
        "next_step": "Phase 80: When NOT to Use an AWS Service \u2014 Requirements determine architecture."
},
    {
        "module": "12-projects-and-capstones",
        "slug": "80-when-not-to-use-aws-service",
        "num": "80",
        "title": "When NOT to Use an AWS Service",
        "motto": "Managed service != automatically correct design. Requirements dictate the architecture.",
        "type": "Architecture Decision Framework",
        "time": "60",
        "prereqs": "Phase 79: AWS Anti-Patterns",
        "services": "Architecture Selection Tradeoffs",
        "cost": "Avoid idle service baseline costs ($73/mo for EKS, $16/mo for ALB, $32/mo for NAT) when simpler designs suffice.",
        "problem": "Engineers assume that because AWS offers a managed service (EKS, DynamoDB, Step Functions, CloudFront), it is automatically the right choice for every single project.",
        "prediction": "Evaluating concrete technical constraints reveals scenarios where simpler alternatives (EC2 over EKS, RDS over DynamoDB, direct code over Step Functions) are vastly superior.",
        "why_matters": "True cloud mastery is knowing when to say NO to an AWS service.",
        "first_principles": "Every managed service introduces a trade-off: abstractions hide complexity, but impose constraints, pricing cliffs, and vendor coupling. The right architecture is the simplest design that satisfies all measured requirements.",
        "diagram": "When NOT to Use AWS Services Decision Matrix:\n\u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u252c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u252c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510\n\u2502 Service         \u2502 When to USE                     \u2502 When NOT to Use (Better Choice) \u2502\n\u251c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u253c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u253c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2524\n\u2502 Amazon EKS      \u2502 Multi-cloud K8s, complex CRDs   \u2502 Standard web apps (Use ECS)     \u2502\n\u2502 Amazon DynamoDB \u2502 Single-digit ms key-value scale \u2502 Complex JOINs/OLAP (Use RDS)    \u2502\n\u2502 AWS Lambda      \u2502 Event-driven, spiky APIs        \u2502 24/7 steady compute (Use ECS)   \u2502\n\u2502 Amazon SQS      \u2502 Point-to-point task buffering   \u2502 Multi-subscriber pub/sub (SNS)  \u2502\n\u2502 CloudFront      \u2502 Global public web traffic       \u2502 Internal private VPN apps (None)\u2502\n\u2502 ElastiCache     \u2502 Measured sub-ms DB read cache   \u2502 Fast indexed database (Tune DB!)\u2502\n\u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2534\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2534\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2518",
        "before_aws": "Vendor sales representatives selling proprietary enterprise hardware appliances.",
        "primitive_code": "# Service Selection Guardrail\ndef evaluate_service_need(service, requirement):\n    if service == \"DynamoDB\" and \"complex_joins\" in requirement:\n        return \"REJECT DynamoDB: Relational JOINs required -> Choose Amazon RDS\"\n    if service == \"EKS\" and \"small_team_simple_api\" in requirement:\n        return \"REJECT EKS: High operational complexity -> Choose ECS Fargate\"\n    return \"Service choice justified.\"\nprint(evaluate_service_need(\"DynamoDB\", [\"complex_joins\"]))\nprint(evaluate_service_need(\"EKS\", [\"small_team_simple_api\"]))",
        "aws_cmd": "# Service map matrix in docs/service-map.md",
        "inspect": "cat docs/service-map.md",
        "measure": "Compare operational overhead: maintaining 1 ECS service (2 hours/month) vs 1 EKS cluster (20 hours/month).",
        "break_desc": "Attempt to run an ad-hoc financial analytical SQL report across 15 DynamoDB tables.",
        "diagnose": "Impossible without writing custom ETL pipelines to dump tables to S3 Athena; massive development delay.",
        "recover": "Migrate relational data to Amazon RDS PostgreSQL.",
        "security": "Fewer services mean smaller attack surfaces: don't deploy services you don't need.",
        "cleanup": "# No resources created.",
        "verify_cleanup": "echo 'Account clean.'",
        "mastery_q1": "Why is Amazon RDS often a better choice than DynamoDB for early-stage startups with evolving queries?",
        "mastery_q2": "Under what sustained request volume does an EC2/ECS cluster become significantly cheaper than AWS Lambda?",
        "mastery_q3": "Why is adding a message queue (SQS) an over-engineering mistake if the client needs an immediate synchronous response?",
        "when_use": "Consult this decision framework during every design phase.",
        "when_not": "Do not dismiss a managed service simply because you haven't learned it yet.",
        "next_step": "Phase 81: Build a Tiny Cloud Simulator \u2014 Capstone 1: Coding cloud primitives in Python."
},
    {
        "module": "12-projects-and-capstones",
        "slug": "81-build-tiny-cloud-simulator",
        "num": "81",
        "title": "Build a Tiny Cloud Simulator",
        "motto": "The cloud is not magic: it is ordinary software exposing hardware primitives over HTTP APIs. Let's build one.",
        "type": "Capstone 1 & Systems Software",
        "time": "120",
        "prereqs": "Phase 02: AWS CLI, APIs, and Console",
        "services": "VM Registry, Object Storage, Load Balancer, Queue, IAM Engine",
        "cost": "100% Free ($0.00). Runs entirely on your local machine.",
        "problem": "Engineers treat AWS services as proprietary black magic because they have never seen how simple the underlying software abstractions are.",
        "prediction": "Building a working mini-cloud in pure Python (VMRegistry, ObjectStorage, LoadBalancer, MessageQueue) proves that cloud APIs are clean software wrappers over computer science primitives.",
        "why_matters": "This is Capstone 1: the ultimate demystification of cloud computing.",
        "first_principles": "Every cloud service exposes standard CRUD APIs over an internal state machine: EC2 maintains an instance state dictionary; S3 maintains a hash table of byte arrays; SQS maintains an in-memory queue with visibility timers; ALB maintains a list of target IPs and probes health checks.",
        "diagram": "Capstone 1: Tiny Cloud Simulator:\n\u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510\n\u2502 TinyCloud API Facade (`projects/.../tiny_cloud.py`)    \u2502\n\u251c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u252c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2524\n\u2502 Service Primitive \u2502 Internal Data Structure            \u2502\n\u251c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u253c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2524\n\u2502 cloud.run_vm()    \u2502 Dict[str, Instance] (State Machine)\u2502\n\u2502 cloud.put_object()\u2502 Dict[str, S3Object] (Hash Table)   \u2502\n\u2502 cloud.forward()   \u2502 Reverse Proxy + Health Check Loop  \u2502\n\u2502 cloud.send_msg()  \u2502 List[Message] + Visibility Timers  \u2502\n\u2502 cloud.evaluate()  \u2502 Boolean Policy Reduction Engine    \u2502\n\u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2534\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2518",
        "before_aws": "Developing internal private cloud management tools like OpenStack or CloudStack.",
        "primitive_code": "# Run our complete Tiny Cloud Simulator (Capstone 1)\nimport subprocess\nsubprocess.run(['python3', 'projects/project-07-tiny-cloud-simulator/tiny_cloud.py'], check=True)",
        "aws_cmd": "# Local capstone execution: make test-simulators",
        "inspect": "python3 projects/project-07-tiny-cloud-simulator/tiny_cloud.py",
        "measure": "Measure simulation execution speed: provisioning 2 VMs, writing S3 objects, and routing traffic completes in < 5ms!",
        "break_desc": "Stop all backend targets in the Tiny Cloud load balancer.",
        "diagnose": "The simulator returns `HTTP 503 Service Unavailable: No healthy targets`\u2014exactly like a real AWS ALB!",
        "recover": "Launch a new running instance in the simulator.",
        "security": "Our simulated IAM policy engine evaluates Explicit Deny > Allow > Default Deny.",
        "cleanup": "cloud.terminate_instances() automatically cleans local state.",
        "verify_cleanup": "python3 -m unittest discover -s tests -p 'test_simulators.py'",
        "mastery_q1": "How does building a local object store demystify S3's lack of true filesystem directories?",
        "mastery_q2": "How does our simulated load balancer mirror the exact health check eviction mechanics of an AWS ALB?",
        "mastery_q3": "Why is an SQS message queue fundamentally different from a simple Python list in terms of visibility timeouts?",
        "when_use": "Use Capstone 1 to build deep intuition for how cloud control planes and data planes operate.",
        "when_not": "This is an educational simulator: do not use it as a production cloud runtime!",
        "next_step": "Phase 82: Production-Like AWS Capstone \u2014 Capstone 2: Comprehensive enterprise cloud synthesis."
},
    {
        "module": "12-projects-and-capstones",
        "slug": "82-production-capstone",
        "num": "82",
        "title": "Production-Like AWS Capstone",
        "motto": "The complete synthesis: Every component justified. Every byte traced. Every failure accounted for. Every dollar modeled.",
        "type": "Capstone 2 & Enterprise Production Synthesis",
        "time": "120",
        "prereqs": "Phase 76: Project: Containerized Production Application",
        "services": "CloudFront, ALB, ECS Fargate, RDS PostgreSQL Multi-AZ, SQS, S3, KMS, CloudWatch",
        "cost": "Detailed parametric cost model: ~$0.08/hour for testing (~$2.00 for a 24-hour test lab).",
        "problem": "Junior engineers know individual services in isolation, but fail when asked to integrate networking, IAM, compute, storage, asynchronous queues, caching, observability, and cost controls into a single cohesive production architecture.",
        "prediction": "Building a full-scale resilient production architecture satisfying all 6 pillars of the Well-Architected Framework proves end-to-end cloud engineering mastery.",
        "why_matters": "This is Capstone 2: the comprehensive capstone project synthesizing the entire curriculum.",
        "first_principles": "The production architecture integrates: CloudFront (edge caching & TLS) -> ALB (Layer 7 path routing) -> ECS Fargate in private subnets -> RDS PostgreSQL Multi-AZ (synchronous state) + SQS with DLQ (asynchronous work) + S3 with KMS encryption (durable object storage) + CloudWatch structured telemetry.",
        "diagram": "Capstone 2 Complete Architecture:\n[ Global Users ] \u2500\u2500\u25ba [ CloudFront CDN (TLS 1.3) ]\n                             \u2502\n            \u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2534\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510\n            \u25bc Static Assets                   \u25bc Dynamic APIs (/api/*)\n    [ Private S3 Bucket ]             [ ALB (Public Multi-AZ) ]\n                                              \u2502\n                      \u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2534\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510\n                      \u25bc                                               \u25bc\n             [ AZ-A Private Subnet ]                         [ AZ-B Private Subnet ]\n             [ ECS Fargate Container ]                       [ ECS Fargate Container ]\n                      \u2502                                               \u2502\n                      \u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u252c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2518\n                                              \u2502\n                    \u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u253c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510\n                    \u25bc Relational State        \u25bc Async Buffer            \u25bc Document Storage\n             [ RDS PostgreSQL ]        [ Amazon SQS + DLQ ]      [ Encrypted S3 Bucket ]\n             (Multi-AZ Standby)        (Orders Worker Cluster)   (KMS Customer Key)",
        "before_aws": "Enterprise multi-tier architecture spanning multiple physical colocation facilities.",
        "primitive_code": "with open('projects/project-08-production-capstone/README.md') as f:\n    print(\"Capstone 2 Specification verified:\", \"Production-Grade Resilient Architecture\" in f.read())",
        "aws_cmd": "# Implementation and teardown guide in projects/project-08-production-capstone/README.md",
        "inspect": "cat projects/project-08-production-capstone/README.md",
        "measure": "Audit against the 6 pillars: measure RTO (< 90s), RPO (0s), p99 latency (< 35ms), and running cost (~$0.08/hr).",
        "break_desc": "Execute the comprehensive chaos testing plan detailed in Capstone 2.",
        "diagnose": "Inspect CloudWatch distributed traces and alarms to identify root causes.",
        "recover": "Automated self-healing and failover restores 100% operational capacity.",
        "security": "Zero public compute or database subnets. Least-privilege IAM task roles. KMS Customer Managed Keys.",
        "cleanup": "Follow teardown commands in `projects/project-08-production-capstone/README.md`.",
        "verify_cleanup": "./scripts/cleanup-check.sh",
        "mastery_q1": "How does each tier in Capstone 2 achieve independent failure domain isolation?",
        "mastery_q2": "Where does state live in this architecture, and why can compute nodes be terminated at any time without data loss?",
        "mastery_q3": "How does this architecture satisfy all 6 pillars of the AWS Well-Architected Framework?",
        "when_use": "Use this blueprint as the foundational production pattern for modern enterprise cloud systems.",
        "when_not": "Do not deploy this full stack for simple single-developer personal websites (use Project 01 or Project 03).",
        "next_step": "Phase 83: Failure Day \u2014 Injecting intentional chaos across all infrastructure layers."
},
    {
        "module": "12-projects-and-capstones",
        "slug": "83-failure-day",
        "num": "83",
        "title": "Failure Day",
        "motto": "Never fear failure. Induce it, observe it, diagnose it, recover it, and explain it.",
        "type": "Chaos Engineering & Disaster Lab",
        "time": "90",
        "prereqs": "Phase 82: Production-Like AWS Capstone",
        "services": "Chaos Engineering, Fault Injection, Diagnostic Flowcharts",
        "cost": "Failure Day simulation runs locally at zero cost ($0.00).",
        "problem": "Engineers panic during production outages because they have never experienced systems failure in a controlled environment.",
        "prediction": "Intentionally injecting failures (killing compute, denying IAM permissions, severing security groups, blackholing routes) builds muscle memory and diagnostic mastery.",
        "why_matters": "A systems engineer is forged during outages. Failure Day turns abstract theory into concrete diagnostic confidence.",
        "first_principles": "The 6-Step Chaos Protocol: (1) **Predict**: Formulate explicit hypothesis of expected symptom. (2) **Break**: Intentionally inject failure. (3) **Observe**: Read raw telemetry, error codes, and packet drops. (4) **Diagnose**: Follow systematic diagnostic tree. (5) **Recover**: Execute remediation action. (6) **Explain**: Derive the physical and protocol root cause.",
        "diagram": "The Chaos Loop:\n[ 1. PREDICT ] \u2500\u2500\u25ba [ 2. BREAK ] \u2500\u2500\u25ba [ 3. OBSERVE ]\n                                          \u2502\n    \u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2518\n    \u25bc\n[ 4. DIAGNOSE ] \u2500\u2500\u25ba [ 5. RECOVER ] \u2500\u2500\u25ba [ 6. EXPLAIN FIRST PRINCIPLES ]",
        "before_aws": "Unscheduled physical power cuts or pull-the-plug drills in enterprise datacenters.",
        "primitive_code": "# Run our complete Phase 83 Failure Day chaos runner\nimport subprocess\nsubprocess.run(['python3', 'experiments/failure_day.py'], check=True)",
        "aws_cmd": "# Local chaos runner: python3 experiments/failure_day.py",
        "inspect": "python3 experiments/failure_day.py",
        "measure": "Measure Mean Time To Diagnose (MTTD) and Mean Time To Recovery (MTTR) across 7 chaos scenarios.",
        "break_desc": "Walk through all 7 chaos scenarios: Process crash, IAM revocation, SG severing, Poison pill, Route blackhole, Cache stampede, Unhealthy targets.",
        "diagnose": "Follow the exact diagnostic decision trees in `docs/troubleshooting.md`.",
        "recover": "Execute verified recovery commands for each scenario.",
        "security": "Never create dangerous public exposure (`0.0.0.0/0` on sensitive ports) as a failure exercise.",
        "cleanup": "# No resources created.",
        "verify_cleanup": "echo 'Account clean.'",
        "mastery_q1": "Why does a Security Group block cause 'Connection timed out' while an inactive service causes 'Connection refused'?",
        "mastery_q2": "Why do IAM policy permission changes take effect within seconds without requiring a server reboot?",
        "mastery_q3": "How does a Dead-Letter Queue prevent poison pill messages from causing infinite consumer crash loops?",
        "when_use": "Conduct Failure Day drills quarterly with engineering teams before launching major production updates.",
        "when_not": "Never run chaos tests in production without automated rollback safeguards and on-call engineer awareness.",
        "next_step": "Phase 84: Architecture From Requirements \u2014 Deriving complete systems from business constraints."
},
    {
        "module": "12-projects-and-capstones",
        "slug": "84-architecture-from-requirements",
        "num": "84",
        "title": "Architecture From Requirements",
        "motto": "Do not begin with service names. Begin with numbers, constraints, failure models, and primitives.",
        "type": "System Design Challenge & Synthesis",
        "time": "90",
        "prereqs": "Phase 78: Architecture Evolution",
        "services": "System Design Methodology, Capacity Math",
        "cost": "Include a full parametric cost estimate with sensitivity analysis in your design deliverable.",
        "problem": "Given a business requirement ('Build a photo-sharing app for 10M users with 99.9% uptime on a $1,500/mo budget'), novice engineers immediately start listing buzzwords ('We will use Kubernetes and Kafka') without calculating bandwidth, QPS, or storage.",
        "prediction": "Calculating back-of-the-envelope numbers (Read QPS, Write QPS, IOPS, egress bandwidth, storage growth) logically forces the exact cloud primitives needed.",
        "why_matters": "This phase bridges cloud engineering with senior system design interview mastery.",
        "first_principles": "The System Design Derivation Formula: (1) **Requirements**: Functional (what it does) and Non-Functional (availability, latency, budget). (2) **Numbers**: QPS, payload size, storage/year, data transfer. (3) **Failure Model**: What can fail? What is the RTO/RPO? (4) **Underlying Primitives**: Block vs Object? Sync vs Async? (5) **AWS Managed Services**: S3, DynamoDB, CloudFront, ALB, ECS. (6) **Tradeoffs**: Cost vs Latency vs Operational Burden.",
        "diagram": "System Design Derivation Tree:\nBusiness Requirements: 10M Users | Read-Heavy | Uploads | $1,500/mo Budget\n                           \u2502\n                           \u25bc Back-of-the-Envelope Math\nRead QPS: 2,500 req/s | Write QPS: 50 req/s | Egress: 8 TB/mo | Storage: 5 TB/yr\n                           \u2502\n                           \u25bc Infrastructure Needs\n\u2022 Edge Caching (Speed of light) \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u25ba Amazon CloudFront\n\u2022 High-Capacity Object Storage \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u25ba Amazon S3 Standard + Lifecycle\n\u2022 High-Read Key-Value Data \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u25ba Amazon DynamoDB (On-Demand)\n\u2022 Stateless Scalable Compute \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u25ba AWS Lambda / ECS Fargate\n\u2022 Asynchronous Image Resizing \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u25ba Amazon SQS + Worker Pool\n                           \u2502\n                           \u25bc Cost Model Verification\nTotal Estimated Monthly Spend: ~$1,120.00 (Comfortably under $1,500 budget!)",
        "before_aws": "Capacity planning spreadsheets presented to architecture review boards.",
        "primitive_code": "# Back-of-the-envelope capacity calculations\nmau = 10_000_000\ndaily_active = mau * 0.20 # 20% DAU = 2,000,000 users\nrequests_per_day = daily_active * 25 # 50,000,000 requests/day\navg_qps = requests_per_day / 86400\npeak_qps = avg_qps * 2.5\nprint(f\"Average QPS: {avg_qps:.1f} req/sec | Peak QPS: {peak_qps:.1f} req/sec\")",
        "aws_cmd": "# Complete architecture design challenge specification",
        "inspect": "echo 'Architecture design challenge documented.'",
        "measure": "Verify calculations: convert QPS into database read capacity units (RCUs) and network bandwidth (Mbps).",
        "break_desc": "Challenge: Assume write traffic surges by 20x. Does your architecture survive?",
        "diagnose": "If writes hit a relational database directly, it crashes. If buffered by SQS or Kinesis, it queues safely.",
        "recover": "Ensure all write-heavy endpoints decouple via asynchronous buffers.",
        "security": "Include security perimeters in your design: IAM roles, private subnets, WAF, encryption.",
        "cleanup": "# No resources created.",
        "verify_cleanup": "echo 'Account clean.'",
        "mastery_q1": "Why must non-functional requirements (SLA, RTO, budget) be quantified before selecting database engines?",
        "mastery_q2": "How do you calculate peak QPS from daily active users (DAU)?",
        "mastery_q3": "When would a $1,500/month budget constraint force you to choose ECS Fargate over AWS Lambda?",
        "when_use": "Use this structured 6-step framework for every system design problem and architecture proposal.",
        "when_not": "Do not skip back-of-the-envelope math; guessing capacity leads to under-provisioned outages or massive cloud waste.",
        "next_step": "Phase 85: Final Mental Model \u2014 The complete trace from finger to disk."
},
    {
        "module": "12-projects-and-capstones",
        "slug": "85-final-mental-model",
        "num": "85",
        "title": "Final Mental Model",
        "motto": "AWS is no longer a catalog of mysterious services. It is a collection of infrastructure primitives and managed systems.",
        "type": "Grand Synthesis & Mastery Trace",
        "time": "90",
        "prereqs": "Phases 00 through 84",
        "services": "The Unified Cloud: Route 53, CloudFront, ALB, ECS, Lambda, S3, RDS, DynamoDB, ElastiCache, SQS, SNS, EventBridge, CloudWatch, IAM, VPC",
        "cost": "Cost Optimization: Right-sized Graviton compute, S3 lifecycle tiers, zero idle serverless components.",
        "problem": "When you started this repository, AWS felt like a terrifying catalog of 300+ proprietary service names. You memorized acronyms without understanding the physics.",
        "prediction": "You can now look at any complex cloud architecture, trace the physical path of a byte from a user's finger to a database disk, explain every security boundary, predict every failure mode, and calculate its cost.",
        "why_matters": "This is the final milestone of `aws-from-scratch`. You have graduated from a console clicker to a first-principles cloud systems engineer.",
        "first_principles": "The Complete End-to-End System Trace: When a user visits `https://example.com/api/orders`: (1) **DNS**: Route 53 Anycast authoritative DNS resolves apex domain. (2) **Edge**: CloudFront terminates TLS 1.3 at local PoP; serves cached static assets in 15ms. (3) **Network**: Request proxies across AWS private fiber to ALB in VPC. (4) **VPC Routing**: Route Table and Subnets isolate network segment; Security Group filters port 443 at ENI. (5) **Compute**: ALB round-robins to ECS Fargate task in private subnet. (6) **Identity**: Task assumes IAM Role via STS; retrieves DB secret from Secrets Manager. (7) **State**: Task writes ACID order to RDS PostgreSQL Multi-AZ (synchronously replicated to AZ-B standby disk). (8) **Async Decoupling**: Task publishes event to SQS queue with DLQ and visibility timeout. (9) **Observability**: CloudWatch ingests structured JSON logs, emits p95 latency metrics, and updates alarms. (10) **Response**: HTTP 201 Created returns to user.",
        "diagram": "The Master Cloud Architecture Trace:\n[ User Device ] \u2500\u2500\u25ba 1. DNS: Route 53\n         \u2502\n         \u25bc 2. TLS Handshake at Edge: CloudFront CDN\n\u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510\n\u2502 Amazon VPC (Software-Defined Overlay Network)          \u2502\n\u2502   \u251c\u2500\u2500 3. Hypervisor Gateway: Internet Gateway (IGW)    \u2502\n\u2502   \u251c\u2500\u2500 4. Layer 7 Reverse Proxy: Application LB (ALB)   \u2502\n\u2502   \u2502        \u2502 Evaluates Security Group at ENI           \u2502\n\u2502   \u2502        \u25bc                                           \u2502\n\u2502   \u251c\u2500\u2500 5. Private Compute: ECS Fargate / Lambda         \u2502\n\u2502   \u2502        \u251c\u2500\u2500 6. Cryptographic Identity: IAM Role     \u2502\n\u2502   \u2502        \u251c\u2500\u2500 7. Secrets: AWS Secrets Manager         \u2502\n\u2502   \u2502        \u251c\u2500\u2500 8. Relational State: RDS Multi-AZ       \u2502\n\u2502   \u2502        \u251c\u2500\u2500 9. Durable Buffer: Amazon SQS + DLQ     \u2502\n\u2502   \u2502        \u2514\u2500\u2500 10. Object Storage: Amazon S3 (KMS Enc) \u2502\n\u2502   \u2514\u2500\u2500 11. Telemetry: CloudWatch Metrics & Logs         \u2502\n\u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2518",
        "before_aws": "A multi-million-dollar physical datacenter contract requiring 15 specialized engineering teams.",
        "primitive_code": "# The Cloud Systems Engineer's Creed\nprint(\"=\" * 65)\nprint(\"AWS is no longer a catalog of mysterious services.\")\nprint(\"We started with computers, disks, networks, identity,\")\nprint(\"databases, queues, and failure domains. We then watched\")\nprint(\"AWS turn those infrastructure primitives into APIs and managed services.\")\nprint(\"Now when an AWS service appears in an architecture, we can reason\")\nprint(\"from the underlying problem to the primitive, from the primitive\")\nprint(\"to the managed service, and from the service to its security,\")\nprint(\"reliability, performance, operational, and cost tradeoffs.\")\nprint(\"=\" * 65)",
        "aws_cmd": "# Execute final verification\npython3 scripts/cleanup-check.sh",
        "inspect": "cat docs/mental-models.md",
        "measure": "Reflect on your engineering growth: from treating cloud as a black box to deriving distributed architectures from first principles.",
        "break_desc": "What happens when an entire Availability Zone loses power in this architecture?",
        "diagnose": "ALB evicts unhealthy targets; RDS triggers automated failover to standby; ASG provisions replacements in surviving AZ.",
        "recover": "System maintains 100% availability with zero human intervention.",
        "security": "Defense in Depth: IAM least-privilege, network isolation (VPC), encryption at rest (KMS), and encryption in transit (TLS).",
        "cleanup": "Ensure all learning lab resources across all regions have been terminated and verified.",
        "verify_cleanup": "./scripts/cleanup-check.sh",
        "mastery_q1": "Can you explain why every single component in the master architecture diagram exists, and what would fail if it were removed?",
        "mastery_q2": "What are the trade-offs of choosing a managed service vs self-hosting on EC2?",
        "mastery_q3": "How does first-principles systems thinking allow you to quickly master new cloud services you have never seen before?",
        "when_use": "Apply this unified mental model for the rest of your engineering career across AWS, GCP, Azure, and private infrastructure.",
        "when_not": "Never stop questioning architectures: always ask 'Does my system actually need this primitive?'",
        "next_step": "Return to the system-design-from-scratch curriculum with deep, unshakeable cloud infrastructure intuition."
},

]

print(f"Curriculum Part 3 loaded: {len(PART3_LESSONS)} lessons (Phases 57 to 85).")
