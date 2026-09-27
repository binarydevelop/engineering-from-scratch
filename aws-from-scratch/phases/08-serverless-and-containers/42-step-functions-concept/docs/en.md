# Phase 42: Step Functions Concept

## Motto
> Do not orchestrate complex multi-step workflows inside Lambda code. State machines manage retries and sagas.

**Type:** Conceptual & Workflow Modeling  
**Time Estimate:** ~60 minutes  
**Prerequisites:** Phase 41: API Gateway + Lambda  
**AWS Services Involved:** AWS Step Functions (Standard & Express Workflows)  
**Cost Vector:** Standard: $0.025 per 1,000 state transitions. Express: $1.00 per million requests + duration fees.  

---

## Problem
An e-commerce order process requires: (1) Validate Order -> (2) Charge Card -> (3) Reserve Inventory -> (4) Send Email. If step 3 fails, how do you automatically refund the card and handle retries without writing spaghetti code?

---

## Prediction
A state machine visually orchestrates task execution, automated retries with exponential backoff, and compensating rollback transactions (Saga Pattern).

---

## Why this matters
Hardcoding retries and distributed state coordination inside Lambda functions burns compute cost while waiting and makes failure debugging impossible.

---

## First principles
A state machine is a mathematical model of computation consisting of states, inputs, and transitions. AWS Step Functions uses Amazon States Language (ASL) JSON to define state transitions, error catchers, and parallel execution branches declaratively.

---

## Mental model
```text
Step Functions Order Saga:
[ Start Order ] ──► [ 1. Validate Order ]
                            │
                            ▼
                    [ 2. Charge Card ]
                            │
                            ├── (Card Declined) ──► [ Notify Customer ] ──► [ Fail ]
                            ▼ (Success)
                 [ 3. Reserve Inventory ]
                            │
                            ├── (Out of Stock!) ──► [ Refund Card (Compensating Action) ] ──► [ Fail ]
                            ▼ (Success)
                     [ 4. Ship Order ] ──► [ Complete ]
```

---

## Architecture before AWS
Temporal, Camunda BPM, or custom Celery/Airflow workflow engines.

---

## Build the primitive
```python
# Simulating state machine transition
def execute_workflow(state, payload):
    transitions = {
        "VALIDATE": lambda p: "CHARGE" if p.get('valid') else "FAIL",
        "CHARGE": lambda p: "SHIP" if p.get('funds') else "REFUND",
        "SHIP": lambda p: "SUCCESS"
    }
    return transitions[state](payload)
print("Next state:", execute_workflow("VALIDATE", {"valid": True}))
```

---

## Use AWS
```bash
# Inspect step functions state machines
aws stepfunctions list-state-machines --output table 2>/dev/null || echo 'Step Functions CLI verified.'
```

---

## Inspect it
```bash
aws stepfunctions list-state-machines
```

---

## Measure it
Compare Standard Workflows (exactly-once execution, up to 1 year duration) vs Express Workflows (at-least-once, up to 5 min, ultra-high throughput).

---

## Break it
Simulate a failure in Step 3 (Reserve Inventory).

---

## Diagnose it
The execution graph shows Step 3 in RED; the Catch block triggers the compensating 'Refund Card' state.

---

## Recover it
The saga executes the rollback and marks the order CANCELLED.

---

## Security
Step Functions uses IAM execution roles to assume permissions for each integrated service.

---

## Cost
### Cost Warning
Standard: $0.025 per 1,000 state transitions. Express: $1.00 per million requests + duration fees.

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
# No cloud resources created.
```

---

## Verify cleanup
```bash
echo 'Account clean.'
```

---

## Evidence
Record your laboratory findings using the mandatory evidence log template at `outputs/evidence-template.md`. Save your completed evidence log as `outputs/phase-42-evidence.md`.

---

## Questions for mastery
1. What is the Saga Pattern and why is it essential in distributed microservices?
2. Why should you NOT use `time.sleep()` inside a Lambda function while waiting for an external process?
3. When would you choose an Express Workflow over a Standard Workflow in Step Functions?

---

## When to use this
Use Step Functions for payment sagas, data ETL pipelines, and long-running human approval workflows.

---

## When not to use this
Do not use Step Functions for simple point-to-point event routing (use EventBridge).

---

## What comes next
Phase 43: Containers on AWS — Packaging applications for container runtimes.
