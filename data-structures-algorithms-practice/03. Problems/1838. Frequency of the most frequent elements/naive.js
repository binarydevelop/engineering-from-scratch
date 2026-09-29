/**
 * @param {number[]} nums
 * @param {number} k
 * @return {number}
 */
var maxFrequency = function(nums, k) {
        nums.sort((a,b) => a-b)
    let maxFrequency = 1
    for(let i = 0; i<= nums.length-1; i++){
        let frequency = 1
        let operationsUsed = 0
        for(let j = i-1; j>=0; j--){
            operationsUsed += (nums[i] - nums[j])

            if(operationsUsed > k){
                break;
            }
        frequency += 1
        }
        maxFrequency = Math.max(frequency, maxFrequency)
    }
    return maxFrequency
};


// The idea is that we sort the array first and then the closes element to the target
// element will have a higher chance to become the target so we keep calculating and 
// see if its within the operations limit