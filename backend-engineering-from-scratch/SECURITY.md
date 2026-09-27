# Backend Security Discipline & Vulnerability Policy

> **Security by Design**: Security is not a feature added at the end of development; it is an architectural invariant embedded in every network boundary, query, and persistence layer.

---

## 1. Core Security Principles in Backend Systems

### 1.1 Password Storage and Hashing
- **Never store plaintext passwords**: Passwords must always be hashed using an adaptive work-factor algorithm with a cryptographically random per-user salt.
- **Approved Algorithms**: `bcrypt` (work factor >= 12) or `Argon2id` (RFC 9106).
- **Prohibited**: Plain MD5, SHA-1, SHA-256, or unsalted hashing algorithms. Fast general-purpose hashing functions allow trillions of guesses per second on commodity GPUs.

### 1.2 SQL Injection Prevention
- **Always parameterize queries**: Never concatenate raw user input into SQL strings (`f"SELECT * FROM users WHERE id = {user_id}"`).
- **Use Driver Placeholders**: Use parameterized query placeholders (`?` in SQLite, `%s` in psycopg) so the database query parser treats input strictly as data, never as executable code.
- **Strict Whitelisting for Dynamic Clauses**: Table names, column names, and `ORDER BY` directions cannot be parameterized in SQL drivers. Any dynamic identifier must be checked against an explicit, hardcoded whitelist.

### 1.3 Strict Input Validation & Resource Limits
- **Validate at the System Boundary**: Deserialization is a vulnerability surface. Use strict schema validation (Pydantic / dataclasses) verifying data types, string length, regex formats, and numeric ranges.
- **Enforce Input Size Limits**: Reject oversized JSON payloads (e.g. max 1MB) and large file uploads early before reading entire buffers into RAM.

### 1.4 Authentication & Token Safety
- **Cryptographic Signatures**: Bearer tokens (JWTs) must be cryptographically signed using secure keys (HS256 with >= 256-bit entropy or RS256/Ed25519).
- **Alg: None Rejection**: Explicitly enforce the allowed signature algorithm and reject tokens with `"alg": "none"`.
- **Token Expiration**: Always specify and enforce token expiration (`exp` claim) to limit the attack window if credentials leak.
- **Session Cookies**: When using session cookies, enforce `HttpOnly` (mitigates XSS cookie theft), `Secure` (HTTPS only), and `SameSite=Lax` or `SameSite=Strict`.

### 1.5 Authorization (Access Control)
- **Separate AuthN from AuthZ**: Authentication verifies *who* the caller is; authorization verifies *what* the caller is permitted to do.
- **Object-Level / Tenant Scoping**: Never rely solely on high-level role checks (e.g. `is_admin`). Always verify that the authenticated caller owns or has explicit rights to the specific target entity ID (`WHERE tenant_id = :tenant_id AND id = :id`).

### 1.6 Cross-Origin Resource Sharing (CORS)
- **Never allow `Access-Control-Allow-Origin: *` with credentials**: Wildcard origins combined with cookies or Authorization headers compromise browser security boundaries.
- **Whitelist Specific Origins**: Explicitly list trusted client domains.

### 1.7 Cross-Site Request Forgery (CSRF)
- **Token vs Cookie Protection**: Token-based APIs using custom `Authorization: Bearer` headers are immune to CSRF in browsers because browsers do not automatically attach custom headers to cross-site requests.
- **Cookie Authentication**: When cookie authentication is used for state-modifying requests (POST, PUT, DELETE), CSRF anti-forgery tokens (Double Submit Cookie or Synchronizer Token) are mandatory.

### 1.8 Rate Limiting & Denial of Service Defense
- **Per-IP and Per-User Throttling**: Protect authentication endpoints (login, password reset) with strict rate limits (e.g. 5 requests/minute) to prevent brute-force attacks.
- **Defensive Timeouts**: Configure socket read timeouts, gateway timeouts, and database statement timeouts to prevent connection exhaustion.

### 1.9 Secret Management & Environment Hygiene
- **Never commit secrets to Git**: Passwords, API tokens, and encryption keys must never appear in source code or default configuration files.
- **Use Environment Variables**: Inject secrets at runtime via `.env` files (excluded by `.gitignore`) or cloud secret managers.

### 1.10 Logging Hygiene & Sensitive Data Redaction
- **No Secrets in Logs**: Never log passwords, payment card numbers, authorization tokens, or sensitive personal identifiable information (PII).
- **Redaction Middleware**: Sanitize headers and request bodies before emitting structured logs.

---

## 2. Insecure Educational Labs Policy

Certain debugging labs in `broken-systems/` deliberately contain security flaws (such as SQL injection or CSRF vulnerabilities) for educational analysis:
- All vulnerable examples are isolated strictly in local testing environments.
- Every vulnerable scenario is labeled with `[VULNERABLE - LOCAL LAB ONLY]`.
- Every broken lab is paired with a corresponding fixed implementation demonstrating proper defense.
