function SumOfTwoElementsEqualToGivenSum(arr, sum){
    for(let i = 0; i < arr.length; i++ ){
        for(let j = i + 1; j < arr.length; j++ ){
            if(arr[i] + arr[j] == sum){
                return [arr[i], arr[j]]
            }
        }
    }
    return -1
}

let arr = [1,4,3,2,5,6,8,7];
console.log(SumOfTwoElementsEqualToGivenSum(arr, 10));

/* 
This is brute force approach and gives first pair which sum up to the given number. 
*/