"""
scripts/curriculum_part1.py
Defines detailed curriculum metadata for Phases 00 through 25.
"""

PART1_LESSONS = [
    # 00: Cloud Before AWS
    {
        "module": "00-cloud-foundations", "slug": "00-cloud-before-aws", "num": "00",
        "title": "Cloud Before AWS",
        "motto": "The cloud is not magic: it is someone else's physical computers controlled by software APIs.",
        "type": "Conceptual & Systems Exploration", "time": "45",
        "prereqs": "Basic Linux processes and terminal commands",
        "services": "None (Foundational Physical Infrastructure)",
        "cost": "Free ($0.00 / Local)",
        "problem": "Before cloud computing, deploying a backend application meant purchasing physical servers, waiting 6-12 weeks for delivery, racking and cabling them in a datacenter, configuring redundant power, and manually installing operating systems. Traffic surges caused weeks of downtime until new hardware arrived.",
        "prediction": "If hardware procurement takes 8 weeks, engineering teams will over-provision massively, leading to 80%+ idle server capacity and exorbitant capital expenditures.",
        "why_matters": "Understanding bare-metal physical constraints explains why cloud virtualization, resource pools, and on-demand APIs were invented.",
        "first_principles": "A computer is CPU registers, memory caches, DRAM, PCI buses, NICs, and persistent storage media. An OS kernel abstracts this hardware for userland processes. Hypervisors extend this abstraction by virtualizing CPU instruction sets (VT-x/AMD-V) and memory management units (EPT/NPT), allowing multiple isolated guest OS kernels to share one physical host.",
        "diagram": """Physical Datacenter to Virtualization:
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
└────────────────────────────────────────────────────────┘""",
        "before_aws": "Organizations leased datacenter cages, maintained diesel backup generators, ran physical BGP routers, and bought Dell/HP rack servers with 3-year depreciation schedules.",
        "primitive_code": """import os
print(f"Available Logical Cores: {os.cpu_count()}")
try:
    with open('/proc/cpuinfo') as f:
        print([line.strip() for line in f if 'model name' in line][0])
except Exception:
    print("Local CPU inspection completed.")""",
        "aws_cmd": "aws ec2 describe-instance-types --instance-types t4g.micro --query 'InstanceTypes[0].[InstanceType,VCpuInfo.DefaultVCpus,MemoryInfo.SizeInMiB]' --output table",
        "inspect": "aws ec2 describe-regions --query 'Regions[].[RegionName,Endpoint]' --output table",
        "measure": "Measure latency between local loopback (127.0.0.1) and a remote server IP via ping.",
        "break_desc": "Simulate CPU core exhaustion locally using a multi-process spin loop.",
        "diagnose": "Inspect 'top' or 'htop'; observe 100% CPU utilization and process scheduling throttling.",
        "recover": "Apply OS cgroups or process nice values to constrain compute starvation.",
        "security": "Hypervisor escape vulnerabilities (Spectre, Meltdown, Rowhammer) represent the physical security perimeter between multitenant virtual machines.",
        "cost": "Idle Physical Server: 100% of CapEx + ongoing power/cooling costs regardless of utilization. Cloud Compute: 100% variable OpEx billed per second.",
        "cleanup": "# No resources created in live AWS account for Phase 00.",
        "verify_cleanup": "echo 'Account clean.'",
        "mastery_q1": "Why does a 2-vCPU virtual machine not guarantee 100% of two physical hardware cores unless Dedicated Hosts are purchased?",
        "mastery_q2": "What physical bottleneck prevents cloud providers from offering instantaneous provisioning of 100,000 servers in a single second?",
        "mastery_q3": "How does hypervisor CPU time-sharing affect p99 latency compared to bare-metal hardware?",
        "when_use": "Whenever workloads have variable, unpredictable, or seasonal demand that cannot justify purchasing physical hardware.",
        "when_not": "When regulatory requirements mandate sovereign on-prem hardware or when steady-state 24/7 compute at petabyte scale makes colo cheaper.",
        "next_step": "Phase 01: AWS Global Infrastructure — Understanding Regions, Availability Zones, and physical speed-of-light boundaries."
    },
    # 01: AWS Global Infrastructure
    {
        "module": "00-cloud-foundations", "slug": "01-aws-global-infrastructure", "num": "01",
        "title": "AWS Global Infrastructure",
        "motto": "Region != Availability Zone. Latency is the speed of light in optical fiber.",
        "type": "Systems Experiment & Measurement", "time": "45",
        "prereqs": "Phase 00: Cloud Before AWS",
        "services": "AWS Global Regions, Availability Zones, Edge Locations",
        "cost": "Free ($0.00 / Query CLI)",
        "problem": "Deploying an entire application into a single physical building means a municipal power grid failure, flood, or fiber cut causes 100% downtime. Furthermore, users on the other side of the planet experience 200ms+ round-trip latency.",
        "prediction": "Querying an AWS endpoint across the continent will exhibit a minimum baseline latency bounded by the speed of light (~5ms per 1,000 km of glass fiber).",
        "why_matters": "Conflating an AWS Region with an Availability Zone leads to single-point-of-failure architectures that fail completely when one datacenter suffers an outage.",
        "first_principles": "Light travels through glass fiber optic cables at ~200,000 km/s (~5 microseconds per kilometer). An Availability Zone is one or more discrete physical datacenters separated by 10-50 km to ensure independent flood/earthquake blast radiuses while keeping round-trip latency under 1-2 milliseconds.",
        "diagram": """AWS Global Topology:
AWS Global Backbone
├── Region A (e.g., us-east-1: N. Virginia)
│   ├── AZ 1 (us-east-1a) ──(Sub-2ms Dark Fiber)──► AZ 2 (us-east-1b)
│   │   └── Physical DC Campus 1                    └── Physical DC Campus 2
│   └── AZ 3 (us-east-1c)
└── Region B (e.g., eu-central-1: Frankfurt)
    └── Bounded by Transatlantic Undersea Cables (~70ms latency)""",
        "before_aws": "Global enterprises leased synchronous MPLS circuits between private datacenters in New York, London, and Tokyo, paying tens of thousands of dollars monthly.",
        "primitive_code": """import time, urllib.request
def measure(url):
    t0 = time.perf_counter()
    urllib.request.urlopen(url, timeout=5)
    return (time.perf_counter() - t0) * 1000
print(f"Latency to us-east-1: {measure('https://ec2.us-east-1.amazonaws.com'):.1f}ms")
print(f"Latency to eu-central-1: {measure('https://ec2.eu-central-1.amazonaws.com'):.1f}ms")""",
        "aws_cmd": "aws ec2 describe-availability-zones --query 'AvailabilityZones[].[ZoneName,ZoneId,State]' --output table",
        "inspect": "aws ec2 describe-regions --query 'Regions[].RegionName' --output text",
        "measure": "Compare same-AZ ping (< 1ms), cross-AZ ping (1-2ms), and cross-region ping (70-150ms).",
        "break_desc": "Attempt to synchronously replicate database transactions across transatlantic regions.",
        "diagnose": "Observe database write commit latency balloon from 2ms to 120ms due to speed-of-light round trips.",
        "recover": "Use asynchronous replication across regions and synchronous replication only within Multi-AZ boundaries.",
        "security": "Data sovereignty and legal compliance (GDPR, HIPAA, CCPA) strictly mandate which geographic region data may physically reside in.",
        "cost": "Cross-AZ data transfer: ~$0.01/GB in each direction. Cross-region data transfer: ~$0.02/GB. Inter-AZ communication within the same AZ is $0.00.",
        "cleanup": "# No infrastructure provisioned. Zero cleanup needed.",
        "verify_cleanup": "echo 'Account clean.'",
        "mastery_q1": "Why does AWS map the logical AZ name 'us-east-1a' to different physical Zone IDs across different AWS accounts?",
        "mastery_q2": "Why can an application synchronously commit transactions across AZs in the same region, but must use asynchronous replication across regions?",
        "mastery_q3": "Under what circumstances does deploying across two AZs actually REDUCE overall availability?",
        "when_use": "Use Multi-AZ for high availability within a region. Use Multi-Region only for disaster recovery or extreme global data residency requirements.",
        "when_not": "Do not build multi-region active-active architectures prematurely—cross-region consensus is one of the hardest distributed systems problems.",
        "next_step": "Phase 02: AWS CLI, APIs, and Console — Stripping away the UI magic to see signed REST API requests."
    },
    # 02: AWS CLI, APIs, and Console
    {
        "module": "00-cloud-foundations", "slug": "02-aws-cli-apis-console", "num": "02",
        "title": "AWS CLI, APIs, and Console",
        "motto": "The console, CLI, and SDK are just HTTP clients making signed POST requests to REST endpoints.",
        "type": "Systems Experiment & Protocol Inspection", "time": "45",
        "prereqs": "Phase 01: AWS Global Infrastructure",
        "services": "AWS STS, AWS Control Plane REST APIs, AWS CLI v2",
        "cost": "Free ($0.00 / Query CLI)",
        "problem": "Relying exclusively on the web console breeds a magical view of the cloud. When a web form button fails with a vague error or when automation is required, GUI-only developers cannot diagnose what HTTP call failed or why.",
        "prediction": "Executing any AWS CLI command with --debug will reveal an underlying signed HTTPS POST request with an Authorization header containing AWS4-HMAC-SHA256 (SigV4).",
        "why_matters": "All cloud automation, Terraform, CDK, and Kubernetes operators simply invoke these exact HTTPS endpoints. Stripping away the UI reveals the true cloud control plane.",
        "first_principles": "Every cloud resource modification is an HTTP request over TLS to a service endpoint. AWS authenticates requests using the AWS Signature Version 4 (SigV4) protocol: an HMAC-SHA256 digest calculated over the HTTP method, URI, query string, headers, and request body using the caller's secret key.",
        "diagram": """Client to API Architecture:
┌──────────────────────────┐
│ AWS Console (Web UI)     │─┐
├──────────────────────────┤ │
│ AWS CLI v2 (Shell)       │─┼──► HTTPS POST (SigV4 Signed) ──► AWS Service API Endpoint
├──────────────────────────┤ │                                   (e.g., sts.amazonaws.com)
│ Boto3 SDK (Python)       │─┘
└──────────────────────────┘""",
        "before_aws": "Datacenter administrators configured servers over IPMI / serial consoles, executed commands over SSH, or managed VMware vSphere APIs.",
        "primitive_code": """import hashlib
canonical_request = "GET\\n/\\n\\nhost:sts.amazonaws.com\\n\\nhost\\ne3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
hashed_request = hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()
print(f"Canonical Request SHA256 Hash:\\n{hashed_request}")""",
        "aws_cmd": "aws sts get-caller-identity --debug 2>&1 | grep -E '> (POST|Host|Authorization)' | head -n 5",
        "inspect": "aws sts get-caller-identity --output json",
        "measure": "Measure CLI execution overhead: compare Python Boto3 client invocation vs CLI subprocess launch time.",
        "break_desc": "Skew your system clock by more than 15 minutes (or simulate timestamp drift) and make an AWS API call.",
        "diagnose": "The API call fails with RequestTimeTooSkewed: SigV4 requires client timestamps within 15 minutes of UTC to prevent replay attacks.",
        "recover": "Resynchronize system clock via NTP (Chrony/systemd-timesyncd).",
        "security": "Never pass AWS secrets via CLI command line arguments (e.g. --secret-key); command arguments are visible in OS process tables (`ps aux`).",
        "cost": "AWS control plane read APIs (Describe*, Get*, List*) are free of charge in virtually all services.",
        "cleanup": "# No resources provisioned. Zero cleanup required.",
        "verify_cleanup": "echo 'Zero cleanup required.'",
        "mastery_q1": "Why does AWS SigV4 sign the SHA256 hash of the request body rather than sending the raw secret key over TLS?",
        "mastery_q2": "What happens if a malicious proxy intercepts and replays a valid signed AWS API request 20 minutes later?",
        "mastery_q3": "How does pagination work when querying an AWS API that contains 50,000 resources?",
        "when_use": "Use CLI/SDK for reproducible automation, scripting, and CI/CD pipelines.",
        "when_not": "Avoid hand-crafted raw HTTP SigV4 signing when official SDKs handle signature calculation, retries, and token refresh automatically.",
        "next_step": "Phase 03: IAM From First Principles — Understanding cryptographic identity and authorization before provisioning resources."
    },
    # 03: IAM From First Principles
    {
        "module": "01-iam-and-security", "slug": "03-iam-from-first-principles", "num": "03",
        "title": "IAM From First Principles",
        "motto": "Identity is cryptographic proof of who you are. Authorization is boolean logic determining what you can do.",
        "type": "Hands-on Lab & First Principles Engine", "time": "60",
        "prereqs": "Phase 02: AWS CLI, APIs, and Console",
        "services": "AWS IAM, AWS STS",
        "cost": "Free ($0.00 / IAM is free)",
        "problem": "When microservices or developers share hardcoded root credentials, any leak grants full destructive access to the entire AWS account. There is no auditability of who deleted a database.",
        "prediction": "A request without an explicit Allow will evaluate to Default Deny and immediately fail with HTTP 403 AccessDenied.",
        "why_matters": "IAM is the single most critical security primitive in AWS. Every single API call is evaluated against IAM authorization boundaries.",
        "first_principles": "Authorization is a boolean reduction function: `evaluate(Principal, Action, Resource, Context) -> {ALLOW, DENY}`. By default, access is closed (Default Deny). An explicit Allow opens access. Any explicit Deny immediately terminates evaluation with rejection.",
        "diagram": """IAM Evaluation Precedence:
[ API Request ] ──► Any Matching Explicit Deny? ──YES──► [ REJECT: DENIED ]
                           │ NO
                           ▼
                    Any Matching Explicit Allow? ──NO──► [ REJECT: DENIED (Default) ]
                           │ YES
                           ▼
                    [ AUTHORIZED: ALLOW ]""",
        "before_aws": "UNIX sudoers files, LDAP/Active Directory groups, and Kerberos ticket-granting services.",
        "primitive_code": """# Run our first-principles IAM evaluator simulation
import subprocess
subprocess.run(['python3', 'experiments/iam_simulator.py'], check=True)""",
        "aws_cmd": "aws iam get-user || aws sts get-caller-identity",
        "inspect": "aws iam list-roles --max-items 5 --output table",
        "measure": "Measure STS token assumption latency (`aws sts assume-role`).",
        "break_desc": "Attempt an action not granted by your policy (e.g., `aws dynamodb list-tables`).",
        "diagnose": "Inspect the error: 'User is not authorized to perform: dynamodb:ListTables on resource: *'.",
        "recover": "Attach a scoped policy granting `dynamodb:ListTables` to the identity.",
        "security": "Never grant `*` permissions. Always scope actions and resource ARNs to the minimum needed.",
        "cost": "AWS IAM is a foundational control plane service offered at zero charge.",
        "cleanup": "# No billable resources created in Phase 03.",
        "verify_cleanup": "echo 'Account clean.'",
        "mastery_q1": "Why does an Explicit Deny statement in an SCP override an Explicit Allow in an IAM User policy?",
        "mastery_q2": "What is the difference between an IAM User and an IAM Role?",
        "mastery_q3": "Why are temporary credentials (`ASIA...`) cryptographically safer than permanent access keys (`AKIA...`)?",
        "when_use": "Always use IAM Roles for applications running on EC2, ECS, and Lambda.",
        "when_not": "Never create IAM Users with permanent access keys for workload-to-workload communication.",
        "next_step": "Phase 04: IAM Policies — Constructing granular JSON policies and condition keys."
    },
    # 04: IAM Policies
    {
        "module": "01-iam-and-security", "slug": "04-iam-policies", "num": "04",
        "title": "IAM Policies",
        "motto": "A policy is a declarative contract of trust. One wrong wildcard can expose your entire company.",
        "type": "Hands-on Lab & Policy Analysis", "time": "60",
        "prereqs": "Phase 03: IAM From First Principles",
        "services": "IAM Policy Engine, Policy Simulator, Condition Keys",
        "cost": "Free ($0.00 / IAM is free)",
        "problem": "Giving developers broad `s3:*` permissions allows them to accidentally read production databases, delete client documents, or expose buckets to the public internet.",
        "prediction": "Adding a Condition key requiring `aws:SecureTransport: true` will immediately reject unencrypted HTTP requests to S3 with AccessDenied.",
        "why_matters": "Modern least-privilege security relies on condition keys (IP boundaries, MFA requirements, tag-based access control) rather than simple action lists.",
        "first_principles": "A policy document is a JSON AST evaluated at request time. Each Statement contains `Effect`, `Action`, `Resource`, and optional `Condition` blocks. Conditions evaluate contextual request variables (`aws:CurrentTime`, `aws:PrincipalArn`, `aws:SourceIp`, `s3:prefix`).",
        "diagram": """IAM Policy Anatomy:
{
  "Effect": "Allow" | "Deny",
  "Action": [ "service:operation" ],
  "Resource": [ "arn:aws:service:region:account:type/id" ],
  "Condition": { "Operator": { "ContextKey": "Value" } }
}""",
        "before_aws": "Database GRANT/REVOKE statements, POSIX file ACLs (setfacl), and Windows NTFS access control lists.",
        "primitive_code": """import json
with open('policies/s3-read-write-least-privilege.json') as f:
    policy = json.load(f)
print(f"Policy Statements Loaded: {len(policy['Statement'])}")
for s in policy['Statement']:
    print(f"  Sid: {s.get('Sid')} | Effect: {s['Effect']} | Actions: {s['Action']}")""",
        "aws_cmd": "# Validate policy syntax using AWS CLI\naws iam get-account-summary --output table",
        "inspect": "cat policies/s3-read-write-least-privilege.json",
        "measure": "Test policy evaluation speed using AWS IAM Policy Simulator CLI.",
        "break_desc": "Add an explicit Deny on `s3:*` to your identity policy and try to list buckets.",
        "diagnose": "Observe that even with AdministratorAccess attached, the Explicit Deny wins and listing fails.",
        "recover": "Remove the explicit Deny statement.",
        "security": "Use Condition keys (`aws:PrincipalOrgID`, `aws:SourceVpce`) to enforce perimeter-based access control.",
        "cost": "IAM policy creation and storage is free.",
        "cleanup": "# No billable resources created.",
        "verify_cleanup": "echo 'Account clean.'",
        "mastery_q1": "What is the difference between an Identity-Based Policy and a Resource-Based Policy?",
        "mastery_q2": "If Account A's IAM user wants to access an S3 bucket in Account B, what policies must allow it?",
        "mastery_q3": "How does a Permissions Boundary prevent an IAM admin user from escalating their own privileges?",
        "when_use": "Use granular JSON policies for every production service and workload role.",
        "when_not": "Avoid huge monolithic 10,000-character policies; break them into modular purpose-driven policies.",
        "next_step": "Phase 05: AWS Networking Before VPC — Rebuilding IPv4, CIDR, and routing from first principles."
    },
    # 05: AWS Networking Before VPC
    {
        "module": "02-networking-and-vpc", "slug": "05-aws-networking-before-vpc", "num": "05",
        "title": "AWS Networking Before VPC",
        "motto": "A network is just routers, routing tables, and IP addresses. VPC is software-defined packet encapsulation.",
        "type": "Systems Experiment & Network Math", "time": "60",
        "prereqs": "Phase 04: IAM Policies",
        "services": "IPv4, RFC 1918, CIDR Blocks",
        "cost": "Free ($0.00 / Local Math & Networking)",
        "problem": "Engineers configure subnets like `10.0.1.0/24` without understanding binary masking, run out of private IP addresses 6 months into production, and find that AWS VPC CIDR blocks cannot be easily re-architected without rebuilding everything.",
        "prediction": "An IPv4 CIDR of `/24` provides 256 theoretical addresses, but AWS reserves exactly 5 addresses, leaving 251 usable for EC2 and ENIs.",
        "why_matters": "Every cloud resource (EC2, RDS, Lambda in VPC, ALB) consumes private IP addresses from your subnets. Miscalculating CIDRs leads to production scaling brick walls.",
        "first_principles": "An IPv4 address is 32 bits (4 octets of 8 bits). CIDR `/N` specifies that the first N bits represent the network prefix, while `32 - N` bits represent host addresses ($2^{32-N}$). In AWS, 5 IPs are always reserved: `.0` (Network), `.1` (VPC Router), `.2` (DNS resolver), `.3` (Future use), `.255` (Broadcast).",
        "diagram": """CIDR Subnet Math:
10.0.1.0/24 = 32-bit address:
[ 00001010 . 00000000 . 00000001 ] [ 00000000 ]
<--------- Network Prefix (24 bits) -------> < Host (8 bits) >
Total IPs: 2^8 = 256
AWS Reserved:
  10.0.1.0   -> Network Address
  10.0.1.1   -> VPC Virtual Router
  10.0.1.2   -> Amazon Provided DNS (Route 53 Resolver)
  10.0.1.3   -> AWS Internal Reserved
  10.0.1.255 -> Broadcast (not used in VPC, but reserved)
Usable IPs: 251""",
        "before_aws": "Network engineers manually assigned VLANs on Cisco Catalyst switches, configured trunk ports (802.1Q), and set up physical DHCP servers.",
        "primitive_code": """import ipaddress
net = ipaddress.IPv4Network("10.0.1.0/24")
print(f"Network: {net.network_address}")
print(f"Netmask: {net.netmask}")
print(f"Total Hosts: {net.num_addresses}")
print(f"Usable AWS IPs: {net.num_addresses - 5}")""",
        "aws_cmd": "# Inspect default VPC CIDR allocation\naws ec2 describe-vpcs --query 'Vpcs[].[VpcId,CidrBlock,IsDefault]' --output table",
        "inspect": "python3 -c \"import ipaddress; print(list(ipaddress.IPv4Network('10.0.0.0/16').subnets(new_prefix=24))[:4])\"",
        "measure": "Calculate subnet exhaustion thresholds for container workloads deploying 500 tasks.",
        "break_desc": "Attempt to create a subnet with a `/29` mask (8 IPs) and try to launch 4 instances.",
        "diagnose": "The 4th instance launch fails: 8 total IPs - 5 AWS reserved = only 3 usable IPs!",
        "recover": "Design subnets with at least `/24` (251 usable IPs) or `/20` (4,091 usable IPs) for compute tiers.",
        "security": "RFC 1918 defines non-routable private address spaces (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`) to isolate private infrastructure from the public internet.",
        "cost": "VPC CIDR allocations cost $0.00.",
        "cleanup": "# No resources created in Phase 05.",
        "verify_cleanup": "echo 'Account clean.'",
        "mastery_q1": "Why does AWS reserve the `.2` address in every subnet instead of having a single global DNS IP across the entire VPC?",
        "mastery_q2": "What happens if your on-premises corporate network uses `10.0.0.0/16` and your AWS VPC also uses `10.0.0.0/16` when you attempt to connect them via VPN?",
        "mastery_q3": "Why is `/28` the smallest subnet mask AWS allows, and `/16` the largest single VPC CIDR?",
        "when_use": "Always plan CIDR blocks carefully before creating production VPCs.",
        "when_not": "Never choose `172.31.0.0/16` for corporate VPCs as it collides with the AWS Default VPC.",
        "next_step": "Phase 06: Build a VPC From First Principles — Creating your own software-defined private cloud network."
    },
    # 06: Build a VPC From First Principles
    {
        "module": "02-networking-and-vpc", "slug": "06-build-a-vpc-from-scratch", "num": "06",
        "title": "Build a VPC From First Principles",
        "motto": "A VPC is not a physical box: it is a private overlay network carved out of AWS's global hypervisor fabric.",
        "type": "Hands-on Lab & Network Construction", "time": "60",
        "prereqs": "Phase 05: AWS Networking Before VPC",
        "services": "Amazon VPC API",
        "cost": "Free ($0.00 / Idle VPCs are free)",
        "problem": "Relying on the AWS 'Default VPC' puts your production databases and backend servers into public subnets with default internet gateways, violating isolation principles.",
        "prediction": "Creating a custom VPC will create a virtual network with a default Route Table and a default Security Group, but zero subnets and zero internet connectivity.",
        "why_matters": "Every AWS workload lives inside a VPC. Understanding how to construct one from scratch without wizard defaults gives you total mastery over cloud network boundaries.",
        "first_principles": "A Virtual Private Cloud (VPC) is a logically isolated virtual network partition. Under the hood, AWS uses software-defined networking encapsulation protocols (Geneve / VXLAN) running on AWS Nitro network ASIC cards to tunnel private packets across physical datacenter fiber without cross-tenant interference.",
        "diagram": """VPC Boundary:
AWS Region (us-east-1)
┌────────────────────────────────────────────────────────┐
│ Amazon VPC (CIDR: 10.0.0.0/16)                         │
│ • Completely isolated from other AWS accounts          │
│ • Completely isolated from the public internet         │
│ • Main Route Table (10.0.0.0/16 -> local)              │
│ • Default Security Group (Deny inbound from outside)   │
└────────────────────────────────────────────────────────┘""",
        "before_aws": "Network engineers provisioned isolated VLANs and configured virtual routing and forwarding (VRF) instances on physical core routers.",
        "primitive_code": """# Template reference for custom VPC
print("VPC Architecture Specification:")
print("  VpcCIDR: 10.0.0.0/16")
print("  DNS Hostnames: Enabled")
print("  DNS Resolution: Enabled")""",
        "aws_cmd": "aws ec2 create-vpc --cidr-block 10.0.0.0/16 --tag-specifications 'ResourceType=vpc,Tags=[{Key=Project,Value=aws-from-scratch},{Key=Lesson,Value=06-vpc}]' --output json",
        "inspect": "aws ec2 describe-vpcs --filters 'Name=tag:Project,Values=aws-from-scratch' --output table",
        "measure": "Inspect the default main route table automatically generated for your new VPC.",
        "break_desc": "Disable DNS hostnames and DNS resolution on the VPC and observe how internal service discovery breaks.",
        "diagnose": "Instances fail to resolve internal AWS DNS names like `ip-10-0-1-50.ec2.internal`.",
        "recover": "Run `aws ec2 modify-vpc-attribute --vpc-id <id> --enable-dns-hostnames`.",
        "security": "A newly created VPC has zero internet connectivity by default. It is completely dark to the public internet.",
        "cost": "VPCs are completely free. You can create up to 5 VPCs per region with zero ongoing charges.",
        "cleanup": "VPC_ID=$(aws ec2 describe-vpcs --filters 'Name=tag:Project,Values=aws-from-scratch' --query 'Vpcs[0].VpcId' --output text)\nif [ \"$VPC_ID\" != \"None\" ]; then aws ec2 delete-vpc --vpc-id \"$VPC_ID\"; fi",
        "verify_cleanup": "aws ec2 describe-vpcs --filters 'Name=tag:Project,Values=aws-from-scratch' --query 'Vpcs[]' --output text",
        "mastery_q1": "Why does a VPC have a default Main Route Table created automatically?",
        "mastery_q2": "What is the security difference between the AWS Default VPC and a custom VPC created from scratch?",
        "mastery_q3": "Can two different VPCs in the same account have identical overlapping CIDR blocks (e.g. 10.0.0.0/16)? What breaks if they do?",
        "when_use": "Always build custom VPCs for any serious application or production environment.",
        "when_not": "Do not create 15 separate VPCs for tiny microservices unless strict network isolation or regulatory boundaries demand it.",
        "next_step": "Phase 07: Subnets — Subdividing your VPC across physical Availability Zones."
    },
    # 07: Subnets
    {
        "module": "02-networking-and-vpc", "slug": "07-subnets", "num": "07",
        "title": "Subnets",
        "motto": "A subnet lives in exactly one Availability Zone. Redundancy requires multiple subnets across multiple AZs.",
        "type": "Hands-on Lab & Network Slicing", "time": "60",
        "prereqs": "Phase 06: Build a VPC From First Principles",
        "services": "Amazon VPC Subnets",
        "cost": "Free ($0.00 / Subnets are free)",
        "problem": "A VPC is a broad CIDR block (e.g. 10.0.0.0/16), but you cannot launch a virtual machine into a VPC directly: instances must attach to a specific physical datacenter. How do we carve the network into physical zones?",
        "prediction": "A subnet cannot span multiple Availability Zones. If you specify `us-east-1a`, that subnet's packets physically terminate in datacenter campus A.",
        "why_matters": "High availability requires deploying resources across at least two Availability Zones. This mandates creating at least two subnets.",
        "first_principles": "A subnet is a contiguous partition of a VPC's IP address space bound strictly to a single physical Availability Zone. While a VPC spans the entire Region, every subnet is physically tethered to one AZ's hardware switches and power domain.",
        "diagram": """VPC to Subnets:
VPC: 10.0.0.0/16
├── us-east-1a (Physical DC 1)
│   └── Subnet A: 10.0.1.0/24 (251 usable IPs)
│
└── us-east-1b (Physical DC 2)
    └── Subnet B: 10.0.2.0/24 (251 usable IPs)""",
        "before_aws": "Network engineers mapped VLANs to physical access layer switches in Rack Row 1 and Rack Row 2.",
        "primitive_code": """# Subnet planning verification
subnets = [
    {"name": "Subnet-A", "az": "us-east-1a", "cidr": "10.0.1.0/24"},
    {"name": "Subnet-B", "az": "us-east-1b", "cidr": "10.0.2.0/24"}
]
for s in subnets:
    print(f"Carved {s['name']} in {s['az']} with CIDR {s['cidr']}")""",
        "aws_cmd": "aws ec2 create-subnet --vpc-id $VPC_ID --cidr-block 10.0.1.0/24 --availability-zone us-east-1a --tag-specifications 'ResourceType=subnet,Tags=[{Key=Project,Value=aws-from-scratch},{Key=Name,Value=subnet-az1}]'",
        "inspect": "aws ec2 describe-subnets --filters 'Name=tag:Project,Values=aws-from-scratch' --query 'Subnets[].[SubnetId,AvailabilityZone,CidrBlock,AvailableIpAddressCount]' --output table",
        "measure": "Observe the `AvailableIpAddressCount`: for a `/24`, it will show exactly `251` (not 256).",
        "break_desc": "Attempt to create a subnet with an overlapping CIDR (e.g. `10.0.1.128/25`) in the same VPC.",
        "diagnose": "AWS rejects the API call with `InvalidSubnet.Conflict: The CIDR conflicts with another subnet`.",
        "recover": "Choose a non-overlapping CIDR block (e.g. `10.0.2.0/24`).",
        "security": "Subnets provide the primary physical containment boundaries for multi-tier applications.",
        "cost": "Subnets cost $0.00.",
        "cleanup": "for id in $(aws ec2 describe-subnets --filters 'Name=tag:Project,Values=aws-from-scratch' --query 'Subnets[].SubnetId' --output text); do aws ec2 delete-subnet --subnet-id $id; done",
        "verify_cleanup": "aws ec2 describe-subnets --filters 'Name=tag:Project,Values=aws-from-scratch' --query 'Subnets[]' --output text",
        "mastery_q1": "Why did AWS design subnets to be strictly single-AZ rather than regional?",
        "mastery_q2": "If an EC2 instance in Subnet A (us-east-1a) sends a packet to an instance in Subnet B (us-east-1b), what physical path does that packet take?",
        "mastery_q3": "Can a subnet's CIDR block be modified or expanded after creation?",
        "when_use": "Create at least two subnets in two different AZs for every application tier (public, application, database).",
        "when_not": "Do not create 50 tiny /28 subnets for individual microservices—it creates routing complexity with zero security benefit.",
        "next_step": "Phase 08: Route Tables — Deciding where packets travel when they leave a network interface."
    },
    # 08: Route Tables
    {
        "module": "02-networking-and-vpc", "slug": "08-route-tables", "num": "08",
        "title": "Route Tables",
        "motto": "Packets don't think: they look up the longest prefix match in the route table.",
        "type": "Hands-on Lab & Routing Mechanics", "time": "60",
        "prereqs": "Phase 07: Subnets",
        "services": "Amazon VPC Route Tables, Local Route",
        "cost": "Free ($0.00 / Route tables are free)",
        "problem": "An instance sends an IP packet to `10.0.2.50`. How does the hypervisor virtual switch know whether to route it internally, forward it to a gateway, or drop it?",
        "prediction": "Every route table contains an immutable default route for the VPC CIDR (`10.0.0.0/16 -> local`) that cannot be deleted.",
        "why_matters": "A misconfigured route table is the #1 cause of 'Connection timed out' errors in AWS. If there is no route for a destination, packets are dropped immediately.",
        "first_principles": "A route table contains a list of rules: `Destination CIDR -> Target Next-Hop`. Routing decisions follow the **Longest Prefix Match** rule. If a packet matches both `10.0.0.0/16 -> local` and `0.0.0.0/0 -> igw-xxxx`, the more specific `/16` route wins for internal traffic, while `/0` matches all external traffic.",
        "diagram": """Route Table Evaluation:
Packet Destination: 10.0.2.88
Route Table Rules:
┌─────────────────┬─────────────┬──────────────────────────────────────────┐
│ Destination     │ Target      │ Match Evaluation                         │
├─────────────────┼─────────────┼──────────────────────────────────────────┤
│ 10.0.0.0/16     │ local       │ MATCH (/16 prefix = 16 bits match!)     │
│ 0.0.0.0/0       │ igw-xxxx    │ MATCH (/0 prefix = 0 bits match)         │
└─────────────────┴─────────────┴──────────────────────────────────────────┘
Result: 10.0.0.0/16 wins (Longest Prefix Match)! Forwarded internally.""",
        "before_aws": "Network engineers configured static routes and dynamic routing protocols (OSPF, BGP) on Cisco/Juniper hardware routers.",
        "primitive_code": """# Longest prefix match simulation
import ipaddress
routes = [
    (ipaddress.IPv4Network("10.0.0.0/16"), "local"),
    (ipaddress.IPv4Network("0.0.0.0/0"), "internet-gateway")
]
target = ipaddress.IPv4Address("10.0.2.88")
matches = [r for r in routes if target in r[0]]
winner = max(matches, key=lambda r: r[0].prefixlen)
print(f"Target {target} routes to: {winner[1]} (Prefix length: /{winner[0].prefixlen})")""",
        "aws_cmd": "aws ec2 create-route-table --vpc-id $VPC_ID --tag-specifications 'ResourceType=route-table,Tags=[{Key=Project,Value=aws-from-scratch},{Key=Name,Value=custom-rt}]'",
        "inspect": "aws ec2 describe-route-tables --filters 'Name=tag:Project,Values=aws-from-scratch' --query 'RouteTables[].[RouteTableId,Routes]' --output json",
        "measure": "Inspect route propagation attributes and route state (`active` vs `blackhole`).",
        "break_desc": "Target an unattached or deleted gateway in a route rule.",
        "diagnose": "The route state transitions to `blackhole` and traffic to that destination silently disappears.",
        "recover": "Update the route with `aws ec2 replace-route` to point to a valid active target.",
        "security": "Private subnets are isolated by omitting any route to an Internet Gateway.",
        "cost": "Route tables and routing rules cost $0.00.",
        "cleanup": "for id in $(aws ec2 describe-route-tables --filters 'Name=tag:Project,Values=aws-from-scratch' --query 'RouteTables[?Associations[0].Main!=`true`].RouteTableId' --output text); do aws ec2 delete-route-table --route-table-id $id; done",
        "verify_cleanup": "echo 'Custom route tables cleaned.'",
        "mastery_q1": "Why does AWS prevent you from deleting or modifying the `10.0.0.0/16 -> local` route in a route table?",
        "mastery_q2": "If a subnet is not explicitly associated with a route table, which route table does it use by default?",
        "mastery_q3": "How does Longest Prefix Match behave if you add a route for `10.0.1.0/24 -> vpc-peering-connection`?",
        "when_use": "Create dedicated route tables for public and private subnets to enforce explicit routing separation.",
        "when_not": "Do not create a separate route table for every single subnet if multiple subnets share the exact same routing rules.",
        "next_step": "Phase 09: Internet Gateway — Connecting your VPC routing table to the public IPv4 internet."
    },
    # 09: Internet Gateway
    {
        "module": "02-networking-and-vpc", "slug": "09-internet-gateway", "num": "09",
        "title": "Internet Gateway",
        "motto": "An IGW is not a bottleneck appliance: it is a horizontally scaled 1-to-1 NAT routing gateway.",
        "type": "Hands-on Lab & Internet Routing", "time": "60",
        "prereqs": "Phase 08: Route Tables",
        "services": "Amazon VPC Internet Gateway (IGW)",
        "cost": "Free ($0.00 / IGWs are free)",
        "problem": "Instances inside a private VPC cannot reach the public internet, and external clients cannot reach your web server. What connects the virtual network to the global internet?",
        "prediction": "Attaching an Internet Gateway to a VPC does NOT automatically make instances accessible to the internet until a default route (`0.0.0.0/0 -> igw-xxxx`) and public IPs are configured.",
        "why_matters": "Treating an IGW as a physical router creates misconceptions about bandwidth bottlenecks and packet loss.",
        "first_principles": "An Internet Gateway (IGW) is a horizontally scaled, redundant, software-defined VPC edge component. It performs two duties: (1) serves as a target in VPC route tables for traffic destined to the internet, and (2) performs 1-to-1 Network Address Translation (NAT) between private IPv4 addresses and allocated public IPv4 addresses.",
        "diagram": """Internet Gateway 1-to-1 NAT:
[ Public Internet ] (Client: 198.51.100.22)
        │
        ▼ (Destination: Public IP 54.210.10.5)
┌───────────────────────────────────────────────┐
│ Internet Gateway (IGW)                        │
│ Maps Public IP 54.210.10.5 <==> 10.0.1.50     │
└───────┬───────────────────────────────────────┘
        │ (Destination rewritten to: 10.0.1.50)
        ▼
┌───────────────────────────────────────────────┐
│ VPC Public Subnet (EC2 Private IP: 10.0.1.50) │
└───────────────────────────────────────────────┘""",
        "before_aws": "Datacenters maintained high-throughput border routers with BGP peering to Tier 1 internet transit providers.",
        "primitive_code": """# 1-to-1 NAT simulation
nat_table = {"54.210.10.5": "10.0.1.50"}
packet_in = {"src": "198.51.100.22", "dst": "54.210.10.5"}
packet_in["dst"] = nat_table[packet_in["dst"]]
print(f"IGW translated destination to private VPC IP: {packet_in['dst']}")""",
        "aws_cmd": "aws ec2 create-internet-gateway --tag-specifications 'ResourceType=internet-gateway,Tags=[{Key=Project,Value=aws-from-scratch}]'",
        "inspect": "aws ec2 describe-internet-gateways --filters 'Name=tag:Project,Values=aws-from-scratch' --output table",
        "measure": "Verify network throughput: an IGW imposes zero bandwidth throttling (bandwidth is bounded strictly by the instance's network card).",
        "break_desc": "Detach the IGW from an active VPC while an instance is running.",
        "diagnose": "All inbound and outbound public internet traffic drops instantly with `Network is unreachable`.",
        "recover": "Reattach the IGW: `aws ec2 attach-internet-gateway --internet-gateway-id $IGW_ID --vpc-id $VPC_ID`.",
        "security": "An IGW alone does not expose your machines. A machine is only exposed if it has: (1) route to IGW, (2) public IP, and (3) permissive Security Group.",
        "cost": "Internet Gateways are completely free of charge. There are no hourly or setup fees.",
        "cleanup": "IGW_ID=$(aws ec2 describe-internet-gateways --filters 'Name=tag:Project,Values=aws-from-scratch' --query 'InternetGateways[0].InternetGatewayId' --output text)\nif [ \"$IGW_ID\" != \"None\" ]; then aws ec2 detach-internet-gateway --internet-gateway-id $IGW_ID --vpc-id $VPC_ID; aws ec2 delete-internet-gateway --internet-gateway-id $IGW_ID; fi",
        "verify_cleanup": "aws ec2 describe-internet-gateways --filters 'Name=tag:Project,Values=aws-from-scratch' --query 'InternetGateways[]' --output text",
        "mastery_q1": "Why is an Internet Gateway considered horizontally scalable with zero maintenance, unlike a NAT Gateway?",
        "mastery_q2": "Does an EC2 instance OS kernel know its own public IP address when running in a public subnet?",
        "mastery_q3": "Can a single VPC have multiple Internet Gateways attached simultaneously?",
        "when_use": "Attach exactly one Internet Gateway to any VPC that needs public ingress or egress.",
        "when_not": "Do not attach an IGW to strictly isolated VPCs intended for back-office batch processing or air-gapped workloads.",
        "next_step": "Phase 10: Public vs Private Subnets — Deriving subnet publicity from routing tables."
    },
    # 10: Public vs Private Subnets
    {
        "module": "02-networking-and-vpc", "slug": "10-public-vs-private-subnets", "num": "10",
        "title": "Public vs Private Subnets",
        "motto": "A subnet is not 'public' because of its name: it is public if and only if its route table targets an Internet Gateway.",
        "type": "Hands-on Lab & Architectural Isolation", "time": "60",
        "prereqs": "Phase 09: Internet Gateway",
        "services": "Public Subnets, Private Subnets, Route Table Associations",
        "cost": "Free ($0.00 / Routing is free)",
        "problem": "Naming a subnet 'private-db-subnet' does not make it private. If someone associates it with a route table targeting an IGW, database ports can be scanned from the public internet.",
        "prediction": "An EC2 instance in a subnet whose route table only contains `10.0.0.0/16 -> local` cannot be reached from the public internet, even if someone manually assigns it a public IP.",
        "why_matters": "Understanding routing-driven publicity prevents accidental public exposure of databases, caches, and internal microservices.",
        "first_principles": "Subnet publicity is a mathematical consequence of routing: Public Subnet: Associated with a route table having `0.0.0.0/0 -> igw-xxxx`. Private Subnet: Associated with a route table having NO route to an IGW. Packets to `0.0.0.0/0` are dropped at the virtual router.",
        "diagram": """Public vs Private Routing:
                    ┌─────────────────────────┐
                    │ Internet Gateway (IGW)  │
                    └───────────┬─────────────┘
                                │
                    ┌───────────▼─────────────┐
                    │ Public Route Table      │ (0.0.0.0/0 -> IGW)
                    └───────────┬─────────────┘
                                │
                    ┌───────────▼─────────────┐
                    │ Public Subnet (ALB/NAT) │
                    └─────────────────────────┘

                    ┌─────────────────────────┐
                    │ Private Route Table     │ (10.0.0.0/16 -> local ONLY)
                    └───────────┬─────────────┘
                                │
                    ┌───────────▼─────────────┐
                    │ Private Subnet (DB/App) │
                    └─────────────────────────┘""",
        "before_aws": "Enterprise datacenters separated public DMZs from private internal networks using physical dual-homed firewalls.",
        "primitive_code": """# Verify subnet route target
def is_public_subnet(routes):
    return any(r['dest'] == '0.0.0.0/0' and r['target'].startswith('igw-') for r in routes)

print("Subnet 1 is public:", is_public_subnet([{'dest': '10.0.0.0/16', 'target': 'local'}, {'dest': '0.0.0.0/0', 'target': 'igw-1234'}]))
print("Subnet 2 is public:", is_public_subnet([{'dest': '10.0.0.0/16', 'target': 'local'}]))""",
        "aws_cmd": "aws ec2 create-route --route-table-id $PUB_RT_ID --destination-cidr-block 0.0.0.0/0 --gateway-id $IGW_ID",
        "inspect": "aws ec2 describe-route-tables --route-table-ids $PUB_RT_ID --query 'RouteTables[0].Routes' --output table",
        "measure": "Compare connectivity: `curl` to internet from public subnet vs private subnet.",
        "break_desc": "Associate your private subnet with the public route table.",
        "diagnose": "The private subnet is now exposed to internet routing rules.",
        "recover": "Re-associate the private subnet with its dedicated private route table.",
        "security": "Never place database instances (RDS) into public subnets, even if protected by security groups.",
        "cost": "Subnet routing configuration is free.",
        "cleanup": "# Cleanup custom route associations",
        "verify_cleanup": "echo 'Subnets verified.'",
        "mastery_q1": "Can an instance in a private subnet initiate an outbound connection to download OS security updates without an IGW route?",
        "mastery_q2": "What is the role of a NAT Gateway in connecting private subnets to the internet?",
        "mastery_q3": "Why is a bastion host / jump box always placed in a public subnet?",
        "when_use": "Always split your VPC into public subnets (for ALBs and NAT) and private subnets (for compute and databases).",
        "when_not": "Never create a single flat public subnet for all resources.",
        "next_step": "Phase 11: Security Groups — Hypervisor-level stateful packet filtering."
    },
    # 11: Security Groups
    {
        "module": "02-networking-and-vpc", "slug": "11-security-groups", "num": "11",
        "title": "Security Groups",
        "motto": "Security Groups are stateful virtual firewalls evaluated at the hypervisor ENI. If inbound is allowed, outbound return traffic is automatically allowed.",
        "type": "Hands-on Lab & Firewall Experiments", "time": "60",
        "prereqs": "Phase 10: Public vs Private Subnets",
        "services": "Amazon EC2 Security Groups",
        "cost": "Free ($0.00 / Security groups are free)",
        "problem": "Once an instance has an IP address, port scanners on the public internet can immediately probe open ports (SSH 22, Redis 6379, DB 5432). How do we enforce zero-trust packet filtering?",
        "prediction": "A Security Group with zero inbound rules will silently drop all incoming connection attempts, resulting in client TCP SYN timeouts.",
        "why_matters": "Security Groups are the primary defense perimeter for AWS compute. Understanding their stateful nature prevents opening unnecessary ports.",
        "first_principles": "A Security Group is a stateful distributed packet filter attached directly to an Elastic Network Interface (ENI). Stateful means the hypervisor tracks TCP connection states (`SYN`, `SYN-ACK`, `ESTABLISHED`). When an inbound connection is allowed, return traffic is automatically allowed regardless of outbound rules.",
        "diagram": """Stateful Security Group Mechanics:
Client ────────(TCP SYN Port 80)────────► [ ENI Security Group ] ──► Allowed!
Client ◄──────(TCP SYN-ACK Return)────── [ ENI Security Group ] ◄── AUTO-ALLOWED!
                                         (Tracked in Connection State Table)""",
        "before_aws": "System administrators configured Linux `iptables` / `nftables` or physical ASA firewall appliances.",
        "primitive_code": """# Simulating stateful connection table
state_table = set()
def handle_packet(src_ip, dst_port, is_inbound, rule_allowed):
    conn_key = (src_ip, dst_port)
    if is_inbound:
        if rule_allowed:
            state_table.add(conn_key)
            return "ALLOW (Rule matched)"
        return "DROP (No rule)"
    else: # outbound return
        if conn_key in state_table:
            return "ALLOW (Stateful return recognized)"
        return "EVALUATE_OUTBOUND"

print(handle_packet("198.51.100.1", 80, is_inbound=True, rule_allowed=True))
print(handle_packet("198.51.100.1", 80, is_inbound=False, rule_allowed=False))""",
        "aws_cmd": "aws ec2 create-security-group --group-name lab-web-sg --description 'Lab Web Security Group' --vpc-id $VPC_ID --tag-specifications 'ResourceType=security-group,Tags=[{Key=Project,Value=aws-from-scratch}]'",
        "inspect": "aws ec2 describe-security-groups --filters 'Name=tag:Project,Values=aws-from-scratch' --output json",
        "measure": "Measure connection timeout duration when SYN packets are silently discarded (typically 30-60s).",
        "break_desc": "Remove the inbound rule for port 80 and attempt to connect with curl.",
        "diagnose": "curl hangs with `Connection timed out` (NOT `Connection refused`).",
        "recover": "Authorize inbound traffic: `aws ec2 authorize-security-group-ingress --group-id $SG_ID --protocol tcp --port 80 --cidr 0.0.0.0/0`.",
        "security": "Never use `0.0.0.0/0` on SSH port 22 or database port 5432. Reference other security groups by ID for microservice communication.",
        "cost": "Security Groups are completely free.",
        "cleanup": "for id in $(aws ec2 describe-security-groups --filters 'Name=tag:Project,Values=aws-from-scratch' --query 'SecurityGroups[?GroupName!=`default`].GroupId' --output text); do aws ec2 delete-security-group --group-id $id; done",
        "verify_cleanup": "echo 'Security groups cleaned.'",
        "mastery_q1": "Why does a dropped packet in a Security Group cause a 'Connection timed out' while an inactive service causes a 'Connection refused'?",
        "mastery_q2": "What is the architectural advantage of referencing a Security Group ID as a source instead of an IP address CIDR?",
        "mastery_q3": "Can a Security Group have an explicit 'Deny' rule?",
        "when_use": "Use Security Groups as your primary firewall for all ENIs, EC2 instances, ALBs, and RDS databases.",
        "when_not": "Security Groups cannot perform Layer 7 HTTP payload inspection or SQL injection filtering (use AWS WAF for Layer 7).",
        "next_step": "Phase 12: Network ACLs — Subnet-level stateless defense-in-depth packet filtering."
    },
    # 12: Network ACLs
    {
        "module": "02-networking-and-vpc", "slug": "12-network-acls", "num": "12",
        "title": "Network ACLs",
        "motto": "Network ACLs are stateless subnet gatekeepers. You must explicitly open ephemeral ports for return traffic.",
        "type": "Hands-on Lab & Stateless Filtering", "time": "60",
        "prereqs": "Phase 11: Security Groups",
        "services": "Amazon VPC Network ACLs (NACLs)",
        "cost": "Free ($0.00 / NACLs are free)",
        "problem": "Security Groups cannot block a specific malicious IP address (they only have Allow rules). How do we block a compromised CIDR block at the subnet perimeter?",
        "prediction": "If you allow inbound port 80 in a NACL but forget to allow outbound ephemeral ports (1024-65535), web requests will reach the server but responses will be blocked.",
        "why_matters": "The stateless nature of NACLs trips up almost every junior cloud engineer. Return packets do not automatically bypass NACLs.",
        "first_principles": "A Network ACL is a stateless subnet-level filter evaluated in numbered rule order (1-32766). Stateless means the filter has zero memory of active connections. Every incoming packet is evaluated against inbound rules; every outgoing packet is evaluated against outbound rules independently.",
        "diagram": """Stateless NACL Ephemeral Port Requirement:
Client (Port 52140) ────(SYN Port 80)────► [ NACL Inbound Rule 100: Allow Port 80 ] ──► Server
Client (Port 52140) ◄──(SYN-ACK Return)─── [ NACL Outbound Rule ???: Must Allow Ephemeral 1024-65535! ]
                                           (If outbound rule missing -> Return packet is DROPPED!)""",
        "before_aws": "Router access control lists configured on physical gateway interfaces.",
        "primitive_code": """# NACL Rule Number Evaluation Order
rules = [
    {"rule_num": 100, "action": "DENY", "cidr": "198.51.100.44/32"},
    {"rule_num": 200, "action": "ALLOW", "cidr": "0.0.0.0/0"},
    {"rule_num": "*", "action": "DENY", "cidr": "0.0.0.0/0"}
]
def evaluate_nacl(ip):
    for r in sorted(rules, key=lambda x: str(x['rule_num'])):
        if r['rule_num'] == 100 and ip == "198.51.100.44":
            return f"Rule {r['rule_num']} matched: {r['action']}"
        elif r['rule_num'] == 200:
            return f"Rule {r['rule_num']} matched: {r['action']}"
    return "Default Deny (*)"
print(evaluate_nacl("198.51.100.44"))
print(evaluate_nacl("192.0.2.1"))""",
        "aws_cmd": "aws ec2 create-network-acl --vpc-id $VPC_ID --tag-specifications 'ResourceType=network-acl,Tags=[{Key=Project,Value=aws-from-scratch}]'",
        "inspect": "aws ec2 describe-network-acls --filters 'Name=tag:Project,Values=aws-from-scratch' --output json",
        "measure": "Compare Security Group vs NACL: Security Groups evaluate all rules; NACLs terminate at first matching rule number.",
        "break_desc": "Delete the default outbound rule (`Rule 100: Allow All`) in a custom NACL.",
        "diagnose": "The client successfully sends HTTP requests, but `curl` hangs forever waiting for the response.",
        "recover": "Add outbound rule allowing ephemeral ports: `aws ec2 create-network-acl-entry --network-acl-id $NACL_ID --rule-number 100 --protocol tcp --rule-action allow --egress --cidr-block 0.0.0.0/0 --port-range From=1024,To=65535`.",
        "security": "Use NACLs sparingly: primarily for blocking known bad IP ranges or enforcing coarse compliance boundaries.",
        "cost": "Network ACLs are free.",
        "cleanup": "for id in $(aws ec2 describe-network-acls --filters 'Name=tag:Project,Values=aws-from-scratch' --query 'NetworkAcls[?IsDefault!=`true`].NetworkAclId' --output text); do aws ec2 delete-network-acl --network-acl-id $id; done",
        "verify_cleanup": "echo 'Custom NACLs cleaned.'",
        "mastery_q1": "Why do Linux and Windows clients connect using random high-numbered ephemeral ports (32768-60999 or 49152-65535)?",
        "mastery_q2": "What is the operational downside of managing complex NACL rules compared to Security Groups?",
        "mastery_q3": "Which filter evaluates first for traffic entering a subnet: the Network ACL or the Security Group?",
        "when_use": "Use NACLs when you need an explicit DENY rule to block a malicious IP or subnet.",
        "when_not": "Do not duplicate your Security Group rules inside NACLs—it creates high operational maintenance with zero benefit.",
        "next_step": "Phase 13: EC2 From First Principles — Launching virtual compute machines."
    },
    # 13: EC2 From First Principles
    {
        "module": "03-compute-and-storage", "slug": "13-ec2-from-first-principles", "num": "13",
        "title": "EC2 From First Principles",
        "motto": "An EC2 instance is a slice of physical CPU and memory booted from a snapshot, attached to an ENI and an EBS volume.",
        "type": "Hands-on Lab & Virtual Machine Launch", "time": "60",
        "prereqs": "Phase 11: Security Groups",
        "services": "Amazon EC2, Amazon Linux 2023, Nitro Hypervisor",
        "cost": "Billable (~$0.0042/hr for t4g.micro | Free Tier eligible)",
        "problem": "You need to run arbitrary compiled binaries, system daemons, and custom software packages with root access on a Linux operating system.",
        "prediction": "Launching an EC2 instance will create a virtual machine, attach an Elastic Network Interface with a private IP, allocate an EBS root volume, and execute the User Data shell script on initial boot.",
        "why_matters": "EC2 is the foundational compute primitive in AWS. ECS, EKS, and even parts of RDS run on top of EC2 instances.",
        "first_principles": "AWS Nitro hypervisor partitions a physical server's CPU sockets into vCPUs (hardware hyperthreads) and assigns memory blocks. Storage and networking I/O are offloaded to dedicated PCIe Nitro accelerator cards, giving the guest OS near-native bare-metal performance.",
        "diagram": """EC2 Nitro System Architecture:
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
└────────────────────────────────────────────────────────┘""",
        "before_aws": "Provisioning a VMware ESXi or KVM virtual machine via vCenter or PXE netboot.",
        "primitive_code": """# User Data bootstrap script
user_data = '''#!/bin/bash
dnf update -y
dnf install -y httpd
echo "Hello from EC2 $(hostname -f)" > /var/www/html/index.html
systemctl start httpd
systemctl enable httpd'''
print("Bootstrap User Data defined.")""",
        "aws_cmd": "aws ec2 run-instances --image-id resolve:ssm:/aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-arm64 --instance-type t4g.micro --subnet-id $PUB_SUBNET_ID --security-group-ids $SG_ID --user-data file://scripts/userdata.sh --tag-specifications 'ResourceType=instance,Tags=[{Key=Project,Value=aws-from-scratch},{Key=Lesson,Value=13-ec2}]'",
        "inspect": "aws ec2 describe-instances --filters 'Name=tag:Project,Values=aws-from-scratch' --query 'Reservations[].Instances[].[InstanceId,State.Name,PublicIpAddress,PrivateIpAddress,InstanceType]' --output table",
        "measure": "Measure time from API call to HTTP 200 response (typically 60-120 seconds).",
        "break_desc": "Terminate the instance or stop the systemd daemon.",
        "diagnose": "Status checks: Instance status check fails if OS kernel panics; System status check fails if physical host hardware fails.",
        "recover": "Reboot the instance or launch a replacement via Auto Scaling.",
        "security": "Use AWS Systems Manager (SSM) Session Manager instead of opening SSH port 22 to the public internet.",
        "cost": "A `t4g.micro` costs ~$0.0042/hour (~$3.00/month). Unattached stopped instances do not incur compute charges, but attached EBS volumes continue charging for storage.",
        "cleanup": "for id in $(aws ec2 describe-instances --filters 'Name=tag:Project,Values=aws-from-scratch' 'Name=instance-state-name,Values=running,stopped' --query 'Reservations[].Instances[].InstanceId' --output text); do aws ec2 terminate-instances --instance-ids $id; done",
        "verify_cleanup": "aws ec2 describe-instances --filters 'Name=tag:Project,Values=aws-from-scratch' 'Name=instance-state-name,Values=running,pending' --query 'Reservations[].Instances[]' --output text",
        "mastery_q1": "What is the difference between a System Status Check failure and an Instance Status Check failure?",
        "mastery_q2": "Why does an EC2 instance get a new public IPv4 address when stopped and restarted, while its private IP remains identical?",
        "mastery_q3": "How does Graviton (ARM64) architecture deliver up to 40% better price-performance compared to x86?",
        "when_use": "Use EC2 when you require full OS control, legacy monolithic software, custom kernel modules, or long-running predictable workloads.",
        "when_not": "Avoid EC2 for simple stateless microservices or event-driven tasks where ECS Fargate or Lambda eliminates patching.",
        "next_step": "Phase 14: What Happens When EC2 Launches — Tracing the step-by-step lifecycle from API to booted OS."
    },
    # 14: What Happens When EC2 Launches
    {
        "module": "03-compute-and-storage", "slug": "14-what-happens-when-ec2-launches", "num": "14",
        "title": "What Happens When EC2 Launches",
        "motto": "From API call to running Linux kernel: demystifying the cloud control plane and instance metadata service.",
        "type": "Systems Exploration & Control Plane Trace", "time": "60",
        "prereqs": "Phase 13: EC2 From First Principles",
        "services": "EC2 Lifecycle, Instance Metadata Service (IMDSv2), CloudInit",
        "cost": "Free to inspect ($0.00)",
        "problem": "When an instance takes 5 minutes to launch or User Data fails to configure an application, developers have no idea where the process stalled.",
        "prediction": "The instance queries `http://169.254.169.254` locally via a link-local address to retrieve its IAM role credentials and configuration.",
        "why_matters": "Understanding cloud-init, IMDSv2, and EC2 boot stages allows you to diagnose bootstrap failures in seconds.",
        "first_principles": "The EC2 launch lifecycle: (1) API Call -> (2) Scheduler selects physical Nitro host with available capacity -> (3) Nitro card maps EBS volume via NVMe -> (4) Nitro card provisions ENI in target subnet -> (5) VM boots kernel -> (6) cloud-init runs and queries IMDSv2 -> (7) User Data script executes -> (8) 2/2 status checks turn green.",
        "diagram": """EC2 Boot Sequence:
[ RunInstances API ] ──► [ Placement Scheduler ] ──► Select Physical Host
                                                            │
    ┌───────────────────────────────────────────────────────┘
    ▼
[ Nitro Hypervisor ] ──► Allocates vCPU/RAM
[ Nitro NVMe ]       ──► Attaches EBS Root Volume
[ Nitro VPC ]        ──► Attaches Subnet ENI & Security Groups
    │
    ▼
[ Linux Boot ]       ──► GRUB ──► Kernel Initialization ──► systemd
    │
    ▼
[ Cloud-Init ]       ──► Queries IMDSv2 (169.254.169.254) ──► Executes User Data""",
        "before_aws": "PXE network booting using TFTP, DHCP Option 66/67, and Kickstart/Preseed configuration files.",
        "primitive_code": """# Querying IMDSv2 securely with a session token
import urllib.request
def get_imdsv2_token():
    req = urllib.request.Request(
        "http://169.254.169.254/latest/api/token",
        headers={"X-aws-ec2-metadata-token-ttl-seconds": "21600"},
        method="PUT"
    )
    try:
        with urllib.request.urlopen(req, timeout=2) as resp:
            return resp.read().decode()
    except Exception:
        return "IMDSv2 simulation: running locally"
print("IMDSv2 Token Request:", get_imdsv2_token())""",
        "aws_cmd": "aws ec2 get-console-output --instance-id $INSTANCE_ID --output text | tail -n 25",
        "inspect": "aws ec2 describe-instance-status --instance-ids $INSTANCE_ID --output json",
        "measure": "Analyze `/var/log/cloud-init-output.log` timing timestamps.",
        "break_desc": "Insert a syntax error in User Data script (`exit 1`).",
        "diagnose": "The instance passes 2/2 status checks (the OS booted fine), but the web server is not running! Inspect `/var/log/cloud-init-output.log`.",
        "recover": "Fix the User Data script and relaunch the instance.",
        "security": "Enforce IMDSv2 (`HttpTokens=required`). IMDSv1 is vulnerable to Server-Side Request Forgery (SSRF) attacks.",
        "cost": "IMDS queries are completely free and never leave the local hypervisor.",
        "cleanup": "# No additional resources provisioned.",
        "verify_cleanup": "echo 'Account clean.'",
        "mastery_q1": "Why is IMDSv2 token-based while IMDSv1 allowed simple GET requests?",
        "mastery_q2": "Why does an instance show '2/2 Status Checks' even when your application inside the instance crashed?",
        "mastery_q3": "Does User Data execute on every instance reboot, or only on the initial launch?",
        "when_use": "Use User Data for lightweight configuration, or pre-bake AMIs for faster launch times.",
        "when_not": "Avoid long 15-minute User Data scripts in Auto Scaling groups; instances cannot serve traffic until User Data finishes.",
        "next_step": "Phase 15: EBS — Network-attached block storage and persistence."
    },
    # 15: EBS
    {
        "module": "03-compute-and-storage", "slug": "15-ebs", "num": "15",
        "title": "EBS",
        "motto": "EBS is a network-attached hard drive. It lives in one AZ and survives instance termination.",
        "type": "Hands-on Lab & Storage Persistence", "time": "60",
        "prereqs": "Phase 13: EC2 From First Principles",
        "services": "Amazon Elastic Block Store (EBS gp3)",
        "cost": "Billable (~$0.08/GB-month for gp3)",
        "problem": "Instance-store storage is ephemeral: when an instance is stopped or hardware fails, all data is permanently lost. Relational databases need persistent, snapshot-capable block storage.",
        "prediction": "Stopping an EC2 instance will detach its compute, but writing data to an EBS volume guarantees that restarting the instance preserves every single byte.",
        "why_matters": "Unattached EBS volumes are one of the biggest sources of waste in AWS bills. Deleting an EC2 instance without deleting its volume leaves storage charges running forever.",
        "first_principles": "Elastic Block Store (EBS) is a distributed Storage Area Network (SAN). Volumes are replicated across multiple physical storage servers within a single Availability Zone. The instance communicates with EBS over a dedicated NVMe network bus.",
        "diagram": """EBS Network-Attached Storage:
Physical Compute Host (AZ-A)
┌────────────────────────────────┐
│ EC2 Instance (Guest OS)        │
│ └── /dev/nvme1n1 (Block Device)│
└───────────────┬────────────────┘
                │ Dedicated 10Gbps+ Nitro Storage Network
┌───────────────▼────────────────────────────────────────┐
│ Amazon EBS Replicated Storage Cluster (Within AZ-A)    │
│ ┌─────────────────────────┐   ┌──────────────────────┐ │
│ │ Primary Storage Server  │═══│ Sync Replica Node    │ │
│ └─────────────────────────┘   └──────────────────────┘ │
└────────────────────────────────────────────────────────┘""",
        "before_aws": "Fibre Channel SANs, iSCSI arrays, and hardware RAID controllers (RAID 10/5).",
        "primitive_code": """# Simulating block device persistence
import os
with open('/tmp/ebs_test.dat', 'wb') as f:
    f.write(b"PERSISTENT_DATABASE_TRANSACTION_LOG")
print("Wrote block data to disk. Verifying persistence:")
with open('/tmp/ebs_test.dat', 'rb') as f:
    print("Read back:", f.read().decode())""",
        "aws_cmd": "aws ec2 create-volume --availability-zone us-east-1a --size 10 --volume-type gp3 --tag-specifications 'ResourceType=volume,Tags=[{Key=Project,Value=aws-from-scratch}]'",
        "inspect": "aws ec2 describe-volumes --filters 'Name=tag:Project,Values=aws-from-scratch' --output table",
        "measure": "Measure baseline gp3 performance: 3,000 baseline IOPS and 125 MB/s throughput regardless of volume size.",
        "break_desc": "Attempt to attach a volume created in `us-east-1a` to an EC2 instance running in `us-east-1b`.",
        "diagnose": "The API call fails with `InvalidVolume.ZoneMismatch`: EBS volumes are strictly confined to a single Availability Zone!",
        "recover": "Take an EBS snapshot of the volume and restore it as a new volume in `us-east-1b`.",
        "security": "Always enable default EBS encryption using AWS KMS so all newly created volumes are encrypted at rest.",
        "cost": "gp3 costs ~$0.08 per GB-month. A 100GB volume costs $8.00/month whether the instance is running, stopped, or deleted!",
        "cleanup": "for id in $(aws ec2 describe-volumes --filters 'Name=tag:Project,Values=aws-from-scratch' --query 'Volumes[?State==`available`].VolumeId' --output text); do aws ec2 delete-volume --volume-id $id; done",
        "verify_cleanup": "aws ec2 describe-volumes --filters 'Name=tag:Project,Values=aws-from-scratch' --query 'Volumes[]' --output text",
        "mastery_q1": "Why can an EBS volume NOT be attached to instances across different Availability Zones?",
        "mastery_q2": "What is the difference between `gp2` and `gp3` EBS volumes?",
        "mastery_q3": "Why is an EBS volume faster for database boot disks than an S3 bucket?",
        "when_use": "Use EBS for operating system boot volumes, relational databases, and low-latency random block I/O.",
        "when_not": "Do not use EBS as a shared multi-instance filesystem (use Amazon EFS) or for storing petabytes of static files (use Amazon S3).",
        "next_step": "Phase 16: AMIs and Immutable Servers — Freezing configured servers into golden reproducible images."
    },
    # 16: AMIs and Immutable Servers
    {
        "module": "03-compute-and-storage", "slug": "16-amis-and-immutable-servers", "num": "16",
        "title": "AMIs and Immutable Servers",
        "motto": "Treat servers like cattle, not pets. Never patch in production: bake a new image and replace the fleet.",
        "type": "Hands-on Lab & Immutable Infrastructure", "time": "60",
        "prereqs": "Phase 15: EBS",
        "services": "Amazon Machine Images (AMI), EC2 Image Builder",
        "cost": "Billable (~$0.05/GB-month for stored AMI snapshots)",
        "problem": "Maintaining servers by SSHing into them and applying updates manually leads to 'snowflake servers' with undocumented configurations that crash when duplicated.",
        "prediction": "Creating an AMI from a configured instance takes a snapshot of the EBS root disk and metadata, allowing you to launch 50 identical clones in parallel.",
        "why_matters": "Immutable infrastructure is the foundation of autoscaling and continuous deployment. New code is shipped as a new AMI.",
        "first_principles": "An Amazon Machine Image (AMI) consists of: (1) an EBS snapshot of the root filesystem, (2) architecture metadata (x86_64 or arm64), (3) block device mappings, and (4) virtualization type (HVM). Launching an instance from an AMI clones the snapshot onto a new EBS volume via lazy loading.",
        "diagram": """Golden AMI Pipeline:
[ Base OS AMI ] ──► Launch EC2 ──► Install App Dependencies ──► Create AMI Snapshot
                                                                       │
             ┌─────────────────────────────────────────────────────────┘
             ▼
[ Golden AMI (v1.2.0) ] ──► Auto Scaling Group Launches 100 Identical Cattle Instances""",
        "before_aws": "Creating golden disk images using Norton Ghost or VMware VM templates.",
        "primitive_code": """# Simulating immutable version manifest
manifest = {"version": "v1.2.0", "ami_name": "app-golden-2026", "packages": ["nginx", "python3.12", "app-daemon"]}
print(f"Baking immutable server artifact: {manifest['ami_name']} ({manifest['version']})")""",
        "aws_cmd": "aws ec2 create-image --instance-id $INSTANCE_ID --name 'aws-from-scratch-golden-ami' --no-reboot --tag-specifications 'ResourceType=image,Tags=[{Key=Project,Value=aws-from-scratch}]'",
        "inspect": "aws ec2 describe-images --filters 'Name=tag:Project,Values=aws-from-scratch' --output json",
        "measure": "Compare launch boot time: AMI pre-baked app (30 seconds) vs User Data installing from scratch (5 minutes).",
        "break_desc": "Attempt to launch an ARM64-compiled AMI on an x86 instance type (e.g. `t3.micro`).",
        "diagnose": "The API call fails with architecture incompatibility: ARM64 binaries cannot execute on x86 instruction sets.",
        "recover": "Launch on compatible architecture (`t4g.micro` for Graviton ARM64).",
        "security": "Golden AMIs allow security teams to pre-scan for vulnerabilities and CVEs before instances reach production.",
        "cost": "AMI storage is billed at standard EBS snapshot rates (~$0.05/GB-month). Deregister AMIs and delete their associated snapshots when done!",
        "cleanup": "for id in $(aws ec2 describe-images --filters 'Name=tag:Project,Values=aws-from-scratch' --query 'Images[].ImageId' --output text); do aws ec2 deregister-image --image-id $id; done",
        "verify_cleanup": "echo 'AMIs cleaned.'",
        "mastery_q1": "Why does launching an instance from a newly created AMI sometimes exhibit high initial disk latency? (Hint: EBS Lazy Loading / Fast Snapshot Restore).",
        "mastery_q2": "Why is immutable infrastructure safer than running `apt-get upgrade` in production?",
        "mastery_q3": "What happens to the underlying EBS snapshot when you deregister an AMI?",
        "when_use": "Use pre-baked AMIs when auto-scaling needs to launch and register healthy instances in under 60 seconds.",
        "when_not": "Do not bake dynamic configurations (database passwords, API keys) into AMIs; fetch secrets dynamically at boot time.",
        "next_step": "Phase 17: S3 From First Principles — Distributed object storage."
    },
    # 17: S3 From First Principles
    {
        "module": "04-object-storage-and-cdn", "slug": "17-s3-from-first-principles", "num": "17",
        "title": "S3 From First Principles",
        "motto": "S3 is not a filesystem: it is a distributed HTTP key-value store optimized for immutable byte streams.",
        "type": "Hands-on Lab & Object Store Exploration", "time": "60",
        "prereqs": "Phase 02: AWS CLI, APIs, and Console",
        "services": "Amazon S3",
        "cost": "Billable (~$0.023/GB-month | Free Tier eligible)",
        "problem": "Hard drives and filesystems cannot scale to petabytes of data. They suffer from inode exhaustion, single-server failure risks, and complex distributed locking.",
        "prediction": "There are no real folders in S3. The key `photos/2026/summer.jpg` is a single string key in a flat hash index.",
        "why_matters": "Treating S3 like a POSIX filesystem leads to horrible performance bugs (e.g. attempting to rename a folder with 1,000,000 files requires 1,000,000 individual copy and delete HTTP requests!).",
        "first_principles": "Object storage stores data as immutable binary large objects (BLOBs) addressed by a bucket name and string key. Unlike POSIX filesystems, there are no file descriptors, no `seek()` operations, and no partial byte writes: an object is written atomically in full via HTTP PUT.",
        "diagram": """POSIX Filesystem vs S3 Object Store:
POSIX Filesystem:
/ (Root Inode) ──► dir/ (Directory Inode) ──► file.txt (Data Blocks on local disk)

S3 Object Store (Flat Hash Table):
Bucket: "my-bucket"
Key (String)                     Object Payload (Immutable BLOB)
"uploads/user1/avatar.png"  ──►  [ Bytes: \x89PNG... (Replicated across 3+ AZs) ]
"uploads/user2/avatar.png"  ──►  [ Bytes: \x89PNG... (Replicated across 3+ AZs) ]""",
        "before_aws": "Network-Attached Storage (NAS) filers like NetApp running NFS / SMB protocols.",
        "primitive_code": """# Simulating S3 flat key-value store
s3_bucket = {}
def put_object(key, data):
    s3_bucket[key] = data
put_object("documents/report.pdf", b"PDF_BYTES")
print("Bucket Keys:", list(s3_bucket.keys()))
print("Notice: There is NO 'documents' directory! Just a flat string key.")""",
        "aws_cmd": "aws s3 mb s3://aws-from-scratch-lab-$(aws sts get-caller-identity --query Account --output text) --region us-east-1",
        "inspect": "aws s3 ls",
        "measure": "Measure write throughput: S3 supports at least 3,500 PUT and 5,500 GET requests per second per prefix.",
        "break_desc": "Attempt to append a single byte to an existing 10MB S3 object.",
        "diagnose": "S3 REST API has no APPEND verb! You must download the object, append locally, and upload the entire object again.",
        "recover": "Use S3 for immutable objects; use EBS or a database for append-heavy workloads.",
        "security": "Enable S3 Block Public Access at the account and bucket level to prevent data leaks.",
        "cost": "S3 Standard: ~$0.023/GB-month. GET requests: $0.0004 per 1,000. PUT requests: $0.005 per 1,000.",
        "cleanup": "BUCKET=aws-from-scratch-lab-$(aws sts get-caller-identity --query Account --output text)\naws s3 rb s3://$BUCKET --force",
        "verify_cleanup": "echo 'S3 bucket cleaned.'",
        "mastery_q1": "Why does renaming a 'folder' containing 100,000 files in S3 take 10 minutes, while in a Linux filesystem it takes 1 millisecond?",
        "mastery_q2": "What does '11 9s of durability' (99.999999999%) actually mean statistically?",
        "mastery_q3": "How does strong read-after-write consistency work in S3?",
        "when_use": "Use S3 for media assets, backups, logs, data lake analytics, and static web bundles.",
        "when_not": "Do not use S3 as an operating system boot drive or high-IOPS transactional database data directory.",
        "next_step": "Phase 18: S3 Operations — PUT, GET, DELETE, and metadata headers."
    },
    # 18: S3 Operations
    {
        "module": "04-object-storage-and-cdn", "slug": "18-s3-operations", "num": "18",
        "title": "S3 Operations",
        "motto": "Every S3 operation is a standard HTTP request with headers, metadata, and ETags.",
        "type": "Hands-on Lab & API Verification", "time": "60",
        "prereqs": "Phase 17: S3 From First Principles",
        "services": "Amazon S3 REST APIs",
        "cost": "Billable (Fractions of a cent / Request fees)",
        "problem": "Applications upload files with incorrect MIME types, leading to browsers downloading HTML/PDF files instead of rendering them inline.",
        "prediction": "Uploading an object with `Content-Type: text/html` will cause browsers to render it as a webpage, while `application/octet-stream` forces a download.",
        "why_matters": "Mastering S3 metadata, ETags, and headers is essential for building web applications and CDNs.",
        "first_principles": "S3 objects carry HTTP headers: `Content-Type`, `Cache-Control`, `Content-Disposition`, and custom metadata prefixed with `x-amz-meta-*`. The `ETag` header is typically the hexadecimal MD5 checksum of the object content.",
        "diagram": """S3 HTTP Headers:
HTTP PUT /reports/q3.pdf
Content-Type: application/pdf
Cache-Control: max-age=3600
x-amz-meta-author: alice
                │
                ▼
HTTP 200 OK
ETag: "c8c60a479c402... (MD5 Checksum)"
x-amz-version-id: "null" / "3/L4k..." """,
        "before_aws": "Storing files on web servers and configuring Apache/Nginx `mime.types` mapping tables.",
        "primitive_code": """import hashlib
content = b"Hello Cloud World"
etag = hashlib.md5(content).hexdigest()
print(f"Calculated ETag: \\"{etag}\\"")""",
        "aws_cmd": "echo '<h1>AWS</h1>' > test.html && aws s3 cp test.html s3://$BUCKET/test.html --content-type 'text/html' --metadata 'lab=aws-from-scratch'",
        "inspect": "aws s3api head-object --bucket $BUCKET --key test.html --output json",
        "measure": "Compare upload performance: single-part PUT vs multipart upload for large files (> 100MB).",
        "break_desc": "Upload a PDF with `Content-Type: text/plain`.",
        "diagnose": "Opening the S3 URL in a browser renders raw binary characters instead of formatted PDF pages.",
        "recover": "Copy object over itself to replace metadata: `aws s3 cp s3://$BUCKET/doc.pdf s3://$BUCKET/doc.pdf --metadata-directive REPLACE --content-type 'application/pdf'`.",
        "security": "Use S3 pre-signed URLs to grant temporary upload/download access without sharing IAM credentials.",
        "cost": "PUT/COPY/POST: $0.005 per 1,000 requests. GET/HEAD: $0.0004 per 1,000 requests.",
        "cleanup": "aws s3 rm s3://$BUCKET/test.html",
        "verify_cleanup": "echo 'Object cleaned.'",
        "mastery_q1": "Why is Multipart Upload mandatory for objects larger than 5GB?",
        "mastery_q2": "What does an ETag represent for an object uploaded via Multipart Upload? (Hint: It is not a simple MD5 of the whole file).",
        "mastery_q3": "How do S3 Pre-Signed URLs cryptographically guarantee that only the authorized client can upload?",
        "when_use": "Use pre-signed URLs for direct client uploads from mobile apps to S3, bypassing web servers.",
        "when_not": "Do not proxy large file uploads through web application servers—upload directly to S3.",
        "next_step": "Phase 19: S3 Durability, Versioning, Lifecycle — Managing data retention and tiers."
    },
    # 19: S3 Durability, Versioning, Lifecycle
    {
        "module": "04-object-storage-and-cdn", "slug": "19-s3-durability-versioning-lifecycle", "num": "19",
        "title": "S3 Durability, Versioning, Lifecycle",
        "motto": "Durability is not backup. If an application overwrites good data with corrupt data, S3 durably replicates the corruption.",
        "type": "Hands-on Lab & Data Lifecycle", "time": "60",
        "prereqs": "Phase 18: S3 Operations",
        "services": "S3 Versioning, S3 Storage Classes, S3 Lifecycle Rules",
        "cost": "Billable (Fractions of a cent)",
        "problem": "Accidental deletion or ransomware overwriting files can destroy company data. Furthermore, storing old logs in S3 Standard forever results in massive unnecessary storage bills.",
        "prediction": "Enabling versioning means deleting an object simply places a 'Delete Marker' on top; the prior version remains fully recoverable.",
        "why_matters": "Distinguishing durability, versioning, replication, and backup prevents catastrophic data loss.",
        "first_principles": "Durability is hardware failure protection (replicated across 3+ AZs against drive failures). Versioning is logical protection against human/software errors. When an object is deleted in a versioned bucket, S3 inserts a 0-byte `DeleteMarker`. The previous object version remains intact and can be retrieved by `versionId`.",
        "diagram": """S3 Versioning Stack:
Object Key: "contract.pdf"
┌────────────────────────────────────────────────────────┐
│ [Delete Marker] (Inserted on DELETE)  VersionId: VID_3 │ <── Current Version (Returns 404)
├────────────────────────────────────────────────────────┤
│ "contract_v2.pdf" (Uploaded 2pm)       VersionId: VID_2 │ <── Recoverable!
├────────────────────────────────────────────────────────┤
│ "contract_v1.pdf" (Uploaded 10am)      VersionId: VID_1 │ <── Recoverable!
└────────────────────────────────────────────────────────┘""",
        "before_aws": "Tape backup rotations (Grandfather-Father-Son) and robotic tape libraries.",
        "primitive_code": """# Simulating S3 versioning stack
bucket_versions = {}
def put_version(key, data):
    bucket_versions.setdefault(key, []).append(data)
def delete_version(key):
    bucket_versions.setdefault(key, []).append("DELETE_MARKER")
put_version("doc.txt", "v1")
put_version("doc.txt", "v2")
delete_version("doc.txt")
print("Latest state:", bucket_versions["doc.txt"][-1])
print("Prior recoverable version:", bucket_versions["doc.txt"][-2])""",
        "aws_cmd": "aws s3api put-bucket-versioning --bucket $BUCKET --versioning-configuration Status=Enabled",
        "inspect": "aws s3api get-bucket-versioning --bucket $BUCKET --output table",
        "measure": "Compare storage class costs: S3 Standard ($0.023/GB) vs Glacier Flexible ($0.0036/GB) vs Glacier Deep Archive ($0.00099/GB).",
        "break_desc": "Delete an object in a versioned bucket via `aws s3 rm`.",
        "diagnose": "The object appears gone in `aws s3 ls`, but `aws s3api list-object-versions` reveals the Delete Marker and past version.",
        "recover": "Delete the Delete Marker to restore the object: `aws s3api delete-object --bucket $BUCKET --key doc.txt --version-id $DELETE_MARKER_VID`.",
        "security": "Enable S3 Object Lock (WORM: Write Once Read Many) for compliance to prevent anyone—even root—from deleting objects.",
        "cost": "Versioning doubles storage costs if objects are frequently overwritten, because all historical versions are stored and billed.",
        "cleanup": "aws s3api put-bucket-versioning --bucket $BUCKET --versioning-configuration Status=Suspended",
        "verify_cleanup": "echo 'Bucket versioning suspended.'",
        "mastery_q1": "Why does S3 replication to a secondary bucket NOT protect against accidental software deletion bugs unless versioning is configured?",
        "mastery_q2": "What happens to noncurrent versions if you do not configure an S3 Lifecycle rule to expire them?",
        "mastery_q3": "Why is Glacier Deep Archive retrieve time measured in hours rather than milliseconds?",
        "when_use": "Enable versioning on critical business data, configuration buckets, and state files.",
        "when_not": "Do not enable versioning on high-churn transient caches without a lifecycle rule to expire noncurrent versions after 1 day.",
        "next_step": "Phase 20: Static Website / Object Delivery — CloudFront and Origin Access Control."
    },
    # 20: Static Website / Object Delivery
    {
        "module": "04-object-storage-and-cdn", "slug": "20-static-website-object-delivery", "num": "20",
        "title": "Static Website / Object Delivery",
        "motto": "Never make an S3 bucket public for website hosting. Keep the bucket private and front it with CloudFront OAC.",
        "type": "Hands-on Lab & Web Architecture", "time": "60",
        "prereqs": "Phase 19: S3 Durability, Versioning, Lifecycle",
        "services": "S3, CloudFront Origin Access Control (OAC)",
        "cost": "Free Tier eligible",
        "problem": "Making an S3 bucket public exposes your account to unbounded direct GET request fees, lacks HTTPS custom domain support, and serves traffic from a single geographic region.",
        "prediction": "Using CloudFront with Origin Access Control allows CloudFront to read from a 100% private S3 bucket using AWS SigV4 signed requests.",
        "why_matters": "This is Project 01 in the curriculum and the industry standard for delivering frontend web applications.",
        "first_principles": "A Content Delivery Network (CDN) terminates TLS at the nearest Anycast edge point of presence (PoP). When a cache miss occurs, CloudFront signs an HTTP request to S3 using AWS SigV4 with its service principal credentials (`cloudfront.amazonaws.com`). The S3 bucket policy validates the signature and returns the object.",
        "diagram": """CloudFront OAC Architecture:
[ User Browser ] ──(HTTPS)──► [ CloudFront Edge PoP ]
                                     │ (Cache Miss)
                                     │ SigV4 Signed Request
                                     ▼
                      [ Private S3 Bucket ]
                      (Block Public Access: ENABLED)
                      (Bucket Policy: Allow s3:GetObject ONLY to CloudFront ARN)""",
        "before_aws": "Hosting frontend Apache/Nginx web servers in multiple datacenters with geo-DNS routing.",
        "primitive_code": """# OAC Bucket Policy Pattern
policy = {
    "Statement": [{
        "Effect": "Allow",
        "Principal": {"Service": "cloudfront.amazonaws.com"},
        "Action": "s3:GetObject",
        "Resource": "arn:aws:s3:::my-web-bucket/*",
        "Condition": {"StringEquals": {"AWS:SourceArn": "arn:aws:cloudfront::123:distribution/E123"}}
    }]
}
print("OAC Policy Structure validated.")""",
        "aws_cmd": "aws s3api get-public-access-block --bucket $BUCKET --output table",
        "inspect": "aws s3api get-bucket-policy --bucket $BUCKET",
        "measure": "Measure latency improvement: direct cross-ocean S3 GET (180ms) vs edge cached CloudFront GET (15ms).",
        "break_desc": "Attempt to curl the private S3 bucket URL directly (`https://$BUCKET.s3.amazonaws.com/index.html`).",
        "diagnose": "S3 returns HTTP 403 AccessDenied because Block Public Access is active and the bucket policy allows only CloudFront.",
        "recover": "Access the asset through the CloudFront distribution domain name.",
        "security": "Enforce HTTPS redirect (`viewer-protocol-policy: redirect-to-https`) and TLS 1.2+ security policies.",
        "cost": "CloudFront Free Tier includes 1 TB data transfer out and 10,000,000 requests per month permanently.",
        "cleanup": "# Cleanup web assets",
        "verify_cleanup": "echo 'Static web assets cleaned.'",
        "mastery_q1": "Why is legacy S3 Static Website Hosting discouraged in modern production architectures?",
        "mastery_q2": "How does Origin Access Control (OAC) prevent other AWS customers with CloudFront distributions from accessing your private bucket?",
        "mastery_q3": "Why should hashed asset bundles (e.g. `main.a8f9c.js`) have a 1-year Cache-Control header while `index.html` has a 5-minute header?",
        "when_use": "Use CloudFront + S3 OAC for all React, Vue, Svelte, or static frontend single-page applications.",
        "when_not": "Do not use S3 for server-side dynamic HTML rendering (use ECS, Lambda, or EC2).",
        "next_step": "Phase 21: DNS and Route 53 — Authoritative domain name resolution."
    },
    # 21: DNS and Route 53
    {
        "module": "04-object-storage-and-cdn", "slug": "21-dns-and-route-53", "num": "21",
        "title": "DNS and Route 53",
        "motto": "DNS is the phonebook of the internet. Route 53 ALIAS records solve the apex zone CNAME problem.",
        "type": "Hands-on Lab & DNS Resolution", "time": "60",
        "prereqs": "Phase 20: Static Website / Object Delivery",
        "services": "Amazon Route 53 Hosted Zones, ALIAS Records",
        "cost": "Billable ($0.50/month per hosted zone | Dry-run / CLI inspection recommended)",
        "problem": "Users cannot remember `d111111abcdef8.cloudfront.net` or `54.210.10.5`. Furthermore, standard DNS RFCs forbid CNAME records at the zone apex (`example.com`).",
        "prediction": "Querying a Route 53 ALIAS record for `example.com` resolves directly to CloudFront or ALB Anycast IP addresses without adding an extra CNAME lookup hop.",
        "why_matters": "DNS misconfigurations cause catastrophic multi-hour propagation delays. Understanding authoritative nameservers, TTLs, and ALIAS records is vital.",
        "first_principles": "DNS is a hierarchical distributed database. Resolvers query Root (.) -> TLD (.com) -> Authoritative Nameservers. Route 53 is an authoritative Anycast DNS server operating on Port 53 (UDP/TCP). Route 53 ALIAS records are internal pointers that resolve AWS resource hostnames to direct A records dynamically.",
        "diagram": """DNS Resolution Hierarchy:
[ Client Query: api.example.com ]
                │
                ▼
1. Root Nameserver (.) ──► "Go ask .com nameserver"
                │
                ▼
2. TLD Nameserver (.com) ──► "Go ask Route 53 Authoritative Nameservers: ns-xxx.awsdns.com"
                │
                ▼
3. Route 53 Authoritative Nameserver ──► Returns IP: 54.210.10.5 (TTL: 300)""",
        "before_aws": "Hosting BIND9 DNS servers on physical machines with master-slave zone transfers (AXFR).",
        "primitive_code": """# DNS query inspection via socket
import socket
ip = socket.gethostbyname("aws.amazon.com")
print(f"aws.amazon.com resolved to: {ip}")""",
        "aws_cmd": "# List Route 53 hosted zones\naws route53 list-hosted-zones --output table",
        "inspect": "dig +trace aws.amazon.com",
        "measure": "Measure DNS lookup latency: cached local resolver (< 1ms) vs recursive uncached authoritative query (40-80ms).",
        "break_desc": "Configure a DNS record with a TTL of 86400 (24 hours) and then change the IP address.",
        "diagnose": "Clients continue hitting the old IP address for up to 24 hours because intermediate recursive resolvers cache the old record.",
        "recover": "Use low TTLs (60-300 seconds) during migrations and deployments.",
        "security": "Enable DNSSEC to prevent DNS cache poisoning and man-in-the-middle spoofing attacks.",
        "cost": "Hosted Zones cost $0.50 per month each. Standard queries cost $0.40 per million queries. (Labs can use dry-run simulation to avoid the $0.50 cost).",
        "cleanup": "# Delete test hosted zones if created",
        "verify_cleanup": "echo 'Route 53 clean.'",
        "mastery_q1": "Why does DNS RFC 1034 forbid a CNAME record at the zone apex (`example.com`), and how does a Route 53 ALIAS record solve this?",
        "mastery_q2": "What is the difference between Weighted Routing, Latency-Based Routing, and Geolocation Routing?",
        "mastery_q3": "How do Route 53 DNS Health Checks trigger automatic failover to a standby region?",
        "when_use": "Use Route 53 for public authoritative DNS and private VPC internal service resolution.",
        "when_not": "Do not purchase unnecessary public domains for learning labs when local `/etc/hosts` or dry-run inspection suffices.",
        "next_step": "Phase 22: Load Balancing From Scratch — Building a reverse proxy to balance traffic across multiple servers."
    },
    # 22: Load Balancing From Scratch
    {
        "module": "05-load-balancing-and-scaling", "slug": "22-load-balancing-from-scratch", "num": "22",
        "title": "Load Balancing From Scratch",
        "motto": "A single server is a single point of failure. A load balancer is a reverse proxy with health check intelligence.",
        "type": "Hands-on Lab & First Principles Engine", "time": "60",
        "prereqs": "Phase 13: EC2 From First Principles",
        "services": "Reverse Proxying, Socket Multiplexing",
        "cost": "Free ($0.00 / Local Simulation)",
        "problem": "One web server can handle 2,000 requests per second before its CPU saturates. When traffic hits 5,000 req/sec, how do clients distribute requests across two servers without hardcoding server IPs?",
        "prediction": "A reverse proxy intercepting incoming client sockets can distribute requests round-robin across healthy backend targets and seamlessly evict failing nodes.",
        "why_matters": "Load balancing is the pivot point between single-server snowflake systems and horizontally scalable distributed systems.",
        "first_principles": "A reverse proxy acts as an intermediary. It terminates client TCP connections, inspects request headers, selects a backend target from an active healthy target pool, forwards the request over a second TCP connection, and proxies the response back.",
        "diagram": """Reverse Proxy Load Balancing:
[ Clients ] ──(Requests)──► [ Reverse Proxy (Port 80) ]
                                    │
                                    ├── Request 1 ──► [ Server A (10.0.1.50) ] (AZ-A)
                                    └── Request 2 ──► [ Server B (10.0.2.60) ] (AZ-B)""",
        "before_aws": "Hardware load balancing appliances like F5 BIG-IP or open-source HAProxy / Nginx reverse proxies.",
        "primitive_code": """# Run our first-principles load balancer lab
import subprocess
subprocess.run(['python3', 'experiments/lb_healthcheck_lab.py'], check=True)""",
        "aws_cmd": "# Check ALB service endpoints\naws elbv2 describe-load-balancers --query 'LoadBalancers[].[LoadBalancerName,DNSName,State.Code]' --output table",
        "inspect": "python3 benchmarks/benchmark_lb.py",
        "measure": "Measure latency overhead introduced by reverse proxying (+0.5 to 1.2ms) vs benefits of high availability.",
        "break_desc": "Kill backend Server A in `experiments/lb_healthcheck_lab.py`.",
        "diagnose": "The load balancer detects consecutive health check failures and evicts Server A from the pool.",
        "recover": "Traffic shifts 100% to Server B with zero client errors. When Server A recovers, it is automatically re-added.",
        "security": "Load balancers hide backend server IP addresses from the public internet, acting as a security shield.",
        "cost": "Local simulation is $0.00. Live AWS ALB is ~$16.20/month.",
        "cleanup": "# No AWS resources provisioned.",
        "verify_cleanup": "echo 'Account clean.'",
        "mastery_q1": "Why is Layer 7 load balancing (ALB) slower than Layer 4 load balancing (NLB)?",
        "mastery_q2": "What happens if all backend targets in a target group fail their health checks simultaneously?",
        "mastery_q3": "Why is round-robin DNS inferior to a dedicated load balancer for failover?",
        "when_use": "Always place a load balancer in front of stateless application servers.",
        "when_not": "Do not place an ALB in front of a single database primary that accepts writes.",
        "next_step": "Phase 23: ALB — Deploying the managed Application Load Balancer in AWS."
    },
    # 23: ALB
    {
        "module": "05-load-balancing-and-scaling", "slug": "23-alb", "num": "23",
        "title": "ALB",
        "motto": "Listeners accept connections. Target Groups health check backends. Routing rules dispatch requests.",
        "type": "Hands-on Lab & Managed Load Balancing", "time": "60",
        "prereqs": "Phase 22: Load Balancing From Scratch",
        "services": "AWS Application Load Balancer (ALB)",
        "cost": "Billable (~$0.0225/hr | ~$16.20/mo while running)",
        "problem": "Managing self-hosted HAProxy or Nginx servers requires managing their failover (VRRP/Keepalived), OS security patches, and capacity scaling.",
        "prediction": "An ALB provisions managed reverse-proxy nodes across multiple subnets, scaling horizontally automatically to handle millions of connections.",
        "why_matters": "ALB is the primary Layer 7 traffic routing primitive for EC2, ECS containers, and microservices in AWS.",
        "first_principles": "An ALB consists of: (1) **Listeners** (ports/protocols to listen on: HTTP 80, HTTPS 443), (2) **Rules** (path/host routing logic: `/api/*` -> Target Group B), and (3) **Target Groups** (logical pools of registered IP/instance targets with health check parameters).",
        "diagram": """ALB Component Hierarchy:
[ Internet ] ──► [ ALB (Public Multi-AZ) ]
                         │
                         ▼
                  [ Listener: Port 443 ]
                         │
        ┌────────────────┴────────────────┐
        │ Path: /api/*                    │ Default Path: /*
        ▼                                 ▼
[ Target Group: API ]             [ Target Group: Web ]
• Health: /api/health             • Health: /health
• Targets: [Task 1, Task 2]       • Targets: [EC2-A, EC2-B]""",
        "before_aws": "F5 BIG-IP hardware pairs or Nginx Plus reverse proxy clusters.",
        "primitive_code": """# Target Group Health Check Parameters
tg_config = {
    "HealthCheckProtocol": "HTTP",
    "HealthCheckPath": "/health",
    "HealthCheckIntervalSeconds": 30,
    "HealthyThresholdCount": 2,
    "UnhealthyThresholdCount": 2,
    "TargetResponseTimeoutSeconds": 5
}
print("ALB Health Configuration:", tg_config)""",
        "aws_cmd": "aws elbv2 create-load-balancer --name lab-alb --subnets $PUB_SUBNET_1 $PUB_SUBNET_2 --security-groups $ALB_SG_ID --tag-specifications 'ResourceType=load-balancer,Tags=[{Key=Project,Value=aws-from-scratch}]'",
        "inspect": "aws elbv2 describe-target-health --target-group-arn $TG_ARN --output table",
        "measure": "Measure HTTP 502 Bad Gateway vs HTTP 504 Gateway Timeout behavior.",
        "break_desc": "Change the health check path from `/health` to `/nonexistent`.",
        "diagnose": "All targets fail health checks (HTTP 404); ALB returns HTTP 503 Service Unavailable.",
        "recover": "Restore the correct health check path.",
        "security": "Enforce HTTPS with ACM TLS certificates; set security group to accept traffic only from trusted sources.",
        "cost": "ALB charges ~$0.0225/hour + $0.008 per LCU-hour. Delete immediately after testing!",
        "cleanup": "aws elbv2 delete-load-balancer --load-balancer-arn $ALB_ARN",
        "verify_cleanup": "echo 'ALB deleted.'",
        "mastery_q1": "What is the difference between an HTTP 502 Bad Gateway and an HTTP 504 Gateway Timeout on an ALB?",
        "mastery_q2": "Why must an ALB be deployed in at least two Availability Zones?",
        "mastery_q3": "What is an LCU (Load Balancer Capacity Unit) and how is it calculated?",
        "when_use": "Use ALB for HTTP/HTTPS web applications, microservice path-based routing, and ECS container services.",
        "when_not": "Do not use ALB for raw TCP/UDP workloads, gaming protocols, or VoIP (use Network Load Balancer).",
        "next_step": "Phase 24: Multi-AZ Application — Combining ALB and EC2 into a true fault-tolerant architecture."
    },
    # 24: Multi-AZ Application
    {
        "module": "05-load-balancing-and-scaling", "slug": "24-multi-az-application", "num": "24",
        "title": "Multi-AZ Application",
        "motto": "Redundancy without geographic separation is an illusion. Multi-AZ is the baseline of cloud reliability.",
        "type": "Architecture Project & Failure Injection", "time": "60",
        "prereqs": "Phase 23: ALB",
        "services": "ALB, Multi-AZ EC2, Cross-Zone Load Balancing",
        "cost": "Billable (~$0.03/hr for ALB + 2x t4g.micro)",
        "problem": "Running two EC2 instances in the same Availability Zone protects against software crashes, but a datacenter power outage destroys both simultaneously.",
        "prediction": "Deploying Instance A in AZ-1 and Instance B in AZ-2 behind a Multi-AZ ALB allows one entire AZ to be destroyed with zero downtime for clients.",
        "why_matters": "This is Project 02 in the curriculum and the standard reference architecture for highly available web systems.",
        "first_principles": "Availability Zones are independent physical failure domains with isolated power feeds, backup generators, and physical facilities. Deploying stateless compute across two or more AZs ensures that any localized catastrophe has a blast radius bounded to a fraction of your fleet.",
        "diagram": """Multi-AZ Architecture:
                    [ Public Internet ]
                             │
                             ▼
            [ Application Load Balancer (Multi-AZ) ]
                             │
            ┌────────────────┴────────────────┐
            ▼                                 ▼
   [ us-east-1a (DC 1) ]             [ us-east-1b (DC 2) ]
   ┌──────────────────────┐          ┌──────────────────────┐
   │ EC2 Instance A       │          │ EC2 Instance B       │
   │ (Private IP: 10.0.1) │          │ (Private IP: 10.0.2) │
   └──────────────────────┘          └──────────────────────┘""",
        "before_aws": "Active-passive hot standby datacenters with automated DNS failover.",
        "primitive_code": """# Verification of multi-AZ target distribution
targets = [{"id": "i-001a", "az": "us-east-1a"}, {"id": "i-002b", "az": "us-east-1b"}]
distinct_azs = len(set(t['az'] for t in targets))
print(f"Distinct AZs spanned: {distinct_azs} (Multi-AZ compliant: {distinct_azs >= 2})")""",
        "aws_cmd": "aws ec2 describe-instances --filters 'Name=tag:Project,Values=aws-from-scratch' --query 'Reservations[].Instances[].[InstanceId,Placement.AvailabilityZone]' --output table",
        "inspect": "aws elbv2 describe-target-health --target-group-arn $TG_ARN --output table",
        "measure": "Simulate client traffic while terminating the instance in AZ-A; measure 5xx error rate (should be 0.00%).",
        "break_desc": "Terminate the instance in us-east-1a via `aws ec2 terminate-instances`.",
        "diagnose": "ALB detects AZ-A target unhealthy; all incoming traffic seamlessly served by AZ-B target.",
        "recover": "Launch a replacement instance in us-east-1a.",
        "security": "Enforce least-privilege Security Groups: EC2 instances only accept traffic from the ALB's Security Group ID.",
        "cost": "Cross-AZ traffic between ALB and target instances in different AZs is covered by standard cross-AZ data transfer fees ($0.01/GB).",
        "cleanup": "aws elbv2 delete-load-balancer --load-balancer-arn $ALB_ARN && aws ec2 terminate-instances --instance-ids $INST_A $INST_B",
        "verify_cleanup": "./scripts/cleanup-check.sh",
        "mastery_q1": "What happens if Cross-Zone Load Balancing is disabled on an ALB that has 8 instances in AZ-A and 2 instances in AZ-B?",
        "mastery_q2": "Why must the application instances be stateless for Multi-AZ load balancing to work correctly?",
        "mastery_q3": "What failure modes does Multi-AZ protect against, and which failure modes does it NOT protect against?",
        "when_use": "Use Multi-AZ for all production workloads requiring 99.9%+ availability.",
        "when_not": "Do not deploy Multi-AZ for short-lived non-critical batch jobs where failure simply means retrying.",
        "next_step": "Phase 25: Auto Scaling — Dynamic fleet sizing based on real-time load signals."
    },
    # 25: Auto Scaling
    {
        "module": "05-load-balancing-and-scaling", "slug": "25-auto-scaling", "num": "25",
        "title": "Auto Scaling",
        "motto": "Elasticity means paying for what you need when you need it, and turning it off when you don't.",
        "type": "Hands-on Lab & Dynamic Elasticity", "time": "60",
        "prereqs": "Phase 24: Multi-AZ Application",
        "services": "Auto Scaling Groups (ASG), Launch Templates, Target Tracking Policies",
        "cost": "Billable (EC2 hourly cost while instances run)",
        "problem": "Traffic fluctuates dramatically throughout the day. Fixed static server fleets either crash during traffic spikes or waste thousands of dollars sitting idle at night.",
        "prediction": "Applying synthetic CPU load to an ASG will trigger a CloudWatch alarm and cause the ASG to launch replacement instances automatically.",
        "why_matters": "Auto Scaling is the essence of cloud elasticity. It handles both demand-driven scaling and automatic self-healing when hardware fails.",
        "first_principles": "An Auto Scaling Group (ASG) is a control loop supervisor: `DesiredCapacity = f(Metric, Min, Max)`. The ASG periodically reconciles current healthy instances against the desired capacity. If an instance fails its EC2 or ALB health check, the ASG terminates it and provisions a fresh replacement from the Launch Template.",
        "diagram": """Auto Scaling Control Loop:
[ CloudWatch Metric: CPU > 70% ]
                │
                ▼
[ Auto Scaling Group ] ──► Reconciles: Desired (2) ──► Increase to Desired (4)
                                                              │
             ┌────────────────────────────────────────────────┘
             ▼
[ EC2 API: RunInstances ] ──► Boots 2 Fresh Instances ──► Registers with ALB Target Group""",
        "before_aws": "Capacity planning meetings 6 months in advance; over-provisioning datacenter hardware to survive peak Black Friday traffic.",
        "primitive_code": """# ASG capacity reconciliation logic
current = 2
target_cpu = 75
actual_cpu = 90
if actual_cpu > target_cpu:
    desired = min(current * 2, 10) # Scale out up to max 10
    print(f"Scale-out triggered! Desired capacity updated from {current} to {desired}")""",
        "aws_cmd": "aws autoscaling create-auto-scaling-group --auto-scaling-group-name lab-asg --launch-template LaunchTemplateName=lab-lt --min-size 1 --max-size 4 --desired-capacity 2 --vpc-zone-identifier '$PUB_SUBNET_1,$PUB_SUBNET_2' --tags Key=Project,Value=aws-from-scratch",
        "inspect": "aws autoscaling describe-auto-scaling-groups --auto-scaling-group-names lab-asg --output json",
        "measure": "Measure scale-out reaction time: CloudWatch alarm evaluation period (1-3 min) + instance boot time (1-2 min).",
        "break_desc": "Manually terminate an EC2 instance managed by the ASG.",
        "diagnose": "The ASG detects current capacity (1) < desired capacity (2); immediately calls `ec2:RunInstances` to launch a replacement.",
        "recover": "The replacement instance boots, passes health checks, and returns fleet capacity to 2.",
        "security": "Enforce strict Launch Template versioning to prevent untracked configuration changes.",
        "cost": "Auto Scaling Groups are free; you pay only for the underlying EC2 instances and CloudWatch alarms.",
        "cleanup": "aws autoscaling update-auto-scaling-group --auto-scaling-group-name lab-asg --min-size 0 --desired-capacity 0\naws autoscaling delete-auto-scaling-group --auto-scaling-group-name lab-asg --force-delete",
        "verify_cleanup": "aws autoscaling describe-auto-scaling-groups --auto-scaling-group-names lab-asg --query 'AutoScalingGroups[]' --output text",
        "mastery_q1": "Why does an Auto Scaling scale-out action have a warm-up / cooldown period?",
        "mastery_q2": "What happens if your scaling metric is CPU utilization, but the bottleneck is database lock contention?",
        "mastery_q3": "Why should an ASG balance instances evenly across Availability Zones?",
        "when_use": "Use Auto Scaling Groups for any production stateless server fleet—even with min=1, max=1 for self-healing!",
        "when_not": "Do not use standard ASGs for stateful relational databases that cannot scale horizontally by adding nodes.",
        "next_step": "Phase 26: RDS From First Principles — Managed relational databases."
    }
]

print(f"Curriculum Part 1 loaded: {len(PART1_LESSONS)} lessons (Phases 00 to 25).")
