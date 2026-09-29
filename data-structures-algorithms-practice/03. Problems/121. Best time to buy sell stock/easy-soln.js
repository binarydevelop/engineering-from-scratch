function soln(nums){
    let min = nums[0]
    let maxprofit = 0
    for(let i = 1; i<nums.length;i++){
        if(nums[i]<min){
            min = nums[i]
        }
        let currentprofit = nums[i] - min
        maxprofit = Math.max(maxprofit, currentprofit)
    }
    
    return maxprofit
}
let nums = [7,6,4,3,1]
console.log(soln(nums))

/* 

*/