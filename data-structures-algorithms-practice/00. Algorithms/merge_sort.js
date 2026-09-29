function mergeSort(nums){
    if(nums.length <= 1){
        return nums
    }
    let mid = Math.floor(nums.length / 2);
    let left = mergeSort(nums.slice(0,mid));
    let right = mergeSort(nums.slice(mid));

    return merge(left,right);
}

function merge(left, right){
    console.log(left,right)
    const result = []

    let i = 0;
    let j = 0;

    while(i < left.length && j < right.length ){
        if(left[i] <= right[j]){
            result.push(left[i])
            i++;
        } else if(right[j] <= left[i]){
            result.push(right[j])
            j++; 
        }
    }

    while(i < left.length){
        result.push(left[i])
        i++
    }
        while(j < right.length){
        result.push(right[j])
        j++
    }

    return result; 
}

let nums = [10,29,14,37,13]
console.log(mergeSort(nums))
