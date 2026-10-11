# Phase 140: gRPC Deep-Dive: HTTP/2 Framing, Protobuf Serialization, and Deadlines

## 1. Why This Matters for MAANG & Senior/Staff Roles
In high-performance microservice meshes (Google Stubby/gRPC, Netflix, Uber), REST over HTTP/1.1 is deprecated for internal east-west traffic. gRPC provides high-performance, strictly typed RPC communication built on HTTP/2 multiplexing and Protocol Buffers. Senior engineers must explain the binary wire format, multiplexed streams, deadline propagation, and load balancing.

---

## 2. Core Concepts & Architecture Deep-Dive
### Core Architecture: Why gRPC Dominates East-West Traffic
1. **HTTP/2 Transport Layer**:
   - Single long-lived TCP connection per host pair.
   - **Stream Multiplexing**: Thousands of concurrent bidirectional requests/responses interleave binary frames across a single TCP socket, eliminating head-of-line blocking and connection handshake overhead.
   - **HPACK Header Compression**: Compresses repetitive headers (auth tokens, path), reducing network overhead by 80%.
2. **Protocol Buffers (Protobuf)**:
   - Compact binary serialization using varints and field tags.
   - Schema defined in `.proto` files acts as the contract; code generation produces client stubs and server interfaces across languages (Java, Go, C++, Python).
3. **Four Communication Patterns**:
   - Unary RPC (1 request -> 1 response).
   - Server Streaming (1 request -> stream of responses).
   - Client Streaming (stream of requests -> 1 response).
   - Bidirectional Streaming (stream of requests <-> stream of responses).

---

## 3. High-Value Interview Angle & Failure Modes
### High-Value Production Patterns
- **Context Deadlines & Cancellation**: If Service A sets a 500ms deadline and calls Service B which calls Service C, the remaining time budget is automatically propagated down the call chain via `grpc-timeout` headers. If Service A cancels or times out, Services B and C terminate immediately, preventing wasted compute.
- **Client-Side vs Proxy Load Balancing**:
  Because HTTP/2 maintains a single long-lived TCP connection, traditional L4 load balancers send all traffic to a single backend pod. Solution:
  1. *Client-side LB*: Client queries headless service DNS/service discovery and round-robins across backend pod IPs.
  2. *L7 Proxy LB*: Envoy sidecars intercept and load-balance requests at the stream level.

---

## 4. Hands-On Practice & Implementation Drills
### Protobuf Definition & Java Stub Drill
```protobuf
syntax = "proto3";

package payment.v1;

service PaymentService {
  // Unary payment charge
  rpc ProcessPayment (PaymentRequest) returns (PaymentResponse);
  
  // Server streaming transaction ledger
  rpc StreamTransactions (AccountRequest) returns (stream TransactionEvent);
}

message PaymentRequest {
  string idempotency_key = 1;
  int64 amount_cents = 2;
  string currency = 3;
}

message PaymentResponse {
  string transaction_id = 1;
  enum Status { SUCCESS = 0; FAILED = 1; }
  Status status = 2;
}
```

---

## 5. Key Takeaways & Cheat Sheet
- gRPC utilizes HTTP/2 binary framing and Protocol Buffers.
- Multiplexing allows thousands of RPCs over a single TCP connection.
- Deadline propagation prevents cascaded resource waste during timeouts.
- Requires L7 load balancing (Envoy) or client-side load balancing due to long-lived TCP connections.
