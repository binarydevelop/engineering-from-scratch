/**
 * @param {number[]} nums
 * @param {number[][]} queries
 * @return {number[]}
 */
var sumEvenAfterQueries = function(nums, queries) {
    let sum = 0 
    let results  = [];

    // fin the sum for even numbers
    for(let num of nums){
        if(num%2 == 0) {
            sum += num
        }
    }

    for(let i = 0; i < queries.length; i++){
        let val = queries[i][0]
        let idx = queries[i][1]

        if(nums[idx] % 2 == 0) {
            sum -= nums[idx]
        }

        let newValue = nums[idx] + val
        nums[idx] = newValue
        if(newValue % 2 == 0) {
            sum += newValue
        }

        results.push(sum)
    }
    return results
};

let nums = [1,2,3,4]
let queries = [[1,0],[-3,1],[-4,0],[2,3]]
console.log(sumEvenAfterQueries(nums, queries))