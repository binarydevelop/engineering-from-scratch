import time

class SnowflakeGenerator:
    def __init__(self, worker_id: int, epoch: int = 1700000000000):
        self.worker_id = worker_id & 0x3FF  # 10 bits
        self.epoch = epoch
        self.sequence = 0
        self.last_timestamp = -1

    def generate(self) -> int:
        timestamp = int(time.time() * 1000)
        if timestamp == self.last_timestamp:
            self.sequence = (self.sequence + 1) & 0xFFF  # 12 bits
            if self.sequence == 0:
                # Wait next millisecond
                while timestamp <= self.last_timestamp:
                    timestamp = int(time.time() * 1000)
        else:
            self.sequence = 0

        self.last_timestamp = timestamp
        # 64-bit ID: 1 sign bit (0) + 41 bit timestamp + 10 bit worker + 12 bit sequence
        snowflake = ((timestamp - self.epoch) << 22) | (self.worker_id << 12) | self.sequence
        return snowflake
