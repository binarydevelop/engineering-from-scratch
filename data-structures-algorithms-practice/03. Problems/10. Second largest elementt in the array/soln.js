function soln(arr) {
    let largest = -1;
    let secondLargest = -1;
  
    for (let i = 0; i < arr.length; i++) {
      if (arr[i] > largest) {
        secondLargest = largest; // Update secondLargest before updating largest
        largest = arr[i];
      } else if (arr[i] > secondLargest && arr[i] < largest) {
        secondLargest = arr[i];
      }
      console.log(i, largest, secondLargest);
    }
  
    if (secondLargest === -1) return -1; // If there's no second largest value
    return secondLargest;
  }
  
  let arr = [28078, 19451, 935, 28892, 2242, 3570, 5480, 231];
  console.log(soln(arr));
  
//   https://www.geeksforgeeks.org/problems/second-largest3735/1?itm_source=geeksforgeeks&itm_medium=article&itm_campaign=practice_card  