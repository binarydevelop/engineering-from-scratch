function usingSingleForLoop(arr, target){
    arr.sort((a,b) => {
        return a - b
    })
    for(let i = 0, j = arr.length-1 ; i< arr.length -1, j > 0 ; ){
        if(arr[i] + arr[j] == target){
            console.log(arr[i], arr[j])
            return [i,j]
        }
        if(arr[i] + arr[j] > target){
            j--;
        }
        if(arr[i] + arr[j] < target){
            i++;
        }
    }
    return [-1, -1]
}

/* 
The time complexity will depend on what time complexity we use 
Merge sort or heap sort O(n logn)
Heap sort O(n^2)
*/