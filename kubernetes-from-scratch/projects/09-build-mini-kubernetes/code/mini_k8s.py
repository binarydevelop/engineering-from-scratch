#!/usr/bin/env python3
"""
mini_k8s.py - Educational Distributed Orchestrator

Capstone 2: Demonstrates the end-to-end orchestration chain:
  API Store -> Desired State -> Controller -> Scheduler -> Node Agent (Kubelet) -> Process

Simulates:
  1. API Server (state store for Deployments, Tasks, and Nodes)
  2. Deployment Controller (reconciles desired vs actual task counts)
  3. Scheduler (binds unscheduled tasks to nodes with spare capacity)
  4. Node Agent (Kubelet running on each node, managing local OS processes)
"""

import sys
import os
import time
import signal
import subprocess
from dataclasses import dataclass, field
from typing import Dict, List, Optional

# --- 1. Data Models ---

@dataclass
class SimulatedNode:
    name: str
    max_tasks: int = 2
    is_alive: bool = True

@dataclass
class Task:
    id: str
    app: str
    assigned_node: Optional[str] = None
    status: str = "Pending"  # Pending, Scheduled, Running, Failed
    pid: Optional[int] = None

@dataclass
class Deployment:
    app: str
    desired_replicas: int

# --- 2. In-Memory API Server ---

class ApiServer:
    def __init__(self):
        self.deployments: Dict[str, Deployment] = {}
        self.tasks: Dict[str, Task] = {}
        self.nodes: Dict[str, SimulatedNode] = {}

    def apply_deployment(self, app: str, replicas: int):
        self.deployments[app] = Deployment(app=app, desired_replicas=replicas)
        print(f"[API] Persisted desired state: Deployment '{app}' with {replicas} replicas.")

    def get_tasks_for_app(self, app: str) -> List[Task]:
        return [t for t in self.tasks.values() if t.app == app]

# --- 3. Autonomous Control Plane Components ---

class DeploymentController:
    """Reconciles Deployment desired_replicas with declared Task objects."""
    def __init__(self, api: ApiServer):
        self.api = api
        self.counter = 0

    def reconcile(self):
        for app, dep in list(self.api.deployments.items()):
            tasks = [t for t in self.api.get_tasks_for_app(app) if t.status != "Failed"]
            actual = len(tasks)
            delta = dep.desired_replicas - actual

            if delta > 0:
                print(f"[CONTROLLER] Deployment '{app}': desired {dep.desired_replicas} > actual {actual}. Creating {delta} task(s)...")
                for _ in range(delta):
                    self.counter += 1
                    task_id = f"{app}-{self.counter:03d}"
                    self.api.tasks[task_id] = Task(id=task_id, app=app)
            elif delta < 0:
                excess = abs(delta)
                print(f"[CONTROLLER] Deployment '{app}': desired {dep.desired_replicas} < actual {actual}. Deleting {excess} task(s)...")
                for t in tasks[:excess]:
                    t.status = "Failed"

class Scheduler:
    """Finds tasks with assigned_node == None, filters nodes, and binds."""
    def __init__(self, api: ApiServer):
        self.api = api

    def schedule(self):
        unscheduled = [t for t in self.api.tasks.values() if t.assigned_node is None and t.status != "Failed"]
        if not unscheduled:
            return

        for task in unscheduled:
            # Filter candidate nodes
            candidates = [
                n for n in self.api.nodes.values()
                if n.is_alive and len([t for t in self.api.tasks.values() if t.assigned_node == n.name and t.status != "Failed"]) < n.max_tasks
            ]
            if not candidates:
                print(f"[SCHEDULER] No available node capacity for Task '{task.id}' (Status: Pending)!")
                continue

            # Prioritize/Score (least loaded node)
            chosen = min(
                candidates,
                key=lambda n: len([t for t in self.api.tasks.values() if t.assigned_node == n.name and t.status != "Failed"])
            )
            task.assigned_node = chosen.name
            task.status = "Scheduled"
            print(f"[SCHEDULER] Bound Task '{task.id}' to Node '{chosen.name}'.")

# --- 4. Node Agent (Kubelet) ---

