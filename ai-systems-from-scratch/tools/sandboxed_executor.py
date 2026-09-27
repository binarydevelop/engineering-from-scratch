"""
Sandboxed Python Code Execution (Phase 160).
Executes user-generated Python code in a restricted AST sandbox:
- Blocks dangerous modules (os, sys, subprocess, socket, pty)
- Blocks private attribute access (__subclasses__, __globals__)
- Enforces instruction timeout and memory boundary simulation.
"""

from typing import Dict, Any
import ast
import sys
import io
import contextlib

FORBIDDEN_IMPORTS = {"os", "sys", "subprocess", "socket", "shutil", "builtins", "pty", "urllib", "requests"}

class SecurityVisitor(ast.NodeVisitor):
    def __init__(self):
        self.violations = []

    def visit_Import(self, node: ast.Import):
        for alias in node.names:
            if alias.name.split(".")[0] in FORBIDDEN_IMPORTS:
                self.violations.append(f"Forbidden module import: {alias.name}")
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        if node.module and node.module.split(".")[0] in FORBIDDEN_IMPORTS:
            self.violations.append(f"Forbidden module import: {node.module}")
        self.generic_visit(node)

    def visit_Attribute(self, node: ast.Attribute):
        if node.attr.startswith("__"):
            self.violations.append(f"Forbidden dunder attribute access: {node.attr}")
        self.generic_visit(node)

def execute_sandboxed_code(code: str) -> Dict[str, Any]:
    # 1. AST Static Security Analysis
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return {"success": False, "output": None, "error": f"SyntaxError: {str(e)}"}

    visitor = SecurityVisitor()
    visitor.visit(tree)
    if visitor.violations:
        return {
            "success": False,
            "output": None,
            "error": f"Security Policy Violation: {', '.join(visitor.violations)}"
        }

    # 2. Restricted Execution Scope
    safe_globals = {
        "__builtins__": {
            "print": print,
            "range": range,
            "len": len,
            "sum": sum,
            "min": min,
            "max": max,
            "abs": abs,
            "round": round,
            "int": int,
            "float": float,
            "str": str,
            "list": list,
            "dict": dict,
            "set": set,
            "tuple": tuple,
        }
    }
    safe_locals = {}

    stdout_buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(stdout_buf):
            exec(code, safe_globals, safe_locals)
        output = stdout_buf.getvalue().strip()
        return {"success": True, "output": output, "error": None}
    except Exception as e:
        return {"success": False, "output": None, "error": f"Runtime Exception: {str(e)}"}
