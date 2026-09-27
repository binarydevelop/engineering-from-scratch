#!/usr/bin/env python3

class Simple1DPointIndex:
    def __init__(self, data):
        # data: list of (doc_id, value)
        self.sorted_data = sorted(data, key=lambda x: x[1])

    def range_query(self, min_val, max_val):
        # Binary search boundaries
        import bisect
        keys = [v for _, v in self.sorted_data]
        left = bisect.bisect_left(keys, min_val)
        right = bisect.bisect_right(keys, max_val)
        return [self.sorted_data[i][0] for i in range(left, right)]

if __name__ == "__main__":
    prices = [(1, 19.99), (2, 49.99), (3, 89.99), (4, 129.99), (5, 299.99)]
    index = Simple1DPointIndex(prices)
    min_p, max_p = 40.0, 150.0
    matching_ids = index.range_query(min_p, max_p)
    print(f"Prices: {prices}")
    print(f"Query range [{min_p}, {max_p}] -> Matching Doc IDs: {matching_ids}")
