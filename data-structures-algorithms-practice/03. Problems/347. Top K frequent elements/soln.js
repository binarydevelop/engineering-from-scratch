function soln(nums, k){
    let freqMap = new Map()

    for(let i = 0; i< nums.length; i++){
        freqMap.set(nums[i], (freqMap.get(nums[i]) || 0) + 1)
    }

    const sorted = [...freqMap.keys()].sort((a,b) => {
        return freqMap.get(b) - freqMap.get(a)
    })

    return sorted.slice(0,k)
}

nums = [1,1,1,2,2,3]
k = 2

console.log(soln(nums, k))

// This can also be done using a heap but we don' have heap implementaion