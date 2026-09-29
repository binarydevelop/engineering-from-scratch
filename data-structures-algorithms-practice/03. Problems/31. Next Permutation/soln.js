/**
 * @param {number[]} nums
 * @return {void} Do not return anything, modify nums in-place instead.
 */
var nextPermutation = function(nums) {
    // find the pivot 
    let i = nums.length-2
    while(i >= 0 && nums[i] >= nums[i+1]){
        i--
    }

    //find the next number which is greater than nums[i]
    if(i >= 0){
        let j = nums.length-1
        while(nums[j] <= nums[i]){
            j--
        }

        [nums[i], nums[j]] = [nums[j], nums[i]]
    }

    //reverse the suffix
    let left = i +1
    let right = nums.length-1

    while(left < right){
        [nums[left], nums[right]] = [nums[right], nums[left]]
        left++
        right-- 
    }
};