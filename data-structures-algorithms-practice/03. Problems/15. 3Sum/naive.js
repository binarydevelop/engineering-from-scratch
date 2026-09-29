function sumOfThreeElements(arr, key){
    if(arr.length < 3){
        return false;
    }
    for(let i = 0; i < arr.length-1; i++){
        for(let j =i +1; j< arr.length; j++){
            for(let k = j + 1; k< arr.length; k++){
                if(arr[i] + arr[j] + arr[k] == key){
                    return [arr[i], arr[j], arr[k]];
                } 
            }
        }
    }
    return false
}

console.log(sumOfThreeElements([1,2,3,7], 10));
