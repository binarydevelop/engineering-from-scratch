# Packet Capture Exercise: HTTP Persistent Connection Reuse

> **Motto**: Understand it. Predict it. Send it. Capture it. Dissect it.

---

## 1. Objective
Reuse TCP handshake.

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
Request 1 and Request 2 exchange payloads sequentially over the exact same (src_ip, src_port <-> dst_ip, 8080) 4-tuple.
```

## 5. Mastery Reasoning Question
> **Question**: What performance advantage does Keep-Alive provide over opening a new TCP connection?

Document your empirical findings in `outputs/evidence-template.md`.
