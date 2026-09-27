"""
Lesson 14: Middleware From First Principles.
Implements an onion-style execution pipeline where middleware wraps execution before and after.
"""

from typing import Callable, Any, List

Request = dict
Response = dict
Handler = Callable[[Request], Response]
Middleware = Callable[[Request, Handler], Response]

class MiddlewarePipeline:
    """An onion-style middleware pipeline runner."""

    def __init__(self, core_handler: Handler):
        self.core_handler = core_handler
        self.middlewares: List[Middleware] = []

    def use(self, middleware: Middleware):
        """Adds a middleware to the outer edge of the pipeline."""
        self.middlewares.append(middleware)

    def execute(self, request: Request) -> Response:
        """Executes the pipeline through all layers and back out."""
        # Compose from inside out: Core handler is the deepest layer
        current_handler = self.core_handler

        # Wrap with middlewares in reverse order so first added is outermost
        for mw in reversed(self.middlewares):
            prev_handler = current_handler
            # Capture mw and prev_handler in default argument to avoid late binding
            current_handler = (lambda req, m=mw, nxt=prev_handler: m(req, nxt))

        return current_handler(request)
