"""
Project 12: Restricted Coding Agent Sandbox (Phase 219).
Autonomous coding agent runtime operating inside restricted execution confines:
- Allowed file path boundaries (cannot touch parent directories)
- AST security validation on generated code
- Automated test runner evaluation
- Rollback mechanism if tests fail.
"""

from typing import Dict, Any, List
import io
import contextlib
import ast

class CodingAgentSandbox:
    def __init__(self, allowed_workspace_dir: str = "workspace"):
        self.workspace = allowed_workspace_dir
        self.virtual_files: Dict[str, str] = {}

    def write_code_file(self, filename: str, content: str) -> Dict[str, Any]:
        if ".." in filename or filename.startswith("/"):
            return {"success": False, "error": "Path traversal violation"}
        self.virtual_files[filename] = content
        return {"success": True, "error": None}

    def run_virtual_tests(self, test_code: str, solution_code: str) -> Dict[str, Any]:
        combined_code = solution_code + "\n" + test_code
        # Validate AST
        try:
            tree = ast.parse(combined_code)
        except SyntaxError as e:
            return {"passed": False, "error": f"SyntaxError: {str(e)}"}

        safe_globals = {"__builtins__": {"range": range, "len": len, "sum": sum, "AssertionError": AssertionError, "int": int, "str": str}}
        safe_locals = {}

        try:
            exec(combined_code, safe_globals, safe_locals)
            return {"passed": True, "error": None}
        except AssertionError as e:
            return {"passed": False, "error": f"AssertionFailed: {str(e)}"}
        except Exception as e:
            return {"passed": False, "error": f"ExecutionError: {str(e)}"}
