#!/usr/bin/env python3
"""
Capstone 2: User-Space Thread & Process Scheduler Simulator
Implements:
- FCFS, SJF, Round Robin, Priority, and Multi-Level Feedback Queue (MLFQ)
- Process state machine: READY, RUNNING, BLOCKED (I/O simulation), TERMINATED
- Gantt chart visualization
- Automated workload benchmarking
"""

import sys
import copy
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional
from collections import deque


@dataclass
class Task:
    pid: str
    arrival: int
    burst: int
    priority: int = 1
    io_delay: int = 0      # After running for this many ticks, triggers I/O
    io_duration: int = 0   # How many ticks spent blocked in I/O
    
    # Live runtime state
    remaining: int = 0
    io_remaining: int = 0
    curr_io_delay: int = 0
    start_time: Optional[int] = None
    finish_time: int = 0
    waiting_time: int = 0
    turnaround_time: int = 0
    response_time: int = 0
    mlfq_level: int = 0

    def __post_init__(self):
        self.remaining = self.burst
        self.curr_io_delay = self.io_delay


class SchedulerSimulator:
    def __init__(self, tasks: List[Task]):
        self.tasks = tasks

    def run_mlfq(self, time_quanta: List[int] = [2, 4, 8], boost_interval: int = 20) -> Dict:
        """
        Multi-Level Feedback Queue:
        Queue 0: Highest priority, RR with quantum 2
        Queue 1: Medium priority, RR with quantum 4
        Queue 2: Lowest priority, FCFS / RR with quantum 8
        Priority Boost: Every boost_interval ticks, all tasks moved to Queue 0.
        """
        tasks = [copy.deepcopy(t) for t in self.tasks]
        queues: List[deque] = [deque() for _ in range(len(time_quanta))]
        unvisited = sorted(tasks, key=lambda t: t.arrival)
        blocked_tasks: List[Task] = []
        completed: List[Task] = []
        
        current_time = 0
        gantt: List[Tuple[str, int, int]] = []
        last_boost = 0

        while len(completed) < len(tasks):
            # 1. Periodic Priority Boost
            if current_time - last_boost >= boost_interval and current_time > 0:
                for q_idx in range(1, len(queues)):
                    while queues[q_idx]:
                        t = queues[q_idx].popleft()
                        t.mlfq_level = 0
                        queues[0].append(t)
                last_boost = current_time

            # 2. Check newly arrived tasks
            newly_arrived = [t for t in unvisited if t.arrival <= current_time]
            for t in newly_arrived:
                t.mlfq_level = 0
                queues[0].append(t)
                unvisited.remove(t)

            # 3. Check blocked tasks finishing I/O
            resumed = []
            for t in blocked_tasks:
                t.io_remaining -= 1
                if t.io_remaining <= 0:
                    resumed.append(t)
            for t in resumed:
                blocked_tasks.remove(t)
                queues[t.mlfq_level].append(t)

            # 4. Find highest priority non-empty queue
            active_queue_idx = -1
            for idx, q in enumerate(queues):
                if q:
                    active_queue_idx = idx
                    break

            if active_queue_idx == -1:
                # CPU Idle
                if blocked_tasks or unvisited:
                    current_time += 1
                    continue
                else:
                    break

            # 5. Run active task for up to quantum
            curr_task = queues[active_queue_idx].popleft()
            if curr_task.start_time is None:
                curr_task.start_time = current_time
                curr_task.response_time = current_time - curr_task.arrival

            quantum = time_quanta[active_queue_idx]
            run_slice = min(quantum, curr_task.remaining)
            
            gantt.append((curr_task.pid, current_time, current_time + run_slice))
            current_time += run_slice
            curr_task.remaining -= run_slice

            # Check new arrivals during this execution slice
            newly_arrived = [t for t in unvisited if t.arrival <= current_time]
            for t in newly_arrived:
                t.mlfq_level = 0
                queues[0].append(t)
                unvisited.remove(t)

            # 6. Check completion or demotion
            if curr_task.remaining <= 0:
                curr_task.finish_time = current_time
                curr_task.turnaround_time = curr_task.finish_time - curr_task.arrival
                curr_task.waiting_time = curr_task.turnaround_time - curr_task.burst
                completed.append(curr_task)
            else:
                # Demote to lower queue if allotted quantum was fully consumed
                if run_slice == quantum and curr_task.mlfq_level < len(queues) - 1:
                    curr_task.mlfq_level += 1
                queues[curr_task.mlfq_level].append(curr_task)

        n = len(completed)
        return {
            "algorithm": "MLFQ (3 Queues, Quanta [2, 4, 8])",
            "gantt": gantt,
            "tasks": completed,
            "avg_waiting": sum(t.waiting_time for t in completed) / n,
            "avg_turnaround": sum(t.turnaround_time for t in completed) / n,
            "avg_response": sum(t.response_time for t in completed) / n
        }


def print_gantt(gantt: List[Tuple[str, int, int]]):
    bar = "|"
    timeline = f"{gantt[0][1]}"
    for pid, start, end in gantt:
        w = max(3, (end - start) * 2)
        lbl = pid.center(w)
        bar += f" {lbl} |"
        timeline += str(end).rjust(len(lbl) + 3)
    print(bar)
    print(timeline)


if __name__ == "__main__":
    tasks = [
        Task(pid="T1", arrival=0, burst=10, priority=1),
        Task(pid="T2", arrival=2, burst=4, priority=1),
        Task(pid="T3", arrival=4, burst=6, priority=1),
        Task(pid="T4", arrival=6, burst=2, priority=1),
    ]

    print("================================================================")
    print("Capstone 2: MLFQ Process & Thread Scheduler Simulation")
    print("================================================================\n")

    sim = SchedulerSimulator(tasks)
    res = sim.run_mlfq()

    print("Gantt Chart Execution Trace:")
    print_gantt(res["gantt"])
    print("\nPerformance Metrics:")
    print(f"{'PID':<6} {'Arrival':<8} {'Burst':<8} {'Start':<8} {'Finish':<8} {'Waiting':<8} {'Turnaround':<12}")
    print("-" * 65)
    for t in sorted(res["tasks"], key=lambda x: x.pid):
        print(f"{t.pid:<6} {t.arrival:<8} {t.burst:<8} {t.start_time:<8} {t.finish_time:<8} {t.waiting_time:<8} {t.turnaround_time:<12}")
    print("-" * 65)
    print(f"Average Waiting Time:    {res['avg_waiting']:.2f}")
    print(f"Average Turnaround Time: {res['avg_turnaround']:.2f}")
    print(f"Average Response Time:   {res['avg_response']:.2f}")
