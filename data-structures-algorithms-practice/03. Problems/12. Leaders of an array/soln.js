// https://www.geeksforgeeks.org/problems/leaders-in-an-array-1587115620/1?itm_source=geeksforgeeks&itm_medium=article&itm_campaign=practice_card


function soln(arr){
    let results = []
    let maxRight = -Infinity;
    
    for(let i = arr.length -1 ; i >= 0; i--){
      if(arr[i] >= maxRight) {
        results.push(arr[i]);
        maxRight = arr[i];
      }
    }
    return results.reverse();
  }
  
  let arr = [61, 61, 17];
  
  console.log(soln(arr));