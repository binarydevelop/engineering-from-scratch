function soln(nums) {
    let leftPrefix = Array(nums.length).fill(1)
    let rightPrefix = []
    leftPrefix[0]= 1
    rightPrefix[nums.length-1] = 1
    let results = []
    for(let i = 1; i<nums.length;i++){
        leftPrefix[i] = nums[i-1] * leftPrefix[i-1]
    }

    for(let i = nums.length-2; i>=0;i--){
        rightPrefix[i] = nums[i+1] * rightPrefix[i+1]
    }

    for(let i =0;i < nums.length;i++){
        results[i] = leftPrefix[i] * rightPrefix[i]
    }

    return results
}

let nums = [1,2,3,4];
console.log(soln(nums));

//[1, 1, ]