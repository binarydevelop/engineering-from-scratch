function soln(nums, k){
    let map = new Map()
let results = []
    for(const num of nums){
        map.set(num, (map.get(num) ||0 ) + 1)
    }
    
    const buckets = Array.from({length: nums.length+1}, () => [])
    
    for(const [num, freq] of map){
        buckets[freq].push(num)
    }
    
    for(let i = buckets.length-1; i >= 0; i--){
        results.push(...buckets[i])
        if(results.length == k) return results
    }

}

let nums = [1,2,1,2,1,2,3,1,3,2]

console.log(soln(nums, 2))