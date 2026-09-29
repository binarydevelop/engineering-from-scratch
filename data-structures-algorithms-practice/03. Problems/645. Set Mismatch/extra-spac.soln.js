/**
 * @param {number[]} nums
 * @return {number[]}
 */
var findErrorNums = function(nums) {
    let map = new Map()
    let missing = -1
    let dup = -1
    for(let i  =0; i < nums.length; i++){
        map.set(nums[i], (map.get(nums[i]) || 0 ) + 1)
    }

    for(let i = 1; i<=nums.length; i++){
        if(map.get(i) == 2){
            dup = i
        }
        if(!map.has(i)){
            missing = i
        }
    }
    return [dup, missing]

};

let nums = [1,2,2,4]
console.log(findErrorNums(nums))