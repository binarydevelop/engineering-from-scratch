const containsDuplicates = (nums) => {
    let freq= {}
    for(let num of nums){
      freq[num] = (freq[num] || 0) + 1;
      if(freq[num] > 1) return true;
    }
    return false
  }
  
  console.log(containsDuplicates([1,2,3,4]))