# Packet Capture Exercise: Plaintext HTTP/1.1 Request/Response

> **Motto**: Understand it. Predict it. Send it. Capture it. Dissect it.

---

## 1. Objective
Exchange application data.

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
sudo tcpdump -i <interface> -nn -vvv -s0 "tcp port 80"
```

## 4. Annotated Wire Dissection
```text
1. Client > Server: GET /index.html HTTP/1.1\r\nHost: example.com
2. Server > Client: HTTP/1.1 200 OK\r\nContent-Length: 45\r\n\r\n<html>...</html>
```

## 5. Mastery Reasoning Question
> **Question**: How does HTTP/1.1 delineate where the headers end and the body begins?

Document your empirical findings in `outputs/evidence-template.md`.
