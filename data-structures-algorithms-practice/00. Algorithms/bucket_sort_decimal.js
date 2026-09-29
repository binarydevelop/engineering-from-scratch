function soln(nums, buckets=10){
    if(nums.length <= 0) return nums
    
    let results = Array.from({length: buckets}, () => [])
    let res = []
    
    for(let i = 0; i<nums.length; i++){
        let index = Math.floor((nums[i]/nums.length) * buckets)
        console.log(index)
        if(index == buckets){
            index--;
        }
        results[index].push(nums[i])
    }
    
    for(bucket of results){
        bucket.sort((a,b) => {
            return a -b
        })
        res.push(...bucket)
    }
    
    return res
}

let nums = [0.5, 0.6,0.1,0.4,0.9]

console.log(soln(nums))