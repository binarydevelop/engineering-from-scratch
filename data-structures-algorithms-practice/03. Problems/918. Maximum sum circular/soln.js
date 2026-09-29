/**
 * @param {number[]} nums
 * @return {number}
 */
var maxSubarraySumCircular = function(nums) {
    let currentMax = nums[0]
    let maxSum = nums[0]
    let minSum = nums[0]
    let currentMin = nums[0]
    let total = nums[0]
    for(let i = 1; i< nums.length; i++){
        currentMax = Math.max(currentMax + nums[i], nums[i])
        maxSum = Math.max(currentMax, maxSum)

        currentMin = Math.min(currentMin + nums[i], nums[i])
        minSum = Math.min(minSum, currentMin)

        total += nums[i]
    }

    if(maxSum < 0){
        return maxSum
    }

    return Math.max(maxSum, total-minSum)

};