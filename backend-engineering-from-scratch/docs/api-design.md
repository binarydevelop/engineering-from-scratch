# API Design Discipline & Contract Engineering

> **Contract First**: An API is an immutable public contract with outside systems. Once clients depend on your schema, wire format, and error semantics, casual changes break downstream consumers.

---

## The 10 Questions for Every Endpoint

Before writing a single line of endpoint code, the backend engineer must answer these 10 questions:

1. **What resource or use-case is represented?**
   - Use nouns for resources (`/orders`, `/users/42/keys`). Avoid RPC-style verb URLs (`/createOrder`, `/doUpdateUser`) in RESTful interfaces unless explicitly modeling an action resource (`/orders/42/cancel`).
2. **What is the strict request contract?**
   - Exactly which fields are accepted? What are their types, lengths, string patterns, and nullability?
   - Reject unexpected fields or unknown query parameters.
3. **What is the response contract?**
   - Never return raw database entity rows directly. Database columns change; API schemas must remain stable. Use explicit Data Transfer Objects (DTOs) / Pydantic schemas.
4. **What validation exists?**
   - Distinguish *syntactic validation* (e.g. valid email format, positive integer quantity) from *semantic domain validation* (e.g. account has sufficient credit, warehouse holds stock).
5. **What HTTP status code should every scenario use?**
   - `200 OK`: Successful retrieval or synchronous mutation with response body.
   - `201 Created`: Resource successfully created (include `Location` header where appropriate).
   - `204 No Content`: Successful mutation where no body is returned (e.g. `DELETE`).
   - `400 Bad Request`: Malformed syntax or invalid query parameters.
   - `401 Unauthorized`: Authentication missing or cryptographically invalid.
   - `403 Forbidden`: Authenticated caller lacks authorization for this specific resource.
   - `404 Not Found`: Resource does not exist or caller should not know it exists.
   - `409 Conflict`: State conflict (unique constraint violation, concurrent edit, race).
   - `422 Unprocessable Entity`: Syntactically valid JSON failing domain schema rules.
   - `429 Too Many Requests`: Rate limit quota exhausted (include `Retry-After`).
   - `500 Internal Server Error`: Unhandled server exception (sanitized, with correlation ID).
   - `502 / 503 / 504`: Upstream gateway or dependency failure/timeout.
6. **Is the operation idempotent?**
   - `GET`, `PUT`, `DELETE`, `HEAD`, `OPTIONS` are idempotent by HTTP specification.
   - `POST` is not idempotent by default. If it causes financial charges or side effects, require an `Idempotency-Key` header.
7. **Can the request be safely retried?**
   - Network timeouts on non-idempotent operations must NOT be retried automatically by clients without deduplication keys.
8. **Does it need pagination, and what strategy should be used?**
   - Never return unbounded arrays (`SELECT * FROM items`). Always enforce pagination.
   - For shallow, random-access admin tables: **Offset Pagination** (`limit`, `offset`).
   - For high-volume, deep scrolling, or infinite feeds: **Keyset / Cursor Pagination** (`limit`, `after_id`).
9. **Does the response expose internal implementation details?**
   - Never leak internal primary keys, foreign key UUIDs of internal services, database table names, SQL error messages, or internal microservice IP addresses in public responses.
10. **What load could this endpoint create?**
    - Could a client call this endpoint in a tight loop and trigger an $O(N)$ table scan, a memory leak, or a cache stampede? Enforce rate limiting, bounded query limits, and proper indexes.
