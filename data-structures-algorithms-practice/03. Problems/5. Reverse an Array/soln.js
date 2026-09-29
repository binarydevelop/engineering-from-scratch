function reverseArray(arr){
    arr = arr.split('');
    let arrLength = arr.length;
    for(let i = 0; i <= Math.ceil((arrLength-1)/2); i++){
      let temp = arr[i];
      arr[i] = arr[arrLength-1];
      arr[arrLength-1] =temp;
      arrLength--;
    }
    return arr.join('');
  }
  
  console.log(reverseArray('APFGMRZXIFPSXKOQD'));
  
  
  