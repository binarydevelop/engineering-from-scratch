def removeDuplicates(self, nums: List[int]) -> int:
    start = 0 
    end = 1

    while end <len(nums):

        if nums[start] != nums[end]:
            start += 1
            nums[start]=nums[end]

            end+=1
        return start+1