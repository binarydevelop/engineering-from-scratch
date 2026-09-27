# Phase 53: Secrets Management

## Motto
> Secrets in source code are an emergency. Secrets in environment variables are a risk. Secrets fetched dynamically via IAM are secure.

**Type:** Hands-on Lab & Secrets Engineering  
**Time Estimate:** ~60 minutes  
**Prerequisites:** Phase 03: IAM From First Principles  
**AWS Services Involved:** AWS Secrets Manager, SSM Parameter Store  
**Cost Vector:** SSM Parameter Store Standard parameters are 100% FREE. Secrets Manager costs $0.40/secret/month + $0.05/10k API calls.  

---

## Problem
Developers commit database passwords or Stripe API keys into Git repositories or bake them into Docker images, where they are scraped by automated botnets in seconds.

---

## Prediction
Applications fetching secrets dynamically from AWS Secrets Manager using IAM role credentials keep credentials out of code, disks, and environment variables.

---

## Why this matters
Credential leakage is the #1 vector for catastrophic cloud account takeovers.

---

## First principles
A secret management service provides an encrypted key-value store backed by KMS envelope encryption. Access is controlled strictly via IAM role evaluation. Secrets Manager adds automated credential rotation: invoking a Lambda function to update the database password and rotate the secret simultaneously with zero downtime.

---

## Mental model
```text
Secrets Manager vs Parameter Store:
┌───────────────────────────────────────┬───────────────────────────────────────┐
│ AWS Secrets Manager                   │ AWS Systems Manager Parameter Store   │
├───────────────────────────────────────┼───────────────────────────────────────┤
│ • $0.40 per secret per month          │ • Standard: 100% FREE ($0.00)         │
│ • Automated password rotation built-in│ • Basic config & encrypted strings    │
│ • Generates random passwords via API  │ • Manual rotation                     │
└───────────────────────────────────────┴───────────────────────────────────────┘

Runtime Flow:
Compute (EC2/ECS/Lambda) ──(IAM Role)──► Fetch Secret at Runtime ──► Connect to DB
(No secrets in Git! No secrets in Dockerfile! No secrets in .env!)
```

---

## Architecture before AWS
HashiCorp Vault or encrypted GPG files committed to repos.

---

## Build the primitive
```python
# Fetching secret dynamically via Boto3 pattern
def mock_get_secret(secret_name):
    # Simulates: boto3.client('secretsmanager').get_secret_value(SecretId=secret_name)
    return {"host": "db.internal", "user": "app_user", "password": "SuperSecretPassword123!"}
secret = mock_get_secret("prod/db")
print("Retrieved secret dynamically:", secret['user'])
```

---

## Use AWS
```bash
aws ssm put-parameter --name '/aws-from-scratch/db-password' --value 'Secret2026!' --type SecureString --tags Key=Project,Value=aws-from-scratch
```

---

## Inspect it
```bash
aws ssm get-parameter --name '/aws-from-scratch/db-password' --with-decryption --output json
```

---

## Measure it
Measure latency: fetching secret over internal AWS network takes 15-30ms during container boot.

---

## Break it
Attempt to fetch a SecureString parameter without `kms:Decrypt` permission on the backing KMS key.

---

## Diagnose it
The API call fails with `AccessDeniedException: The ciphertext refers to a customer master key that does not exist or you are not authorized to use`.

---

## Recover it
Grant `kms:Decrypt` on the KMS key to the application's IAM role.

---

## Security
Never log decrypted secret values in CloudWatch logs or exception stack traces.

---

## Cost
### Cost Warning
SSM Parameter Store Standard parameters are 100% FREE. Secrets Manager costs $0.40/secret/month + $0.05/10k API calls.

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
aws ssm delete-parameter --name '/aws-from-scratch/db-password'
```

---

## Verify cleanup
```bash
echo 'Parameter deleted.'
```

---

## Evidence
Record your laboratory findings using the mandatory evidence log template at `outputs/evidence-template.md`. Save your completed evidence log as `outputs/phase-53-evidence.md`.

---

## Questions for mastery
1. Why is storing secrets in environment variables (`os.environ`) less secure than fetching them at runtime via SDK?
2. What are the architectural differences between SSM Parameter Store and AWS Secrets Manager?
3. How does automated secret rotation work in AWS Secrets Manager without causing downtime for active application connections?

---

## When to use this
Use SSM Parameter Store (SecureString) for configuration and static API keys. Use Secrets Manager for auto-rotating database credentials.

---

## When not to use this
Never store secrets in plaintext parameters, source code, or Docker build arguments.

---

## What comes next
Phase 54: Encryption and KMS — Cryptographic envelope encryption.
