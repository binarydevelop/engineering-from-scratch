class LineageTracker:
    def __init__(self):
        self.graph = {}
    def register(self, upstream_list, downstream):
        self.graph[downstream] = list(upstream_list)
    def trace_upstream(self, target):
        return self.graph.get(target, [])
