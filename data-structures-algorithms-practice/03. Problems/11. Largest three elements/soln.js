function findTopThreeLargest(arr) {
    let l1 = null, l2 = null, l3 = null;
  
    for (let i = 0; i < arr.length; i++) {
      if (arr[i] > l1 || l1 === null) {
        l3 = l2;
        l2 = l1;
        l1 = arr[i];
      } else if ((arr[i] > l2 || l2 === null) && arr[i] < l1) {
        l3 = l2;
        l2 = arr[i];
      } else if ((arr[i] > l3 || l3 === null) && arr[i] < l2) {
        l3 = arr[i];
      }
    }
  
    const result = [];
    if (l1 !== null) result.push(l1);
    if (l2 !== null) result.push(l2);
    if (l3 !== null) result.push(l3);
  
    return result;
  }
  
  // Example Usage
  console.log(findTopThreeLargest([10, 20, 20, 30, 30, 40])); // [40, 30, 20]
  console.log(findTopThreeLargest([5, 5, 5]));               // [5]
  console.log(findTopThreeLargest([-10, -20, -30, -40]));    // [-10, -20, -30]
  console.log(findTopThreeLargest([]));                     // []
  // https://www.geeksforgeeks.org/problems/largest-three-distinct-elements/1?itm_source=geeksforgeeks&itm_medium=article&itm_campaign=practice_card