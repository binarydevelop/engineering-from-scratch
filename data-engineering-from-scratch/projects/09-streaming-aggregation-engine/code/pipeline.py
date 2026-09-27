class StreamAggregator:
    def __init__(self):
        self.windows = {}
    def add_event(self, window_id, val):
        self.windows[window_id] = self.windows.get(window_id, 0) + val
    def get_window(self, window_id):
        return self.windows.get(window_id, 0)
