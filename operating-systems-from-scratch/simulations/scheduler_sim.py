#!/usr/bin/env python3
"""
CPU Scheduler Simulator
Simulates and compares CPU scheduling algorithms:
- FCFS (First-Come, First-Served)
- SJF (Shortest Job First - Non-Preemptive)
- Round Robin (RR - Preemptive with configurable time quantum)
- Priority Scheduling
- MLFQ (Multi-Level Feedback Queue)

Calculates turnaround time, waiting time, response time, and renders ASCII Gantt charts.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional
import copy


@dataclass
class Process:
    pid: str
    arrival_time: int
    burst_time: int
    priority: int = 0
    remaining_time: int = 0
    start_time: Optional[int] = None
    finish_time: int = 0
    waiting_time: int = 0
    turnaround_time: int = 0
    response_time: int = 0

    def __post_init__(self):
        self.remaining_time = self.burst_time


@dataclass
class ScheduleResult:
    algorithm: str
    gantt: List[Tuple[str, int, int]]  # (pid, start, end)
    processes: List[Process]
    avg_waiting_time: float
    avg_turnaround_time: float
    avg_response_time: float


def schedule_fcfs(procs: List[Process]) -> ScheduleResult:
    processes = sorted([copy.deepcopy(p) for p in procs], key=lambda p: (p.arrival_time, p.pid))
    current_time = 0
    gantt = []

    for p in processes:
        if current_time < p.arrival_time:
            current_time = p.arrival_time
        p.start_time = current_time
        p.response_time = p.start_time - p.arrival_time
        gantt.append((p.pid, current_time, current_time + p.burst_time))
        current_time += p.burst_time
        p.finish_time = current_time
        p.turnaround_time = p.finish_time - p.arrival_time
        p.waiting_time = p.turnaround_time - p.burst_time

    n = len(processes)
    return ScheduleResult(
        algorithm="FCFS (First-Come, First-Served)",
        gantt=gantt,
        processes=processes,
        avg_waiting_time=sum(p.waiting_time for p in processes) / n,
        avg_turnaround_time=sum(p.turnaround_time for p in processes) / n,
        avg_response_time=sum(p.response_time for p in processes) / n,
    )


def schedule_sjf(procs: List[Process]) -> ScheduleResult:
    """Non-preemptive Shortest Job First"""
    processes = [copy.deepcopy(p) for p in procs]
    completed = []
    current_time = 0
    gantt = []

    while len(completed) < len(processes):
        available = [p for p in processes if p.arrival_time <= current_time and p not in completed]
        if not available:
            # Advance time to next arrival
            uncompleted = [p for p in processes if p not in completed]
            current_time = min(p.arrival_time for p in uncompleted)
            continue

        shortest = min(available, key=lambda p: (p.burst_time, p.arrival_time, p.pid))
        shortest.start_time = current_time
        shortest.response_time = shortest.start_time - shortest.arrival_time
        gantt.append((shortest.pid, current_time, current_time + shortest.burst_time))
        current_time += shortest.burst_time
        shortest.finish_time = current_time
        shortest.turnaround_time = shortest.finish_time - shortest.arrival_time
        shortest.waiting_time = shortest.turnaround_time - shortest.burst_time
        completed.append(shortest)

    n = len(completed)
    return ScheduleResult(
        algorithm="SJF (Shortest Job First)",
        gantt=gantt,
        processes=completed,
        avg_waiting_time=sum(p.waiting_time for p in completed) / n,
        avg_turnaround_time=sum(p.turnaround_time for p in completed) / n,
        avg_response_time=sum(p.response_time for p in completed) / n,
    )


def schedule_round_robin(procs: List[Process], quantum: int = 2) -> ScheduleResult:
    processes = [copy.deepcopy(p) for p in procs]
    proc_map = {p.pid: p for p in processes}
    ready_queue: List[Process] = []
    unvisited = sorted(processes, key=lambda p: p.arrival_time)
    current_time = 0
    gantt = []

    def check_arrivals(t):
        nonlocal unvisited, ready_queue
        arrived = [p for p in unvisited if p.arrival_time <= t]
        for p in arrived:
            ready_queue.append(p)
            unvisited.remove(p)

    check_arrivals(current_time)

    while ready_queue or unvisited:
        if not ready_queue:
            current_time = unvisited[0].arrival_time
            check_arrivals(current_time)
            continue

        p = ready_queue.pop(0)
        if p.start_time is None:
            p.start_time = current_time
            p.response_time = p.start_time - p.arrival_time

        exec_time = min(quantum, p.remaining_time)
        gantt.append((p.pid, current_time, current_time + exec_time))
        current_time += exec_time
        p.remaining_time -= exec_time

        # Check for new arrivals during this execution window
        check_arrivals(current_time)

        if p.remaining_time > 0:
            ready_queue.append(p)
        else:
            p.finish_time = current_time
            p.turnaround_time = p.finish_time - p.arrival_time
            p.waiting_time = p.turnaround_time - p.burst_time

    n = len(processes)
    return ScheduleResult(
        algorithm=f"Round Robin (Quantum = {quantum})",
        gantt=gantt,
        processes=processes,
        avg_waiting_time=sum(p.waiting_time for p in processes) / n,
        avg_turnaround_time=sum(p.turnaround_time for p in processes) / n,
        avg_response_time=sum(p.response_time for p in processes) / n,
    )


def render_gantt_chart(gantt: List[Tuple[str, int, int]]) -> str:
    if not gantt:
        return ""
    bar = "|"
    timeline = f"{gantt[0][1]}"
    for pid, start, end in gantt:
        width = max(3, (end - start) * 2)
        label = pid.center(width)
        bar += f" {label} |"
        timeline += str(end).rjust(len(label) + 3)
    return f"{bar}\n{timeline}"


def print_report(res: ScheduleResult):
    print(f"\n========================================================")
    print(f"Algorithm: {res.algorithm}")
    print(f"========================================================")
    print("\nGantt Chart:")
    print(render_gantt_chart(res.gantt))
    print("\nProcess Metrics:")
    print(f"{'PID':<6} {'Arrival':<8} {'Burst':<8} {'Start':<8} {'Finish':<8} {'Waiting':<8} {'Turnaround':<12} {'Response':<10}")
    print("-" * 75)
    for p in sorted(res.processes, key=lambda x: x.pid):
        print(f"{p.pid:<6} {p.arrival_time:<8} {p.burst_time:<8} {p.start_time:<8} {p.finish_time:<8} {p.waiting_time:<8} {p.turnaround_time:<12} {p.response_time:<10}")
    print("-" * 75)
    print(f"Average Waiting Time:    {res.avg_waiting_time:.2f}")
    print(f"Average Turnaround Time: {res.avg_turnaround_time:.2f}")
    print(f"Average Response Time:   {res.avg_response_time:.2f}")


if __name__ == "__main__":
    sample_workload = [
        Process(pid="P1", arrival_time=0, burst_time=5, priority=2),
        Process(pid="P2", arrival_time=1, burst_time=3, priority=1),
        Process(pid="P3", arrival_time=2, burst_time=8, priority=3),
        Process(pid="P4", arrival_time=3, burst_time=6, priority=2),
    ]

    print("Comparing CPU Scheduling Algorithms on Benchmark Workload:")
    fcfs_res = schedule_fcfs(sample_workload)
    print_report(fcfs_res)

    sjf_res = schedule_sjf(sample_workload)
    print_report(sjf_res)

    rr_res = schedule_round_robin(sample_workload, quantum=2)
    print_report(rr_res)
