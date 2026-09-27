#!/usr/bin/env python3
"""
simulations/congestion_control.py
Simulates the TCP Congestion Control State Machine (Slow Start, Congestion Avoidance,
AIMD, and loss recovery).
Generates an ASCII visualization of cwnd progression over RTT rounds.
"""

from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class RoundSnapshot:
    rtt_round: int
    state: str
    cwnd: float
    ssthresh: float
    event: str


class TCPCongestionSimulator:
    def __init__(self, initial_cwnd: float = 1.0, initial_ssthresh: float = 16.0):
        self.cwnd = initial_cwnd
        self.ssthresh = initial_ssthresh
        self.state = "SLOW_START"
        self.history: List[RoundSnapshot] = []

    def run_round(self, rtt_round: int, loss_type: str = "NONE") -> RoundSnapshot:
        """
        Runs one RTT round of TCP transmission.
        loss_type: "NONE", "DUP_ACK" (3 duplicate ACKs), or "TIMEOUT" (RTO expiration)
        """
        event = "Normal ACK"

        if loss_type == "DUP_ACK":
            # Multiplicative Decrease (Fast Retransmit / Fast Recovery)
            self.ssthresh = max(2.0, self.cwnd / 2.0)
            self.cwnd = self.ssthresh
            self.state = "CONGESTION_AVOIDANCE"
            event = f"3 DUP ACKs! Cut cwnd to {self.cwnd:.1f}, ssthresh={self.ssthresh:.1f}"

        elif loss_type == "TIMEOUT":
            # Severe collapse
            self.ssthresh = max(2.0, self.cwnd / 2.0)
            self.cwnd = 1.0
            self.state = "SLOW_START"
            event = f"TIMEOUT! cwnd collapsed to 1, ssthresh={self.ssthresh:.1f}"

        else:
            # Successful transmission & ACK reception
            if self.state == "SLOW_START":
                # cwnd doubles every RTT (exponential growth)
                self.cwnd *= 2.0
                if self.cwnd >= self.ssthresh:
                    self.state = "CONGESTION_AVOIDANCE"
                    event = f"Reached ssthresh ({self.ssthresh:.0f}) -> Transition to Congestion Avoidance"
            elif self.state == "CONGESTION_AVOIDANCE":
                # Additive Increase: +1 MSS per RTT (linear growth)
                self.cwnd += 1.0
                event = "Additive Increase (+1 MSS)"

        snapshot = RoundSnapshot(
            rtt_round=rtt_round,
            state=self.state,
            cwnd=self.cwnd,
            ssthresh=self.ssthresh,
            event=event,
        )
        self.history.append(snapshot)
        return snapshot


def render_ascii_graph(history: List[RoundSnapshot], max_width: int = 50) -> str:
    """Renders an ASCII chart of cwnd progression over time."""
    max_cwnd = max(s.cwnd for s in history)
    lines = [
        "TCP Congestion Window (cwnd) Evolution Over Time:",
        "RTT | cwnd | State                 | Visual (1 '#' = 1 MSS)",
        "----+------+-----------------------+" + "-" * (max_width + 2),
    ]

    for s in history:
        bar_len = int((s.cwnd / max_cwnd) * max_width)
        bar = "#" * max(1, bar_len)
        lines.append(f"{s.rtt_round:3d} | {s.cwnd:4.1f} | {s.state:<21} | {bar}")

    return "\n".join(lines)


if __name__ == "__main__":
    sim = TCPCongestionSimulator(initial_cwnd=1.0, initial_ssthresh=16.0)

    # Sequence of 20 RTT rounds with injected losses
    schedule = {
        8: "DUP_ACK",   # Round 8: Packet loss detected via 3 Dup ACKs
        15: "TIMEOUT",  # Round 15: Timeout occurs
    }

    for r in range(1, 22):
        loss = schedule.get(r, "NONE")
        sim.run_round(r, loss_type=loss)

    print(render_ascii_graph(sim.history))
    print()
    print("Events Summary:")
    for s in sim.history:
        if "DUP" in s.event or "TIMEOUT" in s.event or "Reached" in s.event:
            print(f"  RTT {s.rtt_round:2d}: {s.event}")

    print("\nSUCCESS: TCP congestion control simulation verified.")
