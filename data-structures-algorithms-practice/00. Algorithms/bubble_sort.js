function bubbleSort(arr) {
  for (let i = 0; i < arr.length - 1; i++) {

    for (let j = 0; j < arr.length - 1 - i; j++) {

      if (arr[j] > arr[j + 1]) {
        [arr[j], arr[j + 1]] = [arr[j + 1], arr[j]];
      }

    }
  }

  return arr;
}

console.log(bubbleSort([5, 3, 8, 4, 2]));


// Optimised 
function selectionSort(nums) {
    for(let i =0; i < nums.length; i++){
        let flag = false; // because if the flag is not swapped that means the array is already sorted
        for(let j = 0; j < nums.length- 1- i; j++){ // nums.length-1- i is because we subtract one because we compare j with j+1 and i because the last i elements will already be sorted after ith pass. 
            if(nums[j] > nums[j+1]){
                [nums[j], nums[j+1]] = [nums[j+1], nums[j]]
                flag = true // this flips the flag so we know swapping happend 
            }
        }
        if(flag === false) return nums
    }
    return nums
}

console.log(selectionSort([2,1,4,5,3,7]));
