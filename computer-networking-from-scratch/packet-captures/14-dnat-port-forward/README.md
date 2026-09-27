# Packet Capture Exercise: Destination NAT (DNAT / Port Forwarding)

> **Motto**: Understand it. Predict it. Send it. Capture it. Dissect it.

---

## 1. Objective
Forward external port to internal service.

## 2. Hypothesis & Packet Prediction
Before running the capture, predict the sequence of frames:
```text
┌───────────────────────┬────────────────────────────────────────────────────────┐
│ Header Layer          │ Predicted Values / Flags                               │
├───────────────────────┼────────────────────────────────────────────────────────┤
│ Layer 2 (Ethernet II) │ Source MAC, Destination MAC, EtherType                 │
│ Layer 3 (IP)          │ Source IP, Destination IP, TTL, Protocol               │
│ Layer 4 (Transport)   │ Source Port, Destination Port, Flags, Seq/Ack          │
│ Layer 7 (Application) │ Command / Payload / Delimiters                         │
└───────────────────────┴────────────────────────────────────────────────────────┘
```

## 3. tcpdump Capture Command
```bash
sudo tcpdump -i <interface> -nn -vvv -s0 "tcp port 8080"
```

## 4. Annotated Wire Dissection
```text
Ingress on Host:  203.0.113.10:8080 > 192.168.1.1:8080
Forwarded to App: 203.0.113.10:8080 > 10.0.2.10:80
```

## 5. Mastery Reasoning Question
> **Question**: Why must DNAT rules be placed in the PREROUTING chain rather than the POSTROUTING chain?

Document your empirical findings in `outputs/evidence-template.md`.
