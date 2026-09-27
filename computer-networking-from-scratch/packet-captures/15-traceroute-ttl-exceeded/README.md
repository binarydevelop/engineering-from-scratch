# Packet Capture Exercise: Traceroute (ICMP Time Exceeded)

> **Motto**: Understand it. Predict it. Send it. Capture it. Dissect it.

---

## 1. Objective
Discover network path hops.

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
sudo tcpdump -i <interface> -nn -vvv -s0 "icmp or udp"
```

## 4. Annotated Wire Dissection
```text
Packet 1: Probe sent with TTL=1
Packet 2: Router 1 > Client: ICMP time exceeded in-transit (Type 11 Code 0)
```

## 5. Mastery Reasoning Question
> **Question**: Why do some hops in traceroute output display as asterisks (* * *)?

Document your empirical findings in `outputs/evidence-template.md`.
