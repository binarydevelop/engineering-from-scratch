function soln(strs){
    let map = new Map()
    
    for(const str of strs){
        let count = Array(26).fill(0)
        
        for(let ch of str){
            count[ch.charCodeAt(0) - 97]++;
        }
        
        const key = count.join('#')
        
        if(!map.has(key)){
            map.set(key, [])
        }
        
        map.get(key).push(str)

    }
    
    return Array.from(map.values())
}

let strs = ["eat","tea","tan","ate","nat","bat"]
console.log(soln(strs))