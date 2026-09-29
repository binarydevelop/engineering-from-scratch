/**
 * @param {number[]} nums
 * @return {number}
 */
var largestPerimeter = function(nums) {

    nums.sort((a,b) => a-b)
    for(let i = nums.length-3; i >= 0; i--){
        if(nums[i]+ nums[i+1] > nums[i+2]){
            return (nums[i]+ nums[i+1] + nums[i+2])
        }
    }
    return 0 
};

/*  This works on the properties of triangle perimeter
    accroding to which a + b > c. 
    There are two other properties which say
    b+c > a
    a + c > b
    but these become automatically true when we sort so 
    1,2,3 so 2 + 3 will always be greater than 1 which is a in this case.
*/