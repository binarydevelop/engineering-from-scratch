"""
Lesson 09: Routing From Scratch.
Builds a parameter-aware URI router mapping (Method, Path) to callable handlers.
"""

from typing import Callable, Dict, Any, Tuple, Optional
import re

class Router:
    """A path and method dispatcher supporting dynamic path variables like /users/{id}."""

    def __init__(self):
        self.routes: list[Tuple[str, re.Pattern, list[str], Callable]] = []

    def add(self, method: str, path_pattern: str, handler: Callable):
        """Compiles a path pattern with {param} into a regex pattern."""
        param_names = []
        regex_parts = []
        segments = path_pattern.strip("/").split("/")
        
        for segment in segments:
            if not segment:
                continue
            if segment.startswith("{") and segment.endswith("}"):
                name = segment[1:-1]
                param_names.append(name)
                regex_parts.append(r"([^/]+)")
            else:
                regex_parts.append(re.escape(segment))
        
        pattern_str = "^/" + "/".join(regex_parts) + "$" if regex_parts else "^/$"
        pattern = re.compile(pattern_str)
        self.routes.append((method.upper(), pattern, param_names, handler))

    def dispatch(self, method: str, path: str) -> Tuple[int, Any, Dict[str, str]]:
        """
        Dispatches incoming (method, path) to matched handler.
        Returns (HTTP_Status, Result, Params).
        """
        method = method.upper()
        clean_path = "/" + path.strip("/") if path.strip("/") else "/"
        path_matched = False

        for route_method, pattern, param_names, handler in self.routes:
            match = pattern.match(clean_path)
            if match:
                path_matched = True
                if route_method == method:
                    params = dict(zip(param_names, match.groups()))
                    result = handler(params)
                    return 200, result, params

        if path_matched:
            return 405, {"error": "Method Not Allowed"}, {}
        return 404, {"error": "Not Found"}, {}
