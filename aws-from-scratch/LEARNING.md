# The Learning Contract: How to Learn AWS Deeply

> **The Motto:** Understand it. Build it. Observe it. Break it. Recover it. Secure it. Scale it. Cost it. Ship it.

Most developers learn AWS backward:
1. They log into the AWS Management Console.
2. They click around in a wizard with 50 options they don't understand.
3. They copy a stack overflow snippet or Terraform module.
4. Things appear to work.
5. Six months later in production, a subnet runs out of IP addresses, a cross-AZ data transfer bill hits $4,000, or a service fails over to an AZ that lacks capacity, and no one knows why.

This curriculum is designed to permanently cure you of treating AWS as a magic black box.

---

## The Rules of Engagement

To extract maximum value from this repository, adopt these core disciplines:

### 1. Predict Before Running
Before you execute an `aws` command, deploy a CloudFormation template, or run a Python script, **write down your prediction**:
- *What HTTP status code or error do I expect?*
- *Will this packet pass through the Security Group or be dropped by the Network ACL?*
- *Will this Lambda cold start take 20ms or 800ms?*
- *What exact resources will AWS create behind the scenes?*

If reality matches your prediction, your mental model is validated. If reality differs, you have just discovered a blind spot.

### 2. Draw Before Configuring
Never build an architecture without drawing two diagrams on paper or whiteboard:
1. **The Traffic Path:** Trace the byte stream from client browser → DNS query → CDN edge → Load Balancer → Target Group → Network Interface (ENI) → Operating System Socket → Application Process.
2. **The Security Boundary:** Where does authentication happen? Where does authorization happen? Which subnet boundary isolates the data? What IAM role assumes identity?

### 3. The Core Learning Loop
Every lesson in this curriculum executes this progression:

```text
       [ 1. PROBLEM ] ──────────────► Why does the system fail without this?
              │
       [ 2. PREDICT ] ──────────────► Formulate explicit hypothesis
              │
    [ 3. FIRST PRINCIPLES ] ────────► Derive from sockets, disks, packets, memory
              │
    [ 4. BUILD PRIMITIVE ] ─────────► Implement minimal local Python version
              │
       [ 5. USE AWS ] ──────────────► Call AWS API / CLI / SDK
              │
       [ 6. INSPECT ] ──────────────► Query control plane state & verify ENIs/routes
              │
       [ 7. MEASURE ] ──────────────► Quantify latency, throughput, IOPS, cold starts
              │
        [ 8. BREAK ] ───────────────► Intentionally sever connection, kill node, deny IAM
              │
      [ 9. DIAGNOSE ] ──────────────► Read CloudWatch logs, status checks, error codes
              │
      [ 10. RECOVER ] ──────────────► Implement self-healing, failover, or retry
              │
       [ 11. SECURE ] ──────────────► Apply least privilege and network isolation
              │
        [ 12. COST ] ───────────────► Calculate hourly/idle/request burn rate
              │
      [ 13. AUTOMATE ] ─────────────► Express declaratively in Infrastructure as Code
              │
      [ 14. CLEAN UP ] ─────────────► Delete all resources immediately
              │
    [ 15. VERIFY CLEANUP ] ─────────► Prove account returned to zero-cost baseline
```

---

## 4. Console vs. CLI vs. SDK vs. IaC

Understand the tool hierarchy:

```text
┌────────────────────────────────────────────────────────────────────────┐
│                          USER INTERFACES                               │
├─────────────────────┬──────────────────┬────────────────┬──────────────┤
│ AWS Console (Web)   │ AWS CLI (Shell)  │ Boto3 SDK (Py) │ IaC / CDK    │
├─────────────────────┴──────────────────┴────────────────┴──────────────┤
│                                  │                                     │
│                Signed HTTPS REST / JSON API Requests                  │
│                        (AWS SigV4 Signing)                             │
│                                  ▼                                     │
│                     AWS SERVICE CONTROL PLANES                         │
│             (ec2.amazonaws.com, s3.amazonaws.com, etc.)                │
└────────────────────────────────────────────────────────────────────────┘
```

1. **Phase 1: Console for Visual Discovery:** Use the console only when first visualizing how AWS arranges resources.
2. **Phase 2: CLI for Precise Understanding:** Use the CLI to strip away UI magic and see raw JSON structures, request parameters, and response attributes.
3. **Phase 3: Python SDK (Boto3) for Automation:** Interact programmatically to understand exception handling, pagination, and token renewal.
4. **Phase 4: Infrastructure as Code (Terraform/CloudFormation):** Automate reproducibility only **after** you understand every resource being provisioned.

---

## 5. What to Do When Stuck

When an AWS operation fails:
1. **Never guess and randomly change permissions to `*`.**
2. Check the exact error message:
   - `403 AccessDenied` → IAM identity policy, resource policy, permission boundary, or SCP.
   - `Connection timed out` → VPC routing table (missing route) or Security Group (dropped packet).
   - `Connection refused` → Traffic reached the machine, but no process is listening on that port.
   - `502 Bad Gateway` → Load Balancer reached the server, but the server returned garbage or closed the TCP connection.
   - `504 Gateway Timeout` → Load Balancer reached the server, but the server took longer to respond than the target timeout.
3. Consult [docs/troubleshooting.md](docs/troubleshooting.md) for the diagnostic flow chart.

---

## 6. The Definition of Mastery

You have mastered an AWS service when:
1. You can name the low-level computing or networking primitive it abstracts.
2. You can build a simplified working toy version in 50 lines of Python.
3. You can explain exactly how traffic flows into it and where state is preserved.
4. You know what happens when an Availability Zone loses power.
5. You can state its idle hourly cost and scaling cost vector without checking a cheatsheet.
6. You know when **NOT** to use it and what simpler alternative is better.
