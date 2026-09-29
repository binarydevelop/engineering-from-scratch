function soln(nums, target){
    nums.sort((a,b) => a-b)
    let results = []
    for(let i = 0; i< nums.length -2; i++){
        if(i > 0 && nums[i] == nums[i-1]) continue
        let start = i+1
        let end = nums.length -1
        let fixed = nums[i]
        
        while(start < end){
            let sum = nums[start] + nums[end] + fixed
            if(sum == target){
                results.push([nums[start] , nums[end] , nums[i]])
               
                while(nums[start] == nums[start+1]) start++
                while(nums[end] == nums[end-1]) end--
                start++
                end--
            } else if(sum > target){
                end--
            } else {
                start++
            }
        }
    }
    return results;
}


let nums = [0,1,1]
// -4 -1 -1 0 1 2 
let target = 0
console.log(soln(nums, target))