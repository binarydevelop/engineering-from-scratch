/**
 * @param {number[]} nums
 * @return {number[][]}
 */
var subsets = function(nums) {
    let path = []
    let result = []

    function backTrack(i){
        if(i === nums.length){
            result.push([...path])
            return 
        }

        path.push(nums[i])
        backTrack(i + 1)
        path.pop()
        backTrack(i+1)
    }
    backTrack(0)
    return result
};