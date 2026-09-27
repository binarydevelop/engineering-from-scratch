# Phase 60: Rebuild Application Stack With IaC

## Motto
> The entire application stack—API Gateway, Lambda, and DynamoDB—deployed and destroyed in a single command.

**Type:** Hands-on Lab & Full Stack Automation  
**Time Estimate:** ~60 minutes  
**Prerequisites:** Phase 59: Rebuild VPC With IaC  
**AWS Services Involved:** CloudFormation, Serverless API Stack  
**Cost Vector:** Zero running cost ($0.00/month while idle).  

---

## Problem
Setting up an API Gateway, Lambda execution role, Lambda function, and DynamoDB table with least-privilege IAM requires 15 distinct CLI commands and careful ARN wiring.

---

## Prediction
Deploying `infrastructure/serverless-api.yaml` provisions the complete serverless architecture, wires IAM permissions automatically, and exposes a live HTTPS endpoint in 60 seconds.

---

## Why this matters
Demonstrates the power of end-to-end infrastructure automation with zero ongoing idle cost.

---

## First principles
The CloudFormation template wires dependencies: the DynamoDB Table ARN is passed into the Lambda IAM Role policy; the Role ARN is passed into the Lambda Function; the Lambda ARN is attached to the API Gateway. The entire stack deploys atomically.

---

## Mental model
```text
Serverless IaC Stack Dependency Flow:
[ DynamoDB Table ] ──(Generates Arn)──► [ IAM Role Policy ]
                                                │
                                                ▼ (Generates RoleArn)
                                        [ Lambda Function ]
                                                │
                                                ▼ (Generates FunctionArn)
                                        [ API Gateway HTTP API ]
```

---

## Architecture before AWS
Deploying bare-metal database servers, configuring application runtimes, and setting up reverse proxies manually.

---

## Build the primitive
```python
# Inspecting serverless template outputs
with open('infrastructure/serverless-api.yaml') as f:
    print("Template verified:", "AWS::Lambda::Function" in f.read())
```

---

## Use AWS
```bash
aws cloudformation deploy --template-file infrastructure/serverless-api.yaml --stack-name aws-from-scratch-serverless --capabilities CAPABILITY_NAMED_IAM
```

---

## Inspect it
```bash
aws cloudformation describe-stack-resources --stack-name aws-from-scratch-serverless --output table
```

---

## Measure it
Measure total teardown duration: `aws cloudformation delete-stack` purges all resources in ~35 seconds.

---

## Break it
Remove `CAPABILITY_NAMED_IAM` when deploying a template that creates IAM roles.

---

## Diagnose it
The CLI rejects deployment with `RequiresCapabilities: [CAPABILITY_NAMED_IAM]` as a security safeguard.

---

## Recover it
Include `--capabilities CAPABILITY_NAMED_IAM` to explicitly acknowledge IAM role creation.

---

## Security
The template grants the Lambda role access ONLY to the specific DynamoDB table created by the stack.

---

## Cost
### Cost Warning
Zero running cost ($0.00/month while idle).

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
aws cloudformation delete-stack --stack-name aws-from-scratch-serverless
```

---

## Verify cleanup
```bash
aws cloudformation wait stack-delete-complete --stack-name aws-from-scratch-serverless
```

---

## Evidence
Record your laboratory findings using the mandatory evidence log template at `outputs/evidence-template.md`. Save your completed evidence log as `outputs/phase-60-evidence.md`.

---

## Questions for mastery
1. Why does AWS CloudFormation require an explicit flag (`CAPABILITY_NAMED_IAM`) when templates create IAM resources?
2. What happens if a stack update replaces a DynamoDB table? (Hint: DeletionPolicy / UpdateReplacePolicy).
3. How do Nested Stacks help manage huge architectures that exceed CloudFormation resource limits?

---

## When to use this
Use declarative application stacks for reproducible testing, staging, and production environments.

---

## When not to use this
Do not mix stateful production databases into ephemeral application stacks that are frequently destroyed.

---

## What comes next
Phase 61: Reliability From First Principles — Quantifying system failure modes.
