# Lesson 43: CORS

> **Motto**: Cross-Origin Resource Sharing is a browser-enforced security mechanism governing cross-domain HTTP requests.

---

## Motto
"Cross-Origin Resource Sharing is a browser-enforced security mechanism governing cross-domain HTTP requests."

## Problem
Developers think CORS is a server security firewall, leading them to blindly configure `allow_origins=['*']`.

## Prediction
CORS protects users in browsers from malicious websites executing unauthorized API calls using cached credentials.

## Why this matters
CORS does NOT protect APIs from cURL, mobile apps, or backend servers; it is strictly a browser sandbox protocol.

## First principles
Browser sends Preflight `OPTIONS` -> Server returns allowed origins/methods -> Browser allows or blocks JavaScript access.

## Mental model
```text
Browser (domain-a.com) -> HTTP OPTIONS /api -> Server checks Origin -> Returns Access-Control-Allow-Origin: domain-a.com
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: FastAPI CORSMiddleware configuration with explicit allowed origins.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/43-cors/tests/ -v
```

## Inspect it
Observe state directly using operating system, network, or database inspection:
- Inspect raw bytes, socket buffers, or table schemas
- Verify that request transformations match protocol specifications

## Measure it
Quantify latency and resource consumption:
- Measure response latency percentiles (p50, p95, p99)
- Profile memory allocations and database connection usage under load

## Break it
Inject an intentional failure to observe divergence from expected behavior:
- **Failure Injection**: Send an API request from an unauthorized Origin header; observe browser console block and server headers.
- Execute the experiment script:
```bash
python phases/43-cors/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Inspect preflight headers; verify `Access-Control-Allow-Origin` is omitted for unauthorized origins.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Never set `allow_origins=['*']` when `allow_credentials=True`; browsers explicitly reject this combination.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Wildcard CORS with credentials allows any malicious website visited by a user to read their private API data.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: CORS headers must be set on error responses (4xx/5xx) as well, or browser clients will see misleading CORS errors.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. Why is CORS enforced by web browsers but ignored by tools like cURL and Postman?
2. What is a CORS preflight OPTIONS request and when is it triggered?
3. Why is setting `Access-Control-Allow-Origin: *` dangerous when credentials are enabled?

## What comes next
Having understood cors, we next discover its inherent boundaries and transition to **CSRF**.
