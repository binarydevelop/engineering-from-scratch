"""
Resilient, production-ready solution for lab-13-circular-dag-orchestration-deadlock.
"""
def detect_cycle(graph):
    visited = set()
    rec_stack = set()
    def dfs(node):
        visited.add(node)
        rec_stack.add(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                if dfs(neighbor): return True
            elif neighbor in rec_stack:
                return True
        rec_stack.remove(node)
        return False
    for n in graph:
        if n not in visited:
            if dfs(n): return True
    return False
