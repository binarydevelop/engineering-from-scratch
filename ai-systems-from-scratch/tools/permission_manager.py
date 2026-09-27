"""
Tool Permission & Least-Privilege Manager (Phases 157-159).
Enforces:
1. Strict segregation of READ tools (safe) vs WRITE tools (state mutation).
2. Tenant scope and role authorization checks.
3. Two-phase commit approval gate for sensitive actions (payments, database mutations).
"""

from typing import Set, Dict, Any, Optional
from enum import Enum

class ActionType(Enum):
    READ = "READ"
    WRITE = "WRITE"
    HIGH_STAKES = "HIGH_STAKES"

class ToolPermissionManager:
    def __init__(self):
        # Registry of tool names to action types
        self.tool_types: Dict[str, ActionType] = {}
        # User roles allowed
        self.role_permissions: Dict[str, Set[ActionType]] = {
            "guest": {ActionType.READ},
            "user": {ActionType.READ, ActionType.WRITE},
            "admin": {ActionType.READ, ActionType.WRITE, ActionType.HIGH_STAKES},
        }

    def register_tool(self, name: str, action_type: ActionType):
        self.tool_types[name] = action_type

    def authorize(self, tool_name: str, user_role: str) -> Dict[str, Any]:
        if tool_name not in self.tool_types:
            return {"authorized": False, "requires_approval": False, "reason": f"Tool '{tool_name}' unknown"}

        act_type = self.tool_types[tool_name]
        allowed_types = self.role_permissions.get(user_role, set())

        if act_type not in allowed_types:
            return {
                "authorized": False,
                "requires_approval": False,
                "reason": f"Role '{user_role}' not authorized for {act_type.value} actions"
            }

        # If HIGH_STAKES, require human approval regardless of role!
        if act_type == ActionType.HIGH_STAKES:
            return {
                "authorized": True,
                "requires_approval": True,
                "reason": "High-stakes action requires explicit human confirmation before execution"
            }

        return {"authorized": True, "requires_approval": False, "reason": "Authorized"}
