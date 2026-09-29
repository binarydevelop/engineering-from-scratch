function soln(nums, target){
    let maxArea = -1;
    
    let start = 0
    let end = nums.length-1
    
    while(start < end){
        let area = (Math.min(nums[start], nums[end])) * (end- start)
        maxArea = Math.max(area,maxArea)

        if(nums[start] < nums[end]){
            start++
        } else {
            end--
        }
    }
    return maxArea
}


let nums = [1]
// -4 -1 -1 0 1 2 
let target = 0
console.log(soln(nums, target))

// The idea is that we see the area of the two points 
// if the left one is shorter move it otherwise move the right one 