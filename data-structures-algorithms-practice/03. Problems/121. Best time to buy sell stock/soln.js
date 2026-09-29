function soln(nums){
    let start = 0;
    let end = 1;
    let maxProfit = 0
    while(end < nums.length){
        console.log(nums[start], nums[end])
        let profit = 0
        if(nums[end] > nums[start]){
            profit = nums[end] - nums[start]
            maxProfit = Math.max(profit,maxProfit)
        } else {
            start = end
        }
        end++;
    }
    return maxProfit
} 


let nums = [2,1,4]
let target = 0
console.log(soln(nums, target))

/* 
The idea is we keep two pointers now we traverse the whole array, at each point we see if the current value is less than the end value 
if yes just subtract them and find the profit for that day. compare it with maxprofit you've seen so far. 
otherwise set start to the value of end and move end pointer. 
*/