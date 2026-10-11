def bubble_sort(nums):
    n = len(nums)
    for i in range(n-1):
        for j in range(n-1-i):
            if nums[j] > nums[j+1]:
                nums[j], nums[j+1] = nums[j+1], nums[j]
        
    return nums


nums = [64, 25, 12, 22, 11]
print("Sorted array:", bubble_sort(nums)) 

def bubble_sort_optimised(nums):
    n = len(nums)
    for i in range(n-1):
        swapped = False
        for j in range(n-1-i):
            if nums[j] > nums[j+1]:
                nums[j], nums[j+1] = nums[j+1], nums[j]

        if swapped == False:
            break
        
    return nums


nums = [64, 25, 12, 22, 11]
print("Sorted array:", bubble_sort(nums)) 