function kthLargestElement(arr, k){
    arr.sort((a,b) => a- b);
    return arr[k-1];
  }
  
  console.log(kthLargestElement([7, 10, 4, 3, 20, 15],3));