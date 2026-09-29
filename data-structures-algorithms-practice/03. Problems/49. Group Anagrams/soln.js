function soln(strs){
    let results = new Map()
    for(let word of strs){
        key = word.split('').sort().join()
        if(results.get(key)){
            results.push(word)
        } else {
            results[key] = []
        }
    }
    return Object.values(results)
}