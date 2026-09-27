# Phase 21: DNS and Route 53

## Motto
> DNS is the phonebook of the internet. Route 53 ALIAS records solve the apex zone CNAME problem.

**Type:** Hands-on Lab & DNS Resolution  
**Time Estimate:** ~60 minutes  
**Prerequisites:** Phase 20: Static Website / Object Delivery  
**AWS Services Involved:** Amazon Route 53 Hosted Zones, ALIAS Records  
**Cost Vector:** Hosted Zones cost $0.50 per month each. Standard queries cost $0.40 per million queries. (Labs can use dry-run simulation to avoid the $0.50 cost).  

---

## Problem
Users cannot remember `d111111abcdef8.cloudfront.net` or `54.210.10.5`. Furthermore, standard DNS RFCs forbid CNAME records at the zone apex (`example.com`).

---

## Prediction
Querying a Route 53 ALIAS record for `example.com` resolves directly to CloudFront or ALB Anycast IP addresses without adding an extra CNAME lookup hop.

---

## Why this matters
DNS misconfigurations cause catastrophic multi-hour propagation delays. Understanding authoritative nameservers, TTLs, and ALIAS records is vital.

---

## First principles
DNS is a hierarchical distributed database. Resolvers query Root (.) -> TLD (.com) -> Authoritative Nameservers. Route 53 is an authoritative Anycast DNS server operating on Port 53 (UDP/TCP). Route 53 ALIAS records are internal pointers that resolve AWS resource hostnames to direct A records dynamically.

---

## Mental model
```text
DNS Resolution Hierarchy:
[ Client Query: api.example.com ]
                │
                ▼
1. Root Nameserver (.) ──► "Go ask .com nameserver"
                │
                ▼
2. TLD Nameserver (.com) ──► "Go ask Route 53 Authoritative Nameservers: ns-xxx.awsdns.com"
                │
                ▼
3. Route 53 Authoritative Nameserver ──► Returns IP: 54.210.10.5 (TTL: 300)
```

---

## Architecture before AWS
Hosting BIND9 DNS servers on physical machines with master-slave zone transfers (AXFR).

---

## Build the primitive
```python
# DNS query inspection via socket
import socket
ip = socket.gethostbyname("aws.amazon.com")
print(f"aws.amazon.com resolved to: {ip}")
```

---

## Use AWS
```bash
# List Route 53 hosted zones
aws route53 list-hosted-zones --output table
```

---

## Inspect it
```bash
dig +trace aws.amazon.com
```

---

## Measure it
Measure DNS lookup latency: cached local resolver (< 1ms) vs recursive uncached authoritative query (40-80ms).

---

## Break it
Configure a DNS record with a TTL of 86400 (24 hours) and then change the IP address.

---

## Diagnose it
Clients continue hitting the old IP address for up to 24 hours because intermediate recursive resolvers cache the old record.

---

## Recover it
Use low TTLs (60-300 seconds) during migrations and deployments.

---

## Security
Enable DNSSEC to prevent DNS cache poisoning and man-in-the-middle spoofing attacks.

---

## Cost
### Cost Warning
Hosted Zones cost $0.50 per month each. Standard queries cost $0.40 per million queries. (Labs can use dry-run simulation to avoid the $0.50 cost).

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
# Delete test hosted zones if created
```

---

## Verify cleanup
```bash
echo 'Route 53 clean.'
```

---

## Evidence
Record your laboratory findings using the mandatory evidence log template at `outputs/evidence-template.md`. Save your completed evidence log as `outputs/phase-21-evidence.md`.

---

## Questions for mastery
1. Why does DNS RFC 1034 forbid a CNAME record at the zone apex (`example.com`), and how does a Route 53 ALIAS record solve this?
2. What is the difference between Weighted Routing, Latency-Based Routing, and Geolocation Routing?
3. How do Route 53 DNS Health Checks trigger automatic failover to a standby region?

---

## When to use this
Use Route 53 for public authoritative DNS and private VPC internal service resolution.

---

## When not to use this
Do not purchase unnecessary public domains for learning labs when local `/etc/hosts` or dry-run inspection suffices.

---

## What comes next
Phase 22: Load Balancing From Scratch — Building a reverse proxy to balance traffic across multiple servers.
