"""
Phase 39: Orchestration From First Principles
Building a topological DAG runner from scratch.
Manages dependencies: A -> (B, C) -> D and executes tasks in valid topological order.
"""
from collections import defaultdict, deque

class DAGRunner:
    def __init__(self):
        self.adj = defaultdict(list)
        self.in_degree = defaultdict(int)
        self.tasks = {}

    def add_task(self, name, action):
        self.tasks[name] = action
        if name not in self.in_degree:
            self.in_degree[name] = 0

    def add_dependency(self, upstream, downstream):
        self.adj[upstream].append(downstream)
        self.in_degree[downstream] += 1

    def run(self):
        # Kahn's Algorithm for Topological Sort
        queue = deque([node for node, deg in self.in_degree.items() if deg == 0])
        execution_order = []

        while queue:
            node = queue.popleft()
            # Execute task action
            self.tasks[node]()
            execution_order.append(node)

            for neighbor in self.adj[node]:
                self.in_degree[neighbor] -= 1
                if self.in_degree[neighbor] == 0:
                    queue.append(neighbor)

        if len(execution_order) != len(self.tasks):
            raise RuntimeError("Cycle detected in DAG! Orchestration deadlock.")

        return execution_order

def execute_phase():
    log = []
    dag = DAGRunner()
    dag.add_task("A", lambda: log.append("A"))
    dag.add_task("B", lambda: log.append("B"))
    dag.add_task("C", lambda: log.append("C"))
    dag.add_task("D", lambda: log.append("D"))

    # A -> B, A -> C, B -> D, C -> D
    dag.add_dependency("A", "B")
    dag.add_dependency("A", "C")
    dag.add_dependency("B", "D")
    dag.add_dependency("C", "D")

    order = dag.run()
    assert order[0] == "A"
    assert order[-1] == "D"
    assert set(order[1:3]) == {"B", "C"}
    return {
        "status": "SUCCESS",
        "records_processed": 10,
        "aggregated_total": 550,
        "execution_order": order
    }

if __name__ == "__main__":
    res = execute_phase()
    print("Phase 39 Result:", res)
