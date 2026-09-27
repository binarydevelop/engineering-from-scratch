# The Cloud Systems Troubleshooting Guide

When an AWS system breaks, novice engineers change random console settings until something works. Systems engineers follow a diagnostic tree based on protocol layers and control-plane physics.

This guide provides systematic diagnostic procedures for the seven most common cloud failure modes.

---

## 1. IAM `403 AccessDenied` Debugging

When an API call fails with `AccessDenied` or `UnauthorizedOperation`:

```text
[ AccessDenied Error ]
          │
          ├── 1. Decode Authorization Message (if available)
          │      aws sts decode-authorization-message --encoded-message <blob>
          │      Reveals exact policy statement, principal, and resource evaluated!
          │
          ├── 2. Check Principal Identity
          │      aws sts get-caller-identity
          │      Are you who you think you are? (Check profile, role, session).
          │
          ├── 3. Check for Explicit Deny
          │      Does any Service Control Policy (SCP), Permissions Boundary,
          │      or Session Policy contain "Effect": "Deny" matching this action?
          │
          ├── 4. Check Resource-Based Policies
          │      For S3, KMS, SQS: Does the target resource policy allow the caller?
          │      (Cross-account access REQUIRES both identity AND resource policy allow!).
          │
          └── 5. Check KMS Permissions
                 If reading an encrypted S3 object, you must have BOTH s3:GetObject
                 AND kms:Decrypt on the KMS key used to encrypt the object.
```

---

## 2. Network Connectivity: `Timed Out` vs `Connection Refused`

The error message tells you which OSI layer dropped the packet:

```text
Connection timed out:
┌────────────────────────────────────────────────────────────────────────┐
│ The client sent TCP SYN packets, but received NO ACK and NO RST.       │
│ The packet was silently dropped into a black hole.                     │
│ DIAGNOSIS:                                                             │
│ 1. Security Group Inbound Rule: Is the client's IP permitted on port?  │
│ 2. Security Group Outbound Rule: Is return traffic permitted?          │
│ 3. Subnet Route Table: Is there a route to 0.0.0.0/0 via IGW or NAT?   │
│ 4. Network ACL: Is ephemeral port range (1024-65535) open on outbound? │
│ 5. Public IP: Does the instance in a public subnet actually have a     │
│    public IPv4 address assigned?                                       │
└────────────────────────────────────────────────────────────────────────┘

Connection refused:
┌────────────────────────────────────────────────────────────────────────┐
│ The client received an immediate TCP RST packet from the destination.   │
│ The packet reached the host, but the OS rejected the connection.       │
│ DIAGNOSIS:                                                             │
│ 1. Networking works! Routing and Security Groups are NOT the problem.  │
│ 2. Is your application process actually running? (systemctl status)    │
│ 3. Is the application listening on 127.0.0.1 instead of 0.0.0.0?      │
│    (Run 'ss -tulpn' or 'lsof -i :<port>' on the host).                 │
│ 4. Is the host OS local firewall (iptables/ufw) blocking the port?     │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Load Balancer HTTP Errors (ALB)

```text
HTTP 502 Bad Gateway:
- The ALB reached the backend EC2/ECS target, but the target returned a malformed
  response or abruptly closed the TCP connection (TCP RST) before sending headers.
- Fix: Check target application crash logs; ensure target HTTP keep-alive timeout
  is set HIGHER than the ALB idle timeout (ALB idle timeout defaults to 60s;
  backend keep-alive should be 65s+).

HTTP 503 Service Unavailable:
- The Target Group has ZERO healthy targets.
- Fix: Check ALB Target Group health checks. Did all instances fail the health path?

HTTP 504 Gateway Timeout:
- The ALB forwarded the request, but the target failed to respond within the
  idle timeout period (default 60 seconds).
- Fix: Check database query duration or slow upstream microservices.
```

---

## 4. Lambda Failures: Cold Starts vs Timeouts

```text
Task timed out after 3.00 seconds:
- Cause 1: Database connection hanging because Lambda is outside VPC trying
  to reach a private RDS instance (or inside VPC with no NAT/VPC endpoint).
- Cause 2: Under-allocated memory. Lambda allocates CPU proportionally to memory.
  A CPU-intensive task with 128MB RAM may timeout, while at 1024MB it runs in 200ms.

Cold Start Latency Spike:
- Cause: Initial container initialization (`INIT` phase) runs heavyweight SDK
  imports, database connection pooling, or machine learning models.
- Fix: Move static initialization outside the handler function; use Provisioned
  Concurrency for strict latency SLAs; use lightweight runtimes (Python/Node/Go).
```

---

## 5. SQS Visibility Loops & Poison Pill Messages

```text
Symptom: A single message is processed repeatedly forever; queue never empties.
- Mechanism:
  1. Worker receives Message X.
  2. Worker crashes on unhandled exception before calling `DeleteMessage`.
  3. SQS Visibility Timeout (e.g., 30s) expires.
  4. SQS marks Message X visible again.
  5. Another worker receives Message X and crashes again.
- Solution:
  1. Configure a Dead-Letter Queue (DLQ).
  2. Set `maxReceiveCount` (e.g. 3 or 5).
  3. After N failed deliveries, SQS automatically routes the poison pill to DLQ.
```

---

## 6. RDS Connection Exhaustion

```text
FATAL: remaining connection slots are reserved for non-replicated superuser connections
- Relational databases (PostgreSQL/MySQL) fork a process or thread per connection.
  Each connection consumes 5-10 MB of RAM. A `t4g.micro` supports only ~80 connections.
- Symptom: Serverless Lambda scales to 500 concurrent invocations, each opening
  a new DB connection, crushing the RDS instance.
- Solution:
  1. Deploy **Amazon RDS Proxy** to multiplex thousands of ephemeral Lambda
     connections into a small pool of warm database connections.
  2. Use application-level connection pools (e.g., SQLAlchemy `QueuePool`).
```

---

## 7. S3 `403 Forbidden` on "Public" Buckets

```text
Symptom: Bucket policy is set to allow public read, but curl returns 403 Forbidden.
- Check 1: S3 Block Public Access (Account or Bucket Level)
  Is `BlockPublicPolicy` or `IgnorePublicAcls` enabled? (These override bucket policies).
- Check 2: Object Ownership
  If objects were uploaded by another AWS account without `bucket-owner-full-control`,
  the bucket owner does not have permission to read or share the object.
- Check 3: KMS Key Policy
  If the bucket is encrypted with SSE-KMS using a customer-managed key, anonymous
  public callers cannot invoke `kms:Decrypt`.
```
