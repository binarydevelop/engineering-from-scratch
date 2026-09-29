/**
 * @param {number[]} nums
 * @param {number} target
 * @return {number}
 */
var threeSumClosest = function(nums, target) {
    let closest = Infinity
    nums.sort((a,b) => a-b)
    for(let i = 0; i < nums.length; i++){
        let current = nums[i]
        let start = i + 1;
        let end =  nums.length -1; 

        while(start < end){
            let currentSum = current + nums[start]+ nums[end]
            if(Math.abs(target - currentSum) < Math.abs(target-closest)){
                closest = currentSum
            }
            if(currentSum > target){
                end--;
            } else {
                start++;
            }
        }
    }

    return closest
};
