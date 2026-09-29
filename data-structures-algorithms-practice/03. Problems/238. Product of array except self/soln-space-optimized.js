function soln(nums) {
    let results = []
    results[0] = 1
    for(let i = 1; i<nums.length;i++){
        results[i] = nums[i-1] * results[i-1]
    }

    console.log(results) //1 1 2 6
    let rightProduct = 1
    for(let i = nums.length-2; i>=0;i--){
        rightProduct = rightProduct * nums[i+1]
        results[i] = rightProduct * results[i]
    }

    return results
}

let nums = [1,2,3,4];
console.log(soln(nums));

//[24, 12, 8, 6]

