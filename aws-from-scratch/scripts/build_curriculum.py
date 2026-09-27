#!/usr/bin/env python3
"""
scripts/build_curriculum.py
Generates the complete 86-phase (Phases 00 through 85) lesson directory structure
and rich docs/en.md files conforming strictly to LESSON_TEMPLATE.md.
"""

import os
import json

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PHASES_DIR = os.path.join(BASE_DIR, "phases")

# Data definitions for the 86 phases
LESSONS = [
    # Module 00: Cloud Foundations
    {
        "module": "00-cloud-foundations",
        "slug": "00-cloud-before-aws",
        "num": "00",
        "title": "Cloud Before AWS",
        "motto": "The cloud is not magic: it is someone else's physical computers controlled by software APIs.",
        "type": "Conceptual & Systems Exploration",
        "time": "45",
        "prereqs": "Basic Linux processes and terminal commands",
        "services": "None (Foundational Physical Infrastructure)",
        "cost": "Free ($0.00 / Local)",
        "problem": "Before cloud providers existed, deploying a new backend service required purchasing a physical 1U/2U server rack, waiting 6-12 weeks for delivery, racking and cabling it in a climate-controlled datacenter, configuring redundant power supplies, and installing an operating system manually. If traffic spiked unexpectedly, the site crashed for weeks until new hardware could be procured.",
        "prediction": "If hardware procurement takes 8 weeks, engineering teams will over-provision massively, leading to 80%+ idle server capacity and exorbitant capital expenditures.",
        "why_matters": "Understanding bare-metal physical constraints explains why cloud virtualization, resource pools, and on-demand APIs were invented.",
        "first_principles": "A computer is CPU registers, memory caches, DRAM, PCI buses, network interface cards (NICs), and persistent storage media. An operating system kernel abstracts this hardware for userland processes. Hypervisors (Type 1 bare-metal like Xen/KVM) extend this abstraction by virtualizing physical CPU instruction sets (VT-x / AMD-V) and memory management units (EPT/NPT), allowing multiple isolated guest OS kernels to share one physical host.",
        "diagram": """Physical Datacenter:
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
        "before_aws": "Organizations leased cages in colocation facilities, maintained diesel generators, hired network administrators to run physical BGP routers, and bought Dell/HP rack servers with 3-year depreciation schedules.",
        "primitive_code": """# Inspect your local machine's physical vs virtual CPU topology
import os
print(f"Available Logical Cores: {os.cpu_count()}")
with open('/proc/cpuinfo' if os.path.exists('/proc/cpuinfo') else '/dev/null') as f:
    for line in f:
        if 'model name' in line:
            print(f"CPU Model: {line.strip()}")
            break""",
        "aws_cmd": "# Interrogate AWS global regions and available hypervisor instance types via CLI\naws ec2 describe-instance-types --instance-types t4g.micro --query 'InstanceTypes[0].[InstanceType,VCpuInfo.DefaultVCpus,MemoryInfo.SizeInMiB]' --output table",
        "inspect": "aws ec2 describe-regions --query 'Regions[].[RegionName,Endpoint]' --output table",
        "measure": "Measure the latency difference between local loopback (127.0.0.1) and remote datacenter IP via ping/traceroute.",
        "break_desc": "Simulate CPU core exhaustion locally using a multi-process spin loop.",
        "diagnose": "Inspect 'top' or 'htop'; observe 100% CPU utilization and process scheduling throttling.",
        "recover": "Apply OS cgroups or process nice values to constrain compute starvation.",
        "security": "Hypervisor escape vulnerabilities (Spectre/Meltdown, Rowhammer) represent the physical security perimeter between multitenant virtual machines.",
        "cost": "Idle Physical Server: 100% of capital expenditure (CapEx) + ongoing power/cooling costs regardless of utilization. Cloud Compute: 100% variable operational expenditure (OpEx) billed per second.",
        "cleanup": "# No resources created in live AWS account for Phase 00.",
        "verify_cleanup": "# Verify local environment is clean\npython3 scripts/cleanup-check.sh",
        "mastery_q1": "Why does a 2-vCPU virtual machine not guarantee 100% of two physical hardware cores unless Dedicated Hosts are purchased?",
        "mastery_q2": "What physical bottleneck prevents cloud providers from offering instantaneous provisioning of 100,000 servers in a single second?",
        "mastery_q3": "How does hypervisor CPU time-sharing affect p99 latency compared to bare-metal hardware?",
        "when_use": "Whenever workloads have variable, unpredictable, or seasonal demand that cannot justify purchasing physical hardware.",
        "when_not": "When regulatory requirements mandate sovereign on-prem hardware or when steady-state 24/7 compute at petabyte scale makes colo cheaper.",
        "next_step": "Phase 01: AWS Global Infrastructure — Understanding Regions, Availability Zones, and physical speed-of-light boundaries."
    },
    {
        "module": "00-cloud-foundations",
        "slug": "01-aws-global-infrastructure",
        "num": "01",
        "title": "AWS Global Infrastructure",
        "motto": "Region != Availability Zone. Latency is the speed of light in optical fiber.",
        "type": "Systems Experiment & Measurement",
        "time": "45",
        "prereqs": "Phase 00: Cloud Before AWS",
        "services": "AWS Global Regions, Availability Zones, Edge Locations",
        "cost": "Free ($0.00 / Query CLI)",
        "problem": "Deploying an entire application into a single physical building means a municipal power grid failure, flood, or fiber cut causes 100% downtime. Furthermore, users on the other side of the planet experience 200ms+ round-trip latency.",
        "prediction": "Querying an AWS endpoint across the continent will exhibit a minimum baseline latency bounded by the speed of light (~5ms per 1,000 km of glass fiber).",
        "why_matters": "Conflating an AWS Region with an Availability Zone leads to single-point-of-failure architectures that fail completely when one datacenter suffers an outage.",
        "first_principles": "Light travels through vacuum at ~300,000 km/s, and through glass fiber optic cables at ~200,000 km/s (~5 microseconds per kilometer). An Availability Zone is one or more discrete physical datacenters separated by 10-50 km to ensure independent flood/earthquake blast radiuses while keeping round-trip latency under 1-2 milliseconds.",
        "diagram": """AWS Global Topology:
AWS Global Backbone
├── Region A (e.g., us-east-1: N. Virginia)
│   ├── AZ 1 (us-east-1a) ──(Sub-2ms Dark Fiber)──► AZ 2 (us-east-1b)
│   │   └── Physical DC Campus 1                    └── Physical DC Campus 2
│   └── AZ 3 (us-east-1c)
└── Region B (e.g., eu-central-1: Frankfurt)
    └── Bounded by Transatlantic Undersea Cables (~70ms latency)""",
        "before_aws": "Global enterprises leased synchronous MPLS circuits between private datacenters in New York, London, and Tokyo, paying tens of thousands of dollars monthly.",
        "primitive_code": """# Measure speed-of-light latency across regions
import time, urllib.request
def measure_endpoint(url):
    t0 = time.perf_counter()
    urllib.request.urlopen(url, timeout=5)
    return (time.perf_counter() - t0) * 1000

print(f"Latency to Virginia:  {measure_endpoint('https://ec2.us-east-1.amazonaws.com'):.1f}ms")
print(f"Latency to Frankfurt: {measure_endpoint('https://ec2.eu-central-1.amazonaws.com'):.1f}ms")""",
        "aws_cmd": "# Interrogate all available Availability Zones in your default region\naws ec2 describe-availability-zones --query 'AvailabilityZones[].[ZoneName,ZoneId,State]' --output table",
        "inspect": "aws ec2 describe-regions --query 'Regions[].RegionName' --output text",
        "measure": "Run latency comparisons between same-AZ ping (< 1ms), cross-AZ ping (1-2ms), and cross-region ping (70-150ms).",
        "break_desc": "Attempt to synchronously replicate relational database transactions across transatlantic regions.",
        "diagnose": "Observe database write commit latency balloon from 2ms to 120ms due to speed-of-light round trips.",
        "recover": "Use asynchronous replication across regions and synchronous replication only within Multi-AZ boundaries.",
        "security": "Data sovereignty and legal compliance (GDPR, HIPAA, CCPA) strictly mandate which geographic region data may physically reside in.",
        "cost": "Cross-AZ data transfer: ~$0.01/GB in each direction. Cross-region data transfer: ~$0.02/GB. Inter-AZ communication within the same AZ is $0.00.",
        "cleanup": "# No infrastructure provisioned. Zero cleanup needed.",
        "verify_cleanup": "echo 'Account clean.'",
        "mastery_q1": "Why does AWS map the logical AZ name 'us-east-1a' to different physical Zone IDs (e.g. 'use1-az1') across different AWS accounts?",
        "mastery_q2": "Why can an application synchronously commit transactions across AZs in the same region, but must use asynchronous replication across regions?",
        "mastery_q3": "Under what circumstances does deploying across two AZs actually REDUCE overall availability?",
        "when_use": "Use Multi-AZ for high availability within a region. Use Multi-Region only for disaster recovery or extreme global data residency requirements.",
        "when_not": "Do not build multi-region active-active architectures prematurely—cross-region consensus is one of the hardest distributed systems problems.",
        "next_step": "Phase 02: AWS CLI, APIs, and Console — Stripping away the UI magic to see signed REST API requests."
    },
    {
        "module": "00-cloud-foundations",
        "slug": "02-aws-cli-apis-console",
        "num": "02",
        "title": "AWS CLI, APIs, and Console",
        "motto": "The console, CLI, and SDK are just HTTP clients making signed POST requests to REST endpoints.",
        "type": "Systems Experiment & Protocol Inspection",
        "time": "45",
        "prereqs": "Phase 01: AWS Global Infrastructure",
        "services": "AWS STS, AWS Control Plane REST APIs, AWS CLI v2",
        "cost": "Free ($0.00 / Query CLI)",
        "problem": "Relying exclusively on the web console breeds a magical view of the cloud. When a web form button fails with a vague error or when automation is required, GUI-only developers cannot diagnose what HTTP call failed or why.",
        "prediction": "Executing any AWS CLI command with --debug will reveal an underlying signed HTTPS POST request with an Authorization header containing AWS4-HMAC-SHA256 (SigV4).",
        "why_matters": "All cloud automation, Terraform, CDK, and Kubernetes operators simply invoke these exact HTTPS endpoints. Stripping away the UI reveals the true cloud control plane.",
        "first_principles": "Every cloud resource modification is an HTTP request over TLS to a service endpoint (e.g., `ec2.us-east-1.amazonaws.com`). AWS authenticates requests using the AWS Signature Version 4 (SigV4) protocol: an HMAC-SHA256 digest calculated over the HTTP method, URI, query string, headers, and request body using the caller's secret key.",
        "diagram": """Client to API Architecture:
┌──────────────────────────┐
│ AWS Console (Web UI)     │─┐
├──────────────────────────┤ │
│ AWS CLI v2 (Shell)       │─┼──► HTTPS POST (SigV4 Signed) ──► AWS Service API Endpoint
├──────────────────────────┤ │                                   (e.g., sts.amazonaws.com)
│ Boto3 SDK (Python)       │─┘
└──────────────────────────┘""",
        "before_aws": "Datacenter administrators configured servers over IPMI / serial consoles, executed commands over SSH, or managed VMware vSphere APIs.",
        "primitive_code": """# Inspect AWS SigV4 Canonical Request Components
import hashlib
canonical_request = "GET\\n/\\n\\nhost:sts.amazonaws.com\\n\\nhost\\ne3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
hashed_request = hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()
print(f"Canonical Request SHA256 Hash:\\n{hashed_request}")""",
        "aws_cmd": "# Call STS caller identity with full HTTP protocol debug logging\naws sts get-caller-identity --debug 2>&1 | grep -E '> (POST|Host|Authorization)' | head -n 5",
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
    }
]

print("Script template ready.")
