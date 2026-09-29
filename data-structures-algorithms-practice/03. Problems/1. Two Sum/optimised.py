def soln(nums, target):
    map = {}

    for i in range(len(nums)):
        difference = target - nums[i]
        if difference in map:
            return [i, map[difference]]
        
        map[nums[i]] = i

    return []

nums = [2,7,11,15]
target = 9

print(soln(nums, target))