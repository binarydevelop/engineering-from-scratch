# Phase 39: Lambda From First Principles

## Motto
> Serverless does not mean no servers: it means you do not manage, provision, or pay for idle servers.

**Type:** Hands-on Lab & Serverless Compute  
**Time Estimate:** ~60 minutes  
**Prerequisites:** Phase 03: IAM From First Principles  
**AWS Services Involved:** AWS Lambda, Firecracker Micro-VMs  
**Cost Vector:** First 1,000,000 requests and 3,200,000 seconds of compute time per month are free permanently under the AWS Free Tier.  

---

## Problem
Running an EC2 instance 24/7 to execute an image resizing script that runs twice a day costs $15/month for 99.9% idle time.

---

## Prediction
AWS Lambda will boot an ephemeral micro-VM in milliseconds upon receiving an event, execute the Python function, and bill strictly for execution duration.

---

## Why this matters
Lambda changed cloud computing economics by moving from provisioned capacity to pure utility consumption.

---

## First principles
AWS Lambda runs on **Firecracker**, an open-source lightweight virtualization technology built on Linux KVM. Firecracker boots minimalist micro-VMs in ~5 milliseconds with < 5MB memory footprint. Lambda executes your handler function within this isolated micro-VM, freezes it upon completion, and destroys it when idle.

---

## Mental model
```text
AWS Lambda Firecracker Execution:
[ Trigger Event (S3 / API / SQS) ]
                │
                ▼
[ Lambda Worker Host ] ──► Spawns Firecracker Micro-VM (~5ms)
                                └── Boots Guest Linux Kernel
                                └── Mounts Customer Code
                                └── Runs handler(event, context)
                                └── Flushes Logs to CloudWatch
                                └── Micro-VM Freezes or Destroys
```

---

## Architecture before AWS
Cron daemons running Python scripts on dedicated Linux virtual machines.

---

## Build the primitive
```python
# Standard Lambda Handler Structure
def lambda_handler(event, context):
    name = event.get('name', 'Cloud Engineer')
    return {
        'statusCode': 200,
        'body': f'Hello from first-principles Lambda, {name}!'
    }
print(lambda_handler({'name': 'Alice'}, None))
```

---

## Use AWS
```bash
aws lambda create-function --function-name lab-hello --runtime python3.12 --role $ROLE_ARN --handler index.lambda_handler --zip-file fileb://function.zip --tags Project=aws-from-scratch
```

---

## Inspect it
```bash
aws lambda get-function --function-name lab-hello --output json
```

---

## Measure it
Measure execution duration in CloudWatch logs: `Billed Duration: 24 ms Memory Size: 128 MB Max Memory Used: 42 MB`.

---

## Break it
Set memory to 128MB and run a CPU-intensive matrix multiplication loop.

---

## Diagnose it
The function times out after 3.0 seconds because Lambda CPU scales proportionally with allocated RAM.

---

## Recover it
Increase memory to 1024MB; execution time drops to 150ms.

---

## Security
Enforce strict IAM Execution Roles: grant the function access ONLY to the specific S3 buckets or DynamoDB tables it needs.

---

## Cost
### Cost Warning
First 1,000,000 requests and 3,200,000 seconds of compute time per month are free permanently under the AWS Free Tier.

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
aws lambda delete-function --function-name lab-hello
```

---

## Verify cleanup
```bash
echo 'Lambda function deleted.'
```

---

## Evidence
Record your laboratory findings using the mandatory evidence log template at `outputs/evidence-template.md`. Save your completed evidence log as `outputs/phase-39-evidence.md`.

---

## Questions for mastery
1. How does AWS Lambda allocate CPU cores to a function based on memory configuration?
2. Why is an execution duration limit of 15 minutes enforced on AWS Lambda?
3. Why should database connection initialization code be placed OUTSIDE the `lambda_handler` function?

---

## When to use this
Use Lambda for event-driven processing, asynchronous queue workers, HTTP APIs, and scheduled maintenance tasks.

---

## When not to use this
Do not use Lambda for continuous long-running processes (> 15 mins), heavy GPU model training, or stateful websockets.

---

## What comes next
Phase 40: Lambda Lifecycle — Cold starts vs warm reuse.
