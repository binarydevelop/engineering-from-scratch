# Packet Capture Exercise: TLS 1.3 Handshake Metadata

> **Motto**: Understand it. Predict it. Send it. Capture it. Dissect it.

---

## 1. Objective
Encrypt connection.

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
sudo tcpdump -i <interface> -nn -vvv -s0 "tcp port 443"
```

## 4. Annotated Wire Dissection
```text
1. Client > Server: ClientHello (Cipher Suites, Supported Groups, Key Share)
2. Server > Client: ServerHello, ChangeCipherSpec, EncryptedExtensions, Finished
```

## 5. Mastery Reasoning Question
> **Question**: Why does TLS 1.3 require only 1 round-trip time (1-RTT) compared to TLS 1.2's 2-RTT?

Document your empirical findings in `outputs/evidence-template.md`.
