# Packet Capture Exercise: ARP Request & Reply

> **Motto**: Understand it. Predict it. Send it. Capture it. Dissect it.

---

## 1. Objective
Resolve local MAC address.

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
sudo tcpdump -i <interface> -nn -vvv -s0 "arp"
```

## 4. Annotated Wire Dissection
```text
Frame 1: Broadcast Who has 10.0.1.20? Tell 10.0.1.10
Frame 2: Unicast 10.0.1.20 is at 52:54:00:22:22:22
```

## 5. Mastery Reasoning Question
> **Question**: Why is the ARP request sent to ff:ff:ff:ff:ff:ff, but the reply is unicast?

Document your empirical findings in `outputs/evidence-template.md`.
