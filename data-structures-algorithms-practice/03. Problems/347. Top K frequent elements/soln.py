def topKFrequent(nums, k):
    freq = {}

    for num in nums:
        freq[num] = freq.get(num, 0) + 1

        sorted_nums = sorted(freq.keys(), key=lambda x: freq[x], reverse=True)

        return sorted_nums[:k]