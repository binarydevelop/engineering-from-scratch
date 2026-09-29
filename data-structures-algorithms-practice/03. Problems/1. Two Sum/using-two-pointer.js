function usingTwoPointer(arr, key){
    let start = 0; 
    let end = arr.length -1;

    arr.sort((a, b) => {
        return a - b
    });
    while(start <= end ){
        if(arr[start] + arr[end] == key){
            return [arr[start], arr[end]]
        }
        if(arr[start] + arr[end] > key ){
            end--;
        }
        if(arr[start] + arr[end] < key ){
            start++;
        }
    }
    return [-1,-1];
}