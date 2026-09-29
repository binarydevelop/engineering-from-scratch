function soln(arr){
    let res = [];
    let alternateArray = helper(arr, 0, res);
    return alternateArray;
  }
  
  function helper(arr, index, res){
    if(index > arr.length -1){
      return res;
    }
    res.push(arr[index]);
    return helper(arr, index+2, res)
  }
  
  let arr =  [1, 2, 3, 4, 5];
  console.log(soln(arr));
  