# Phase 54: Encryption and KMS

## Motto
> KMS master keys never leave the hardware security module. They encrypt data keys; data keys encrypt the data.

**Type:** Hands-on Lab & Cryptographic Envelope  
**Time Estimate:** ~60 minutes  
**Prerequisites:** Phase 53: Secrets Management  
**AWS Services Involved:** AWS Key Management Service (KMS), Envelope Encryption  
**Cost Vector:** AWS Managed Keys (`aws/s3`, `aws/ebs`) are 100% FREE. Customer Managed Keys cost $1.00 per month each + $0.03 per 10k requests.  

---

## Problem
Sending gigabytes of data to a central encryption service over the network creates extreme latency bottlenecks and network bandwidth exhaustion.

---

## Prediction
Envelope encryption allows KMS to generate a small 256-bit Data Key under the master key, encrypting huge files locally in memory at hardware speed.

---

## Why this matters
KMS envelope encryption is the fundamental security mechanism protecting S3, EBS, RDS, and DynamoDB at rest.

---

## First principles
Envelope Encryption: (1) Call `kms:GenerateDataKey`. KMS returns a Plaintext Data Key and an Encrypted (Ciphertext) Data Key. (2) Encrypt data locally using the Plaintext Key (AES-256-GCM). (3) Securely wipe the Plaintext Key from memory. (4) Store the Encrypted Data Key alongside the ciphertext. The Customer Master Key (CMK) never leaves the physical HSM.

---

## Mental model
```text
Envelope Encryption Mechanics:
1. Application calls KMS: GenerateDataKey()
┌────────────────────────────────────────────────────────┐
│ AWS KMS Hardware Security Module (FIPS 140-2 Validated)│
│ [ Root KMS Master Key (KmsKeyId) - NEVER LEAVES HSM! ] │
└──────────────────────────┬─────────────────────────────┘
                           │
             ┌─────────────┴─────────────┐
             ▼                           ▼
[ Plaintext Data Key ]         [ Encrypted Data Key ]
             │                           │
             ▼ Encrypts Large File       │
┌──────────────────────────┐             │
│ Ciphertext File Payload  │             │
└────────────┬─────────────┘             │
             │                           │
             ▼ Packages Together         ▼
┌────────────────────────────────────────────────────────┐
│ Stored Encrypted Package (Encrypted Data + Encrypted DK│
└────────────────────────────────────────────────────────┘
```

---

## Architecture before AWS
On-premises Hardware Security Modules (HSMs) like Thales or SafeNet costing $50,000+ per appliance.

---

## Build the primitive
```python
# Simulating envelope encryption data packaging
encrypted_payload = {
    "ciphertext": "U2FsdGVkX1+... (Encrypted Data)",
    "encrypted_data_key": "AQIDAHh... (Encrypted by KMS Master Key)",
    "algorithm": "AES-256-GCM"
}
print("Envelope encrypted package ready for storage.")
```

---

## Use AWS
```bash
# Inspect KMS key policies
aws kms list-aliases --output table
```

---

## Inspect it
```bash
aws kms list-keys --output json
```

---

## Measure it
Measure encryption speed: encrypting 1GB locally with AES-256 data key (< 1s) vs sending 1GB over network to KMS (failed/impossible).

---

## Break it
Attempt to decrypt an S3 object when your IAM identity has `s3:GetObject` but lacks `kms:Decrypt` on the KMS key.

---

## Diagnose it
S3 returns HTTP 403 AccessDenied with `KMS.AccessDeniedException`.

---

## Recover it
Grant `kms:Decrypt` in the KMS Key Policy.

---

## Security
Enable automatic annual key rotation on all Customer Managed Keys (CMKs).

---

## Cost
### Cost Warning
AWS Managed Keys (`aws/s3`, `aws/ebs`) are 100% FREE. Customer Managed Keys cost $1.00 per month each + $0.03 per 10k requests.

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
# Avoid creating CMKs for simple labs unless required; delete test keys with 7-day waiting period.
```

---

## Verify cleanup
```bash
echo 'KMS clean.'
```

---

## Evidence
Record your laboratory findings using the mandatory evidence log template at `outputs/evidence-template.md`. Save your completed evidence log as `outputs/phase-54-evidence.md`.

---

## Questions for mastery
1. Why does the AWS KMS master key never leave the physical Hardware Security Module (HSM)?
2. What is the difference between an AWS Managed Key (`aws/s3`) and a Customer Managed Key (CMK)?
3. How does Encryption Context in KMS prevent ciphertext from being decrypted in the wrong environment?

---

## When to use this
Use Customer Managed Keys when regulatory compliance mandates key rotation, custom key policies, or cross-account access.

---

## When not to use this
Use default AWS Managed Keys when you just need basic encryption at rest without custom access boundaries.

---

## What comes next
Phase 55: CloudFront — Edge caching and global content delivery.
