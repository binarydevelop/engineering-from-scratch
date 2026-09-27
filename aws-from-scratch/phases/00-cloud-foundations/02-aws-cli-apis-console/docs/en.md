# Phase 02: AWS CLI, APIs, and Console

## Motto
> The console, CLI, and SDK are just HTTP clients making signed POST requests to REST endpoints.

**Type:** Systems Experiment & Protocol Inspection  
**Time Estimate:** ~45 minutes  
**Prerequisites:** Phase 01: AWS Global Infrastructure  
**AWS Services Involved:** AWS STS, AWS Control Plane REST APIs, AWS CLI v2  
**Cost Vector:** AWS control plane read APIs (Describe*, Get*, List*) are free of charge in virtually all services.  

---

## Problem
Relying exclusively on the web console breeds a magical view of the cloud. When a web form button fails with a vague error or when automation is required, GUI-only developers cannot diagnose what HTTP call failed or why.

---

## Prediction
Executing any AWS CLI command with --debug will reveal an underlying signed HTTPS POST request with an Authorization header containing AWS4-HMAC-SHA256 (SigV4).

---

## Why this matters
All cloud automation, Terraform, CDK, and Kubernetes operators simply invoke these exact HTTPS endpoints. Stripping away the UI reveals the true cloud control plane.

---

## First principles
Every cloud resource modification is an HTTP request over TLS to a service endpoint. AWS authenticates requests using the AWS Signature Version 4 (SigV4) protocol: an HMAC-SHA256 digest calculated over the HTTP method, URI, query string, headers, and request body using the caller's secret key.

---

## Mental model
```text
Client to API Architecture:
┌──────────────────────────┐
│ AWS Console (Web UI)     │─┐
├──────────────────────────┤ │
│ AWS CLI v2 (Shell)       │─┼──► HTTPS POST (SigV4 Signed) ──► AWS Service API Endpoint
├──────────────────────────┤ │                                   (e.g., sts.amazonaws.com)
│ Boto3 SDK (Python)       │─┘
└──────────────────────────┘
```

---

## Architecture before AWS
Datacenter administrators configured servers over IPMI / serial consoles, executed commands over SSH, or managed VMware vSphere APIs.

---

## Build the primitive
```python
import hashlib
canonical_request = "GET\n/\n\nhost:sts.amazonaws.com\n\nhost\ne3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
hashed_request = hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()
print(f"Canonical Request SHA256 Hash:\n{hashed_request}")
```

---

## Use AWS
```bash
aws sts get-caller-identity --debug 2>&1 | grep -E '> (POST|Host|Authorization)' | head -n 5
```

---

## Inspect it
```bash
aws sts get-caller-identity --output json
```

---

## Measure it
Measure CLI execution overhead: compare Python Boto3 client invocation vs CLI subprocess launch time.

---

## Break it
Skew your system clock by more than 15 minutes (or simulate timestamp drift) and make an AWS API call.

---

## Diagnose it
The API call fails with RequestTimeTooSkewed: SigV4 requires client timestamps within 15 minutes of UTC to prevent replay attacks.

---

## Recover it
Resynchronize system clock via NTP (Chrony/systemd-timesyncd).

---

## Security
Never pass AWS secrets via CLI command line arguments (e.g. --secret-key); command arguments are visible in OS process tables (`ps aux`).

---

## Cost
### Cost Warning
AWS control plane read APIs (Describe*, Get*, List*) are free of charge in virtually all services.

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
# No resources provisioned. Zero cleanup required.
```

---

## Verify cleanup
```bash
echo 'Zero cleanup required.'
```

---

## Evidence
Record your laboratory findings using the mandatory evidence log template at `outputs/evidence-template.md`. Save your completed evidence log as `outputs/phase-02-evidence.md`.

---

## Questions for mastery
1. Why does AWS SigV4 sign the SHA256 hash of the request body rather than sending the raw secret key over TLS?
2. What happens if a malicious proxy intercepts and replays a valid signed AWS API request 20 minutes later?
3. How does pagination work when querying an AWS API that contains 50,000 resources?

---

## When to use this
Use CLI/SDK for reproducible automation, scripting, and CI/CD pipelines.

---

## When not to use this
Avoid hand-crafted raw HTTP SigV4 signing when official SDKs handle signature calculation, retries, and token refresh automatically.

---

## What comes next
Phase 03: IAM From First Principles — Understanding cryptographic identity and authorization before provisioning resources.
