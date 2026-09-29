
var dailyTemperatures = function(temperatures) {
        let results = Array(temperatures.length).fill(0)
    
    let stack = []
    
    for(let i = 0; i< temperatures.length; i++){
        while( stack.length > 0 && temperatures[i] > stack[stack.length-1][0]){
            let [temperature, index] = stack.pop()
            results[index] = i - index
        }
        stack.push([temperatures[i], i])
    }
    return results
};