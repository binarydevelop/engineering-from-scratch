def bubble_sort(nums):
    n = len(nums)
    for i in range(1, n):
        current = nums[i]
        j = i-1
        while j >= 0 and nums[j] > current :
            nums[j+1] = nums[j]
            j-=1
            
        nums[j+1] = current
        
    return nums


nums = [64, 25, 12, 22, 11]
print("Sorted array:", bubble_sort(nums)) 