function soln(arr){
    let largest = -1;
    for(let i = 0; i<=arr.length-1; i++){
      if(arr[i] > largest) largest = arr[i];
    }
    return largest;
  }
  
  let arr =  [10, 8, 30, 4, 5];
  console.log(soln(arr));

//   https://www.geeksforgeeks.org/program-to-find-largest-element-in-an-array/


function soln(arr){
  return Math.max(...arr);
}