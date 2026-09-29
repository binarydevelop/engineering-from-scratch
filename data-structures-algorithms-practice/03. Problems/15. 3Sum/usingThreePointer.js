function usingThreePointer(arr, key){
    let start = 1;
    let end = arr.length - 1; 
    for(let i = 0; i< arr.length - 2; i++ ){
        while(start < end){
            if(arr[i] + arr[start] + arr[end] == key){
                return [arr[i] , arr[start] , arr[end]]
            }
            if(arr[i] + arr[start] + arr[end] > key){
                end--;
            }
            if(arr[i] + arr[start] + arr[end] < key){
                start++;
            }
        }
    }
    return [-1,-1,-1];
}

let arr = [1, 2, 3, 4, 5];
console.log(usingThreePointer(arr, 9));


//works for sorted array