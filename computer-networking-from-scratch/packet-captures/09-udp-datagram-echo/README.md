# Packet Capture Exercise: UDP Datagram Transmission

> **Motto**: Understand it. Predict it. Send it. Capture it. Dissect it.

---

## 1. Objective
Send independent datagram.

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
sudo tcpdump -i <interface> -nn -vvv -s0 "udp and port 9999"
```

## 4. Annotated Wire Dissection
```text
Packet 1: Client.54321 > Server.9999: UDP, length 12
Packet 2: Server.9999 > Client.54321: UDP, length 12
```

## 5. Mastery Reasoning Question
> **Question**: What happens to the application when an intermediate router drops a UDP packet?

Document your empirical findings in `outputs/evidence-template.md`.
