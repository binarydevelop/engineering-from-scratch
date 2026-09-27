# Packet Capture Exercise: IPv6 Neighbor Discovery (NDP)

> **Motto**: Understand it. Predict it. Send it. Capture it. Dissect it.

---

## 1. Objective
Resolve IPv6 link-layer address.

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
sudo tcpdump -i <interface> -nn -vvv -s0 "icmp6"
```

## 4. Annotated Wire Dissection
```text
Packet 1: ICMPv6 neighbor solicitation, who has fe80::2 (Multicast)
Packet 2: ICMPv6 neighbor advertisement, tgt is fe80::2 (Unicast)
```

## 5. Mastery Reasoning Question
> **Question**: Why did IPv6 eliminate broadcast ARP in favor of multicast Neighbor Solicitation?

Document your empirical findings in `outputs/evidence-template.md`.
