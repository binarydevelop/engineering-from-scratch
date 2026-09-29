function soln(nums, target){
    let count = 0
    let sum =0
    let map = new Map();
    map.set(0,1)

    for(const num of nums){
        sum += num
        
        let needed = sum - target
        if(map.has(needed)) {
            count += map.get(needed)
        }
        
        map.set(sum, (map.get(sum) || 0) + 1)
    }
    
    return count
}

console.log(soln([1,1,1], 2))

// The idea is we traverse the whole array and at each point store the sum now whenever we go to an element
// we check the difference between the target value and the current sum and check if it 
// was at any point in the map or seen before, if yes we increase the count by getting the 
// value of that needed value, cause if two elements would have given the same sum
// they both make a subarray.
// we first set the map as (0,1) so that we know before starting also we have seen the
// sum 0