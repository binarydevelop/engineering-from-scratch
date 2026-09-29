/**
 * @param {number[]} nums
 * @return {number}
 */
var pivotIndex = function(nums) {
    let total = nums.reduce((sum, num) => sum + num, 0)

    let leftSum = 0

    for(let i = 0; i< nums.length; i++ ){
        let rightSum = total - leftSum - nums[i];

        if(leftSum == rightSum){
            return i;
        }

        leftSum += nums[i]
    }

    return -1
};

let nums = [1,7,3,6,5,6]

console.log(pivotIndex(nums))