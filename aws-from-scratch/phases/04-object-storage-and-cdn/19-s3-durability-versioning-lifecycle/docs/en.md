# Phase 19: S3 Durability, Versioning, Lifecycle

## Motto
> Durability is not backup. If an application overwrites good data with corrupt data, S3 durably replicates the corruption.

**Type:** Hands-on Lab & Data Lifecycle  
**Time Estimate:** ~60 minutes  
**Prerequisites:** Phase 18: S3 Operations  
**AWS Services Involved:** S3 Versioning, S3 Storage Classes, S3 Lifecycle Rules  
**Cost Vector:** Versioning doubles storage costs if objects are frequently overwritten, because all historical versions are stored and billed.  

---

## Problem
Accidental deletion or ransomware overwriting files can destroy company data. Furthermore, storing old logs in S3 Standard forever results in massive unnecessary storage bills.

---

## Prediction
Enabling versioning means deleting an object simply places a 'Delete Marker' on top; the prior version remains fully recoverable.

---

## Why this matters
Distinguishing durability, versioning, replication, and backup prevents catastrophic data loss.

---

## First principles
Durability is hardware failure protection (replicated across 3+ AZs against drive failures). Versioning is logical protection against human/software errors. When an object is deleted in a versioned bucket, S3 inserts a 0-byte `DeleteMarker`. The previous object version remains intact and can be retrieved by `versionId`.

---

## Mental model
```text
S3 Versioning Stack:
Object Key: "contract.pdf"
┌────────────────────────────────────────────────────────┐
│ [Delete Marker] (Inserted on DELETE)  VersionId: VID_3 │ <── Current Version (Returns 404)
├────────────────────────────────────────────────────────┤
│ "contract_v2.pdf" (Uploaded 2pm)       VersionId: VID_2 │ <── Recoverable!
├────────────────────────────────────────────────────────┤
│ "contract_v1.pdf" (Uploaded 10am)      VersionId: VID_1 │ <── Recoverable!
└────────────────────────────────────────────────────────┘
```

---

## Architecture before AWS
Tape backup rotations (Grandfather-Father-Son) and robotic tape libraries.

---

## Build the primitive
```python
# Simulating S3 versioning stack
bucket_versions = {}
def put_version(key, data):
    bucket_versions.setdefault(key, []).append(data)
def delete_version(key):
    bucket_versions.setdefault(key, []).append("DELETE_MARKER")
put_version("doc.txt", "v1")
put_version("doc.txt", "v2")
delete_version("doc.txt")
print("Latest state:", bucket_versions["doc.txt"][-1])
print("Prior recoverable version:", bucket_versions["doc.txt"][-2])
```

---

## Use AWS
```bash
aws s3api put-bucket-versioning --bucket $BUCKET --versioning-configuration Status=Enabled
```

---

## Inspect it
```bash
aws s3api get-bucket-versioning --bucket $BUCKET --output table
```

---

## Measure it
Compare storage class costs: S3 Standard ($0.023/GB) vs Glacier Flexible ($0.0036/GB) vs Glacier Deep Archive ($0.00099/GB).

---

## Break it
Delete an object in a versioned bucket via `aws s3 rm`.

---

## Diagnose it
The object appears gone in `aws s3 ls`, but `aws s3api list-object-versions` reveals the Delete Marker and past version.

---

## Recover it
Delete the Delete Marker to restore the object: `aws s3api delete-object --bucket $BUCKET --key doc.txt --version-id $DELETE_MARKER_VID`.

---

## Security
Enable S3 Object Lock (WORM: Write Once Read Many) for compliance to prevent anyone—even root—from deleting objects.

---

## Cost
### Cost Warning
Versioning doubles storage costs if objects are frequently overwritten, because all historical versions are stored and billed.

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
aws s3api put-bucket-versioning --bucket $BUCKET --versioning-configuration Status=Suspended
```

---

## Verify cleanup
```bash
echo 'Bucket versioning suspended.'
```

---

## Evidence
Record your laboratory findings using the mandatory evidence log template at `outputs/evidence-template.md`. Save your completed evidence log as `outputs/phase-19-evidence.md`.

---

## Questions for mastery
1. Why does S3 replication to a secondary bucket NOT protect against accidental software deletion bugs unless versioning is configured?
2. What happens to noncurrent versions if you do not configure an S3 Lifecycle rule to expire them?
3. Why is Glacier Deep Archive retrieve time measured in hours rather than milliseconds?

---

## When to use this
Enable versioning on critical business data, configuration buckets, and state files.

---

## When not to use this
Do not enable versioning on high-churn transient caches without a lifecycle rule to expire noncurrent versions after 1 day.

---

## What comes next
Phase 20: Static Website / Object Delivery — CloudFront and Origin Access Control.
