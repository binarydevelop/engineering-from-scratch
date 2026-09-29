def soln(nums):
    map = {}

    for i in range(len(nums)):
        if nums[i] in map:
            return True
        
        map[nums[i]] = i

    return False

nums = [2,7,11,15]

print(soln(nums))