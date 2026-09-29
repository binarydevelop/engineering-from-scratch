function soln(nums){
    let total = 0
    let lmax = []
    let rmax = []
    lmax[0] = nums[0]
    rmax[nums.length - 1] = nums[nums.length-1]
    
    for(let i= 1; i< nums.length; i++){
        lmax[i] = Math.max(nums[i], lmax[i-1])
    }
    
    for(let i= nums.length-2; i>= 0; i--){
        rmax[i] = Math.max(nums[i], rmax[i+1])
    }
    
    for(let i = 0; i<nums.length;i++){
        total += Math.min(lmax[i], rmax[i]) - nums[i]
    }
    
    return total
} 


let nums = [4,2,0,3,2,5]
console.log(soln(nums))

// the idea is we get the prefix max and suffix max arrays and then at each point find the unit of water we can store. 