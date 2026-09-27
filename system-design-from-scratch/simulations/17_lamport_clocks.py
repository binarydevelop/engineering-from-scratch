class LamportClock:
    def __init__(self):
        self.time = 0

    def tick(self) -> int:
        self.time += 1
        return self.time

    def send_event(self) -> int:
        return self.tick()

    def receive_event(self, received_time: int) -> int:
        self.time = max(self.time, received_time) + 1
        return self.time
