"""
Project: Todo Task Management API
"""
from typing import Optional, Dict, Any, List, Set, Tuple, Union, Callable
class TaskService:
    def __init__(self):
        self.tasks = {}
        self.id_counter = 0

    def create(self, owner_id: str, title: str) -> dict:
        self.id_counter += 1
        task = {"id": self.id_counter, "owner_id": owner_id, "title": title, "completed": False}
        self.tasks[self.id_counter] = task
        return task

    def get_user_tasks(self, owner_id: str, limit: int = 10) -> list:
        return [t for t in self.tasks.values() if t["owner_id"] == owner_id][:limit]

    def complete(self, owner_id: str, task_id: int) -> dict:
        task = self.tasks.get(task_id)
        if not task:
            raise KeyError("Task not found")
        if task["owner_id"] != owner_id:
            raise PermissionError("Forbidden")
        task["completed"] = True
        return task
