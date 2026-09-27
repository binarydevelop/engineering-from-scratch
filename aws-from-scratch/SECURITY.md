# Account Security & Threat Model: The Zero-Trust Lab Protocol

> **Rule 0 of Cloud Security:** You do not manage security by perimeter alone. You manage identity, authorization boundaries, and explicit cryptographic trust.

An AWS account provides access to raw compute, storage, networking, and public DNS. An exposed access key with administrative privileges can lead to cryptocurrency mining botnets, compromised proprietary data, and catastrophic financial bills within minutes.

This document establishes the mandatory security rules and account hardening practices required before touching any AWS infrastructure in this repository.

---

## 1. The Root Account Protocol

The **root user** is the identity created when the AWS account was first registered. It possesses absolute, immutable administrative control over every resource, cannot be restricted by IAM policies, and has access to billing and account closure actions.

### Mandatory Rules for Root:
1. **Never use the root user for daily learning or lab commands.**
2. **Never create root access keys.** If root access keys exist in your AWS Console, delete them immediately.
3. **Enable Hardware or Authenticator App Multi-Factor Authentication (MFA)** on the root account immediately (FIDO2 WebAuthn security keys like YubiKey or authenticator apps).
4. **Lock root credentials in a password manager** and use root only for emergency account recovery or changing AWS support plans.

---

## 2. Identity Architecture for Labs

Instead of root or long-lived static administrator keys, use modern AWS identity patterns:

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        SECURE IDENTITY WORKFLOW                        │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│   Option A: AWS IAM Identity Center (Recommended)                      │
│   Human Developer ──► SSO Portal (MFA) ──► Short-Lived STS Token       │
│                                            (~1 - 8 hours duration)     │
│                                                                        │
│   Option B: Dedicated IAM Lab User + AssumeRole                        │
│   IAM User (Zero Permissions) ──► sts:AssumeRole ──► LabExecutionRole  │
│                                   (MFA Required)    (Least Privilege)  │
│                                                                        │
│   Option C: Workload Identity (EC2, ECS, Lambda)                       │
│   Instance / Container / Function ──► IAM Instance Profile / Role      │
│                                       (Rotated automatically by AWS)   │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

### Why Permanent Access Keys (`AKIA...`) are an Antipattern
A permanent access key:
- Never expires automatically.
- Can be accidentally committed to Git repositories.
- Can be scraped from compiled binaries or Docker images.
- Is often given excessive `AdministratorAccess` permissions out of convenience.

### The Temporary Credentials Primitives (`STS`)
When you use AWS IAM Identity Center (`aws sso login`) or `aws sts assume-role`, AWS issues three temporary tokens:
1. `AWS_ACCESS_KEY_ID` (starts with `ASIA...` indicating temporary STS credential).
2. `AWS_SECRET_ACCESS_KEY` (ephemeral secret).
3. `AWS_SESSION_TOKEN` (cryptographic proof of session validity and expiration).

These credentials automatically expire after a set time (e.g. 1 hour). If leaked after expiration, an attacker gets zero access.

---

## 3. Workload Identity: IAM Roles Over Static Keys

**NEVER put AWS access keys into code running on EC2 instances, ECS containers, or Lambda functions.**

- **EC2 Instances:** Attach an **IAM Instance Profile**. The instance queries the AWS Instance Metadata Service (IMDSv2) at `http://169.254.169.254/latest/meta-data/` using session tokens to retrieve automatically rotated credentials.
- **ECS Tasks:** Configure an `executionRoleArn` (for pulling container images and writing logs) and a `taskRoleArn` (for application permissions like reading from DynamoDB or S3).
- **Lambda Functions:** Attach an **Execution Role** granting access only to the specific resources the function interacts with.

---

## 4. Least Privilege Principle

Do not use `AdministratorAccess` (`"Action": "*", "Resource": "*"`) as a shortcut. Every lab in this repository defines tightly scoped IAM policies:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowLabS3BucketReadWrite",
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject"
      ],
      "Resource": "arn:aws:s3:::aws-from-scratch-lab-data/*"
    }
  ]
}
```

Key IAM Concepts:
1. **Explicit Deny overrides everything:** If any policy statement evaluates to `Deny`, the request is immediately rejected regardless of any `Allow`.
2. **Default Deny:** If no explicit `Allow` statement matches the principal, action, and resource, access is denied by default.
3. **Resource-Based Policies vs Identity Policies:** Identity policies attach to principals (users, roles). Resource policies attach directly to the target (S3 bucket policy, SQS queue policy, KMS key policy).

---

## 5. Secret Protection & Git Hygiene

Secrets must never enter version control or disk in plaintext:

### Never Store In:
- Git repositories (commit history persists even if deleted in a later commit).
- Docker images (`COPY .env .` burns secrets into image layers).
- Environment variables committed to repositories.
- Client-side code.

### Secure Storage Primitives:
- **AWS Systems Manager Parameter Store**: For configuration values and basic encrypted strings (`SecureString` backed by KMS).
- **AWS Secrets Manager**: For database credentials, API keys, and auto-rotating secrets.

---

## 6. IAM Access Analyzer & Public Access Guardrails

1. **S3 Block Public Access**: Enabled at the account level and bucket level unless an explicit, authenticated educational pattern dictates otherwise.
2. **IAM Access Analyzer**: Periodically inspects resource policies (S3 buckets, KMS keys, SQS queues) to identify permissions granting cross-account or public internet access.

---

## 7. Safety Checklist Before Running Any Live Lab

- [ ] I am NOT logged in as the AWS root user.
- [ ] Root account has MFA enabled and zero active access keys.
- [ ] My active CLI profile identity (`aws sts get-caller-identity`) is an IAM role or dedicated IAM learning identity.
- [ ] `.gitignore` contains `.env`, `*.pem`, `*.key`, `terraform.tfstate`, and credentials files.
- [ ] Git pre-commit hooks or secret scanners (e.g. `gitleaks`, `git-secrets`) are aware of AWS credential patterns.
