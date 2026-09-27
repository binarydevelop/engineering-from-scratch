#!/usr/bin/env python3
"""
Page Replacement Algorithm Simulator
Compares virtual memory page eviction policies:
- FIFO (First-In, First-Out)
- LRU (Least Recently Used)
- Clock (Second-Chance Approximation)
- OPT (Belady's Optimal)

Demonstrates page fault curves and Belady's Anomaly.
"""

from typing import List, Dict, Optional, Tuple
from collections import OrderedDict, deque


def simulate_fifo(reference_string: List[int], num_frames: int) -> Tuple[int, List[List[Optional[int]]]]:
    frames: deque[int] = deque()
    faults = 0
    history = []

    for page in reference_string:
        if page not in frames:
            faults += 1
            if len(frames) >= num_frames:
                frames.popleft()  # Evict oldest
            frames.append(page)
        # Pad with None up to num_frames for visualization
        snapshot = list(frames) + [None] * (num_frames - len(frames))
        history.append(snapshot)

    return faults, history


def simulate_lru(reference_string: List[int], num_frames: int) -> Tuple[int, List[List[Optional[int]]]]:
    frames: OrderedDict[int, bool] = OrderedDict()
    faults = 0
    history = []

    for page in reference_string:
        if page in frames:
            frames.move_to_end(page)  # Mark as recently used
        else:
            faults += 1
            if len(frames) >= num_frames:
                frames.popitem(last=False)  # Evict least recently used
            frames[page] = True
        snapshot = list(frames.keys()) + [None] * (num_frames - len(frames))
        history.append(snapshot)

    return faults, history


def simulate_clock(reference_string: List[int], num_frames: int) -> Tuple[int, List[List[Optional[int]]]]:
    frames: List[Optional[int]] = [None] * num_frames
    use_bits: List[int] = [0] * num_frames
    hand = 0
    faults = 0
    history = []

    for page in reference_string:
        if page in frames:
            idx = frames.index(page)
            use_bits[idx] = 1
        else:
            faults += 1
            # Advance clock hand looking for a frame with use_bit == 0
            while True:
                if frames[hand] is None:
                    # Empty frame available
                    frames[hand] = page
                    use_bits[hand] = 1
                    hand = (hand + 1) % num_frames
                    break
                elif use_bits[hand] == 1:
                    # Give second chance
                    use_bits[hand] = 0
                    hand = (hand + 1) % num_frames
                else:
                    # Evict page with use_bit == 0
                    frames[hand] = page
                    use_bits[hand] = 1
                    hand = (hand + 1) % num_frames
                    break

        history.append(list(frames))

    return faults, history


def simulate_optimal(reference_string: List[int], num_frames: int) -> Tuple[int, List[List[Optional[int]]]]:
    frames: List[int] = []
    faults = 0
    history = []

    for i, page in enumerate(reference_string):
        if page not in frames:
            faults += 1
            if len(frames) < num_frames:
                frames.append(page)
            else:
                # Find page in frame that will not be used for longest time in future
                furthest_use = -1
                victim_idx = 0
                for f_idx, f_page in enumerate(frames):
                    future_slice = reference_string[i + 1:]
                    if f_page not in future_slice:
                        victim_idx = f_idx
                        break
                    else:
                        next_use = future_slice.index(f_page)
                        if next_use > furthest_use:
                            furthest_use = next_use
                            victim_idx = f_idx
                frames[victim_idx] = page
        snapshot = list(frames) + [None] * (num_frames - len(frames))
        history.append(snapshot)

    return faults, history


if __name__ == "__main__":
    trace = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1]
    frames = 3

    print("================================================================")
    print("Page Replacement Policy Evaluation")
    print(f"Reference String ({len(trace)} accesses): {trace}")
    print(f"Physical Memory Frames: {frames}")
    print("================================================================\n")

    f_fifo, _ = simulate_fifo(trace, frames)
    f_lru, _ = simulate_lru(trace, frames)
    f_clk, _ = simulate_clock(trace, frames)
    f_opt, _ = simulate_optimal(trace, frames)

    print(f"{'Algorithm':<25} {'Total Faults':<15} {'Hit Ratio':<12}")
    print("-" * 55)
    print(f"{'FIFO':<25} {f_fifo:<15} {(len(trace)-f_fifo)/len(trace)*100:.1f}%")
    print(f"{'Clock (Second-Chance)':<25} {f_clk:<15} {(len(trace)-f_clk)/len(trace)*100:.1f}%")
    print(f"{'LRU':<25} {f_lru:<15} {(len(trace)-f_lru)/len(trace)*100:.1f}%")
    print(f"{'Optimal (Belady MIN)':<25} {f_opt:<15} {(len(trace)-f_opt)/len(trace)*100:.1f}%")

    print("\n----------------------------------------------------------------")
    print("Belady's Anomaly Demonstration (FIFO):")
    print("Under FIFO, increasing memory frames from 3 to 4 can INCREASE faults!")
    belady_trace = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]
    b_faults_3, _ = simulate_fifo(belady_trace, 3)
    b_faults_4, _ = simulate_fifo(belady_trace, 4)
    print(f"Trace: {belady_trace}")
    print(f"Frames = 3 -> FIFO Faults: {b_faults_3}")
    print(f"Frames = 4 -> FIFO Faults: {b_faults_4} (ANOMALY DETECTED!)")
