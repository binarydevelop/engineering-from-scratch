function soln(nums, target){
    let count = 0 
    for(let i = 0; i<nums.length; i++){
        let currSum = 0
        for(let j = i; j<nums.length; j++){
            currSum += nums[j]
            if(currSum == target){
                count++;
            }
        }
    }

    return count;
}

let nums = [1,1,1]
let k = 2
console.log(soln(nums,k))