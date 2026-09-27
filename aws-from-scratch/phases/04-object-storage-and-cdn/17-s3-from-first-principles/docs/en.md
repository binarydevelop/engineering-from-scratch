# Phase 17: S3 From First Principles

## Motto
> S3 is not a filesystem: it is a distributed HTTP key-value store optimized for immutable byte streams.

**Type:** Hands-on Lab & Object Store Exploration  
**Time Estimate:** ~60 minutes  
**Prerequisites:** Phase 02: AWS CLI, APIs, and Console  
**AWS Services Involved:** Amazon S3  
**Cost Vector:** S3 Standard: ~$0.023/GB-month. GET requests: $0.0004 per 1,000. PUT requests: $0.005 per 1,000.  

---

## Problem
Hard drives and filesystems cannot scale to petabytes of data. They suffer from inode exhaustion, single-server failure risks, and complex distributed locking.

---

## Prediction
There are no real folders in S3. The key `photos/2026/summer.jpg` is a single string key in a flat hash index.

---

## Why this matters
Treating S3 like a POSIX filesystem leads to horrible performance bugs (e.g. attempting to rename a folder with 1,000,000 files requires 1,000,000 individual copy and delete HTTP requests!).

---

## First principles
Object storage stores data as immutable binary large objects (BLOBs) addressed by a bucket name and string key. Unlike POSIX filesystems, there are no file descriptors, no `seek()` operations, and no partial byte writes: an object is written atomically in full via HTTP PUT.

---

## Mental model
```text
POSIX Filesystem vs S3 Object Store:
POSIX Filesystem:
/ (Root Inode) ──► dir/ (Directory Inode) ──► file.txt (Data Blocks on local disk)

S3 Object Store (Flat Hash Table):
Bucket: "my-bucket"
Key (String)                     Object Payload (Immutable BLOB)
"uploads/user1/avatar.png"  ──►  [ Bytes: PNG... (Replicated across 3+ AZs) ]
"uploads/user2/avatar.png"  ──►  [ Bytes: PNG... (Replicated across 3+ AZs) ]
```

---

## Architecture before AWS
Network-Attached Storage (NAS) filers like NetApp running NFS / SMB protocols.

---

## Build the primitive
```python
# Simulating S3 flat key-value store
s3_bucket = {}
def put_object(key, data):
    s3_bucket[key] = data
put_object("documents/report.pdf", b"PDF_BYTES")
print("Bucket Keys:", list(s3_bucket.keys()))
print("Notice: There is NO 'documents' directory! Just a flat string key.")
```

---

## Use AWS
```bash
aws s3 mb s3://aws-from-scratch-lab-$(aws sts get-caller-identity --query Account --output text) --region us-east-1
```

---

## Inspect it
```bash
aws s3 ls
```

---

## Measure it
Measure write throughput: S3 supports at least 3,500 PUT and 5,500 GET requests per second per prefix.

---

## Break it
Attempt to append a single byte to an existing 10MB S3 object.

---

## Diagnose it
S3 REST API has no APPEND verb! You must download the object, append locally, and upload the entire object again.

---

## Recover it
Use S3 for immutable objects; use EBS or a database for append-heavy workloads.

---

## Security
Enable S3 Block Public Access at the account and bucket level to prevent data leaks.

---

## Cost
### Cost Warning
S3 Standard: ~$0.023/GB-month. GET requests: $0.0004 per 1,000. PUT requests: $0.005 per 1,000.

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
BUCKET=aws-from-scratch-lab-$(aws sts get-caller-identity --query Account --output text)
aws s3 rb s3://$BUCKET --force
```

---

## Verify cleanup
```bash
echo 'S3 bucket cleaned.'
```

---

## Evidence
Record your laboratory findings using the mandatory evidence log template at `outputs/evidence-template.md`. Save your completed evidence log as `outputs/phase-17-evidence.md`.

---

## Questions for mastery
1. Why does renaming a 'folder' containing 100,000 files in S3 take 10 minutes, while in a Linux filesystem it takes 1 millisecond?
2. What does '11 9s of durability' (99.999999999%) actually mean statistically?
3. How does strong read-after-write consistency work in S3?

---

## When to use this
Use S3 for media assets, backups, logs, data lake analytics, and static web bundles.

---

## When not to use this
Do not use S3 as an operating system boot drive or high-IOPS transactional database data directory.

---

## What comes next
Phase 18: S3 Operations — PUT, GET, DELETE, and metadata headers.
