/**
 * @param {number[]} nums
 * @return {boolean}
 */
var increasingTriplet = function(nums) {
    let num1 = Infinity
    let num2 = Infinity

    let num3 = 0

    for(let i =0; i< nums.length; i++){
        if(nums[i] <= num1) { console.log('here')
            num1 = nums[i]
        } else if(nums[i] <= num2){
            num2 = nums[i]
        } else {
            return true
        }
    }


    return false
};
let nums =[2,1,5,0,4,6]
console.log(increasingTriplet(nums))