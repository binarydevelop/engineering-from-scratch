class Task:
    def __init__(self, name, action, deps=None):
        self.name = name
        self.action = action
        self.deps = deps or []
        self.state = "PENDING"

class DAGRunner:
    def __init__(self, tasks):
        self.tasks = {t.name: t for t in tasks}
    def run(self):
        executed = []
        for name, task in self.tasks.items():
            for d in task.deps:
                if self.tasks[d].state != "SUCCESS":
                    task.state = "SKIPPED"
                    break
            if task.state != "SKIPPED":
                try:
                    task.action()
                    task.state = "SUCCESS"
                    executed.append(name)
                except Exception:
                    task.state = "FAILED"
        return executed
