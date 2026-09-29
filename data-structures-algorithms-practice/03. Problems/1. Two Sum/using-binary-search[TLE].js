/*
Given an array Arr of N positive integers and another number X.
Determine whether or not there exist two elements in Arr whose sum is exactly X.
*/
function binarySearch(arr, key, start, end){
    while(start <= end){
      let mid = Math.floor(start + (end -start)/2);
      if(arr[mid] == key){ 
        return mid 
      }
      if(arr[mid] > key){
        end = mid - 1;
      }
      if(arr[mid] < key){
        start = mid + 1;
      }
    }
    return -1;
  }
  
  function usingBinarySearch(arr, sum){
    for(let i = 0; i< arr.length -1 ; i++){
      if(arr[i] < sum){
        let key = sum - arr[i];
        let sumIndex = binarySearch(arr, key, i + 1, arr.length -1 )
        if(sumIndex > 0){
          return sumIndex
        }
      }
    }
    return -1;
  }
  
  console.log(usingBinarySearch([1, 4, 45, 6, 10, -8], 16));