# Back-of-the-Envelope Estimation Guide

System design estimations are not about finding the exact decimal; they are about discovering the **order of magnitude** ($10^2$ vs $10^5$ vs $10^8$) to select appropriate architectural strategies.

---

## 1. Quick Reference: Powers of 2 & 10

| Power of 2 | Exact Value | Approximate Metric | Practical Name |
| :--- | :--- | :--- | :--- |
| $2^{10}$ | 1,024 | $\approx 10^3$ | 1 Thousand ($1\text{ KB}$) |
| $2^{20}$ | 1,048,576 | $\approx 10^6$ | 1 Million ($1\text{ MB}$) |
| $2^{30}$ | 1,073,741,824 | $\approx 10^9$ | 1 Billion ($1\text{ GB}$) |
| $2^{40}$ | 1,099,511,627,776 | $\approx 10^{12}$ | 1 Trillion ($1\text{ TB}$) |
| $2^{50}$ | 1,125,899,906,842,624 | $\approx 10^{15}$ | 1 Quadrillion ($1\text{ PB}$) |

---

## 2. Time Conversion Constants

- **Seconds per day**: $24 \times 60 \times 60 = 86,400\text{ seconds} \approx 10^5\text{ seconds}$ (or $\approx 86,400$).
- **Quick mental shortcut**: 
  - $1\text{ million requests / day} \approx 12\text{ req/s}$.
  - $10\text{ million requests / day} \approx 116\text{ req/s}$.
  - $100\text{ million requests / day} \approx 1,160\text{ req/s}$.
  - $1\text{ billion requests / day} \approx 11,600\text{ req/s}$.
- **Peak Factor**: Typically assume peak traffic is $2\times$ to $3\times$ the daily average.

---

## 3. Storage Estimation Formula

$$\text{Storage / Day} = \text{Writes / Day} \times \text{Average Record Size}$$

$$\text{Storage / 5 Years} = \text{Storage / Day} \times 365 \times 5 \approx \text{Storage / Day} \times 1,825$$

### Example:
- Writes / Day: $20\text{ million}$
- Average Record Size: $500\text{ bytes}$
- Storage / Day: $20,000,000 \times 500 = 10,000,000,000\text{ bytes} \approx 10\text{ GB/day}$.
- Storage / 5 Years: $10\text{ GB/day} \times 1,825 \approx 18.25\text{ TB}$.
- With 3x Replication: $18.25\text{ TB} \times 3 \approx 54.75\text{ TB}$.

---

## 4. Bandwidth Estimation Formula

$$\text{Ingress Bandwidth} = \text{Write RPS} \times \text{Payload Size}$$
$$\text{Egress Bandwidth} = \text{Read RPS} \times \text{Payload Size}$$

### Note on Bits vs Bytes:
- Storage is measured in **Bytes** ($1\text{ Byte} = 8\text{ bits}$).
- Network interfaces and cloud bandwidth are quoted in **bits per second** ($1\text{ Gbps} = 125\text{ MB/s}$).
- $100\text{ MB/s}$ egress requires an $800\text{ Mbps}$ network link.

---

## 5. Cache Sizing: The 80/20 Rule

The Pareto Principle states that roughly 80% of read traffic accesses 20% of the data.

$$\text{Cache Memory} = 0.20 \times \text{Daily Read Data Volume}$$

### Example:
- Daily read data volume = $1\text{ TB}$.
- Cache sizing requirement = $200\text{ GB}$ of RAM.
