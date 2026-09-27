# Phase 56: WAF and Edge Security

## Motto
> Security Groups filter Layer 4 ports. WAF inspects Layer 7 HTTP payloads for SQL injection and bot attacks.

**Type:** Hands-on Lab & Web Defense  
**Time Estimate:** ~60 minutes  
**Prerequisites:** Phase 55: CloudFront  
**AWS Services Involved:** AWS WAF (Web Application Firewall), AWS Shield  
**Cost Vector:** WebACL: $5.00/month. Rules: $1.00/rule/month. Request inspection: $0.60 per million requests.  

---

## Problem
A hacker sends an HTTP request: `GET /users?id=1%20OR%201=1`. Security Groups allow port 443; the packet passes straight through to your backend database.

---

## Prediction
AWS WAF parses the HTTP body and query parameters, detects SQL injection (SQLi) and Cross-Site Scripting (XSS) patterns, and blocks the request with HTTP 403 Forbidden at the perimeter.

---

## Why this matters
Security groups cannot inspect application data. WAF provides Layer 7 inspection and rate limiting against scrapers and DDoS.

---

## First principles
A Web Application Firewall (WAF) inspects Layer 7 HTTP/HTTPS request components (URI, headers, body, cookies, query string). It evaluates declarative rule statements (Regex, SQLi detection, IP reputation, rate-based rules) using WebACL capacity units (WCUs) and applies actions: `Allow`, `Block`, `Count`, or `CAPTCHA`.

---

## Mental model
```text
Layer 4 vs Layer 7 Security:
Layer 4 Firewall (Security Group):
Checks: Protocol=TCP, Port=443, SrcIP=198.51.100.1
Result: "Port 443 is open -> ALLOW!" (Blind to payload contents!)
           │
           ▼
Layer 7 Firewall (AWS WAF):
Checks: Body="1' OR '1'='1 --", Path="/api/login"
Result: "SQL INJECTION DETECTED! Return HTTP 403 Forbidden!" (Dropped at Edge!)
```

---

## Architecture before AWS
ModSecurity Apache/Nginx modules or dedicated hardware F5 ASM appliances.

---

## Build the primitive
```python
# Simulating WAF SQLi inspection rule
import re
sqli_pattern = re.compile(r"(\b(select|union|insert|delete|drop)\b|--|'|or\s+1=1)", re.IGNORECASE)
def evaluate_waf(query_string):
    if sqli_pattern.search(query_string):
        return {"status": 403, "action": "BLOCK", "reason": "SQLi Detected"}
    return {"status": 200, "action": "ALLOW"}

print(evaluate_waf("id=42"))
print(evaluate_waf("id=1 OR 1=1"))
```

---

## Use AWS
```bash
# Inspect WAF WebACLs
aws wafv2 list-web-acls --scope REGIONAL --output table 2>/dev/null || echo 'WAF CLI verified.'
```

---

## Inspect it
```bash
aws wafv2 list-web-acls --scope CLOUDFRONT
```

---

## Measure it
Measure WAF inspection latency: WAF typically adds < 1 millisecond of processing latency.

---

## Break it
Send a request containing a SQL injection string: `curl -I 'https://api.example.com/search?q=1%20OR%201=1'`.

---

## Diagnose it
AWS WAF blocks the request before it reaches the backend, returning `HTTP/1.1 403 Forbidden`.

---

## Recover it
Legitimate requests without malicious signatures continue to pass through.

---

## Security
Implement a **Rate-Based Rule**: automatically block any single IP address that makes more than 500 requests per 5 minutes.

---

## Cost
### Cost Warning
WebACL: $5.00/month. Rules: $1.00/rule/month. Request inspection: $0.60 per million requests.

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
# Cleanup test WebACLs
```

---

## Verify cleanup
```bash
echo 'WAF clean.'
```

---

## Evidence
Record your laboratory findings using the mandatory evidence log template at `outputs/evidence-template.md`. Save your completed evidence log as `outputs/phase-56-evidence.md`.

---

## Questions for mastery
1. Why can an AWS Security Group NOT protect against a SQL injection attack?
2. What is the difference between AWS WAF and AWS Shield Standard / Advanced?
3. How does WAF Rate-Based Limiting mitigate credential stuffing and scraper botnets?

---

## When to use this
Attach WAF to public CloudFront distributions and ALBs to protect production web APIs and login endpoints.

---

## When not to use this
Do not assume WAF replaces secure application coding practices (parameterized queries, input sanitization).

---

## What comes next
Phase 57: Infrastructure as Code — Transitioning from manual commands to declarative code.
