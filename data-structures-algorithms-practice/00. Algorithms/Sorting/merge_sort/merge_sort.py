
def merge_sort(nums):
    if len(nums) <= 1:
        return nums
        
    mid = (len(nums)// 2)
    
    left_sorted = merge_sort(nums[mid:])
    right_sorted = merge_sort(nums[:mid])

    return merge(left_sorted, right_sorted)

def merge(left,right):
    sorted_arr = []
    i = 0 
    j = 0

    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            sorted_arr.append(left[i])
            i+=1
        else: 
            sorted_arr.append(right[j])
            j+=1
        
    sorted_arr.extend(left[i:])
    sorted_arr.extend(right[j:])

    return sorted_arr


nums = [64, 25, 12, 22, 11]
print("Sorted array:", merge_sort(nums)) 