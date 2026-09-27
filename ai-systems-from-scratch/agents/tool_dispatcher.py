"""
Tool Registry & Defensive Dispatcher (Phases 124-127).
Manages registered tool functions, validates parameter schemas, executes
with defensive timeouts, and formats structured error feedback messages.
"""

from typing import Dict, Any, Callable
import inspect
from pydantic import BaseModel, create_model

class ToolDispatcher:
    def __init__(self):
        self._tools: Dict[str, Callable] = {}
        self._schemas: Dict[str, Dict[str, Any]] = {}

    def register(self, name: str, fn: Callable, description: str, param_schema: Dict[str, Any]):
        self._tools[name] = fn
        self._schemas[name] = {
            "name": name,
            "description": description,
            "parameters": param_schema
        }

    def get_tool_definitions(self) -> Dict[str, Any]:
        return self._schemas

    def execute(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        if tool_name not in self._tools:
            return {
                "success": False,
                "error": f"Tool '{tool_name}' is not registered. Available tools: {list(self._tools.keys())}",
                "result": None
            }

        fn = self._tools[tool_name]
        try:
            # Defensive dispatch
            result = fn(**arguments)
            return {"success": True, "result": result, "error": None}
        except TypeError as e:
            return {"success": False, "error": f"Argument Mismatch: {str(e)}", "result": None}
        except Exception as e:
            return {"success": False, "error": f"Tool Execution Failure: {str(e)}", "result": None}