class Kubelet:
    """Runs on each node. Reconciles assigned tasks with live local OS processes."""
    def __init__(self, node_name: str, api: ApiServer):
        self.node_name = node_name
        self.api = api
        self.processes: Dict[str, subprocess.Popen] = {}

    def sync(self):
        node = self.api.nodes.get(self.node_name)
        if not node or not node.is_alive:
            self.stop_all()
            return

        # 1. Health check running processes
        for task_id, proc in list(self.processes.items()):
            poll = proc.poll()
            if poll is not None:
                print(f"[{self.node_name}:KUBELET] Task '{task_id}' crashed/exited with code {poll}!")
                task = self.api.tasks.get(task_id)
                if task:
                    task.status = "Failed"
                del self.processes[task_id]

        # 2. Start newly scheduled tasks
        assigned = [
            t for t in self.api.tasks.values()
            if t.assigned_node == self.node_name and t.status in ["Scheduled", "Running"]
        ]
        for task in assigned:
            if task.id not in self.processes:
                # Start real background OS process
                proc = subprocess.Popen(
                    [sys.executable, "-c", "import time; time.sleep(300)"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                self.processes[task.id] = proc
                task.pid = proc.pid
                task.status = "Running"
                print(f"[{self.node_name}:KUBELET] Started container process PID {proc.pid} for Task '{task.id}'.")

    def stop_all(self):
        for task_id, proc in list(self.processes.items()):
            try:
                proc.terminate()
                proc.wait(timeout=1)
            except Exception:
                proc.kill()
            del self.processes[task_id]

# --- 5. Cluster Orchestrator ---

class MiniCluster:
    def __init__(self):
        self.api = ApiServer()
        # Add 3 simulated nodes
        self.api.nodes["node-01"] = SimulatedNode("node-01", max_tasks=2)
        self.api.nodes["node-02"] = SimulatedNode("node-02", max_tasks=2)
        self.api.nodes["node-03"] = SimulatedNode("node-03", max_tasks=2)

        self.controller = DeploymentController(self.api)
        self.scheduler = Scheduler(self.api)
        self.kubelets = {
            name: Kubelet(name, self.api) for name in self.api.nodes.keys()
        }

    def tick(self):
        self.controller.reconcile()
        self.scheduler.schedule()
        for kubelet in self.kubelets.values():
            kubelet.sync()

    def print_status(self):
        print("\n" + "="*65)
        print(f"{'TASK ID':<12} {'APP':<8} {'NODE':<10} {'STATUS':<12} {'PID':<8}")
        print("-"*65)
        for t in self.api.tasks.values():
            print(f"{t.id:<12} {t.app:<8} {t.assigned_node or '<none>':<10} {t.status:<12} {str(t.pid or '-'):<8}")
        print("="*65 + "\n")

    def shutdown(self):
        print("[CLUSTER] Tearing down mini cluster and killing processes...")
        for kubelet in self.kubelets.values():
            kubelet.stop_all()

# --- 6. Automated Verification Test ---

def run_test():
    print("Executing MiniK8s End-to-End Orchestrator Test...")
    cluster = MiniCluster()
    try:
        # Step 1: Declare desired state
        cluster.api.apply_deployment(app="web-api", replicas=3)
        cluster.tick() # Controller creates tasks, Scheduler binds, Kubelets start procs
        cluster.print_status()

        running_tasks = [t for t in cluster.api.tasks.values() if t.status == "Running"]
        assert len(running_tasks) == 3, f"Expected 3 running tasks, got {len(running_tasks)}"

        # Step 2: Fault Injection -> Kill a task's OS process directly
        killed_task = running_tasks[0]
        print(f"\n[INJECT FAULT] Killing OS process PID {killed_task.pid} for Task '{killed_task.id}'...")
        os.kill(killed_task.pid, signal.SIGKILL)
        time.sleep(0.5)

        # Step 3: Trigger reconciliation cycle
        print("[RECONCILE] Running control cycle after process failure...")
        cluster.tick() # Kubelet notices crash, marks Failed
        cluster.tick() # Controller creates replacement, Scheduler binds, Kubelet starts proc
        cluster.print_status()

        active_tasks = [t for t in cluster.api.tasks.values() if t.status == "Running"]
        assert len(active_tasks) == 3, f"Expected 3 active tasks after recovery, got {len(active_tasks)}"
        print("[SUCCESS] Mini Kubernetes successfully detected process termination, rescheduled, and restored 3 replicas!")
    finally:
        cluster.shutdown()

if __name__ == "__main__":
    if "--test" in sys.argv:
        run_test()
    else:
        print("Running MiniK8s in interactive demonstration mode...")
        run_test()
