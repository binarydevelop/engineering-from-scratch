/**
 * @param {number[]} numbers
 * @param {number} target
 * @return {number[]}
 */
var twoSum = function(numbers, target) {
    let start = 0
    let end = numbers.length-1

    while(start < end){
        let currentSum = numbers[start] + numbers[end]
        if(currentSum == target){
            return [start+1, end+1]
        } else if(currentSum > target){
            end--
        } else {
            start++
        }
    }

    return []
};