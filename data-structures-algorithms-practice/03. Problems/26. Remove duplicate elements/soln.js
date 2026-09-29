function solution(arr) {
    let j = 1; // Pointer for the next unique position
    for (let i = 1; i < arr.length; i++) {
      if (arr[i] !== arr[i - 1]) {
        arr[j] = arr[i]; // Place the next unique element
        j++;
      }
    }
    return arr.slice(0, j); // Return the array of unique elements
  }
  
  let arr = [2, 2, 2, 2, 2];
  console.log(solution(arr)); // Output: [1, 2, 3, 4]
  
  // https://www.geeksforgeeks.org/problems/remove-duplicate-elements-from-sorted-array/1?itm_source=geeksforgeeks&itm_medium=article&itm_campaign=practice_card