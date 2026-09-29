/**
 * @param {number} target
 * @param {number[]} nums
 * @return {number}
 */
var minSubArrayLen = function(target, nums) {
    let start = 0
    let sum = 0 
    let minSize = Infinity;
    for(let end =0; end <nums.length; end++){
        sum += nums[end]

        while(sum >= target){
            minSize = Math.min(minSize, end- start + 1)
            sum-= nums[start]
            start++
        }
    }
    return minSize == Infinity ? 0 : minSize
};