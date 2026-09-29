/**
 * @param {number[]} temperatures
 * @return {number[]}
 */
var dailyTemperatures = function(temperatures) {
        let results = Array(temperatures.length).fill(0)
        
    for(let i = 0; i < temperatures.length; i++){
        for(let j = i+1; j<temperatures.length;j++){
            if(temperatures[j] > temperatures[i]){
                results[i] = ((j-i) )
                break;
            } 
        }
    }
    
    return results
};


//TLE error