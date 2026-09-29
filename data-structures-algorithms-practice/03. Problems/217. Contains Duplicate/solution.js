var containsDuplicate = function(nums) {
    let parity = [];
for(let i =0; i< nums.length; i++){
  if(parity.includes(nums[i])){
    return true;
  } else {
    parity.push(nums[i]);
  }
}
return false
};


/* https://leetcode.com/problems/contains-duplicate/ */