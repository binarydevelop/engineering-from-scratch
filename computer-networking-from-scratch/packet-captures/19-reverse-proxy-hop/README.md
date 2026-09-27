# Packet Capture Exercise: Reverse Proxy Two-Legged Transfer

> **Motto**: Understand it. Predict it. Send it. Capture it. Dissect it.

---

## 1. Objective
Inspect client vs backend hops.

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
sudo tcpdump -i <interface> -nn -vvv -s0 "port 80 or port 8080"
```

## 4. Annotated Wire Dissection
```text
Leg 1: Client > Proxy:80 (GET / HTTP/1.1)
Leg 2: Proxy:52000 > Backend:8080 (GET / HTTP/1.1\r\nX-Forwarded-For: ClientIP)
```

## 5. Mastery Reasoning Question
> **Question**: Why does the backend application server see the reverse proxy's IP address as the socket source?

Document your empirical findings in `outputs/evidence-template.md`.
