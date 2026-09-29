
def moveZeroes(self, nums):
        start = 0
        end = 0

        while end < len(nums):
            if nums[end] != 0:
                nums[start] = nums[end]
                start+=1

            end += 1
    
        for num in range(start, len(nums)):
            nums[num] = 0
        return nums
            