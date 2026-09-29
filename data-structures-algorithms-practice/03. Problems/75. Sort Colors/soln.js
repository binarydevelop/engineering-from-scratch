/**
 * @param {number[]} nums
 * @return {void} Do not return anything, modify nums in-place instead.
 */
var sortColors = function(nums) {
let i = 0
let j = 0
let k = nums.length -1

while(j<=k){
    if(nums[j]==0){
        [nums[i], nums[j]] = [nums[j], nums[i]]
        i++
        j++
    }
    else if(nums[j] == 2){
        [nums[j], nums[k]] = [nums[k], nums[j]]
        k--
    } else{
        j++
    }
}
    return nums
};

let nums = [2,0,2,1,1,0]

console.log(sortColors(nums))