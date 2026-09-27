# Project 01: Secure Static Web Architecture (CloudFront + S3)

> **Motto:** S3 stores the bits; CloudFront accelerates and secures the delivery.

---

## 1. Architectural Diagram

```text
[ User / Browser ]
        │
        │ 1. HTTPS GET /index.html (Anycast Routing via Route 53)
        ▼
[ CloudFront Edge Distribution ] ──(Cache Hit: 10-30ms)──► Return Cached HTML/CSS
        │
        │ (Cache Miss)
        │ 2. SigV4 Authenticated Origin Request
        │    via Origin Access Control (OAC)
        ▼
[ Private Amazon S3 Bucket ]
(Block Public Access: ON | Static Website Hosting: OFF)
(Bucket Policy: Allow s3:GetObject ONLY to CloudFront Distribution ARN)
```

---

## 2. Why S3 Website Hosting is an Anti-Pattern

In legacy architectures, developers enabled "Static Website Hosting" on S3 buckets and made the entire bucket publicly readable to `0.0.0.0/0`.

**Why this is dangerous in production:**
1. **Unencrypted HTTP:** S3 static website hosting endpoints only support plain HTTP (no native custom TLS/SSL certificates).
2. **Global Latency:** Requests must travel across the globe to the single AWS Region where the bucket lives (e.g. Sydney to Virginia = 220ms round-trip).
3. **Financial Exposure:** Direct bucket access exposes your account to unbounded GET request billing if an attacker hotlinks or hammers the endpoint.
4. **Data Exfiltration Risk:** Public buckets invite accidental leaks of non-public files placed in the bucket.

**The Well-Architected Pattern:**
- S3 bucket remains **100% private** with Block Public Access enabled.
- CloudFront terminates TLS at the nearest edge PoP.
- CloudFront accesses S3 using **Origin Access Control (OAC)**, signing requests with AWS SigV4.

---

## 3. Well-Architected Review

### Operational Excellence
- Deployment via CloudFormation or CI/CD uploading to S3, followed by a targeted CloudFront invalidation (`aws cloudfront create-invalidation --paths "/index.html"`).
- Telemetry: CloudFront standard access logs written to a separate logging S3 bucket.

### Security
- **Origin Access Control (OAC):** Only the specific CloudFront distribution ARN can invoke `s3:GetObject`.
- **Enforce TLS 1.3:** CloudFront security policy set to `TLSv1.2_2021` or higher.
- **Security Headers:** Response headers policy injecting `Strict-Transport-Security`, `X-Content-Type-Options: nosniff`, and `Content-Security-Policy`.

### Reliability
- Multi-region edge caching across 450+ Points of Presence worldwide.
- S3 provides 99.999999999% (11 9's) data durability.

### Performance Efficiency
- Asset compression via Brotli and Gzip negotiated at the edge.
- Cache-Control headers: Immutable hashed assets (`/assets/*.js`) cached for 1 year (`max-age=31536000, immutable`); `index.html` cached for 5 minutes (`max-age=300`).

### Cost Optimization
- **CloudFront Free Tier:** 1 TB of data transfer out and 10,000,000 HTTP/HTTPS requests per month.
- S3 standard storage: ~$0.023 / GB-month (fractions of a cent for typical frontend bundles).
- Zero idle compute costs: No running EC2 VMs or load balancer hourly charges.

---

## 4. Hands-on Deployment

### Step 1: Create Private S3 Bucket
```bash
BUCKET_NAME="aws-from-scratch-web-$(aws sts get-caller-identity --query Account --output text)"

aws s3api create-bucket \
    --bucket "$BUCKET_NAME" \
    --region us-east-1

# Enforce Block Public Access
aws s3api put-public-access-block \
    --bucket "$BUCKET_NAME" \
    --public-access-block-configuration "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true"
```

### Step 2: Upload Assets
```bash
echo "<html><body><h1>AWS from Scratch: CloudFront + S3</h1></body></html>" > index.html

aws s3 cp index.html "s3://$BUCKET_NAME/index.html" \
    --content-type "text/html" \
    --cache-control "max-age=300"
```

---

## 5. Cost Warning
- S3 Storage: ~$0.023/GB-mo.
- CloudFront: Included in Free Tier for typical learning traffic.
- Invalidation: First 1,000 paths/month are free; $0.005 per path thereafter.

---

## 6. Cleanup
```bash
# Empty S3 bucket
aws s3 rm "s3://$BUCKET_NAME" --recursive

# Delete bucket
aws s3api delete-bucket --bucket "$BUCKET_NAME"
```

### Verify Cleanup
```bash
aws s3api list-buckets --query "Buckets[?Name=='$BUCKET_NAME'].Name" --output text
# Must return empty!
```
