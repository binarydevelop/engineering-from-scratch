# Phase 18: S3 Operations

## Motto
> Every S3 operation is a standard HTTP request with headers, metadata, and ETags.

**Type:** Hands-on Lab & API Verification  
**Time Estimate:** ~60 minutes  
**Prerequisites:** Phase 17: S3 From First Principles  
**AWS Services Involved:** Amazon S3 REST APIs  
**Cost Vector:** PUT/COPY/POST: $0.005 per 1,000 requests. GET/HEAD: $0.0004 per 1,000 requests.  

---

## Problem
Applications upload files with incorrect MIME types, leading to browsers downloading HTML/PDF files instead of rendering them inline.

---

## Prediction
Uploading an object with `Content-Type: text/html` will cause browsers to render it as a webpage, while `application/octet-stream` forces a download.

---

## Why this matters
Mastering S3 metadata, ETags, and headers is essential for building web applications and CDNs.

---

## First principles
S3 objects carry HTTP headers: `Content-Type`, `Cache-Control`, `Content-Disposition`, and custom metadata prefixed with `x-amz-meta-*`. The `ETag` header is typically the hexadecimal MD5 checksum of the object content.

---

## Mental model
```text
S3 HTTP Headers:
HTTP PUT /reports/q3.pdf
Content-Type: application/pdf
Cache-Control: max-age=3600
x-amz-meta-author: alice
                │
                ▼
HTTP 200 OK
ETag: "c8c60a479c402... (MD5 Checksum)"
x-amz-version-id: "null" / "3/L4k..." 
```

---

## Architecture before AWS
Storing files on web servers and configuring Apache/Nginx `mime.types` mapping tables.

---

## Build the primitive
```python
import hashlib
content = b"Hello Cloud World"
etag = hashlib.md5(content).hexdigest()
print(f"Calculated ETag: \"{etag}\"")
```

---

## Use AWS
```bash
echo '<h1>AWS</h1>' > test.html && aws s3 cp test.html s3://$BUCKET/test.html --content-type 'text/html' --metadata 'lab=aws-from-scratch'
```

---

## Inspect it
```bash
aws s3api head-object --bucket $BUCKET --key test.html --output json
```

---

## Measure it
Compare upload performance: single-part PUT vs multipart upload for large files (> 100MB).

---

## Break it
Upload a PDF with `Content-Type: text/plain`.

---

## Diagnose it
Opening the S3 URL in a browser renders raw binary characters instead of formatted PDF pages.

---

## Recover it
Copy object over itself to replace metadata: `aws s3 cp s3://$BUCKET/doc.pdf s3://$BUCKET/doc.pdf --metadata-directive REPLACE --content-type 'application/pdf'`.

---

## Security
Use S3 pre-signed URLs to grant temporary upload/download access without sharing IAM credentials.

---

## Cost
### Cost Warning
PUT/COPY/POST: $0.005 per 1,000 requests. GET/HEAD: $0.0004 per 1,000 requests.

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
aws s3 rm s3://$BUCKET/test.html
```

---

## Verify cleanup
```bash
echo 'Object cleaned.'
```

---

## Evidence
Record your laboratory findings using the mandatory evidence log template at `outputs/evidence-template.md`. Save your completed evidence log as `outputs/phase-18-evidence.md`.

---

## Questions for mastery
1. Why is Multipart Upload mandatory for objects larger than 5GB?
2. What does an ETag represent for an object uploaded via Multipart Upload? (Hint: It is not a simple MD5 of the whole file).
3. How do S3 Pre-Signed URLs cryptographically guarantee that only the authorized client can upload?

---

## When to use this
Use pre-signed URLs for direct client uploads from mobile apps to S3, bypassing web servers.

---

## When not to use this
Do not proxy large file uploads through web application servers—upload directly to S3.

---

## What comes next
Phase 19: S3 Durability, Versioning, Lifecycle — Managing data retention and tiers.
