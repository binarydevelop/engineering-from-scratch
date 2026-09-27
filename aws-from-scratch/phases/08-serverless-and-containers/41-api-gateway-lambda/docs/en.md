# Phase 41: API Gateway + Lambda

## Motto
> API Gateway is the HTTP front door. Lambda is the compute brain. Together, they create a zero-idle-cost API.

**Type:** Hands-on Lab & Serverless REST API  
**Time Estimate:** ~60 minutes  
**Prerequisites:** Phase 40: Lambda Lifecycle  
**AWS Services Involved:** Amazon API Gateway (HTTP API v2), AWS Lambda  
**Cost Vector:** API Gateway HTTP APIs cost $1.00 per million requests. Zero idle cost ($0.00 when traffic is zero).  

---

## Problem
Lambda functions cannot be reached by a client browser directly without signed AWS IAM requests. Web applications need standard public HTTPS endpoints.

---

## Prediction
API Gateway HTTP APIs will receive public HTTP requests, translate the headers and body into a JSON event payload, invoke Lambda, and translate the return JSON into an HTTP response.

---

## Why this matters
This is Project 03 in the curriculum and the architecture behind thousands of production serverless APIs.

---

## First principles
API Gateway is a managed Layer 7 reverse proxy. It terminates TLS, validates request paths, enforces rate limits and authorization, formats the HTTP request into a proxy event payload (`APIGatewayProxyRequestEvent`), invokes Lambda synchronously (`RequestResponse`), and unpacks the returned JSON status code and body to send back to the client.

---

## Mental model
```text
API Gateway + Lambda Proxy Integration:
[ Browser Client ]
        │
        │ 1. HTTPS POST /orders (Body: {"item": "book"})
        ▼
[ Amazon API Gateway (HTTP API v2) ]
        │ 2. Transforms HTTP into JSON Event Payload:
        │    { "rawPath": "/orders", "body": "...", "headers": {...} }
        ▼
[ AWS Lambda (orders-function) ]
        │ 3. Executes Python handler:
        │    return {"statusCode": 201, "body": json.dumps({"order_id": 99})}
        ▼
[ Amazon API Gateway ]
        │ 4. Translates Lambda dict back into real HTTP response
        ▼
[ Browser Receives: HTTP 201 Created ]
```

---

## Architecture before AWS
Configuring Nginx reverse proxy passing requests to Gunicorn / UWSGI Python processes.

---

## Build the primitive
```python
# Simulating API Gateway proxy event translation
raw_http = "POST /api/orders HTTP/1.1\r\nHost: api.example.com\r\n\r\n{\"item\": \"widget\"}"
proxy_event = {"rawPath": "/api/orders", "body": '{"item": "widget"}', "requestContext": {"http": {"method": "POST"}}}
print("API Gateway Proxy Event generated:", proxy_event)
```

---

## Use AWS
```bash
aws apigatewayv2 create-api --name lab-api --protocol-type HTTP --target $LAMBDA_ARN --tags Project=aws-from-scratch
```

---

## Inspect it
```bash
aws apigatewayv2 get-apis --query 'Items[].[ApiId,Name,ApiEndpoint]' --output table
```

---

## Measure it
Measure round-trip latency via curl: `curl -w '@scripts/curl-format.txt' https://$API_ID.execute-api.us-east-1.amazonaws.com/orders`.

---

## Break it
Return a string from Lambda instead of a dictionary with `statusCode` and `body`.

---

## Diagnose it
API Gateway returns HTTP 500 Internal Server Error because it cannot parse the Lambda return contract.

---

## Recover it
Ensure Lambda returns `{'statusCode': 200, 'body': json.dumps(...)}`.

---

## Security
Configure API Gateway JWT authorizers or Lambda authorizers to validate OAuth2 / Cognito tokens before invoking backend compute.

---

## Cost
### Cost Warning
API Gateway HTTP APIs cost $1.00 per million requests. Zero idle cost ($0.00 when traffic is zero).

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
aws apigatewayv2 delete-api --api-id $API_ID
```

---

## Verify cleanup
```bash
echo 'API Gateway cleaned.'
```

---

## Evidence
Record your laboratory findings using the mandatory evidence log template at `outputs/evidence-template.md`. Save your completed evidence log as `outputs/phase-41-evidence.md`.

---

## Questions for mastery
1. Why are API Gateway HTTP APIs (v2) over 70% cheaper than legacy REST APIs (v1)?
2. What is the difference between Lambda Proxy Integration and Lambda Non-Proxy Integration?
3. How does API Gateway default throttling prevent a sudden traffic surge from crushing downstream databases?

---

## When to use this
Use API Gateway + Lambda for serverless microservices, webhooks, and spiky REST APIs.

---

## When not to use this
Do not use API Gateway for high-frequency steady-state APIs (> 50M requests/mo); ALB + ECS is significantly cheaper at high sustained volumes.

---

## What comes next
Phase 42: Step Functions Concept — Orchestrating multi-step serverless workflows.
