# Tool and Curriculum Versions

This document records the exact tool versions, API versions, and documentation baseline used when this curriculum was verified and generated.

| Property | Value | Notes |
|:---|:---|:---|
| **Curriculum Generation Date** | September 23, 2026 | Baseline AWS API & architectural guidance |
| **AWS CLI Version** | `2.35.23` (`Python/3.14.6 Darwin/25.6.0 exe/arm64`) | AWS CLI v2 required |
| **Python Runtime** | Python 3.12+ (Tested on 3.14.7) | Standard for learning scripts and local primitives |
| **Boto3 SDK** | `>= 1.35.0` | Official AWS SDK for Python |
| **Docker Engine** | `29.7.2` | Local container simulation and packaging |
| **Terraform (Reference IaC)** | `>= 1.9.0` | Declarative IaC reference |
| **AWS CloudFormation** | Current AWS API (2010-09-09 baseline) | Native IaC templates |

---

## AWS Documentation Baseline

This curriculum is built on official AWS documentation and Well-Architected Framework guidance as of **September 2026**.

Key architectural standards adhered to in this repository:

1. **Identity & Access Management (IAM):**
   - IAM Roles and temporary STS credentials (`sts:AssumeRole`) are the mandatory default for compute workloads.
   - Long-lived root credentials and IAM user access keys are discouraged; root user access is strictly forbidden for everyday labs.
   - Resource-based policies, condition keys (`aws:PrincipalArn`, `aws:SourceVpce`), and permission boundaries are taught as security primitives.

2. **Virtual Private Cloud (VPC):**
   - Subnet allocations strictly observe the 5 reserved IP addresses per CIDR block (network, router, DNS, future use, broadcast).
   - No unnecessary NAT Gateways: NAT Gateways accrue continuous hourly baseline costs (~$0.045/hr + data processing). Public jumpboxes/bastions, VPC Endpoints (Gateway endpoints for S3/DynamoDB are free), or direct public subnets with security groups are used for cost-conscious learning.
   - Explicit distinction between Stateful filtering (Security Groups) and Stateless filtering (Network ACLs).

3. **Compute (EC2, ECS, Lambda):**
   - Modern instance families (`t4g`, `t3`, `c6g`, `m7g`) and Graviton / ARM64 cost efficiencies are highlighted.
   - EBS storage defaults to `gp3` (independent baseline of 3,000 IOPS and 125 MB/s throughput without sizing penalties of legacy `gp2`).
   - ECS Fargate default network mode `awsvpc` with task-level IAM roles and security groups.
   - Lambda ephemeral compute with microsecond billing and execution environment lifecycle (cold init vs warm invoke).

4. **Storage & Databases (S3, RDS, DynamoDB):**
   - S3 Block Public Access is enabled by default across all buckets; access is granted via IAM identity policies, bucket policies, or CloudFront Origin Access Control (OAC).
   - DynamoDB access-pattern-first modeling (single-table and partition/sort key design) over relational antipatterns.
   - Amazon RDS Multi-AZ synchronous replication vs read replicas (asynchronous replication) clearly distinguished.

5. **Behavior That Differs by Environment:**
   - **Region:** Service availability (e.g., Bedrock, specific Graviton instance types), pricing, and latency vary by Region (`us-east-1`, `us-west-2`, `eu-west-1`, `ap-south-1`).
   - **Account Type:** AWS Free Tier entitlements (12-month Free, Always Free, Short-Term Trials) differ based on account age and prior consumption.
   - **CLI vs Console vs SDK:** All three invoke the exact same underlying HTTPS REST/JSON AWS APIs, with different pagination, retry, and credential resolution behavior.

---

## Change Log & Deprecation Watch

- **Legacy S3 Website Hosting with Public Buckets**: Deprecated in favor of CloudFront + S3 Origin Access Control (OAC).
- **EC2-Classic**: Permanently retired; all workloads require VPC.
- **Legacy gp2 EBS Volumes**: Replaced by gp3 as the architectural standard.
- **Permanent Access Keys**: Replaced by IAM Identity Center (SSO), temporary credentials, and EC2/ECS Instance Profiles.
