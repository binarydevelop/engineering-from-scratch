# Project 03: RFC 1035 UDP DNS Server & Cache

> **Motto**: DNS is an in-memory distributed key-value store queried using lightweight UDP datagrams containing binary length-prefixed domain labels.

---

## 1. Overview
In this project, you construct a functional Domain Name System (DNS) server listening on UDP port 5353. It decodes standard RFC 1035 query packets, extracts QNAME and QTYPE fields, performs in-memory lookup with TTL caching, and packages valid DNS responses that standard CLI utilities like `dig` parse seamlessly.

## 2. Packet Flow
```text
Client (dig) ──[ UDP Query: example.com (Type A) ]──► DNS Server
                                                      ├─ Parse QNAME
                                                      ├─ Check Cache
                                                      └─ Construct Response
Client (dig) ◄──[ UDP Response: 93.184.216.34 ]───────
```

## 3. Running the Server
```bash
python3 dns_server.py 5353

# In another terminal:
dig @127.0.0.1 -p 5353 example.com
dig @127.0.0.1 -p 5353 api.internal
dig @127.0.0.1 -p 5353 invalid.domain
```

## 4. Test Suite
```bash
python3 test_dns.py
```
